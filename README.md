# Claude Code Skills 完整指南

一个帮助创建、优化、测试、评估和打包 Claude Code Skills 的完整工具。

## 功能

| 功能 | 命令示例 |
| :-- | :-- |
| **创建 Skill** | `创建 skill` 或 `写一个 skill` |
| **优化 Skill** | `优化 skill` 或 `改进 skill` |
| **测试评估** | `测试 skill` 或 `验证 skill` |
| **基准测试** | `基准测试 skill` |
| **盲比较** | `比较两个版本` |
| **Description 优化** | `description 优化` |
| **打包** | `打包 skill` |
| **解答问题** | `如何写 skill` |

---

## 两层分类体系

创建 Skill 时需要确定两个维度：

### 第一层：功能模式（做什么）

| 类型 | 功能特征 |
| :-- | :-- |
| **文档/资产创建** | 生成文档、模板、配置文件 |
| **工作流程自动化** | 自动化多步骤工作流 |
| **多 MCP 协调** | 跨多个 MCP 服务器操作 |

### 第二层：调用控制（怎么触发）

| 类型 | 判断条件 | 配置 |
| :-- | :-- | :-- |
| **副作用型** | deploy/commit/发消息 | `disable-model-invocation: true` |
| **背景知识型** | 架构/规范文档 | `user-invocable: false` |
| **普通工作流** | 其他 | 默认 |

---

## 核心规范

### 目录结构

```
skill-name/
├── SKILL.md              # 必需 - ≤200行
├── reference/            # 可选 - 详细文档
├── scripts/              # 可选 - 可执行脚本
├── agents/               # 可选 - 子 agent 指导
└── evals/                # 可选 - 测试用例
```

### Frontmatter

| 字段 | 规范 |
| :-- | :-- |
| name | 小写+数字+连字符，≤64字符 |
| description | 前置触发关键词，写得 pushy |
| disable-model-invocation | 副作用型：true |
| user-invocable | 背景知识型：false |

### description 示例

```yaml
# ✅ 合规
description: 生成 API 文档。当用户说"生成接口文档"时触发。即使用户只提到"文档"，也应使用此 skill。

# ❌ 无触发关键词
description: 本 Skill 用于生成 API 文档
```

---

## 本项目结构

```
claude-code-skills-guide/
├── SKILL.md                    # 核心流程 + 9 模式（282行）
├── README.md                   # 说明文档
├── reference/                  # 详细文档（按需加载）
│   ├── guide.md                # 创建详解、边界情况、示例
│   ├── testing.md              # 测试评估流程
│   ├── benchmark.md            # 基准测试流程
│   ├── comparison.md           # 盲比较流程
│   ├── description-optimization.md  # Description 优化
│   └── schemas.md              # JSON 格式定义
├── agents/                     # 子 agent 指导
│   ├── grader.md               # 评估 Skill 输出
│   ├── validator.md            # 验证 Skill 结构
│   ├── comparator.md           # 盲比较两个输出
│   └── analyzer.md             # 分析比较结果
└── scripts/                    # 可执行脚本
    ├── quick_validate.py       # 验证 Skill 结构
    ├── package_skill.py        # 打包 Skill
    ├── run_eval.py             # 触发评估
    ├── run_loop.py             # Description 优化循环
    └── aggregate_benchmark.py  # 聚合基准测试
```

---

## 快速开始

1. **创建 Skill**：说 `创建 skill`，按提示确认配置
2. **验证**：`python scripts/quick_validate.py <skill-dir>`
3. **打包**：`python scripts/package_skill.py <skill-dir>`

---

## 参考来源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills 完全指南](https://juejin.cn/post/7612486041334136842)
- [obra/superpowers](https://github.com/obra/superpowers)

---

> 📦 **GitHub**：[daijun288/claude-code-skills-guide](https://github.com/daijun288/claude-code-skills-guide)

MIT License