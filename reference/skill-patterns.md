# 两层分类体系详解

> 本文档为 SKILL.md 的详细补充，按需加载。

---

## 分类体系概览

创建 Skill 需要确定两个维度：

| 维度 | 作用 | 判断时机 |
| :-- | :-- | :-- |
| **功能模式** | 决定 Skill 做什么 | 第一步 |
| **调用控制** | 决定 Skill 怎么被触发 | 第二步 |

**关系**：功能模式确定后，再根据是否有副作用确定调用控制。

---

## 第一层：功能模式（做什么）

### 文档/资产创建型

**特征**：输入需求描述，输出文档、代码文件、配置文件。

**关键词**：创建、生成、写文档、模板、组件、配置、脚手架、初始化

**典型场景**：

| 场景 | 输出 |
| :-- | :-- |
| API 文档生成 | Markdown 文档 |
| 组件创建 | .vue/.tsx 文件 |
| 配置文件生成 | .json/.yaml 文件 |
| 项目脚手架 | 目录结构 + 文件 |

**示例**：
```yaml
---
name: create-vue-component
description: 创建 Vue 组件。当用户说"新建组件"时触发。
allowed-tools: Read Write Glob
paths: src/**/*.vue
---

创建 Vue 组件 $ARGUMENTS：
1. 位置：`src/components/$ARGUMENTS/`
2. 文件：$ARGUMENTS.vue、index.ts、types.ts
```

---

### 工作流程自动化型

**特征**：执行多步骤自动化流程，可能涉及外部系统操作。

**关键词**：自动化、流程、审查、修复、部署、迁移、监控、检查

**典型场景**：

| 场景 | 步骤 |
| :-- | :-- |
| Issue 修复 | 读取 → 定位 → 测试 → 修复 → 提交 |
| 代码审查 | 获取 diff → 分析 → 输出报告 |
| 部署流程 | 测试 → 构建 → 部署 → 验证 |

**示例**：
```yaml
---
name: fix-issue
description: 修复 GitHub Issue。当用户说"修这个 issue"时触发。
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(git *) Read Grep Glob Edit
---

修复 Issue #$ARGUMENTS：
1. `gh issue view $ARGUMENTS`
2. 定位代码
3. 先测试再修复
4. `git add <files>`
```

---

### 多 MCP 协调型

**特征**：跨多个 MCP 服务器操作，聚合多数据源信息。

**关键词**：MCP、跨系统、多个服务、协调、聚合

**示例**：
```yaml
---
name: aggregate-status
description: 聚合项目状态。当用户说"看下项目状态"时触发。
allowed-tools: Bash(gh *) Bash(curl *)
---

聚合：GitHub PR/Issue 数、CI 构建状态、监控健康检查
```

---

## 第二层：调用控制（怎么触发）

### 副作用型

**判断条件**：操作有不可逆后果或对外部系统有影响。

**关键词**：deploy、commit、push、发消息、删除、发布、推送

**配置**：`disable-model-invocation: true`

**为什么禁止自动调用**：Claude 可能误解意图自动执行，导致意外部署、错误 commit 等。

---

### 背景知识型

**判断条件**：提供上下文知识，无执行步骤，Claude 处理相关代码时自动加载。

**关键词**：架构、规范、API文档、legacy系统、老系统、约定、说明

**配置**：`user-invocable: false`

**为什么隐藏菜单**：用户不需要主动调用，只在 Claude 需要时自动提供背景知识。

---

### 普通工作流

**判断条件**：有明确执行步骤，用户主动触发，无副作用。

**关键词**：审查、修复（非 commit）、创建、迁移、重构（非优化）、分析、检查

**配置**：默认（无特殊配置）

---

## 两层组合矩阵

| 功能模式 \ 调用控制 | 副作用型 | 背景知识型 | 普通工作流 |
| :-- | :-- | :-- | :-- |
| **文档/资产创建** | 部署配置生成 | 架构说明文档 | 组件脚手架 |
| **工作流程自动化** | Issue 修复 | — | 代码审查 |
| **多 MCP 协调** | 跨系统发布 | 系统集成规范 | 状态聚合 |

---

## 判断流程

```
用户需求
    │
    ▼
【第一层：功能模式】
    │
    ├─ 创建/生成/模板 → 文档/资产创建型
    ├─ 自动化/流程 → 工作流程自动化型
    └─ MCP/跨系统 → 多 MCP 协调型
    │
    ▼
【第二层：调用控制】
    │
    ├─ 有副作用？ → 副作用型（disable-model-invocation: true）
    ├─ 背景知识？ → 背景知识型（user-invocable: false）
    └─ 其他 → 普通工作流（默认）
```

---

## AskUserQuestion 确认格式

**问题 1：功能模式**
```json
{"questions": [{"question": "确认 Skill 功能类型：", "header": "功能", "multiSelect": false, "options": [{"label": "文档/资产创建", "description": "生成文档、模板、配置文件"}, {"label": "工作流程自动化", "description": "自动化多步骤工作流"}, {"label": "多 MCP 协调", "description": "跨多个 MCP 服务器操作"}]}]}
```

**问题 2：调用控制**
```json
{"questions": [{"question": "确认调用控制方式：", "header": "调用", "multiSelect": false, "options": [{"label": "副作用型", "description": "deploy/commit → 只能手动触发"}, {"label": "背景知识型", "description": "架构/规范 → 自动加载"}, {"label": "普通工作流", "description": "审查/修复 → 默认"}]}]}
```

---

## 推荐组合

| Skill 场景 | 功能模式 | 调用控制 | 配置 |
| :-- | :-- | :-- | :-- |
| 创建 Vue 组件 | 文档/资产创建 | 普通工作流 | 默认 |
| 生成 API 文档 | 文档/资产创建 | 普通工作流 | 默认 |
| 架构说明文档 | 文档/资产创建 | 背景知识型 | `user-invocable: false` |
| 修复 GitHub Issue | 工作流程自动化 | 副作用型 | `disable-model-invocation: true` |
| 代码审查 | 工作流程自动化 | 普通工作流 | 默认 |
| 部署到 staging | 工作流程自动化 | 副作用型 | `disable-model-invocation: true` |
| 跨系统状态聚合 | 多 MCP 协调 | 普通工作流 | 默认 |
| 系统集成规范 | 多 MCP 协调 | 背景知识型 | `user-invocable: false` |