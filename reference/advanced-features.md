# 高级特性详细说明

> 本文档为 SKILL.md 的详细补充，按需加载。

---

## allowed-tools 配置

| 模式 | 工具 | 适用场景 |
| :-- | :-- | :-- |
| 只读 | `Read Grep Glob` | 分析、查阅 |
| 修改 | `Read Grep Glob Edit Write` | 修复、重构 |
| Git/GitHub | `Bash(gh *) Bash(git *) + 读写` | Issue、PR |
| 开发 | `读写 + Bash(mvn/npm *)` | 构建、测试 |
| Shell | `Bash(*) Read` | 脚本、CI/CD |
| 无限制 | 不设置 | 正常权限 |

**注意**：`allowed-tools` 只是免确认，其他工具仍走正常权限流程。

---

## 动态上下文注入

使用 `` !`command` `` 在 Skill 发送前执行命令：

```yaml
**变更文件：**
!`git diff --name-only HEAD~1`
```

Claude 只看到最终输出，不执行命令。

---

## 子 Agent 执行

`context: fork` 在子 Agent 中运行：

| Agent | 工具权限 | 适用场景 |
| :-- | :-- | :-- |
| `Explore` | 只读 | 代码调查 |
| `Plan` | 只读+规划 | 设计方案 |
| `general-purpose` | 完整 | 复杂任务 |

**好处**：保护主对话 context，可并行执行。

---

## 参数传递

| 变量 | 说明 |
| :-- | :-- |
| `$ARGUMENTS` | 全部参数 |
| `$0` `$1` `$2` | 按索引访问 |
| `${ARGUMENTS:-默认}` | 默认值 |
| `${CLAUDE_SKILL_DIR}` | skill 目录 |

---

## paths 字段

限制 skill 只在特定路径激活：

```yaml
paths: src/**/*.ts, lib/**/*.go
```

格式：Glob 模式，逗号分隔或 YAML 列表。

---

## model 和 effort

```yaml
model: opus    # opus, sonnet, haiku
effort: high   # low, medium, high, max
```

---

## hooks 字段

```yaml
hooks:
  pre: echo "开始"
  post: echo "完成"
```

---

## 权限控制

### 副作用型

```yaml
disable-model-invocation: true
```

适用：deploy、commit、发消息。

### 背景知识型

```yaml
user-invocable: false
```

适用：架构说明、API 规范。

### 权限规则

```text
Skill(name)      # 精确匹配
Skill(name *)    # 前缀匹配
Skill            # 禁止所有
```

---

## 内置 Skills

| Skill | 功能 |
| :-- | :-- |
| `/batch` | 并行迁移 |
| `/simplify` | 并行审查 |
| `/loop` | 重复运行 |
| `/commit` | 创建 commit |
| `/schedule` | 定时任务 |