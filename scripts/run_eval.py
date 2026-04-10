#!/usr/bin/env python3
"""
运行触发评估 - 测试 Skill description 是否正确触发

用法:
    python run_eval.py --eval-set evals.json --skill-path <skill-dir>
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple:
    """解析 SKILL.md"""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    name = ""
    description = ""
    for line in lines[1:end_idx]:
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            description = line[len("description:"):].strip().strip('"').strip("'")

    return name, description, content


def find_project_root() -> Path:
    """查找项目根目录"""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def run_single_query(query: str, skill_name: str, skill_description: str,
                     timeout: int, project_root: str, model: str = None) -> bool:
    """运行单个查询，返回是否触发"""
    unique_id = uuid.uuid4().hex[:8]
    clean_name = f"{skill_name}-skill-{unique_id}"
    command_dir = Path(project_root) / ".claude" / "commands"
    command_file = command_dir / f"{clean_name}.md"

    try:
        command_dir.mkdir(parents=True, exist_ok=True)
        command_content = f"---\ndescription: {skill_description}\n---\n\n# {skill_name}\n\n{skill_description}"
        command_file.write_text(command_content)

        cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose"]
        if model:
            cmd.extend(["--model", model])

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=project_root, env=env
        )

        triggered = False
        start_time = time.time()
        buffer = ""

        while time.time() - start_time < timeout:
            if process.poll() is not None:
                break

            import select
            ready, _, _ = select.select([process.stdout], [], [], 1.0)
            if not ready:
                continue

            chunk = os.read(process.stdout.fileno(), 8192)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")

            if clean_name in buffer:
                triggered = True
                break

        if process.poll() is None:
            process.kill()
            process.wait()

        return triggered

    finally:
        if command_file.exists():
            command_file.unlink()


def run_eval(eval_set: list, skill_name: str, description: str,
             runs_per_query: int = 3, timeout: int = 30,
             project_root: Path = None, model: str = None) -> dict:
    """运行完整评估集"""
    results = []

    for item in eval_set:
        triggers = []
        for _ in range(runs_per_query):
            result = run_single_query(
                item["query"], skill_name, description,
                timeout, str(project_root), model
            )
            triggers.append(result)

        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        passed = (trigger_rate >= 0.5) if should_trigger else (trigger_rate < 0.5)

        results.append({
            "query": item["query"],
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": passed
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {"total": total, "passed": passed, "failed": total - passed}
    }


def main():
    parser = argparse.ArgumentParser(description="运行触发评估")
    parser.add_argument("--eval-set", required=True, help="评估集 JSON 文件路径")
    parser.add_argument("--skill-path", required=True, help="Skill 目录路径")
    parser.add_argument("--model", default=None, help="使用的模型")
    parser.add_argument("--runs-per-query", type=int, default=3, help="每个查询运行次数")
    parser.add_argument("--timeout", type=int, default=30, help="每个查询超时秒数")
    parser.add_argument("--verbose", action="store_true", help="打印详细信息")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    name, description, _ = parse_skill_md(skill_path)
    project_root = find_project_root()

    if args.verbose:
        print(f"评估: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        runs_per_query=args.runs_per_query,
        timeout=args.timeout,
        project_root=project_root,
        model=args.model
    )

    if args.verbose:
        s = output["summary"]
        print(f"结果: {s['passed']}/{s['total']} 通过", file=sys.stderr)

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()