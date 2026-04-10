# 实战示例集

> 完整代码见 [examples-full.md](examples-full.md)，分类体系见 [skill-patterns.md](reference/skill-patterns.md)

---

## 按两层分类

### 文档/资产创建 + 普通工作流

| Skill | 功能 | 输出 |
| :-- | :-- | :-- |
| gen-api-doc | 生成 API 接口文档 | Markdown 文档 |
| gen-test-case | 生成测试用例 | 测试文件 |
| gen-migration | 生成数据库迁移脚本 | SQL 文件 |

### 文档/资产创建 + 背景知识型

| Skill | 功能 | 配置 |
| :-- | :-- | :-- |
| db-schema | 数据库表结构说明 | `user-invocable: false` |
| api-contract | API 契约规范 | `user-invocable: false` |

### 工作流程自动化 + 副作用型

| Skill | 功能 | 副作用 |
| :-- | :-- | :-- |
| release-publish | 发布新版本 | npm publish、git tag |
| db-migrate | 执行数据库迁移 | ALTER TABLE |
| send-notification | 发送团队通知 | 消息推送 |

### 工作流程自动化 + 普通工作流

| Skill | 功能 | 特性 |
| :-- | :-- | :-- |
| analyze-perf | 性能分析报告 | fork Agent |
| security-scan | 安全漏洞扫描 | 只读分析 |

### 多 MCP 协调 + 普通工作流

| Skill | 功能 | 涉及系统 |
| :-- | :-- | :-- |
| sync-docs | 文档同步 | Notion + GitHub |

---

## 示例 1：gen-api-doc

**分类**：文档/资产创建 + 普通工作流

```yaml
---
name: gen-api-doc
description: 生成 API 文档。当用户说"生成接口文档"、"写 API 文档"时触发。
allowed-tools: Read Grep Glob Write
paths: src/**/*.controller.ts
---

生成 $ARGUMENTS 的 API 文档：

1. 读取控制器文件
2. 提取路由、参数、返回值
3. 生成 Markdown 格式文档
```

---

## 示例 2：db-schema

**分类**：文档/资产创建 + 背景知识型

```yaml
---
name: db-schema
description: 数据库表结构说明。处理数据库相关代码时自动加载。
user-invocable: false
---

## 核心表
- `users`：用户信息
- `orders`：订单数据
- `products`：商品信息

## 字段约定
- 主键：`id` BIGINT AUTO_INCREMENT
- 时间：`created_at`、`updated_at`
- 软删除：`deleted_at`
```

---

## 示例 3：release-publish

**分类**：工作流程自动化 + 副作用型

```yaml
---
name: release-publish
description: 发布新版本。当用户说"发布版本"、"release"时触发。
disable-model-invocation: true
allowed-tools: Bash(npm *) Bash(git *) Read
---

发布版本 $ARGUMENTS：

1. 更新版本号
2. 运行测试：`npm test`
3. 构建：`npm run build`
4. 发布：`npm publish`
5. 打标签：`git tag v$ARGUMENTS`

## 禁止
- MUST NOT 跳过测试直接发布
```

---

## 示例 4：analyze-perf

**分类**：工作流程自动化 + 普通工作流

```yaml
---
name: analyze-perf
description: 性能分析。当用户说"分析性能"、"性能报告"时触发。
context: fork
agent: Explore
allowed-tools: Read Grep Glob
---

分析 $ARGUMENTS 性能：

1. 识别热点循环
2. 检查 N+1 查询
3. 分析内存使用
4. 输出优化建议
```

---

## 示例 5：sync-docs

**分类**：多 MCP 协调 + 普通工作流

```yaml
---
name: sync-docs
description: 同步文档。当用户说"同步文档到 Notion"时触发。
allowed-tools: Bash(notion-cli *) Read Write
---

同步流程：
1. 读取本地 Markdown 文件
2. 转换格式
3. 推送到 Notion
```

---

## 分类判断示例

| 用户需求 | 功能模式 | 调用控制 | 配置 |
| :-- | :-- | :-- | :-- |
| "生成 API 文档" | 文档/资产创建 | 普通工作流 | 默认 |
| "发布新版本" | 工作流程自动化 | 副作用型 | `disable-model-invocation: true` |
| "分析性能" | 工作流程自动化 | 普通工作流 | 默认 |
| "数据库表结构说明" | 文档/资产创建 | 背景知识型 | `user-invocable: false` |
| "同步文档到 Notion" | 多 MCP 协调 | 普通工作流 | 默认 |

---

**完整代码**：[examples-full.md](examples-full.md)