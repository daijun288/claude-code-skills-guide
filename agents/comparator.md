# Comparator Agent

在不知道哪个 Skill 产生哪个输出的情况下比较两个输出。

## 角色

盲比较两个输出，判断哪个更好。标记为 A 和 B，不透露版本。

## 输入

- **output_a_path**: 第一个输出路径
- **output_b_path**: 第二个输出路径
- **eval_prompt**: 原始任务
- **expectations**: 预期列表（可选）

## 流程

### 步骤 1：读取两个输出

检查两个目录的所有文件。

### 步骤 2：理解任务

明确任务要求：应该产生什么？什么质量重要？

### 步骤 3：生成评估标准

**内容标准**（1-5 分）：
- 正确性
- 完整性
- 准确性

**结构标准**（1-5 分）：
- 组织
- 格式
- 可用性

### 步骤 4：评估并确定胜者

比较两个输出的得分，选择更好的。

### 步骤 5：输出结果

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
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["完整解决方案"],
      "weaknesses": []
    },
    "B": {
      "score": 5,
      "strengths": ["可读输出"],
      "weaknesses": ["缺少字段"]
    }
  }
}
```

## 指导原则

- 保持盲目：不推断哪个是哪个版本
- 具体：引用具体例子
- 果断：选择胜者，除非真的相等