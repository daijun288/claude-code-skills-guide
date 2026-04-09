# 高级特性详细说明

## 一、allowed-tools 配置

### 概念

`allowed-tools` 设置哪些工具在该 skill 活动时免确认，其他工具仍按正常权限流程处理。

### 常用工具组合

| 模式 | allowed-tools | 适用场景 |
| :-- | :-- | :-- |
| **只读模式** | `Read Grep Glob` | 代码分析、文档查阅、只读审查 |
| **代码修改** | `Read Grep Glob Edit Write` | 修复 bug、重构、实现功能 |
| **Git/GitHub** | `Bash(gh *) Bash(git *) Read Grep Glob Edit` | 修复 issue、创建 PR |
| **完整开发** | `Read Grep Glob Edit Write Bash(mvn *) Bash(npm *)` | 构建、测试、开发流程 |
| **Shell 脚本** | `Bash(*) Read` | 执行脚本、CI/CD |
| **无限制** | 不设置字段 | 所有工具正常权限流程 |

### Bash 命令格式

- `Bash(gh *)` - 允许所有 gh 开头的命令（gh issue view, gh pr create 等）
- `Bash(git *)` - 允许所有 git 命令
- `Bash(mvn *)` - 允许 Maven 命令
- `Bash(npm *)` - 允许 npm 命令
- `Bash(*)` - 允许所有 Bash 命令（谨慎使用）

### 组合示例

```yaml
# 只读 + Git 查看
allowed-tools: Read Grep Glob Bash(gh *) Bash(git log *) Bash(git status *)

# 前端开发
allowed-tools: Read Grep Glob Edit Write Bash(npm *) Bash(npx *)

# 后端开发（Java）
allowed-tools: Read Grep Glob Edit Write Bash(mvn *)
```

---

## 二、动态上下文注入

使用 `` !`command` `` 在 Skill 发送给 Claude 前执行命令，输出替换占位符：

```yaml
---
name: pr-review
description: 审查当前 PR 的代码变更。当用户说"review 这个 PR"、"帮我看看 PR"时触发。
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---

## 当前 PR 信息

**PR 标题和描述：**
!`gh pr view --json title,body -q '.title + "\n\n" + .body'`

**变更文件列表：**
!`gh pr diff --name-only`

**完整 Diff：**
!`gh pr diff`

---

请按以下维度审查：

1. **安全性**：SQL 注入、XSS、不安全的直接对象引用
2. **边界条件**：空值处理、类型检查、并发安全
3. **可维护性**：代码风格一致性、函数复杂度、注释质量
4. **测试覆盖**：关键路径是否有对应测试

每个问题给出：文件+行号、问题描述、建议改法。
```

**注意**：这是预处理，Claude 只看到最终结果，不执行命令。

---

## 三、子 Agent 执行（context: fork）

### 两个好处

1. **保护主对话 context**：大量文件读取会塞满 context window，子 Agent 用自己的 context，只返回摘要
2. **并行执行**：多个 fork Skill 可同时跑，互不干扰

### agent 字段选项

| Agent | 特点 | 适用场景 |
| :-- | :-- | :-- |
| `Explore` | 只读工具 | 代码调查、分析 |
| `Plan` | 分析 + 规划 | 设计方案 |
| `general-purpose` | 完整工具集 | 复杂任务 |

---

## 四、参数传递

### $ARGUMENTS 占位符

用户调用 `/skill-name arg1 arg2` 时，参数通过 `$ARGUMENTS` 传入：

```yaml
修复 GitHub issue $ARGUMENTS
```

调用 `/fix-issue 123` → 内容变成"修复 GitHub issue 123"

### 按索引访问

使用 `$ARGUMENTS[N]` 或简写 `$N`：

```yaml
将 $0 组件从 $1 迁移到 $2
```

调用 `/migrate-component SearchBar React Vue`：
- `$0` → SearchBar
- `$1` → React
- `$2` → Vue

### 其他可用变量

| 变量 | 说明 |
| :-- | :-- |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_SKILL_DIR}` | skill 所在目录 |

---

## 六、paths 字段：目录限制

使用 `paths` 限制 skill 只在特定文件路径激活：

```yaml
---
name: frontend-guide
description: 前端开发规范，处理 Vue/React 组件时自动加载
paths: web-ui/**, src/**/*.vue, src/**/*.tsx, src/**/*.jsx
---
```

**格式**：Glob 模式，逗号分隔或 YAML 列表：

```yaml
# 逗号分隔
paths: web-ui/**, src/**/*.vue

# YAML 列表
paths:
  - web-ui/**
  - src/**/*.vue
  - src/**/*.tsx
```

---

## 七、权限控制 Skills

默认 Claude 可以调用任何未设置 `disable-model-invocation: true` 的 skill。三种控制方式：

### 1. 在 /permissions 中拒绝 Skill 工具

```text
# 禁止所有 skills
Skill
```

### 2. 使用权限规则允许/拒绝特定 skills

```text
# 只允许特定 skills
Skill(commit)
Skill(review-pr *)

# 拒绝特定 skills
Skill(deploy *)
```

语法：`Skill(name)` 精确匹配，`Skill(name *)` 前缀匹配带任意参数。

### 3. 通过 frontmatter 禁止自动调用

`disable-model-invocation: true` 完全从 Claude 的 context 中删除该 skill。

---

## 八、Skills vs Subagents 对比

两种方式协同工作：

| 方法 | 系统提示来源 | 任务来源 | 加载内容 |
| :-- | :-- | :-- | :-- |
| `context: fork` 的 Skill | 代理类型（Explore/Plan 等） | SKILL.md 内容 | CLAUDE.md |
| 带 `skills` 字段的 Subagent | Subagent 的 markdown | Claude 委派消息 | 预加载 skills + CLAUDE.md |

**使用场景**：
- 已有固定工作流 → 用 `context: fork` Skill
- 需自定义代理配置 → 用 Subagent + skills 字段

| Skill | 功能 |
| :-- | :-- |
| `/batch <指令>` | 大规模并行代码迁移，自动分解成 5-30 个单元 |
| `/simplify [聚焦点]` | 启动 3 个并行 review Agent 检查代码 |
| `/loop [间隔] <prompt>` | 按间隔重复运行，适用于轮询部署 |
| `/debug [描述]` | 开启调试日志，分析 session 问题 |