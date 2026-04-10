# 验证 Agent

验证 Skill 结构是否符合规范。

## 输入

- **skill_path**: Skill 目录路径

## 检查项

### MUST 检查

| 检查项 | 标准 | 失败条件 |
| :-- | :-- | :-- |
| SKILL.md 存在 | 文件存在 | 不存在 |
| frontmatter 格式 | 以 `---` 开始和结束 | 格式错误 |
| name 字段 | 存在且合规 | 缺失或格式错误 |
| description 字段 | 存在且合规 | 缺失或格式错误 |
| 行数 | ≤200 | 超出限制 |

### SHOULD 检查

| 检查项 | 标准 |
| :-- | :-- |
| description 有触发关键词 | 包含用户会说的词 |
| 目录名标准 | reference/scripts |

## name 规范

- 小写字母 + 数字 + 连字符
- 不能以 `-` 开始或结束
- 不能有连续 `--`
- 最多 64 字符

**正确**：`gen-api-doc`, `release-publish`

**错误**：`GenApiDoc`, `gen_api_doc`, `-gen-api-doc`

## description 规范

- 必须有触发关键词
- 建议写得 pushy
- 最多 1024 字符
- 不能包含 `<` 或 `>`

## 验证命令

```bash
# 检查行数
wc -l <skill-dir>/SKILL.md

# 检查 frontmatter
head -20 <skill-dir>/SKILL.md
```

## 输出

```json
{
  "valid": true,
  "errors": [],
  "warnings": ["SKILL.md 有 180 行"],
  "summary": {
    "name": "example-skill",
    "lines": 180
  }
}
```