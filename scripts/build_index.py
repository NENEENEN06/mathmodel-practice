#!/usr/bin/env python3
"""由 problems/meta.json 生成 problems/README.md 的真题索引。

只替换 <!-- problems-index:start --> 与 <!-- problems-index:end --> 之间的内容，
标记外的说明文字手写维护。

用法：
    python3 scripts/build_index.py
    python3 scripts/build_index.py --check          # 只检查有没有缺文件/缺元数据，不写
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, "problems", "meta.json")
OUT = os.path.join(ROOT, "problems", "README.md")
START = "<!-- problems-index:start -->"
END = "<!-- problems-index:end -->"


def load_meta() -> dict:
    with open(META, encoding="utf-8") as f:
        return json.load(f)


def rel_link(target: str, from_dir: str) -> str:
    """从索引文件所在目录到题目文件的相对链接。

    只转义空格（GitHub 渲染中文路径没问题），避免把中文路径编码成一串 %E6%98%A5
    那样没法读、也没法手工改。
    """
    rel = os.path.relpath(os.path.join(ROOT, "problems", target), from_dir)
    return rel.replace(os.sep, "/").replace(" ", "%20")


def collect_rows(meta: dict) -> tuple[list[tuple], list[str]]:
    rows, problems_missing = [], []
    base = os.path.join(ROOT, "problems")
    for comp, cinfo in meta["competitions"].items():
        for year in sorted(cinfo.get("years", {}), key=lambda y: -int(y)):
            for item in cinfo["years"][year]:
                path = os.path.join(base, item["file"])
                if not os.path.exists(path):
                    problems_missing.append(f"{comp}/{year}/{item['id']} -> {item['file']}")
                rows.append((comp, cinfo["name"], year, item))
    return rows, problems_missing


def build_body(meta: dict) -> str:
    rows, missing = collect_rows(meta)
    lines = []

    lines.append("## 概览\n")
    lines.append("| 竞赛 | 全称 | 年份 | 年份范围 | 题量 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for comp, cinfo in meta["competitions"].items():
        years = sorted(int(y) for y in cinfo.get("years", {}))
        count = sum(len(v) for v in cinfo.get("years", {}).values())
        if not years:
            lines.append(f"| `{comp}` | {cinfo['name']} | — | — | 0 |")
            continue
        span = f"{years[0]}–{years[-1]}" if len(years) > 1 else str(years[0])
        lines.append(f"| `{comp}` | {cinfo['name']} | {len(years)} | {span} | {count} |")
    total = sum(len(v) for c in meta["competitions"].values() for v in c.get("years", {}).values())
    lines.append(f"\n**合计 {total} 道题。**\n")

    for comp, cinfo in meta["competitions"].items():
        years = cinfo.get("years", {})
        if not years:
            continue
        lines.append(f"## {cinfo['name']}\n")
        if cinfo.get("site"):
            lines.append(f"- 官网：{cinfo['site']}")
        if cinfo.get("organizer"):
            lines.append(f"- 主办：{cinfo['organizer']}")
        if cinfo.get("note"):
            lines.append(f"- 说明：{cinfo['note']}")
        lines.append("")
        for year in sorted(years, key=lambda y: -int(y)):
            items = years[year]
            lines.append(f"### {year} 年（{len(items)} 题）\n")
            lines.append("| 题号 | 标题 | 主题 | 题目原文 |")
            lines.append("| --- | --- | --- | --- |")
            for it in items:
                topics = "、".join(it.get("topics", [])) or "—"
                link = rel_link(it["file"], os.path.dirname(OUT))
                lines.append(f"| {it['id']} | {it.get('title', '—')} | {topics} | [打开]({link}) |")
            lines.append("")

    if missing:
        lines.append("## ⚠️ 缺失文件\n")
        lines.append("以下条目在 `meta.json` 里登记了，但文件不在仓库中：\n")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 problems/README.md 索引")
    ap.add_argument("--check", action="store_true", help="只报告问题，不写文件")
    args = ap.parse_args()

    meta = load_meta()
    body = build_body(meta)
    _rows, missing = collect_rows(meta)

    if args.check:
        print(f"缺文件：{len(missing)}")
        for m in missing:
            print("  ", m)
        return 1 if missing else 0

    if os.path.exists(OUT):
        text = open(OUT, encoding="utf-8").read()
    else:
        text = f"# 真题库\n\n{START}\n{END}\n"
    if START not in text or END not in text:
        print(f"错误：{OUT} 里找不到 {START} / {END} 标记", file=sys.stderr)
        return 1
    head, rest = text.split(START, 1)
    _old, tail = rest.split(END, 1)
    open(OUT, "w", encoding="utf-8").write(f"{head}{START}\n{body}{END}{tail}")
    print(f"已更新 {OUT}（{len(_rows)} 道题）")
    if missing:
        print(f"注意：有 {len(missing)} 个条目缺文件，见索引末尾。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
