---
name: claude-code-skills-guide
description: 创建、优化、测试、评估和打包 Claude Code Skills。当用户说"创建 skill"、"写一个 skill"、"帮我做个 skill"、"优化 skill"、"怎么写 skill"、"skill 创建"、"skill 打包"、"skill 测试"、"skill 基准测试"、"description 优化"时触发。即使用户只提到"skill"或想要定制化 Claude 的工作流，也应使用此 skill。
argument-hint: [问题或需求]
---

# Claude Code Skills 完整指南

## ⚠️ 核心约束

1. **创建 Skill 前 MUST 使用 AskUserQuestion 确认配置**
2. **SKILL.md 行数 MUST ≤200 行**
3. **副作用型 Skill MUST 设置 `disable-model-invocation: true`**
4. **回答问题 MUST 从 reference/ 读取，MUST NOT 编造**

---

## 执行模式

| 关键词 | 模式 | 说明 |
| :-- | :-- | :-- |
| 打包/package | E | 打包 Skill |
| 基准测试/benchmark | G | 量化评估（见 reference/benchmark.md） |
| 盲比较/比较 | H | 客观比较（见 reference/comparison.md） |
| description 优化 | I | 触发优化（见 reference/description-optimization.md） |
| 优化/改进 | D | 优化 Skill |
| 创建/写一个/做个 | A | 创建 Skill |
| 测试/验证/评估 | F | 测试评估（见 reference/testing.md） |
| 如何/怎么 | B | 解答问题 |
| 其他 | C | 快速参考 |

---

$ARGUMENTS

---

## 模式 A：创建 Skill

### 流程（按顺序执行）

```
步骤 1：捕获意图 → 步骤 2：判断配置 → 步骤 3：确认配置 → 步骤 4：编写 → 步骤 5：验证
```

---

### 步骤 1：捕获意图

如果对话中已有工作流程，提取：工具、步骤、修正、输入输出。

如果信息不完整，询问：
- 这个 Skill 做什么？
- 什么时候触发？
- 输出格式是什么？

---

### 步骤 2：判断配置

**功能模式**：

| 关键词 | 类型 |
| :-- | :-- |
| 创建/生成/模板 | 文档/资产创建 |
| 自动化/流程/部署 | 工作流程自动化 |
| MCP/跨系统 | 多 MCP 协调 |

**调用控制**：

| 判断条件 | 配置 |
| :-- | :-- |
| deploy/commit/发消息/删除 | **MUST** `disable-model-invocation: true` |
| 架构/规范/API文档 | **MUST** `user-invocable: false` |
| 其他 | 默认 |

---

### 步骤 3：确认配置

**⚠️ MUST 使用 AskUserQuestion 确认三个问题**：

**问题 1 - 功能类型**：
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

**问题 2 - 调用控制**：
```json
{
  "questions": [{
    "question": "确认调用控制方式：",
    "header": "调用",
    "multiSelect": false,
    "options": [
      {"label": "副作用型", "description": "deploy/commit → 只能手动触发"},
      {"label": "背景知识型", "description": "架构/规范 → 自动加载"},
      {"label": "普通工作流", "description": "默认配置"}
    ]
  }]
}
```

**问题 3 - 工具权限**：
```json
{
  "questions": [{
    "question": "选择需要的工具（免确认）：",
    "header": "工具",
    "multiSelect": false,
    "options": [
      {"label": "只读", "description": "Read Grep Glob"},
      {"label": "修改", "description": "读写 + Edit Write"},
      {"label": "Git/GitHub", "description": "Bash(gh/git *) + 读写"},
      {"label": "无限制", "description": "不设置"}
    ]
  }]
}
```

---

### 步骤 4：编写 SKILL.md

**Frontmatter 规范**：

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符，不以 `-` 开始/结束 |
| description | 前置触发关键词，写得 pushy |
| 行数 | **MUST ≤200 行** |

**description 格式**：

```
<功能简述>。当用户说"<关键词>"时触发。即使用户提到<相关概念>，也应使用此 skill。
```

---

### 步骤 5：验证

**✅ 检查点**：

- [ ] name 合规
- [ ] description 有触发关键词且 pushy
- [ ] 副作用型已设置 `disable-model-invocation: true`
- [ ] 背景知识型已设置 `user-invocable: false`
- [ ] 行数 ≤200

```bash
wc -l <skill-dir>/SKILL.md
```

---

## 模式 D：优化 Skill

### 诊断

| 检查项 | 标准 |
| :-- | :-- |
| 行数 | **MUST ≤200** |
| name | 合规格式 |
| description | 有触发词、pushy |

### 优化

| 问题 | 操作 |
| :-- | :-- |
| 行数 > 200 | **MUST** 拆分到 reference/ |
| description 无触发词 | **MUST** 前置关键词 |
| Skill 不触发 | 见模式 I |

### 检查点

- [ ] 行数 ≤200
- [ ] description 已优化
- [ ] 配置正确

---

## 模式 E：打包

```bash
python scripts/quick_validate.py <skill-dir>
python scripts/package_skill.py <skill-dir>
```

---

## 模式 B：解答问题

**MUST 从 reference/ 读取，MUST NOT 编造。**

---

## 模式 C：快速参考

### 目录结构

```
skill-name/
├── SKILL.md              # MUST - ≤200行
├── reference/            # 可选
├── scripts/              # 可选
├── agents/               # 可选
└── evals/                # 可选 - 测试用例
```

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词，pushy |
| disable-model-invocation | 副作用型：**MUST** true |
| user-invocable | 背景知识型：**MUST** false |

### 两层分类

| 功能模式 \ 调用控制 | 副作用型 | 背景知识型 | 普通 |
| :-- | :-- | :-- | :-- |
| 文档/资产创建 | 迁移执行 | 表结构说明 | API 文档 |
| 工作流程自动化 | 版本发布 | — | 性能分析 |
| 多 MCP 协调 | 跨系统同步 | 集成规范 | 文档同步 |

---

## 详细资源（按需读取）

| 文件 | 内容 |
| :-- | :-- |
| [reference/guide.md](reference/guide.md) | 创建详解、边界情况、示例 |
| [reference/testing.md](reference/testing.md) | 测试评估流程 |
| [reference/benchmark.md](reference/benchmark.md) | 基准测试流程 |
| [reference/comparison.md](reference/comparison.md) | 盲比较流程 |
| [reference/description-optimization.md](reference/description-optimization.md) | Description 优化 |
| [reference/schemas.md](reference/schemas.md) | JSON 格式定义 |

---

## Agents（按需委托）

| 文件 | 用途 |
| :-- | :-- |
| `agents/grader.md` | 评估 Skill 输出 |
| `agents/validator.md` | 验证 Skill 结构 |
| `agents/comparator.md` | 盲比较两个输出 |
| `agents/analyzer.md` | 分析比较结果 |

---

## 脚本

| 脚本 | 用途 |
| :-- | :-- |
| `scripts/quick_validate.py` | 验证 Skill 结构 |
| `scripts/package_skill.py` | 打包 Skill |
| `scripts/run_eval.py` | 触发评估 |
| `scripts/run_loop.py` | Description 优化循环 |
| `scripts/aggregate_benchmark.py` | 聚合基准测试 |

---

## 核心流程

```
理解需求 → 确认配置 → 编写 Skill → 测试验证 → 改进 → 打包
```

**MUST 使用 TaskList 追踪进度。**