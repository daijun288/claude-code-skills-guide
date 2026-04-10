# 创建 Skill 完整指南

> 本文档为 SKILL.md 的详细补充，提供 AskUserQuestion 完整格式。

---

## AskUserQuestion 完整选项

创建 skill 时 **MUST 使用 AskUserQuestion 工具**，按顺序询问三个问题：

### 问题 1：功能模式

```json
{
  "questions": [{
    "question": "确认 Skill 功能类型：",
    "header": "功能",
    "multiSelect": false,
    "options": [
      {"label": "文档/资产创建", "description": "生成文档、模板、配置文件"},
      {"label": "工作流程自动化", "description": "自动化多步骤工作流"},
      {"label": "多 MCP 协调", "description": "跨多个 MCP 服务器操作"}
    ]
  }]
}
```

### 问题 2：调用控制

```json
{
  "questions": [{
    "question": "确认调用控制方式：",
    "header": "调用",
    "multiSelect": false,
    "options": [
      {"label": "副作用型", "description": "deploy/commit → disable-model-invocation: true"},
      {"label": "背景知识型", "description": "架构/规范 → user-invocable: false"},
      {"label": "普通工作流", "description": "默认配置"}
    ]
  }]
}
```

### 问题 3：allowed-tools

```json
{
  "questions": [{
    "question": "选择需要的工具（免确认）：",
    "header": "工具",
    "multiSelect": false,
    "options": [
      {"label": "只读", "description": "Read Grep Glob - 分析、查阅"},
      {"label": "修改", "description": "Read Grep Glob Edit Write - 修复、重构"},
      {"label": "Git/GitHub", "description": "Bash(gh/git *) + 读写 - Issue、PR"},
      {"label": "开发", "description": "读写 + Bash(mvn/npm *) - 构建、测试"},
      {"label": "Shell", "description": "Bash(*) Read - 脚本、CI/CD"},
      {"label": "无限制", "description": "不设置"}
    ]
  }]
}
```

---

## 推荐判断

| 判断条件 | MUST 推荐 |
| :-- | :-- |
| deploy/commit/发消息/删除 | "副作用型" |
| 架构/规范/API文档/legacy系统 | "背景知识型" |
| 其他 | "普通工作流" |

---

## Frontmatter 字段完整列表

| 字段 | 说明 |
| :-- | :-- |
| `name` | MUST：小写+数字+连字符，≤64字符 |
| `description` | MUST：前置触发关键词 |
| `argument-hint` | 参数提示，如 `[issue-number]` |
| `allowed-tools` | 免确认工具，空格分隔 |
| `disable-model-invocation` | `true` 禁止自动调用 |
| `user-invocable` | `false` 隐藏菜单 |
| `model` | 指定模型：`opus`/`sonnet`/`haiku` |
| `effort` | 工作量级别：`low`/`medium`/`high`/`max` |
| `paths` | 限制激活范围，Glob 模式 |
| `context` | `fork` 在子 Agent 中运行 |
| `agent` | 子 Agent 类型：`Explore`/`Plan`/`general-purpose` |
| `hooks` | 生命周期 hooks：`pre`/`post` |
| `shell` | 内联 shell：`bash`/`powershell` |

---

## 优化诊断表

| 检查项 | 方法 | 标准 | 等级 |
| :-- | :-- | :-- | :-- |
| 行数 | `wc -l` | ≤200 | MUST |
| name | 检查 frontmatter | 合格式 | MUST |
| description | 检查 frontmatter | 有触发词 | MUST |
| 目录名 | `ls -la` | reference/scripts/assets | SHOULD |
| 引用路径 | 检查 markdown | 相对路径 | SHOULD |

---

## 优化操作表

| 问题 | 操作 |
| :-- | :-- |
| 行数 > 200 | 拆分到 `reference/` |
| description 无触发词 | 前置用户会说的话 |
| name 不合规 | 重命名目录 |
| 目录名非标准 | `mv docs reference` |
| 引用路径绝对 | 改为相对路径 |

---

## 验证清单

- [ ] `wc -l` 结果 ≤200
- [ ] frontmatter 格式正确
- [ ] name 合规
- [ ] description 有触发关键词
- [ ] 目录名标准

验证通过：`✅ Skill 创建/优化成功：/<name>`