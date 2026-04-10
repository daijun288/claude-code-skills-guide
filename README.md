# Claude Code Skills 创建指南

一个交互式 Claude Code Skill 创建与优化工具，帮助用户快速构建符合规范的 Skills。

## 功能

| 功能 | 命令示例 |
| :-- | :-- |
| **创建 Skill** | `/claude-code-skills-guide 创建代码审查 skill` |
| **优化 Skill** | `/claude-code-skills-guide 优化 fix-issue skill` |
| **解答问题** | `/claude-code-skills-guide 如何传入参数？` |
| **查看指南** | `/claude-code-skills-guide` |

## 核心规范

### 目录结构

```
your-skill-name/
├── SKILL.md              # 必需 - ≤200行
├── reference/            # 可选 - 详细文档
├── scripts/              # 可选 - 可执行脚本
└── assets/               # 可选 - 模板资源
```

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词（用户实际会说的话） |
| allowed-tools | 空格分隔的工具列表 |
| disable-model-invocation | true 禁止自动调用 |
| user-invocable | false 隐藏菜单 |

### description 编写

```yaml
# ✅ 合规
description: 审查代码。当用户说"review一下"时触发。检查安全、性能。

# ❌ 违规
description: 代码审查工具，检查代码质量
```

## 本项目结构

```
claude-code-skills-guide/
├── SKILL.md                    # 主入口（128行）
├── README.md                   # 说明文档
└── reference/                  # 详细文档（按需加载）
    ├── create-guide.md         # 创建/优化完整流程
    ├── examples.md             # 示例概览
    ├── examples-full.md        # 完整代码示例
    ├── advanced-features.md    # 高级特性
    ├── best-practices.md       # 最佳实践
    ├── common-issues.md        # 常见问题
    └── decision-guide.md       # 工具选择决策
```

## 创建流程

1. **需求分析** → 提取功能目标、触发关键词
2. **确定位置** → 项目级（默认）或个人级
3. **询问配置** → allowed-tools + 调用控制
4. **创建目录** → `mkdir -p <skill-dir>/reference`
5. **编写 SKILL.md** → 遵守 ≤200行规范
6. **验证** → `wc -l` 检查行数

## 配置选项

### allowed-tools

| 模式 | 工具 | 场景 |
| :-- | :-- | :-- |
| 只读 | Read Grep Glob | 分析、查阅 |
| 修改 | Read Grep Glob Edit Write | 修复、重构 |
| Git/GitHub | Bash(gh/git *) + 读写 | Issue、PR |
| 开发 | 读写 + Bash(mvn/npm *) | 构建、测试 |
| Shell | Bash(*) Read | 脚本、CI/CD |

### 调用控制

| 选项 | 适用场景 |
| :-- | :-- |
| 默认 | 普通工作流 |
| 只能手动触发 | deploy、commit 等有副作用操作 |
| 只能自动触发 | legacy 系统说明等背景知识 |

## 参考来源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills 完全指南](https://juejin.cn/post/7612486041334136842) - AlienZHOU

## 许可证

MIT License