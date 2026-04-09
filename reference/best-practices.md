# 团队共享最佳实践与踩坑记录

## 一、团队共享目录结构

```
.claude/skills/
├── review-pr/
│   ├── SKILL.md
│   └── checklist.md      # 项目特有审查清单
├── create-component/
│   ├── SKILL.md
│   └── templates/        # 组件模板文件
├── deploy-staging/
│   └── SKILL.md          # disable-model-invocation: true
└── legacy-context/
    ├── SKILL.md          # user-invocable: false
    └── architecture.md
```

## 二、关键原则

| Skill 类型 | 配置建议 |
| :-- | :-- |
| 有副作用的 Skill | `disable-model-invocation: true`（deploy、commit、发消息） |
| 背景知识型 Skill | `user-invocable: false`（让 Claude 自动加载） |
| 检查清单 | 放支持文件，不塞 CLAUDE.md |

**优先级**：项目级 > 个人级（团队可强制覆盖个人习惯）

---

## 三、踩坑记录

### 坑一：description 写成技术文档

❌ `"本 Skill 提供代码审查功能，支持安全性检查……"`
→ Claude 从不自动触发，因为没有用户会说的关键词

✅ `"当用户说'帮我 review'、'看看这段代码'时触发"`
→ 自动触发率明显提高

### 坑二：CLAUDE.md 当 Skills 用

把所有规范塞进 CLAUDE.md 写了 500 行
→ session 开始消耗大量 token，Claude 经常"忘记"后面规则

**正确做法**：CLAUDE.md 只保留 10-20 条核心规则，其余按场景做成 Skills

### 坑三：context: fork 里写条件判断

子 Agent 没有主对话历史，你说的"这次只检查安全问题"它不知道

**解决**：用 $ARGUMENTS 显式传入：`/pr-review security-only`

### 坑四：allowed-tools 误解

`allowed-tools` 只是这些工具免确认，其他工具还会触发正常权限流程。要真正限制工具访问，需在权限设置里配置。

---

## 四、排查 Skill 不触发

1. 运行 `What skills are available?` 看能否列出
2. 能列出但不触发 → description 关键词和你说的话差距太大
3. 列不出来 → 检查路径是否正确（必须是 `skills/<name>/SKILL.md`）
4. Skills 太多 → description 预算超出（约 8000 字符），考虑精简

---

## 五、obra/superpowers 项目

GitHub 上 obra/superpowers（12万+ ⭐）是一套基于 Claude Code Skills 构建的大型 Skills 框架。

**本质**：别人写好的、可直接安装使用的 Skill 集合。

**选择**：
- 快速上手 → 直接用 superpowers
- 定制团队工作流 → 自己写 Skills 更灵活

---

## 六、更多踩坑

### 坑五：Skill 触发过于频繁

如果 Claude 在不想要时使用你的 skill：

1. 使 description 更具体
2. 添加 `disable-model-invocation: true` 只手动触发

### 坑六：argument-hint 未生效

检查文件路径：必须在 `skills/<name>/SKILL.md`，不是 `skills/<name>.md`。

### 坑七：context: fork 子 Agent 无结果

子 Agent 需要有明确的任务指令，不是背景知识。如果 SKILL.md 只是"使用这些约定"没有任务，子 Agent 会返回空。

**正确**：在 `context: fork` 的 Skill 中写明具体任务步骤。