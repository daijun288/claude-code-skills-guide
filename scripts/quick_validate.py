#!/usr/bin/env python3
"""
快速验证 Skill 结构

用法: python quick_validate.py <skill_directory>
"""

import sys
import re
from pathlib import Path


def validate_skill(skill_path):
    """验证 Skill 结构"""
    skill_path = Path(skill_path)
    errors = []
    warnings = []

    # 检查 SKILL.md 存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, ["SKILL.md 不存在"], []

    content = skill_md.read_text()
    lines = content.split('\n')

    # 检查 frontmatter
    if not content.startswith('---'):
        errors.append("frontmatter 格式错误：必须以 --- 开始")
    else:
        # 查找结束的 ---
        end_idx = None
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == '---':
                end_idx = i
                break

        if end_idx is None:
            errors.append("frontmatter 格式错误：缺少结束的 ---")
        else:
            # 提取 frontmatter
            frontmatter = '\n'.join(lines[1:end_idx])

            # 检查 name
            name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
            if not name_match:
                errors.append("缺少 name 字段")
            else:
                name = name_match.group(1).strip().strip('"').strip("'")
                if not re.match(r'^[a-z0-9-]+$', name):
                    errors.append(f"name '{name}' 格式错误：必须是小写字母、数字、连字符")
                elif name.startswith('-') or name.endswith('-'):
                    errors.append(f"name '{name}' 不能以连字符开始或结束")
                elif '--' in name:
                    errors.append(f"name '{name}' 不能包含连续连字符")
                elif len(name) > 64:
                    errors.append(f"name '{name}' 超过 64 字符")

            # 检查 description
            desc_match = re.search(r'^description:\s*(.+)$', frontmatter, re.MULTILINE)
            if not desc_match:
                errors.append("缺少 description 字段")

    # 检查行数
    line_count = len(lines)
    if line_count > 200:
        errors.append(f"SKILL.md 有 {line_count} 行，MUST ≤200 行")

    if errors:
        return False, errors, warnings

    return True, [], warnings


def main():
    if len(sys.argv) < 2:
        print("用法: python quick_validate.py <skill_directory>")
        sys.exit(1)

    skill_path = sys.argv[1]
    print(f"🔍 验证: {skill_path}")

    valid, errors, warnings = validate_skill(skill_path)

    if errors:
        print("\n❌ 错误:")
        for e in errors:
            print(f"   • {e}")

    if warnings:
        print("\n⚠️ 警告:")
        for w in warnings:
            print(f"   • {w}")

    if valid:
        print("\n✅ 验证通过")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()