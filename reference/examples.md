# 实战示例集

> 完整代码见 [examples-full.md](examples-full.md)，分类体系见 [skill-patterns.md](reference/skill-patterns.md)

---

## 按两层分类

### 文档/资产创建 + 普通工作流

| Skill | 功能 | 输出 |
| :-- | :-- | :-- |
| create-vue-component | 创建 Vue 组件 | .vue/.ts 文件 |
| api-doc-generator | 生成 API 文档 | Markdown 文档 |
| config-generator | 生成配置文件 | .json/.yaml 文件 |

### 文档/资产创建 + 背景知识型

| Skill | 功能 | 配置 |
| :-- | :-- | :-- |
| legacy-payment | 老支付系统架构 | `user-invocable: false` |
| api-specification | API 规范说明 | `user-invocable: false` |

### 工作流程自动化 + 副作用型

| Skill | 功能 | 副作用 |
| :-- | :-- | :-- |
| fix-issue | 修复 GitHub Issue | commit、push、PR |
| deploy-staging | 部署到 staging | 发布操作 |
| watch-deploy | 部署监控 | 轮询 API |

### 工作流程自动化 + 普通工作流

| Skill | 功能 | 特性 |
| :-- | :-- | :-- |
| pr-review | PR 代码审查 | fork Agent |
| codebase-visualizer | 代码库可视化 | 生成 HTML |

### 多 MCP 协调 + 普通工作流

| Skill | 功能 | 涉及系统 |
| :-- | :-- | :-- |
| aggregate-status | 项目状态聚合 | GitHub + CI + 监控 |

---

## 示例 1：create-vue-component

**分类**：文档/资产创建 + 普通工作流

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

## 示例 2：legacy-payment

**分类**：文档/资产创建 + 背景知识型

```yaml
---
name: legacy-payment
description: 老支付系统架构说明。处理支付相关代码时自动加载。
user-invocable: false
---

已知问题：
- MUST 避免：直接修改 `payments` 表
- MUST 使用：`PaymentService.updateStatus()`
```

---

## 示例 3：fix-issue

**分类**：工作流程自动化 + 副作用型

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
4. `git add <files>`（禁止 `git add .`）
```

---

## 示例 4：pr-review

**分类**：工作流程自动化 + 普通工作流

```yaml
---
name: pr-review
description: 审查当前 PR。当用户说"review PR"时触发。
context: fork
agent: Explore
allowed-tools: Bash(gh *) Read Grep Glob
---

变更文件：!`gh pr diff --name-only`
审查维度：安全、边界、可维护性、测试
```

---

## 示例 5：aggregate-status

**分类**：多 MCP 协调 + 普通工作流

```yaml
---
name: aggregate-status
description: 聚合项目状态。当用户说"看下项目状态"时触发。
allowed-tools: Bash(gh *) Bash(curl *)
---

聚合：
1. GitHub：PR/Issue 数
2. CI：构建状态
3. 监控：健康检查
```

---

## 分类判断示例

| 用户需求 | 功能模式 | 调用控制 | 配置 |
| :-- | :-- | :-- | :-- |
| "创建部署脚本" | 文档/资产创建 | 普通工作流 | 默认 |
| "修复 issue #123" | 工作流程自动化 | 副作用型 | `disable-model-invocation: true` |
| "审查这个 PR" | 工作流程自动化 | 普通工作流 | 默认 |
| "老系统架构说明" | 文档/资产创建 | 背景知识型 | `user-invocable: false` |
| "跨系统数据查询" | 多 MCP 协调 | 普通工作流 | 默认 |

---

**完整代码**：[examples-full.md](examples-full.md)