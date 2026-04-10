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

**Bash 格式**：`Bash(gh *)` 允许所有 gh 命令，`Bash(*)` 允许所有命令。

---

## 动态上下文注入

使用 `` !`command` `` 在 Skill 发送前执行命令：

```yaml
**变更文件：**
!`gh pr diff --name-only`
```

Claude 只看到最终输出，不执行命令。

---

## 子 Agent 执行

`context: fork` 在子 Agent 中运行：

| Agent | 特点 | 适用场景 |
| :-- | :-- | :-- |
| `Explore` | 只读工具 | 代码调查 |
| `Plan` | 分析+规划 | 设计方案 |
| `general-purpose` | 完整工具集 | 复杂任务 |

好处：保护主对话 context，可并行执行。

---

## 参数传递

| 变量 | 说明 |
| :-- | :-- |
| `$ARGUMENTS` | 全部参数 |
| `$0` `$1` `$2` | 按索引访问 |
| `${CLAUDE_SESSION_ID}` | 会话 ID |
| `${CLAUDE_SKILL_DIR}` | skill 目录 |

---

## paths 字段

限制 skill 只在特定路径激活：

```yaml
paths: web-ui/**, src/**/*.vue, src/**/*.tsx
```

格式：Glob 模式，逗号分隔或 YAML 列表。

---

## 权限控制

### 禁止自动调用

```yaml
disable-model-invocation: true
```

### 权限规则

```text
# 只允许特定 skills
Skill(commit)
Skill(review-pr *)

# 拒绝特定 skills
Skill(deploy *)
```

---

## Skills vs Subagents

| 方法 | 系统提示来源 | 适用场景 |
| :-- | :-- | :-- |
| `context: fork` Skill | 代理类型 | 固定工作流 |
| Subagent + skills 字段 | 自定义配置 | 自定义代理 |

---

## 内置 Skills

| Skill | 功能 |
| :-- | :-- |
| `/batch` | 大规模并行代码迁移 |
| `/simplify` | 3 个并行 review Agent |
| `/loop` | 按间隔重复运行 |
| `/debug` | 开启调试日志 |