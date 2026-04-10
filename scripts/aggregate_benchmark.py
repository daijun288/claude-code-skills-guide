#!/usr/bin/env python3
"""
聚合基准测试结果

用法:
    python aggregate_benchmark.py --results-dir benchmark_results/
"""

import argparse
import json
from pathlib import Path
from datetime import datetime


def aggregate_results(results_dir: Path) -> dict:
    """聚合所有基准测试结果"""
    results = []

    for result_file in results_dir.glob("*.json"):
        try:
            data = json.loads(result_file.read_text())
            results.append({
                "file": result_file.name,
                "data": data
            })
        except (json.JSONDecodeError, KeyError):
            continue

    if not results:
        return {"error": "未找到有效的结果文件"}

    # 聚合统计
    total_evals = 0
    total_passed_baseline = 0
    total_passed_skill = 0
    total_time_baseline = 0
    total_time_skill = 0

    skill_wins = 0
    baseline_wins = 0
    ties = 0

    for item in results:
        data = item["data"]
        summary = data.get("summary", {})

        total_evals += summary.get("total", 0)
        total_passed_baseline += summary.get("baseline_passed", 0)
        total_passed_skill += summary.get("skill_passed", 0)
        total_time_baseline += summary.get("baseline_time", 0)
        total_time_skill += summary.get("skill_time", 0)

        # 统计胜者
        winner = summary.get("winner")
        if winner == "skill":
            skill_wins += 1
        elif winner == "baseline":
            baseline_wins += 1
        else:
            ties += 1

    # 计算指标
    baseline_pass_rate = total_passed_baseline / total_evals if total_evals > 0 else 0
    skill_pass_rate = total_passed_skill / total_evals if total_evals > 0 else 0

    improvement = skill_pass_rate - baseline_pass_rate

    return {
        "aggregated_at": datetime.now().isoformat(),
        "total_evals": total_evals,
        "total_runs": len(results),
        "baseline": {
            "passed": total_passed_baseline,
            "pass_rate": round(baseline_pass_rate, 3),
            "avg_time": round(total_time_baseline / len(results), 1) if results else 0
        },
        "skill": {
            "passed": total_passed_skill,
            "pass_rate": round(skill_pass_rate, 3),
            "avg_time": round(total_time_skill / len(results), 1) if results else 0
        },
        "comparison": {
            "improvement": round(improvement, 3),
            "skill_wins": skill_wins,
            "baseline_wins": baseline_wins,
            "ties": ties
        },
        "files": [r["file"] for r in results]
    }


def main():
    parser = argparse.ArgumentParser(description="聚合基准测试结果")
    parser.add_argument("--results-dir", required=True, help="结果目录路径")
    parser.add_argument("--output", help="输出文件路径（可选）")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    aggregated = aggregate_results(results_dir)

    output = json.dumps(aggregated, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output)
        print(f"结果已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()