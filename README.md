# Claude Code Skills 创建指南

一个用于创建、管理和学习 Claude Code Skills 的交互式指南工具。

## 功能特性

- **直接创建 Skill**：描述需求，自动生成 SKILL.md
- **解答问题**：回答 Skills 相关的技术问题
- **查看指南**：完整的 Skills 开发参考

## 快速使用

```bash
# 创建新 skill
/claude-code-skills-guide 创建代码审查 skill，检查 Java 规范

# 解答问题
/claude-code-skills-guide 如何传入多个参数？

# 查看完整指南
/claude-code-skills-guide
```

## 目录结构

```
claude-code-skills-guide/
├── SKILL.md                    # 主入口文件
└── reference/                  # 详细文档（按需加载）
    ├── create-guide.md         # 创建完整指南
    ├── advanced-features.md    # 高级特性详解
    ├── best-practices.md       # 最佳实践与踩坑
    ├── common-issues.md        # 常见问题
    ├── examples.md             # 实战示例
    └── decision-guide.md       # 工具选择决策
```

## 创建 Skill 流程

1. **分析需求** - 理解功能、参数、触发条件
2. **确定位置** - 项目级或个人级
3. **询问配置** - 使用 AskUserQuestion 选择工具和调用控制
4. **创建目录** - 采用渐进式加载结构
5. **编写文件** - 遵循创建规范
6. **验证** - 确认可用

## 核心配置选项

### allowed-tools 预设

| 选项 | 工具 | 场景 |
| :-- | :-- | :-- |
| 只读 | Read Grep Glob | 分析、查阅 |
| 修改 | Read Grep Glob Edit Write | 修复、重构 |
| Git/GitHub | Bash(gh/git *) + 读写 | Issue、PR |
| 开发 | 读写 + Bash(mvn/npm *) | 构建、测试 |
| Shell | Bash(*) Read | 脚本、CI/CD |

### 调用控制

| 选项 | 配置 | 场景 |
| :-- | :-- | :-- |
| 默认 | 不设置 | 普通工作流 |
| 只能手动触发 | disable-model-invocation: true | deploy、commit |
| 只能自动触发 | user-invocable: false | 背景知识 |

## 参考来源

- [Claude Code 官方文档](https://code.claude.com/docs)
- Redis 高手码哥《Claude Code Skills 完全指南》实战经验

## 许可证

MIT License