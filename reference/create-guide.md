# 创建 Skill 完整指南

## AskUserQuestion 配置选项

创建 skill 时使用 AskUserQuestion 工具询问用户：

### allowed-tools 选项

```json
{
  "question": "选择该 skill 需要的工具（免确认模式）：",
  "options": [
    {"label": "只读", "description": "Read Grep Glob - 分析、查阅", "value": "Read Grep Glob"},
    {"label": "修改", "description": "Read Grep Glob Edit Write - 修复、重构", "value": "Read Grep Glob Edit Write"},
    {"label": "Git/GitHub", "description": "Bash(gh/git *) + 读写 - Issue、PR", "value": "Bash(gh *) Bash(git *) Read Grep Glob Edit"},
    {"label": "开发", "description": "读写 + Bash(mvn/npm *) - 构建、测试", "value": "Read Grep Glob Edit Write Bash(mvn *) Bash(npm *)"},
    {"label": "Shell", "description": "Bash(*) Read - 脚本、CI/CD", "value": "Bash(*) Read"},
    {"label": "自定义", "description": "手动输入工具列表", "value": "custom"},
    {"label": "无限制", "description": "不设置，正常权限流程", "value": ""}
  ]
}
```

### 调用控制选项

```json
{
  "question": "选择调用控制方式：",
  "options": [
    {"label": "默认", "description": "用户和 Claude 都能触发", "value": ""},
    {"label": "只能手动触发", "description": "disable-model-invocation: true - deploy/commit 等有副作用的操作", "value": "disable-model-invocation: true"},
    {"label": "只能自动触发", "description": "user-invocable: false - 背景知识型，用户看不到", "value": "user-invocable: false"},
    {"label": "自定义", "description": "手动输入配置", "value": "custom"}
  ]
}
```

**推荐提示**：
- 有副作用（deploy、commit、发消息）→ 推荐"只能手动触发"
- 背景知识（legacy 系统、API 规范）→ 推荐"只能自动触发"
- 普通工作流 → 推荐"默认"

---

## 存放位置

| 位置 | 路径 | 适用范围 |
| :-- | :-- | :-- |
| 个人级 | `~/.claude/skills/<name>/SKILL.md` | 你的所有项目 |
| 项目级 | `.claude/skills/<name>/SKILL.md` | 当前项目（可团队共享） |
| 插件级 | `<plugin>/skills/<name>/SKILL.md` | 启用插件的位置 |

**优先级**：项目级 > 个人级（团队可强制覆盖个人习惯）

### 嵌套目录自动发现

在子目录工作时，Claude Code 会自动从嵌套的 `.claude/skills/` 目录发现 skills。例如在 `packages/frontend/` 编辑文件时，也会查找 `packages/frontend/.claude/skills/`。

适用于 monorepo，每个包可以有独立的 skills。

### --add-dir 目录中的 Skills

使用 `--add-dir` 标志添加的目录，其中的 `.claude/skills/` 也会自动加载。可以在会话期间编辑这些 skills 无需重启。

## SKILL.md 结构

每个 Skill 必须包含 `SKILL.md` 文件，由 YAML frontmatter 和 markdown 内容组成：

```yaml
---
name: my-skill              # Skill 名称（变成 /my-skill 命令）
description: 功能描述        # Claude 用此判断何时自动加载
argument-hint: [参数提示]    # 可选：显示在自动完成中
allowed-tools: Read Grep    # 可选：免确认的工具列表
---

Skill 的具体指令内容...
```

### Frontmatter 完整字段参考

所有字段均为可选，推荐使用 `description`：

| 字段 | 说明 |
| :-- | :-- |
| `name` | Skill 名称。仅小写字母、数字、连字符，最多 64 字符。省略则使用目录名 |
| `description` | **推荐**。功能描述，前置关键用例。前 250 字符决定自动触发 |
| `argument-hint` | 参数提示，如 `[issue-number]`，显示在自动完成中 |
| `disable-model-invocation` | `true` 禁止 Claude 自动调用，只有用户手动触发 |
| `user-invocable` | `false` 从 `/` 菜单隐藏，只有 Claude 能调用 |
| `allowed-tools` | 允许免确认的工具列表（空格分隔或 YAML 列表） |
| `model` | 指定使用的模型 |
| `effort` | 工作量级别：`low`、`medium`、`high`、`max`（仅 Opus 4.6） |
| `context` | `fork` 在子 Agent 中运行 |
| `agent` | 子 Agent 类型（需 `context: fork`）：`Explore`、`Plan`、`general-purpose` |
| `paths` | Glob 模式限制激活范围，逗号分隔或 YAML 列表 |
| `shell` | 内联命令 shell：`bash`（默认）或 `powershell` |
| `hooks` | Skill 生命周期 hooks（详见 hooks 文档） |

## 实战示例：修复 GitHub Issue

```yaml
# ~/.claude/skills/fix-issue/SKILL.md
---
name: fix-issue
description: 分析并修复 GitHub Issue，自动读取 issue 详情、定位相关代码、实现修复、写测试、提 PR。当用户说"修这个 issue"、"fix issue"或提到 issue 编号时触发。
disable-model-invocation: true
allowed-tools: Bash(gh *), Read, Grep, Glob, Edit
---

分析并修复 GitHub Issue #$ARGUMENTS，遵循以下步骤：

1. **读取 Issue 详情**
   运行 `gh issue view $ARGUMENTS` 获取完整描述、标签、评论

2. **理解问题**
   - 从 issue 描述中提取核心问题和复现步骤
   - 判断影响范围（UI bug / 逻辑错误 / 性能问题 / 安全问题）

3. **定位相关代码**
   - 搜索 issue 中提到的关键词、函数名、文件名
   - 阅读相关文件，理解当前实现

4. **实现修复**
   - 先写一个能复现问题的失败测试
   - 然后修改代码让测试通过
   - 确保不影响已有测试

5. **提交和 PR**
   - `git add` 相关文件（不要用 `git add .`）
   - commit message 格式：`fix: [issue#号] 问题简述`
   - 运行 `gh pr create` 创建 PR，body 里 close #$ARGUMENTS

**注意**：如果修复需要数据库 migration，暂停并告知用户，不要自动执行。
```

## 关键配置解释

- `disable-model-invocation: true`：用户选择"只能手动触发"，涉及 git 操作不能让 AI 自行判断
- `allowed-tools: Bash(gh *)`：用户选择 Git/GitHub 模式，只允许 gh 命令免确认
- `description`：前置用户会说的关键词，不是技术描述

## 写好 description 的原则

description 前 250 字符决定自动触发关键词。**把用户实际会说的话放前面，技术术语放后面**：

```yaml
# ❌ 差的 description
description: 代码审查工具，用于检查代码质量、安全性和性能问题

# ✅ 好的 description  
description: 审查代码。当用户说"review 一下"、"帮我看看这段代码"、"code review"时触发。检查安全漏洞、性能问题、代码规范。
```

### description 预算限制

- 每条 description 在 skill 列表中被截断为 **250 字符**
- 整个 session 所有 skills 的 description 总预算约 **8000 字符**（随上下文窗口动态调整）
- 如果 skills 很多导致预算超出，考虑：
  - 精简 description
  - 提高 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量

## 调用控制字段详解

| 字段 | 设为 true 效果 | 适用场景 |
| :-- | :-- | :-- |
| `disable-model-invocation: true` | 只有用户手动 /invoke 才触发 | deploy、commit、发消息等有副作用的操作 |
| `user-invocable: false` | 用户看不到，只有 Claude 自动触发 | legacy 系统说明、内部 API 规范等背景知识 |

## 背景知识型 Skill 示例

用户选择"只能自动触发"时的配置：

```yaml
---
name: legacy-payment-system
description: 老支付系统架构说明和踩坑记录。处理支付相关代码时自动加载。
user-invocable: false
---

老支付系统使用 X 架构，已知问题：...
```

## 支持文件结构

**创建 skill 时优先采用渐进式加载**，分文件按需读取：

```
my-skill/
├── SKILL.md           # 主文件：执行指令 + 快速参考 + 资源导航（保持简洁）
├── reference/         # 详情目录（按需加载）
│   ├── guide.md       # 详细指南
│   ├── examples.md    # 使用示例
│   └── faq.md         # 常见问题
└── scripts/           # 脚本文件（需要时执行）
    └── helper.sh
```

### 渐进式加载原则

1. **SKILL.md 保持简洁**：只放执行指令和快速参考，不超过 200 行
2. **详情放支持文件**：详细指南、示例、FAQ 放 `reference/` 目录
3. **按需加载**：在 SKILL.md 中引用支持文件，Claude 需要时才读取
4. **节省 token**：避免每次触发都加载完整内容

### SKILL.md 结构模板

```yaml
---
name: my-skill
description: 简短描述，前置触发关键词
---

# 主标题

## 执行指令
简要步骤说明

$ARGUMENTS

## 快速参考
核心配置表格

## 详细资源
- 指南：[reference/guide.md](reference/guide.md)
- 示例：[reference/examples.md](reference/examples.md)
- FAQ：[reference/faq.md](reference/faq.md)
```

### 复杂 Skill 示例

```
api-designer/
├── SKILL.md          # 主文件（概述和导航，<200行）
├── reference/
│   ├── guide.md      # 设计指南详细说明
│   ├── examples.md   # 15 个 API 设计示例
│   ├── anti-patterns.md  # 常见反模式
│   └── checklist.md  # 上线前自检清单
└── templates/
    └── endpoint.md   # 端点模板
```

### 何时拆分

| 内容长度 | 建议 |
| :-- | :-- |
| SKILL.md < 100 行 | 可以不拆分 |
| SKILL.md 100-200 行 | 考虑拆分 |
| SKILL.md > 200 行 | **必须拆分**到支持文件 |