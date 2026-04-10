# Claude Code Skills 创建指南

一个交互式 Claude Code Skill 创建与优化工具，帮助用户快速构建符合规范的 Skills。

## 功能

| 功能 | 命令示例 |
| :-- | :-- |
| **创建 Skill** | `/claude-code-skills-guide 创建代码审查 skill` |
| **优化 Skill** | `/claude-code-skills-guide 优化 fix-issue skill` |
| **解答问题** | `/claude-code-skills-guide 如何传入参数？` |
| **查看指南** | `/claude-code-skills-guide` |

---

## 两层分类体系

创建 Skill 时需要确定两个维度：

### 第一层：功能模式（做什么）

| 类型 | 功能特征 | 典型场景 |
| :-- | :-- | :-- |
| **文档/资产创建** | 生成文档、模板、配置文件 | 写文档、创建组件、生成配置 |
| **工作流程自动化** | 自动化多步骤工作流 | 代码审查、Issue 修复、部署 |
| **多 MCP 协调** | 跨多个 MCP 服务器操作 | 查多个数据源、跨系统操作 |

### 第二层：调用控制（怎么触发）

| 类型 | 判断条件 | 配置 |
| :-- | :-- | :-- |
| **副作用型** | deploy/commit/发消息/删除 | `disable-model-invocation: true` |
| **背景知识型** | 架构/规范/API文档/legacy系统 | `user-invocable: false` |
| **普通工作流** | 其他所有情况 | 默认 |

### 组合示例

| Skill 场景 | 功能模式 | 调用控制 |
| :-- | :-- | :-- |
| Issue 修复 | 工作流程自动化 | 副作用型 |
| 架构说明文档 | 文档/资产创建 | 背景知识型 |
| 代码审查 | 工作流程自动化 | 普通工作流 |
| 组件脚手架 | 文档/资产创建 | 普通工作流 |

---

## 创建流程

1. **需求分析** → 提取功能目标、触发关键词
2. **判断功能模式** → 文档/资产创建、工作流程自动化、多 MCP 协调
3. **判断调用控制** → 副作用型、背景知识型、普通工作流
4. **确定位置** → 项目级（默认）或个人级
5. **询问配置** → 使用 AskUserQuestion 确认
6. **创建目录** → `mkdir -p <skill-dir>/reference`
7. **编写 SKILL.md** → 遵守 ≤200 行规范
8. **验证** → `wc -l` 检查行数

---

## 核心规范

### 目录结构

```
your-skill-name/
├── SKILL.md              # 必需 - ≤200行
├── reference/            # 可选 - 详细文档
├── scripts/              # 可选 - 可执行脚本
└── assets/               # 可选 - 模板资源
```

**禁止目录名**：`docs/`、`templates/`、`data/`

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词（用户实际会说的话） |
| allowed-tools | 空格分隔的工具列表 |
| disable-model-invocation | 副作用型：true |
| user-invocable | 背景知识型：false |

### description 编写

```yaml
# ✅ 合规
description: 审查代码。当用户说"review一下"时触发。检查安全、性能。

# ❌ 违规（无触发关键词）
description: 代码审查工具，检查代码质量
```

### 存放位置

| 级别 | 路径 | 判断 |
| :-- | :-- | :-- |
| 项目级 | `.claude/skills/<name>/` | 默认 |
| 个人级 | `~/.claude/skills/<name>/` | 用户指定"个人" |

---

## 本项目结构

```
claude-code-skills-guide/
├── SKILL.md                    # 主入口（174行）
├── README.md                   # 说明文档
└── reference/                  # 详细文档（按需加载）
    ├── create-guide.md         # AskUserQuestion 完整格式
    ├── skill-patterns.md       # 两层分类体系详解
    ├── examples.md             # 示例概览
    ├── examples-full.md        # 完整代码示例
    ├── advanced-features.md    # 高级特性
    ├── best-practices.md       # 最佳实践
    ├── common-issues.md        # 常见问题
    └── decision-guide.md       # CLAUDE.md vs Skills vs Hooks
```

---

## 参考来源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills 完全指南](https://juejin.cn/post/7612486041334136842) - AlienZHOU
- [obra/superpowers](https://github.com/obra/superpowers) - 社区 Skills 框架

## 许可证

MIT License