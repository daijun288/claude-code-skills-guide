# 常见问题解答

## Q: Skills 和 CLAUDE.md 指令，Claude 更听哪个？

没有优先级之分，都是 context，Claude 会"参考"但不强制执行。区别在于加载时机。**绝对强制执行用 Hooks**。

---

## Q: Skill 描述加了关键词但不触发？

**排查步骤**：

1. 运行 `What skills are available?` 看能否列出
2. 能列出但不触发 → description 关键词和你说的话差距太大
3. 列不出来 → 检查路径是否正确（必须是 `skills/<name>/SKILL.md`）
4. Skills 太多 → description 预算超出（约 8000 字符）

**解决**：
- 精简 description
- 提高 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量

---

## Q: context: fork 结果在哪里？

子 Agent 结果以摘要返回主对话，工作过程（读了哪些文件）不出现在主对话，保持 context 干净。

---

## Q: 30 个 Skills 会导致 session 慢吗？

不会。只有 description 加载到 context（每条最多 250 字符），完整内容触发时才加载。

---

## Q: allowed-tools 设置后其他工具还能用吗？

能。`allowed-tools` 只是这些工具免确认，其他工具仍触发正常权限流程。

---

## Q: 如何传入多个参数？

使用 `$N` 按位置访问：

```yaml
将 $0 组件从 $1 迁移到 $2
```

调用：`/skill-name arg1 arg2 arg3`

---

## Q: 如何不传参数时使用默认值？

```yaml
分析项目：${ARGUMENTS:-.}
```

当用户未传参数时，`.` 作为默认值。

---

## Q: 如何只在特定目录激活？

使用 `paths` 字段：

```yaml
---
name: frontend-guide
description: 前端开发规范
paths: web-ui/**, src/**/*.vue, src/**/*.ts
---
```