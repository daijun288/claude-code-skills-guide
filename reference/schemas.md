# JSON 格式定义

> 本文档定义测试用例的 JSON 结构。

---

## evals.json

测试用例定义，位于 `<skill-dir>/evals/evals.json`。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户的测试 prompt",
      "expected_output": "预期结果描述",
      "expectations": [
        "输出包含 X",
        "使用了脚本 Y"
      ]
    }
  ]
}
```

**字段说明**：
- `skill_name`: 与 Skill frontmatter 中 name 匹配
- `evals[].id`: 唯一数字标识
- `evals[].prompt`: 执行的任务
- `evals[].expected_output`: 成功的人类可读描述
- `evals[].expectations`: 可验证的陈述列表

---

## 测试用例示例

```json
{
  "skill_name": "gen-api-doc",
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
    },
    {
      "id": 2,
      "prompt": "写一下 product 相关的接口文档",
      "expected_output": "产品相关 API 文档",
      "expectations": [
        "输出包含产品相关路由",
        "格式正确"
      ]
    }
  ]
}
```

---

## 注意事项

- 所有 JSON 文件使用 UTF-8 编码
- 布尔值使用 `true/false`，不是字符串
- 数值使用数字类型