# 实战示例集

## 一、视觉输出 Skill：代码库可视化

生成交互式 HTML 树形视图，展示项目文件结构。

### SKILL.md

```yaml
---
name: codebase-visualizer
description: 生成代码库可视化图。当用户说"可视化项目"、"展示目录结构"时触发。
allowed-tools: Bash(python *)
---

# 代码库可视化器

生成交互式 HTML 树形视图，显示项目文件结构：

- 可折叠目录
- 文件大小显示
- 文件类型颜色编码
- 目录总计大小

## 使用方法

```bash
python ${CLAUDE_SKILL_DIR}/scripts/visualize.py $ARGUMENTS
```

默认生成 `codebase-map.html` 并在浏览器打开。

## 参数

- 无参数：当前目录
- 路径参数：指定目录，如 `/codebase-visualizer src/`
```

### scripts/visualize.py

```python
#!/usr/bin/env python3
"""生成代码库交互式可视化"""

import json, sys, webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    # ... HTML 生成逻辑
    pass

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

---

## 二、PR 审查 Skill（完整版）

```yaml
---
name: pr-review
description: 审查当前 PR。当用户说"review PR"、"审查这个 PR"时触发。
context: fork
agent: Explore
allowed-tools: Bash(gh *), Read, Grep, Glob
---

## PR 信息

**标题与描述：**
!`gh pr view --json title,body -q '.title + "\n\n" + .body'`

**变更文件：**
!`gh pr diff --name-only`

**完整 Diff：**
!`gh pr diff`

**评论：**
!`gh pr view --comments --json comments -q '.comments[] | "[\(.author.login)]: " + .body'`

---

## 审查维度

1. **安全性**：SQL 注入、XSS、敏感信息泄露
2. **边界处理**：空值、类型检查、并发
3. **可维护性**：风格一致性、复杂度、注释
4. **测试覆盖**：关键路径测试

输出格式：文件+行号 | 问题 | 建议改法
```

---

## 三、后台部署监控 Skill

```yaml
---
name: watch-deploy
description: 监控部署状态。当用户说"看下部署进度"、"监控 CI"时触发。
disable-model-invocation: true
allowed-tools: Bash(gh *), Bash(curl *)
---

监控部署 #$ARGUMENTS：

1. 每 30 秒检查 CI 状态
2. 成功/失败时通知
3. 超过 10 分钟提醒

运行命令：
```bash
while true; do
  status=$(gh run view $ARGUMENTS --json status -q '.status')
  echo "[$(date)] Status: $status"
  if [[ "$status" == "completed" ]]; then
    conclusion=$(gh run view $ARGUMENTS --json conclusion -q '.conclusion')
    echo "Deploy finished: $conclusion"
    break
  fi
  sleep 30
done
```
```

---

## 四、组件创建 Skill（带模板）

```yaml
---
name: create-vue-component
description: 创建 Vue 组件。当用户说"新建组件"、"创建 Vue 组件"时触发。
allowed-tools: Read, Write, Glob
paths: web-ui/**, src/**/*.vue
---

创建 Vue 组件 $ARGUMENTS：

1. 确定组件位置：`src/components/$ARGUMENTS/`
2. 生成文件：
   - `$ARGUMENTS.vue` - 组件本体（参考模板）
   - `index.ts` - 导出
   - `$ARGUMENTS.types.ts` - 类型定义（如需要）

3. 模板来自：${CLAUDE_SKILL_DIR}/templates/vue-component.md

## 模板

查看 [templates/vue-component.md](templates/vue-component.md) 的标准结构。
```

---

## 五、API 设计 Skill（多文件结构）

```
api-designer/
├── SKILL.md            # 概述 + 导航
├── examples.md         # 15 个 API 设计示例
├── anti-patterns.md    # 常见反模式
├── checklist.md        # 上线自检清单
└── templates/
    └── endpoint.md     # 端点模板
```

SKILL.md 内容：

```yaml
---
name: api-designer
description: API 设计指南。当用户说"设计 API"、"新建端点"时触发。
paths: src/**/controller/**, src/**/api/**
---

设计 RESTful API 端点：$ARGUMENTS

## 设计原则

遵循项目 API 规范，参考：
- 示例：[examples.md](examples.md)
- 避免：[anti-patterns.md](anti-patterns.md)
- 模板：[templates/endpoint.md](templates/endpoint.md)

## 完成后自检

运行 [checklist.md](checklist.md) 确认设计质量。
```