# 最佳实践与踩坑记录

---

## 团队共享目录结构

```
.claude/skills/
├── gen-api-doc/
│   └── SKILL.md          # 普通工作流
├── release-publish/
│   └── SKILL.md          # disable-model-invocation: true
├── analyze-perf/
│   └── SKILL.md          # 普通工作流，fork Agent
└── db-schema/
    └── SKILL.md          # user-invocable: false
```

---

## 关键原则

| Skill 类型 | 配置建议 |
| :-- | :-- |
| 有副作用的 Skill | `disable-model-invocation: true` |
| 背景知识型 Skill | `user-invocable: false` |

**优先级**：项目级 > 个人级

---

## 踩坑记录

### 坑一：description 写成技术文档

❌ `"本 Skill 用于生成 API 文档..."`

✅ `"生成 API 文档。当用户说"生成接口文档"时触发..."`

### 坑二：SKILL.md 过长

把所有内容塞进 SKILL.md 写了 500 行

**正确做法**：SKILL.md 保持 ≤200 行，其余拆分到 `reference/`

### 坑三：context: fork 里写条件判断

子 Agent 没有主对话历史

**解决**：用 `$ARGUMENTS` 显式传参

### 坑四：allowed-tools 误解

`allowed-tools` 只是免确认，其他工具仍可用

---

## 排查 Skill 不触发

1. 运行 `What skills are available?` 看能否列出
2. 检查 description 关键词
3. 检查路径：`skills/<name>/SKILL.md`
4. 检查 description 预算（约 8000 字符）

---

## Skill 触发过于频繁

如果 Claude 在不想要时使用你的 skill：

1. 使 description 更具体
2. 添加 `disable-model-invocation: true`