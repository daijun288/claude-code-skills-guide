# Description 优化流程

> 本文档为 SKILL.md 的详细补充，模式 I 的完整流程。

---

## 适用场景

- Skill 不触发或触发过多
- 需要优化 description 的触发效果

---

## 流程概览

```
创建触发测试集 → 运行优化循环 → 应用结果
```

---

## 步骤 1：创建触发测试集

### 数量

约 20 个查询：

- **should-trigger**：8-10 个
- **should-not-trigger**：8-10 个

### 格式

```json
[
  {"query": "生成 users 接口文档", "should_trigger": true},
  {"query": "写一下产品相关的 API", "should_trigger": true},
  {"query": "帮我写一个 fibonacci 函数", "should_trigger": false}
]
```

### 设计原则

**should-trigger 查询**：
- 用户可能说的各种变体
- 不同表达方式
- 不明确提及 Skill 名称的场景

**should-not-trigger 查询**：
- 相似但不同的领域
- 容易混淆的场景
- 边界情况

### 为什么测试集重要

好的测试集能发现 description 的问题。太简单的负例测试不了什么；真正的边界情况才能暴露问题。

---

## 步骤 2：运行优化循环

```bash
python scripts/run_loop.py \
  --eval-set trigger_evals.json \
  --skill-path <skill-dir> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

### 脚本自动执行

1. 分割训练集/测试集（防止过拟合）
2. 评估当前 description
3. 调用 Claude 改进 description
4. 重新评估
5. 选择测试集得分最高的版本

### 输出格式

```json
{
  "original_description": "原来的 description",
  "best_description": "优化后的 description",
  "best_score": "16/20",
  "iterations_run": 3,
  "history": [...]
}
```

---

## 步骤 3：应用结果

取输出中的 `best_description` 更新 SKILL.md frontmatter。

---

## Description 写法规范

### 格式

```
<功能简述>。当用户说"<关键词>"时触发。即使用户提到<相关概念>，也应使用此 skill。
```

### 为什么写得 pushy

Claude 有"不触发"倾向——该用 Skill 时不用。主动说明何时应该使用可以解决这个问题。

### 示例

```yaml
# 好的 description
description: 生成 API 文档。当用户说"生成接口文档"、"写 API 文档"时触发。即使用户只提到"文档"或"接口"，也应优先考虑使用此 skill。

# 不好的 description
description: 本 Skill 用于生成 API 文档
```

---

## 相关文件

- `scripts/run_eval.py` - 触发评估
- `scripts/run_loop.py` - 优化循环