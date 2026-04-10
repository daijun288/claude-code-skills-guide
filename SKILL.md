---
name: claude-code-skills-guide
description: Claude Code Skills 创建与优化指南。当用户说"创建 skill"、"写一个 skill"、"帮我做个 skill"、"优化 skill"、"怎么写 skill"时触发。支持创建、优化、解答问题、查看指南。
argument-hint: [问题或需求]
---

# Claude Code Skills 创建指南

## 执行模式判断

扫描 `$ARGUMENTS` 关键词，按优先级判断：

| 关键词 | 模式 | 执行 |
| :-- | :-- | :-- |
| 优化/改进/重构/完善 | D | 优化 Skill |
| 创建/写一个/做个/添加 | A | 创建 Skill |
| 如何/怎么/什么是/能否 | B | 解答问题 |
| 其他或空 | C | 显示快速参考 |

---

$ARGUMENTS

---

## 模式 A：创建 Skill

**MUST 按顺序执行**：

### 步骤 1：需求分析

提取：功能目标、触发关键词、参数需求

### 步骤 2：判断功能模式

| 关键词 | 类型 |
| :-- | :-- |
| 创建/生成/模板/配置 | 文档/资产创建 |
| 自动化/流程/部署/审查 | 工作流程自动化 |
| MCP/跨系统/协调 | 多 MCP 协调 |

### 步骤 3：判断调用控制

| 判断条件 | 配置 |
| :-- | :-- |
| deploy/commit/发消息/删除 | `disable-model-invocation: true` |
| 架构/规范/API文档 | `user-invocable: false` |
| 其他 | 默认 |

### 步骤 4：确定位置

含"个人"→ `~/.claude/skills/<name>/`，无指定→ `.claude/skills/<name>/`

### 步骤 5：询问配置（MUST 使用 AskUserQuestion）

**问题 1：功能模式**

选项：文档/资产创建 | 工作流程自动化 | 多 MCP 协调

**问题 2：调用控制**

选项：副作用型（`disable-model-invocation: true`）| 背景知识型（`user-invocable: false`）| 普通工作流（默认）

**问题 3：allowed-tools**

选项：只读 | 修改 | Git/GitHub | Shell | 无限制

### 步骤 6：创建目录

```bash
mkdir -p <skill-dir>/reference
```

### 步骤 7：编写 SKILL.md

| 项目 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词 |
| 行数 | MUST ≤200行 |

**description 格式**：`<关键词>。当用户说"<关键词>"时触发。<功能简述>`

### 步骤 8：验证

```bash
wc -l <skill-dir>/SKILL.md  # MUST ≤200
```

检查：name 合规、description 有触发关键词、目录名标准

---

## 模式 D：优化 Skill

### 步骤 1：定位

```bash
ls -la .claude/skills/<name>/ 2>/dev/null || ls -la ~/.claude/skills/<name>/ 2>/dev/null
```

### 步骤 2：诊断

| 检查项 | 方法 | 标准 | 等级 |
| :-- | :-- | :-- | :-- |
| 行数 | `wc -l` | ≤200 | MUST |
| name | 检查 frontmatter | 合规格式 | MUST |
| description | 检查 frontmatter | 有触发词 | MUST |
| 目录名 | `ls -la` | reference/scripts/assets | SHOULD |

### 步骤 3：优化

| 问题 | 操作 |
| :-- | :-- |
| 行数 > 200 | 拆分到 `reference/` |
| description 无触发词 | 前置关键词 |
| 目录名非标准 | 重命名 |

### 步骤 4：验证

确认修复成功，输出：`✅ Skill 优化完成：/<name>`

---

## 模式 B：解答问题

MUST 从 `reference/` 读取，MUST NOT 编造。

---

## 模式 C：显示快速参考

展示下方内容。

---

## 创建规范（快速参考）

### 目录结构

```
your-skill-name/
├── SKILL.md              # MUST - ≤200行
├── reference/            # 可选
├── scripts/              # 可选
└── assets/               # 可选
```

**禁止目录名**：`docs/`、`templates/`、`data/`

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词 |
| disable-model-invocation | 副作用型：true |
| user-invocable | 背景知识型：false |

### 存放位置

项目级：`.claude/skills/<name>/`（默认）
个人级：`~/.claude/skills/<name>/`（用户指定"个人"）

---

## 详细资源

- **AskUserQuestion 完整 JSON**：[reference/create-guide.md](reference/create-guide.md)
- **两层分类详解**：[reference/skill-patterns.md](reference/skill-patterns.md)
- **示例**：[reference/examples.md](reference/examples.md)
- **高级特性**：[reference/advanced-features.md](reference/advanced-features.md)
- **最佳实践**：[reference/best-practices.md](reference/best-practices.md)