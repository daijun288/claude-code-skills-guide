# 创建 Skill 完整指南

> 本文档为 SKILL.md 的详细补充，按需加载。

---

## AskUserQuestion 完整选项

创建 skill 时 **MUST 使用 AskUserQuestion 工具**，完整格式：

### 问题 1：allowed-tools

```json
{
  "questions": [{
    "question": "选择该 skill 需要的工具（免确认模式）：",
    "header": "工具",
    "multiSelect": false,
    "options": [
      {"label": "只读", "description": "Read Grep Glob - 分析、查阅"},
      {"label": "修改", "description": "Read Grep Glob Edit Write - 修复、重构"},
      {"label": "Git/GitHub", "description": "Bash(gh/git *) + 读写 - Issue、PR"},
      {"label": "开发", "description": "读写 + Bash(mvn/npm *) - 构建、测试"},
      {"label": "Shell", "description": "Bash(*) Read - 脚本、CI/CD"},
      {"label": "无限制", "description": "不设置，正常权限流程"}
    ]
  }]
}
```

### 问题 2：调用控制

```json
{
  "questions": [{
    "question": "选择调用控制方式：",
    "header": "调用",
    "multiSelect": false,
    "options": [
      {"label": "默认", "description": "用户和 Claude 都能触发"},
      {"label": "只能手动触发", "description": "disable-model-invocation: true - deploy/commit 等有副作用的操作"},
      {"label": "只能自动触发", "description": "user-invocable: false - 背景知识型，用户看不到"}
    ]
  }]
}
```

### 推荐判断

| 场景 | MUST 推荐 |
| :-- | :-- |
| 有副作用（deploy/commit/发消息/删除） | "只能手动触发" |
| 背景知识（legacy/API 规范/架构说明） | "只能自动触发" |
| 普通工作流 | "默认" |

---

## 创建流程详解

### 步骤 1：需求分析

从 `$ARGUMENTS` 提取：
- **功能目标**：skill 做什么（如"代码审查"、"修复 issue"）
- **触发关键词**：用户会说什么话触发此 skill
- **参数需求**：是否需要 argument-hint（如 `[issue-number]`）

### 步骤 2：确定位置

| 用户表述 | MUST 使用 |
| :-- | :-- |
| 含"个人"/"全局"/"所有项目" | `~/.claude/skills/<name>/` |
| 无指定或含"项目"/"当前" | `.claude/skills/<name>/` |

### 步骤 3：询问配置

使用上方 AskUserQuestion JSON 格式。

### 步骤 4：创建目录

```bash
mkdir -p <skill-dir>/reference
# 按需创建
mkdir -p <skill-dir>/scripts   # 需要脚本
mkdir -p <skill-dir>/assets    # 需要模板
```

### 步骤 5：编写 SKILL.md

**MUST 遵守**：

| 项目 | 规范 | 违规后果 |
| :-- | :-- | :-- |
| name | 小写+数字+连字符，≤64字符 | 无法注册 |
| description | 前置触发关键词 | 无法自动触发 |
| allowed-tools | 空格分隔 | 格式错误无效 |
| 行数 | ≤200行 | 违反规范 |

**description 格式**：
```
<触发关键词>。当用户说"<关键词>"时触发。<功能简述>
```

**内容拆分原则**：
- 详细指南 → `reference/guide.md`
- 示例 → `reference/examples.md`
- FAQ → `reference/faq.md`
- SKILL.md 保留：执行指令 + 快速参考 + 资源导航

### 步骤 6：验证

```bash
wc -l <skill-dir>/SKILL.md  # MUST ≤200
ls -la <skill-dir>          # 检查目录结构
```

手动检查 frontmatter 格式、name 合规、description 有触发词。

---

## 优化流程详解

### 步骤 1：定位 Skill

```bash
ls -la .claude/skills/<name>/ 2>/dev/null || ls -la ~/.claude/skills/<name>/ 2>/dev/null
```

无名称 → AskUserQuestion 询问用户。

### 步骤 2：读取现状

```bash
cat <skill-dir>/SKILL.md
wc -l <skill-dir>/SKILL.md
ls -la <skill-dir>
```

### 步骤 3：诊断问题

| 检查项 | 方法 | 标准 | 等级 |
| :-- | :-- | :-- | :-- |
| 行数 | `wc -l` | ≤200 | MUST |
| name | 检查 frontmatter | 合格式 | MUST |
| description | 检查 frontmatter | 有触发词 | MUST |
| 目录名 | `ls -la` | reference/scripts/assets | SHOULD |
| 引用路径 | 检查 markdown | 相对路径 | SHOULD |

### 步骤 4：执行优化

| 问题 | 操作 |
| :-- | :-- |
| 行数 > 200 | 拆分到 `reference/` |
| description 无触发词 | 前置用户会说的话 |
| name 不合规 | 重命名目录 |
| 目录名非标准 | `mv docs reference` |
| 引用路径绝对 | 改为相对路径 |

---

## 核心约束规则

### MUST

1. SKILL.md 必须存在且 ≤200行
2. name 合规（小写+数字+连字符）
3. description 前置触发关键词
4. 使用标准目录名（reference/scripts/assets）

### MUST NOT

1. 禁止 SKILL.md 超 200 行不拆分
2. 禁止 description 只写技术描述
3. 禁止非标准目录名
4. 禁止绝对路径引用

---

## 验证清单

创建/优化完成后 MUST 检查：

- [ ] `wc -l` 结果 ≤200
- [ ] frontmatter 格式正确
- [ ] name 合规
- [ ] description 有触发关键词
- [ ] 目录名标准

验证通过输出：`✅ Skill 创建/优化成功：/<name>`