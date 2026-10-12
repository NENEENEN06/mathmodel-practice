#!/usr/bin/env python3
"""下载真题附件数据（不入库）。

国赛每年的题目 + 附件打包在一起，所以这里下载的是官方年度压缩包，
解压到 data/attachments/<竞赛>/<年份>/ 后就地取用；题目 PDF 已经在 problems/ 里。

用法：
    python3 scripts/download_attachments.py --all
    python3 scripts/download_attachments.py --competition cumcm --year 2024
    python3 scripts/download_attachments.py --all --keep-archive      # 保留下载的压缩包
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "problems", "attachments.json")
DATA_DIR = os.path.join(ROOT, "data", "attachments")
UA = "Mozilla/5.0 (X11; Linux x86_64)"


def download(url: str, dst: str) -> None:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as r, open(dst, "wb") as f:
        shutil.copyfileobj(r, f, length=1 << 20)


def extract(archive: str, outdir: str) -> bool:
    os.makedirs(outdir, exist_ok=True)
    for tool in (["7z", "x", "-y", f"-o{outdir}", archive], ["unzip", "-o", archive, "-d", outdir]):
        try:
            p = subprocess.run(tool, capture_output=True, text=True, timeout=3600)
            if p.returncode == 0:
                return True
        except FileNotFoundError:
            continue
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="下载真题附件数据到本地（不入 Git）")
    ap.add_argument("--all", action="store_true", help="下载清单里的全部年份")
    ap.add_argument("--competition", help="只下某个竞赛（如 cumcm）")
    ap.add_argument("--year", type=int, help="只下某一年")
    ap.add_argument("--keep-archive", action="store_true", help="保留下载的压缩包")
    args = ap.parse_args()

    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)

    if not (args.all or args.competition or args.year):
        print(__doc__)
        print("可用清单：")
        for comp, years in manifest.items():
            ids = sorted(years, key=lambda x: int(x))
            print(f"  {comp}: {', '.join(ids)}")
        return 0

    targets = []
    for comp, years in manifest.items():
        if args.competition and comp != args.competition:
            continue
        for year, info in sorted(years.items(), key=lambda kv: int(kv[0])):
            if args.year and int(year) != args.year:
                continue
            targets.append((comp, year, info))

    if not targets:
        print("没有匹配的条目，检查 --competition / --year")
        return 1

    for comp, year, info in targets:
        outdir = os.path.join(DATA_DIR, comp, year)
        mark = os.path.join(outdir, ".extracted")
        if os.path.exists(mark):
            print(f"[跳过] {comp} {year} 已解压：{outdir}")
            continue
        ext = os.path.splitext(info["url"])[1] or ".zip"
        archive = os.path.join(DATA_DIR, comp, "_archives", f"{year}{ext}")
        try:
            if not os.path.exists(archive):
                print(f"[下载] {comp} {year} <- {info['url']}")
                download(info["url"], archive)
            else:
                print(f"[存在] {archive}")
        except (urllib.error.URLError, OSError) as e:
            print(f"[失败] {comp} {year}: {e}", file=sys.stderr)
            continue
        print(f"[解压] {archive} -> {outdir}")
        if extract(archive, outdir):
            open(mark, "w").close()
            if not args.keep_archive:
                os.remove(archive)
        else:
            print(f"[失败] 解压失败，压缩包保留在 {archive}", file=sys.stderr)

    print(f"\n完成。附件在 {DATA_DIR}（已在 .gitignore 中，不会提交）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
