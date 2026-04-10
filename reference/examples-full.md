# 实战示例完整代码

> 本文件为 examples.md 的详细补充，按需加载。

---

## fix-issue

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

禁止：自动执行数据库 migration
```

---

## pr-review（fork Agent）

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

## legacy-payment（背景知识）

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

## codebase-visualizer（带脚本）

SKILL.md：

```yaml
---
name: codebase-visualizer
description: 生成代码库可视化。当用户说"可视化项目"时触发。
allowed-tools: Bash(python *)
---

运行：`python ${CLAUDE_SKILL_DIR}/scripts/visualize.py $ARGUMENTS`
生成交互式 HTML 树形视图。
```

scripts/visualize.py（核心逻辑）：

```python
IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'dist', 'build'}

def scan(path, stats):
    result = {"name": path.name, "children": [], "size": 0}
    for item in sorted(path.iterdir()):
        if item.name in IGNORE or item.name.startswith('.'):
            continue
        # 文件/目录处理逻辑...
    return result
```

---

## watch-deploy（轮询）

```yaml
---
name: watch-deploy
description: 监控部署状态。当用户说"看下部署进度"时触发。
disable-model-invocation: true
allowed-tools: Bash(gh *) Bash(curl *)
---

监控 $ARGUMENTS：每 30 秒检查 CI 状态，完成时通知。
```

---

## create-vue-component（带模板）

```yaml
---
name: create-vue-component
description: 创建 Vue 组件。当用户说"新建组件"时触发。
allowed-tools: Read, Write, Glob
paths: web-ui/**, src/**/*.vue
---

创建 $ARGUMENTS：
- `$ARGUMENTS.vue` - 组件本体
- `index.ts` - 导出
模板：${CLAUDE_SKILL_DIR}/assets/vue-component.md
```

---

## api-designer（复杂结构）

目录结构：

```
api-designer/
├── SKILL.md              # 概述 + 导航
├── reference/
│   ├── examples.md       # 15 个示例
│   └── checklist.md      # 上线自检
└── assets/
    └── endpoint.md       # 端点模板
```

SKILL.md：

```yaml
---
name: api-designer
description: API 设计指南。当用户说"设计 API"时触发。
paths: src/**/controller/**, src/**/api/**
---

设计 API 端点：$ARGUMENTS

参考：
- 示例：[reference/examples.md](reference/examples.md)
- 模板：[assets/endpoint.md](assets/endpoint.md)
- 自检：[reference/checklist.md](reference/checklist.md)
```