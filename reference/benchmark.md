# 基准测试流程

> 本文档为 SKILL.md 的详细补充，模式 G 的完整流程。

---

## 适用场景

- 量化比较 Skill 与 baseline 的差异
- 评估 Skill 稳定性（方差分析）
- 多次运行获取可靠数据

---

## 流程概览

```
准备测试集 → 并行运行 → 收集数据 → 评估聚合 → 分析模式
```

---

## 步骤 1：准备测试集

创建 2-3 个测试用例，保存到 `evals/evals.json`。

---

## 步骤 2：并行运行

**⚠️ MUST 同一轮启动 with-skill 和 baseline 子 Agent**

### With-skill 运行

```
执行任务：
- Skill 路径: <path-to-skill>
- 任务: <eval prompt>
- 保存输出到: <workspace>/eval-<ID>/with_skill/outputs/
```

### Baseline 运行

- 创建新 Skill：无 skill
- 改进现有 Skill：旧版本 skill

```
执行任务：
- Skill 路径: none（或旧版本路径）
- 任务: <eval prompt>
- 保存输出到: <workspace>/eval-<ID>/without_skill/outputs/
```

---

## 步骤 3：收集数据

每个运行完成后，**MUST 立即保存** timing 数据：

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

**为什么必须立即保存**：这些数据只通过任务通知传递一次，之后无法恢复。

---

## 步骤 4：评估聚合

### 评估每个输出

委托 `agents/grader.md` 评估：

```
评估任务：
- expectations: <expectations list>
- outputs_dir: <run-dir>/outputs/
- 保存结果到: <run-dir>/grading.json
```

### 聚合结果

```bash
python scripts/aggregate_benchmark.py <workspace> --skill-name <name>
```

生成：
- `benchmark.json` - 完整数据
- `benchmark.md` - 人类可读报告

---

## 步骤 5：分析模式

委托 `agents/analyzer.md` 分析：

```
分析任务：
- benchmark.json 路径: <workspace>/benchmark.json
- 输出分析说明
```

识别：
- 哪些预期总是通过（可能不区分 Skill 价值）
- 哪些预期高方差（可能不稳定）
- Skill 增加的价值在哪里

---

## 输出格式

### benchmark.json

```json
{
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05},
      "time_seconds": {"mean": 45.0, "stddev": 12.0}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08},
      "time_seconds": {"mean": 32.0, "stddev": 8.0}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0"
    }
  }
}
```

---

## 相关文件

- [reference/schemas.md](schemas.md) - JSON 格式定义
- [agents/grader.md](../agents/grader.md) - 评估 Agent
- [agents/analyzer.md](../agents/analyzer.md) - 分析 Agent