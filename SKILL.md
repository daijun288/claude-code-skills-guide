---
name: claude-code-skills-guide
description: Claude Code Skills 创建与优化指南。当用户说"创建 skill"、"写一个 skill"、"帮我做个 skill"、"优化 skill"、"怎么写 skill"时触发。支持创建、优化、解答问题、查看指南。
argument-hint: [问题或需求]
---

# Claude Code Skills 创建指南

## 执行模式判断

**判断规则**：扫描 `$ARGUMENTS` 全文关键词，按优先级判断：

| 关键词（优先级高→低） | 模式 | 执行 |
| :-- | :-- | :-- |
| 含"优化"/"改进"/"重构"/"完善" | D | 优化 Skill |
| 含"创建"/"写一个"/"做个"/"添加"/"修改 skill" | A | 创建 Skill |
| 含"如何"/"怎么"/"什么是"/"能否"/"区别" | B | 解答问题 |
| 其他或空 | C | 显示快速参考 |

---

$ARGUMENTS

---

## 模式 A：创建 Skill

**执行流程（MUST 按顺序）**：

1. **需求分析**：提取功能目标、触发关键词、参数需求
2. **确定位置**：含"个人"→个人级，无指定→项目级（见[create-guide.md](reference/create-guide.md)）
3. **询问配置**：MUST 使用 AskUserQuestion（完整选项见[create-guide.md](reference/create-guide.md)）
4. **创建目录**：`mkdir -p <skill-dir>/reference`
5. **编写 SKILL.md**：遵守规范（见下方）
6. **验证**：`wc -l` 检查行数，检查 frontmatter

**详细流程**：[reference/create-guide.md](reference/create-guide.md)

---

## 模式 D：优化 Skill

**执行流程（MUST 按顺序）**：

1. **定位 Skill**：搜索 `.claude/skills/` 和 `~/.claude/skills/`
2. **读取现状**：`wc -l` + `cat SKILL.md` + `ls -la`
3. **诊断问题**：对照规范检查（诊断表见[create-guide.md](reference/create-guide.md)）
4. **执行优化**：根据诊断结果修复
5. **验证结果**：确认修复成功

**详细流程**：[reference/create-guide.md](reference/create-guide.md)

---

## 模式 B：解答问题

MUST 从 `reference/` 读取内容，MUST NOT 编造。

---

## 模式 C：显示快速参考

展示下方「创建规范」章节。

---

## 创建规范（快速参考）

### 目录结构

```
your-skill-name/
├── SKILL.md              # MUST - ≤200行
├── reference/            # 可选 - 详细文档
├── scripts/              # 可选 - 可执行脚本
└── assets/               # 可选 - 模板资源
```

**禁止目录名**：`docs/`、`templates/`、`data/`

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | MUST：小写+数字+连字符，≤64字符 |
| description | MUST：前置触发关键词 |
| allowed-tools | 可选：空格分隔 |
| disable-model-invocation | 可选：true 禁止自动调用 |
| user-invocable | 可选：false 隐藏菜单 |

### description 编写

**格式**：`<触发关键词>。当用户说"<关键词>"时触发。<功能简述>`

```yaml
# ✅ 合规
description: 审查代码。当用户说"review一下"时触发。检查安全、性能。

# ❌ 违规
description: 代码审查工具，检查代码质量
```

### 存放位置

| 级别 | 路径 | 判断 |
| :-- | :-- | :-- |
| 项目级 | `.claude/skills/<name>/` | 默认 |
| 个人级 | `~/.claude/skills/<name>/` | 用户指定"个人" |

---

## 详细资源

- **完整流程+选项**：[reference/create-guide.md](reference/create-guide.md)
- **示例概览**：[reference/examples.md](reference/examples.md)
- **完整代码**：[reference/examples-full.md](reference/examples-full.md)
- **高级特性**：[reference/advanced-features.md](reference/advanced-features.md)
- **最佳实践**：[reference/best-practices.md](reference/best-practices.md)
- **常见问题**：[reference/common-issues.md](reference/common-issues.md)

---

## 使用示例

```bash
/claude-code-skills-guide 创建代码审查 skill
/claude-code-skills-guide 帮我优化 fix-issue skill
/claude-code-skills-guide 如何传入参数？
```