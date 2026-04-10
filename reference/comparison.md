# 盲比较流程

> 本文档为 SKILL.md 的详细补充，模式 H 的完整流程。

---

## 适用场景

- 用户问"新版本真的更好吗？"
- 需要无偏见评估两个版本

---

## 流程概览

```
准备输出 → 盲比较 → 分析原因
```

---

## 步骤 1：准备两个输出

运行两个版本的 Skill，保存输出到不同目录：

```
<workspace>/
├── output-a/
└── output-b/
```

---

## 步骤 2：盲比较

委托 `agents/comparator.md` 比较：

```
比较任务：
- output_a_path: <workspace>/output-a/
- output_b_path: <workspace>/output-b/
- eval_prompt: <原始任务>
- expectations: <预期列表>
- 保存结果到: <workspace>/comparison.json
```

**关键**：不告诉 comparator 哪个是哪个版本，避免偏见。

---

## 步骤 3：分析原因

委托 `agents/analyzer.md` 分析：

```
分析任务：
- winner: <比较结果中的胜者>
- winner_skill_path: <胜者 Skill 路径>
- loser_skill_path: <败者 Skill 路径>
- comparison_result_path: <workspace>/comparison.json
- 保存结果到: <workspace>/analysis.json
```

生成：
- 胜者优势
- 败者弱点
- 改进建议

---

## 输出格式

### comparison.json

```json
{
  "winner": "A",
  "reasoning": "输出 A 提供了完整的解决方案...",
  "rubric": {
    "A": {
      "content": {"correctness": 5, "completeness": 5, "accuracy": 4},
      "structure": {"organization": 4, "formatting": 5, "usability": 4},
      "overall_score": 9.0
    },
    "B": {
      "overall_score": 5.4
    }
  }
}
```

### analysis.json

```json
{
  "winner_strengths": ["清晰的多步骤指令", "包含验证脚本"],
  "loser_weaknesses": ["模糊指令导致不一致行为"],
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "用明确步骤替换模糊指令"
    }
  ]
}
```

---

## 相关文件

- [agents/comparator.md](../agents/comparator.md) - 比较 Agent
- [agents/analyzer.md](../agents/analyzer.md) - 分析 Agent