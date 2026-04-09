# 工具选择决策指南

## CLAUDE.md vs Skills vs Hooks

很多人会把这三个混用，效果都不好。按"触发时机"和"强制程度"选择：

```
我想让 Claude 记住某件事 → 每次都需要吗？
  是，每次 session 就要用 → CLAUDE.md
  不是，只在特定场景触发 → 需要强制执行吗？
    是，不能让 Claude 自己决定 → Hooks
    不是，AI 判断即可 → 有固定工作流步骤吗？
      是，多个步骤可复用流程 → Skills
      不是，只是上下文知识 → CLAUDE.md
```

## 三者本质差异

| 特性 | CLAUDE.md | Skills | Hooks |
| :-- | :-- | :-- | :-- |
| 加载时机 | 每次 session 全量加载 | 按需加载（相关时自动或手动） | 工具事件触发 |
| 消耗 Token | 是，每次消耗 | 只在使用时消耗 | 否（Shell 脚本） |
| 强制程度 | 建议性（可能忽略） | 建议性 | **强制执行** |
| 适合场景 | 项目规范、架构背景 | 可复用工作流、团队规范 | 安全检查、质量门禁 |

## 关键提示

- CLAUDE.md 超 200 行，Claude 遵从度明显下降
- Skills 按需触发，30 个 Skills 的 description 加起来 token 开销很小
- 绝对强制执行用 Hooks，CLAUDE.md 和 Skills 都是建议性的