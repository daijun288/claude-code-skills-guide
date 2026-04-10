# 实战示例完整代码

> 本文件为 examples.md 的详细补充，按需加载。

---

## gen-api-doc

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

输出格式：接口路径、请求方法、参数说明、返回示例
```

---

## gen-test-case（fork Agent）

```yaml
---
name: gen-test-case
description: 生成测试用例。当用户说"生成测试"、"写单元测试"时触发。
context: fork
agent: Explore
allowed-tools: Read Grep Glob
---

生成 $ARGUMENTS 测试用例：

1. 分析函数输入输出
2. 识别边界条件
3. 生成正常/异常测试
4. 输出测试文件
```

---

## db-schema（背景知识）

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
- 主键：`id` BIGINT
- 时间：`created_at`、`updated_at`
- 软删除：`deleted_at`

## 索引规范
- MUST：外键字段建索引
- MUST：查询条件字段建索引
```

---

## release-publish（副作用型）

```yaml
---
name: release-publish
description: 发布新版本。当用户说"发布版本"、"release"时触发。
disable-model-invocation: true
allowed-tools: Bash(npm *) Bash(git *) Read
---

发布版本 $ARGUMENTS：

1. 检查分支状态
2. 运行测试：`npm test`
3. 构建：`npm run build`
4. 发布：`npm publish`
5. 打标签：`git tag v$ARGUMENTS`

## 禁止
- MUST NOT 跳过测试
- MUST NOT 在 dirty 状态发布
```

---

## analyze-perf（性能分析）

```yaml
---
name: analyze-perf
description: 性能分析。当用户说"分析性能"、"性能报告"时触发。
context: fork
agent: Explore
allowed-tools: Read Grep Glob
---

分析 $ARGUMENTS 性能问题：

1. 识别热点循环
2. 检查 N+1 查询
3. 分析大对象分配
4. 检查同步阻塞

输出格式：问题位置、影响程度、优化建议
```

---

## security-scan（安全扫描）

```yaml
---
name: security-scan
description: 安全扫描。当用户说"安全检查"、"扫描漏洞"时触发。
allowed-tools: Read Grep Glob
---

安全扫描 $ARGUMENTS：

1. SQL 注入风险
2. XSS 漏洞
3. 敏感信息硬编码
4. 不安全的依赖

输出：漏洞等级、位置、修复建议
```

---

## sync-docs（多 MCP 协调）

```yaml
---
name: sync-docs
description: 同步文档。当用户说"同步文档到 Notion"时触发。
allowed-tools: Bash(notion-cli *) Read Write
---

同步流程：

1. 读取本地 Markdown
2. 转换为 Notion 格式
3. 推送到指定页面
4. 更新同步记录
```

---

## gen-migration（数据库迁移生成）

目录结构：

```
gen-migration/
├── SKILL.md              # 主文件
├── reference/
│   └── templates.md      # 迁移模板
└── assets/
    └── migration.tpl     # SQL 模板
```

SKILL.md：

```yaml
---
name: gen-migration
description: 生成数据库迁移。当用户说"生成迁移"、"建迁移脚本"时触发。
allowed-tools: Read Write Glob
---

生成迁移脚本 $ARGUMENTS：

1. 分析表结构变更
2. 生成 UP/DOWN SQL
3. 输出到 migrations/

模板：[assets/migration.tpl](assets/migration.tpl)
```