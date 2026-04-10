# 实战示例集

> 完整代码见 [examples-full.md](examples-full.md)

---

## 示例概览

| Skill | 功能 | 特性 |
| :-- | :-- | :-- |
| fix-issue | 修复 GitHub Issue | 禁止自动调用、gh/git 工具 |
| codebase-visualizer | 代码库可视化图 | scripts 脚本、视觉输出 |
| pr-review | PR 代码审查 | fork Agent、动态注入 |
| watch-deploy | 部署监控 | 禁止自动调用、轮询脚本 |
| legacy-payment | 背景知识 | 隐藏菜单、自动加载 |

---

## 示例 1：fix-issue（标准 Skill）

```yaml
---
name: fix-issue
description: 修复 GitHub Issue。当用户说"修这个issue"时触发。
argument-hint: [issue-number]
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(git *) Read Grep Glob Edit
---

修复 Issue #$ARGUMENTS：

1. MUST：`gh issue view $ARGUMENTS`
2. 搜索相关代码
3. 先写测试，再修复
4. `git add` 具体文件（禁止 `git add .`）

## 禁止
- MUST NOT 自动执行数据库 migration
```

---

## 示例 2：pr-review（fork Agent）

```yaml
---
name: pr-review
description: 审查当前 PR。当用户说"review PR"时触发。
context: fork
agent: Explore
allowed-tools: Bash(gh *) Read Grep Glob
---

**变更文件：**
!`gh pr diff --name-only`

审查维度：安全、边界、可维护性、测试覆盖
```

---

## 示例 3：legacy-payment（背景知识）

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

## 示例 4：codebase-visualizer（带脚本）

```yaml
---
name: codebase-visualizer
description: 生成代码库可视化。当用户说"可视化项目"时触发。
allowed-tools: Bash(python *)
---

运行：`python ${CLAUDE_SKILL_DIR}/scripts/visualize.py $ARGUMENTS`
生成交互式 HTML 树形视图。
```

---

## 示例 5：watch-deploy（轮询脚本）

```yaml
---
name: watch-deploy
description: 监控部署状态。当用户说"看下部署进度"时触发。
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(curl *)
---

监控 $ARGUMENTS：
每 30 秒检查 CI 状态，完成时通知。
```

---

## 复杂结构示例

```
api-designer/
├── SKILL.md              # 概述 + 导航
├── reference/
│   ├── examples.md       # 15 个示例
│   └── checklist.md      # 上线自检
└── assets/
    └── endpoint.md       # 端点模板
```

---

**完整代码**：[examples-full.md](examples-full.md)