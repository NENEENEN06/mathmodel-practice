#!/usr/bin/env python3
"""跑一遍资料库里所有模型脚本，报告通过/失败。

改完公共库先跑这个，别把坏的实现留给队友：
    python3 run_all.py
    python3 run_all.py 03-optimization      # 只跑某个分类
"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"run_all.py", "requirements.txt"}


def main() -> int:
    only = sys.argv[1] if len(sys.argv) > 1 else None
    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__"))]
        rel_dir = os.path.relpath(dirpath, ROOT)
        if only and rel_dir != "." and not rel_dir.startswith(only):
            continue
        for f in sorted(filenames):
            if f.endswith(".py") and f not in SKIP:
                targets.append(os.path.join(dirpath, f))

    if not targets:
        print("没找到要跑的脚本（检查分类名）")
        return 1

    failed = []
    for path in sorted(targets):
        rel = os.path.relpath(path, ROOT)
        try:
            p = subprocess.run([sys.executable, path], capture_output=True, text=True,
                               timeout=600, cwd=os.path.dirname(path))
        except subprocess.TimeoutExpired:
            print(f"超时  {rel}")
            failed.append(rel)
            continue
        if p.returncode == 0:
            print(f"通过  {rel}")
        else:
            print(f"失败  {rel}（exit {p.returncode}）")
            tail = "\n".join((p.stderr or p.stdout).strip().splitlines()[-6:])
            print("      " + tail.replace("\n", "\n      "))
            failed.append(rel)

    print(f"\n共 {len(targets)} 个脚本，失败 {len(failed)} 个")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
