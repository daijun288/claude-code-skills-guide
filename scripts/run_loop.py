#!/usr/bin/env python3
"""
运行 Description 优化循环

用法:
    python run_loop.py --eval-set trigger_evals.json --skill-path <skill-dir> --model <model-id>
"""

import argparse
import json
import re
import subprocess
import os
import sys
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


def call_claude(prompt: str, model: str, timeout: int = 300) -> str:
    """调用 claude -p"""
    cmd = ["claude", "-p", "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True, env=env, timeout=timeout
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude -p 失败: {result.stderr}")

    return result.stdout


def improve_description(skill_name: str, current_description: str,
                        eval_results: dict, model: str) -> str:
    """调用 Claude 改进 description"""
    failed_triggers = [r for r in eval_results["results"] if r["should_trigger"] and not r["pass"]]
    false_triggers = [r for r in eval_results["results"] if not r["should_trigger"] and not r["pass"]]

    prompt = f"""你正在优化名为 "{skill_name}" 的 Skill 的 description。

当前 description:
"{current_description}"

当前得分: {eval_results['summary']['passed']}/{eval_results['summary']['total']}

"""

    if failed_triggers:
        prompt += "应该触发但没触发:\n"
        for r in failed_triggers:
            prompt += f'  - "{r["query"][:80]}"\n'
        prompt += "\n"

    if false_triggers:
        prompt += "不该触发但触发了:\n"
        for r in false_triggers:
            prompt += f'  - "{r["query"][:80]}"\n'
        prompt += "\n"

    prompt += """基于失败情况，写一个改进的 description。

提示:
- 使用祈使语气
- 关注用户意图，而非实现细节
- 不超过 200 字
- 不要列举具体查询

只输出新的 description，用 <new_description> 标签包裹。"""

    text = call_claude(prompt, model)

    match = re.search(r"<new_description>(.*?)</new_description>", text, re.DOTALL)
    description = match.group(1).strip().strip('"') if match else text.strip().strip('"')

    return description


def run_loop(eval_set: list, skill_path: Path, model: str,
             max_iterations: int = 5, verbose: bool = False) -> dict:
    """运行优化循环"""
    from scripts.run_eval import run_eval, find_project_root

    name, original_description, content = parse_skill_md(skill_path)
    current_description = original_description
    project_root = find_project_root()

    history = []

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n迭代 {iteration}/{max_iterations}", file=sys.stderr)
            print(f"Description: {current_description[:80]}...", file=sys.stderr)

        # 运行评估
        eval_results = run_eval(
            eval_set=eval_set,
            skill_name=name,
            description=current_description,
            runs_per_query=3,
            timeout=30,
            project_root=project_root,
            model=model
        )

        passed = eval_results["summary"]["passed"]
        total = eval_results["summary"]["total"]

        history.append({
            "iteration": iteration,
            "description": current_description,
            "passed": passed,
            "total": total
        })

        if verbose:
            print(f"结果: {passed}/{total} 通过", file=sys.stderr)

        if passed == total:
            if verbose:
                print(f"\n全部通过！", file=sys.stderr)
            break

        # 改进 description
        current_description = improve_description(
            skill_name=name,
            current_description=current_description,
            eval_results=eval_results,
            model=model
        )

    # 找最佳结果
    best = max(history, key=lambda h: h["passed"])

    return {
        "original_description": original_description,
        "best_description": best["description"],
        "best_score": f"{best['passed']}/{best['total']}",
        "iterations_run": len(history),
        "history": history
    }


def main():
    parser = argparse.ArgumentParser(description="运行 Description 优化循环")
    parser.add_argument("--eval-set", required=True, help="触发测试集 JSON 文件")
    parser.add_argument("--skill-path", required=True, help="Skill 目录路径")
    parser.add_argument("--model", required=True, help="使用的模型")
    parser.add_argument("--max-iterations", type=int, default=5, help="最大迭代次数")
    parser.add_argument("--verbose", action="store_true", help="打印详细信息")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    output = run_loop(
        eval_set=eval_set,
        skill_path=skill_path,
        model=args.model,
        max_iterations=args.max_iterations,
        verbose=args.verbose
    )

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()