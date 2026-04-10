# 高级特性详细说明

> 本文档为 SKILL.md 的详细补充，按需加载。

---

## allowed-tools 配置

| 模式 | 工具 | 适用场景 |
| :-- | :-- | :-- |
| 只读 | `Read Grep Glob` | 分析、查阅 |
| 修改 | `Read Grep Glob Edit Write` | 修复、重构 |
| Git/GitHub | `Bash(gh *) Bash(git *) Read Grep Glob Edit` | Issue、PR |
| 开发 | `Read Grep Glob Edit Write Bash(mvn *) Bash(npm *)` | 构建、测试 |
| Shell | `Bash(*) Read` | 脚本、CI/CD |
| 无限制 | 不设置 | 正常权限流程 |

**Bash 格式**：
- `Bash(gh *)` - 允许所有 gh 命令
- `Bash(git *)` - 允许所有 git 命令
- `Bash(*)` - 允许所有命令（谨慎使用）

**注意**：`allowed-tools` 只是免确认，其他工具仍走正常权限流程。

---

## 动态上下文注入

使用 `` !`command` `` 在 Skill 发送给 Claude 前执行命令，输出替换占位符：

```yaml
---
name: pr-review
description: 审查当前 PR。当用户说"review PR"时触发。
context: fork
agent: Explore
---

**变更文件：**
!`gh pr diff --name-only`

**完整 Diff：**
!`gh pr diff`
```

**特点**：Claude 只看到最终输出，不执行命令。

---

## 子 Agent 执行（context: fork）

`context: fork` 在子 Agent 中运行 Skill：

| Agent | 工具权限 | 适用场景 |
| :-- | :-- | :-- |
| `Explore` | 只读 | 代码调查、分析 |
| `Plan` | 只读+规划 | 设计方案 |
| `general-purpose` | 完整 | 复杂任务 |

**好处**：保护主对话 context，可并行执行。

---

## 参数传递

| 变量 | 说明 | 示例 |
| :-- | :-- | :-- |
| `$ARGUMENTS` | 全部参数 | `修复 $ARGUMENTS` |
| `$0` `$1` `$2` | 按索引访问 | `将 $0 从 $1 迁移到 $2` |
| `${ARGUMENTS:-默认}` | 默认值 | `分析 ${ARGUMENTS:-.}` |
| `${CLAUDE_SESSION_ID}` | 会话 ID | 日志追踪 |
| `${CLAUDE_SKILL_DIR}` | skill 目录 | 引用脚本 |

---

## paths 字段

限制 skill 只在特定文件路径激活：

```yaml
paths: web-ui/**, src/**/*.vue, src/**/*.tsx
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

## model 和 effort 字段

### model

指定 Skill 使用的模型：

```yaml
model: opus    # 或 sonnet, haiku
```

### effort

设置工作量级别（仅 Opus 4.6）：

```yaml
effort: high    # low, medium, high, max
```

| 级别 | 适用场景 |
| :-- | :-- |
| `low` | 简单任务 |
| `medium` | 常规任务（默认） |
| `high` | 复杂分析 |
| `max` | 最复杂任务 |

---

## hooks 字段

Skill 生命周期 hooks：

```yaml
---
name: my-skill
hooks:
  pre: echo "Skill starting"
  post: echo "Skill finished"
---
```

| Hook | 触发时机 |
| :-- | :-- |
| `pre` | Skill 执行前 |
| `post` | Skill 执行后 |

---

## 权限控制详解

### disable-model-invocation

禁止 Claude 自动调用，只能用户手动触发：

```yaml
disable-model-invocation: true
```

适用：deploy、commit、发消息等有副作用的操作。

### user-invocable

从 `/` 菜单隐藏，只有 Claude 能调用：

```yaml
user-invocable: false
```

适用：legacy 系统说明、API 规范等背景知识。

### 权限规则设置

在 `/permissions` 中配置：

```text
# 只允许特定 skills
Skill(commit)
Skill(review-pr *)

# 拒绝特定 skills
Skill(deploy *)

# 禁止所有 skills
Skill
```

**语法**：`Skill(name)` 精确匹配，`Skill(name *)` 前缀匹配。

---

## Skills vs Subagents

| 方法 | 适用场景 |
| :-- | :-- |
| `context: fork` Skill | 固定工作流 |
| Subagent + skills 字段 | 自定义代理配置 |

---

## 内置 Skills

| Skill | 功能 |
| :-- | :-- |
| `/batch` | 并行代码迁移 |
| `/simplify` | 并行 review |
| `/loop` | 按间隔重复运行 |
| `/commit` | 创建 commit |
| `/schedule` | 定时远程 agent |