---
name: claude-code-skills-guide
description: Claude Code Skills 创建指南。当用户说"创建 skill"、"写一个 skill"、"帮我做个 skill"、"怎么写 skill"时触发。支持直接创建、解答问题、查看指南。
argument-hint: [问题或需求]
---

# Claude Code Skills 创建指南

## 执行模式

根据 $ARGUMENTS 内容判断：

### 模式 A：创建/修改 Skill

触发词：创建、帮我、修改、添加、写一个

**执行步骤**：
1. 分析需求 → 理解功能、参数、触发条件
2. 确定位置 → 项目级（默认）或个人级（用户指定"个人"）
3. 询问配置 → **使用 AskUserQuestion 工具**，选项见 [reference/create-guide.md](reference/create-guide.md)
4. 创建目录 → `mkdir -p <skill-dir>/reference`（渐进式加载）
5. 编写文件 → 遵循 [创建规范](#创建规范)，采用 [渐进式加载](#渐进式加载)
6. 验证 → 确认创建成功，告知测试方法

### 模式 B：解答问题

触发词：如何、怎么、什么是、能否、区别

从支持文件提取相关内容解答。

### 模式 C：显示指南

无参数或"指南"、"帮助"

展示快速参考，需要详情时加载支持文件。

---

$ARGUMENTS

---

## 快速参考

### 创建规范

| 项目 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词，前250字符决定自动触发 |
| allowed-tools | 用户 AskUserQuestion 选择 |
| 调用控制 | 用户 AskUserQuestion 选择 |
| SKILL.md | ≤200行，超出拆分到支持文件 |

### 渐进式加载

```
my-skill/
├── SKILL.md           # 执行指令 + 快速参考 + 资源导航
└── reference/         # 详情按需加载
    ├── guide.md
    └── examples.md
```

### 存放位置

| 级别 | 路径 | 范围 |
| :-- | :-- | :-- |
| 项目级 | `.claude/skills/<name>/` | 当前项目 |
| 个人级 | `~/.claude/skills/<name>/` | 所有项目 |

---

## 详细资源

- **创建指南**：[reference/create-guide.md](reference/create-guide.md) - Frontmatter、allowed-tools 选项、调用控制选项、示例
- **高级特性**：[reference/advanced-features.md](reference/advanced-features.md) - 动态注入、子Agent、paths、权限控制
- **最佳实践**：[reference/best-practices.md](reference/best-practices.md) - 团队共享、踩坑记录
- **常见问题**：[reference/common-issues.md](reference/common-issues.md) - FAQ
- **实战示例**：[reference/examples.md](reference/examples.md) - 完整示例代码
- **工具选择**：[reference/decision-guide.md](reference/decision-guide.md) - CLAUDE.md vs Skills vs Hooks

---

## 使用示例

```bash
# 创建 skill
/claude-code-skills-guide 创建代码审查 skill

# 解答问题
/claude-code-skills-guide 如何传入多个参数？

# 查看指南
/claude-code-skills-guide
```
