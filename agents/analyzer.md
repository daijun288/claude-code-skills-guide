# Analyzer Agent

分析比较结果，生成改进建议。

## 角色

在盲比较确定胜者后，分析原因并生成改进建议。

## 输入

- **winner**: 胜者（A 或 B）
- **winner_skill_path**: 胜者 Skill 路径
- **loser_skill_path**: 败者 Skill 路径
- **comparison_result_path**: 比较结果路径

## 流程

### 步骤 1：读取比较结果

了解胜者和推理。

### 步骤 2：读取两个 Skill

识别结构差异：
- 指令清晰度
- 脚本/工具使用
- 示例覆盖
- 边界情况处理

### 步骤 3：分析指令遵循

评估每个 Skill 的指令是否被遵循。

### 步骤 4：识别优势弱点

**胜者优势**：什么让它更好？
**败者弱点**：什么阻碍了它？

### 步骤 5：生成改进建议

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner",
    "loser_skill": "path/to/loser"
  },
  "winner_strengths": [
    "清晰的多步骤指令",
    "包含验证脚本"
  ],
  "loser_weaknesses": [
    "模糊指令导致不一致行为",
    "无验证脚本"
  ],
  "instruction_following": {
    "winner": {"score": 9, "issues": []},
    "loser": {"score": 6, "issues": ["未使用格式模板"]}
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "用明确步骤替换模糊指令",
      "expected_impact": "消除歧义"
    }
  ]
}
```

## 建议类别

| 类别 | 说明 |
| :-- | :-- |
| instructions | 指令修改 |
| tools | 脚本/工具 |
| examples | 示例 |
| error_handling | 错误处理 |

## 优先级

- **high**：很可能改变结果
- **medium**：改善质量
- **low**：锦上添花

---

## 基准测试分析模式

分析 benchmark.json 时，发现模式和异常：

### 检查项

- 哪些预期总是通过（不区分价值）
- 哪些预期高方差（不稳定）
- Skill 增加的价值在哪里

### 输出格式

```json
[
  "预期'输出是 PDF'总是通过 - 不区分 Skill 价值",
  "Eval 3 高方差（50% ± 40%）- 可能不稳定",
  "Skill 增加 13 秒但提高 50% 通过率"
]
```