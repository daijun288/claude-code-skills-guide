# 详细指南

> 本文档为 SKILL.md 的详细补充，按需加载。

---

## 为什么有这些约束？

### 为什么 MUST 使用 AskUserQuestion？

**问题**：用户经常配置错误：
- 副作用型没禁止自动调用 → Claude 自动执行了发布
- 背景知识型没隐藏菜单 → 用户不知道什么时候调用

**解决**：通过 AskUserQuestion 强制确认，避免错误。

### 为什么副作用型 MUST 设置 disable-model-invocation: true？

**场景**：用户说"帮我发布一下新版本"

**风险**：
- Claude 可能理解为"立即执行发布"
- 意外部署到生产环境
- 错误的 commit 污染历史

**解决**：禁止自动调用，必须用户明确手动触发。

### 为什么背景知识型 MUST 设置 user-invocable: false？

**场景**：创建了"数据库表结构说明"Skill

**问题**：用户不需要知道这个 Skill 存在

**解决**：隐藏菜单，Claude 处理相关代码时自动加载。

### 为什么 description MUST 写得 pushy？

**问题**：Claude 有"不触发"倾向——该用 Skill 时不用

**解决**：主动说明"即使用户只提到 X，也应使用此 skill"。

### 为什么 SKILL.md MUST ≤200 行？

**原因**：
- 过长消耗更多 token
- Claude 遵从度下降

---

## 判断配置详解

### 功能模式边界情况

| 情况 | 判断 | 原因 |
| :-- | :-- | :-- |
| 生成 SQL 迁移脚本 | 文档创建 | 输出文件 |
| 执行 SQL 迁移 | 工作流程 | 执行操作 |
| 同步到 Notion | 多 MCP 协调 | 跨系统 |
| 本地格式转换 | 工作流程 | 单系统 |

### 调用控制边界情况

| 操作 | 配置 | 原因 |
| :-- | :-- | :-- |
| 创建 PR | 副作用型 | PR 公开可见 |
| 创建本地分支 | 普通 | 本地可逆 |
| 发送消息 | 副作用型 | 不可撤回 |
| 写本地文件 | 普通 | git 可恢复 |

---

## 判断流程

```
用户需求
    │
    ▼
【第一层：功能模式】
最终输出是文件？ ──────────────────→ 文档/资产创建
    │
    否
    │
    ▼
涉及多个外部系统？ ────────────────→ 多 MCP 协调
    │
    否
    │
    ▼
工作流程自动化
    │
    ▼
【第二层：调用控制】
有不可逆后果？ ────────────────────→ 副作用型
    │
    否
    │
    ▼
提供背景知识无执行步骤？ ──────────→ 背景知识型
    │
    否
    │
    ▼
普通工作流
```

---

## 完整示例

### gen-api-doc（文档创建 + 普通工作流）

```yaml
---
name: gen-api-doc
description: 生成 API 文档。当用户说"生成接口文档"、"写 API 文档"时触发。即使用户只提到"文档"或"接口"，也应使用此 skill。
allowed-tools: Read Grep Glob Write
paths: src/**/*.controller.ts
---

生成 $ARGUMENTS 的 API 文档：

1. 读取控制器文件
2. 提取路由、参数、返回值
3. 生成 Markdown 格式文档
```

**为什么用默认配置**：
- 功能：生成文档 → 文档创建
- 副作用：只写文件，无不可逆操作 → 普通工作流

---

### release-publish（工作流程 + 副作用型）

```yaml
---
name: release-publish
description: 发布新版本。当用户说"发布版本"、"release"时触发。
disable-model-invocation: true
allowed-tools: Bash(npm *) Bash(git *) Read
---

发布版本 $ARGUMENTS：

1. 运行测试：`npm test`
2. 构建：`npm run build`
3. 发布：`npm publish`
4. 打标签：`git tag v$ARGUMENTS`
```

**为什么禁止自动调用**：发布有不可逆副作用（npm publish、git tag）。

---

### db-schema（文档创建 + 背景知识型）

```yaml
---
name: db-schema
description: 数据库表结构说明。处理数据库相关代码时自动加载。
user-invocable: false
---

## 核心表
- `users`：用户信息
- `orders`：订单数据

## 字段约定
- 主键：`id` BIGINT
- 时间：`created_at`、`updated_at`
```

**为什么隐藏菜单**：用户不需要主动调用，Claude 处理数据库代码时自动加载。

---

## 踩坑记录

### 坑一：description 写成技术文档

**错误**：`本 Skill 用于生成 API 文档...`

**正确**：`生成 API 文档。当用户说"生成接口文档"时触发。`

### 坑二：SKILL.md 过长

**问题**：写了 500 行

**解决**：MUST ≤200 行，详细内容移到 reference/

### 坑三：副作用型没禁止自动调用

**问题**：创建"发布版本"Skill 没设置 `disable-model-invocation: true`

**风险**：Claude 可能自动执行发布

### 坑四：背景知识型没隐藏菜单

**问题**：创建"数据库规范"Skill 设置了默认配置

**影响**：用户看到菜单但不知道什么时候调用

---

## 排查 Skill 不触发

1. 运行 `What skills are available?`
2. 能列出但不触发 → description 关键词不匹配
3. 列不出来 → 检查路径（必须是 `skills/<name>/SKILL.md`）
4. Skills 太多 → description 预算超出（约 8000 字符）

### 常见原因

| 原因 | 解决 |
| :-- | :-- |
| 无触发关键词 | 添加用户会说的关键词 |
| 不够 pushy | 添加"即使用户只提到 X，也应使用" |
| 关键词太抽象 | 用用户实际会说的词 |