#!/usr/bin/env python3
"""
打包 Skill 为 .skill 文件

用法: python package_skill.py <skill_directory>
"""

import sys
import zipfile
from pathlib import Path


def package_skill(skill_path):
    """打包 Skill 目录"""
    skill_path = Path(skill_path).resolve()

    # 检查目录
    if not skill_path.exists():
        print(f"❌ 目录不存在: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ SKILL.md 不存在")
        return None

    # 输出文件
    skill_name = skill_path.name
    output_file = skill_path.parent / f"{skill_name}.skill"

    # 打包
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  添加: {arcname}")

        print(f"\n✅ 打包成功: {output_file}")
        return output_file

    except Exception as e:
        print(f"❌ 打包失败: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: python package_skill.py <skill_directory>")
        sys.exit(1)

    print(f"📦 打包: {sys.argv[1]}")
    result = package_skill(sys.argv[1])

    if result:
        print(f"\n安装: claude skill install {result}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()