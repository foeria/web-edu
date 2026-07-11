#!/usr/bin/env python3
"""
删除 data 下每个 articles 目录中对应的 images 子文件夹。

默认直接删除；
传入 --dry-run 后仅演习，不真正删除。
"""

import argparse
import shutil
import sys
from pathlib import Path


def find_article_images_dirs(root: Path) -> list[Path]:
    """查找 data/**/articles/*/images 形式的目录。"""
    matches: list[Path] = []
    if not root.exists():
        return matches

    for articles_dir in root.rglob("articles"):
        if not articles_dir.is_dir():
            continue
        for item in articles_dir.iterdir():
            images_dir = item / "images"
            if item.is_dir() and images_dir.is_dir():
                matches.append(images_dir)

    return sorted(matches)


def delete_directories(dirs: list[Path], *, dry_run: bool) -> None:
    for directory in dirs:
        if dry_run:
            print(f"[DRY-RUN] 将删除: {directory}")
        else:
            print(f"[DELETE] 正在删除: {directory}")
            shutil.rmtree(directory, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="删除 data 下 articles 目录中的 images 子文件夹"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅演习，不真正删除",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data"),
        help="data 目录路径（默认: data）",
    )
    args = parser.parse_args()

    targets = find_article_images_dirs(args.root.resolve())

    if not targets:
        print(f"在 {args.root} 下未找到任何 articles/*/images 目录")
        return 0

    mode = "演习模式" if args.dry_run else "真实删除模式"
    print(f"共发现 {len(targets)} 个目标目录，当前为：{mode}\n")

    delete_directories(targets, dry_run=args.dry_run)

    if args.dry_run:
        print(
            "\n提示：以上仅为演习输出。去掉 --dry-run 即可真正删除。"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
