# 测试评估流程

> 本文档为 SKILL.md 的详细补充，模式 F 的完整流程。

---

## 流程概览

```
创建测试用例 → 运行测试 → 评估结果 → 收集反馈 → 迭代改进
```

---

## 创建测试用例

### 用例设计原则

| 原则 | 说明 |
| :-- | :-- |
| 真实性 | 用户真实会说的 prompt |
| 多样性 | 覆盖正常、边界、异常 |
| 可验证 | 预期结果可客观判断 |

### 保存位置

`<skill-dir>/evals/evals.json`

### 格式

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "帮我生成 users 控制器的 API 文档",
      "expected_output": "Markdown 格式的 API 文档",
      "expectations": [
        "输出包含 GET /users 路由",
        "输出包含 POST /users 路由",
        "输出包含参数说明"
      ]
    }
  ]
}
```

---

## 运行测试

### 简单测试

用子 Agent 执行测试 prompt：

```
执行任务：
- Skill 路径: <path-to-skill>
- 任务: <eval prompt>
- 保存输出到: <workspace>/eval-<ID>/outputs/
```

### 检查输出

对照 expectations 检查每个预期是否满足。

---

## 评估结果

### 使用 grader agent

委托 `agents/grader.md` 评估输出：

```
评估任务：
- expectations: ["输出包含 X", "使用了脚本 Y"]
- outputs_dir: <workspace>/eval-<ID>/outputs/
```

### 输出格式

```json
{
  "expectations": [
    {
      "text": "输出包含 GET /users 路由",
      "passed": true,
      "evidence": "在输出第 5 行找到"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  }
}
```

---

## 收集反馈

让用户查看输出，收集改进建议。

---

## 迭代改进

根据反馈修改 Skill，重新测试。

---

## 相关文件

- [reference/schemas.md](schemas.md) - JSON 格式定义
- [agents/grader.md](../agents/grader.md) - 评估 Agent