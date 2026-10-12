"""求解入口骨架 —— 复制到 practices/<场次>/code/ 后按题目改。

用法：
    python main.py                     # 用内置示例数据跑通流程
    python main.py --data ../../data/attachments/xxx.csv --out results
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

from utils import ensure_dir, read_table, save_fig, set_seed, setup_matplotlib


def build_model(df: pd.DataFrame) -> dict:
    """模型主体：这里换成题目要求的模型。返回需要落盘的指标。"""
    numeric = df.select_dtypes(include=[np.number])
    return {
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "columns": list(df.columns),
        "mean": {c: float(numeric[c].mean()) for c in numeric.columns},
        "std": {c: float(numeric[c].std(ddof=0)) for c in numeric.columns},
    }


def make_figures(df: pd.DataFrame, out_dir: str) -> list[str]:
    """出图：论文里的图直接从这里生成，别用截图。"""
    import matplotlib.pyplot as plt

    saved = []
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        return saved

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=150)
    ax.hist(numeric.iloc[:, 0].dropna(), bins=20, color="#3b6ea5", edgecolor="white")
    ax.set_title(f"分布：{numeric.columns[0]}")
    ax.set_xlabel(numeric.columns[0])
    ax.set_ylabel("频数")
    ax.grid(alpha=0.25, axis="y")
    saved.append(save_fig(fig, os.path.join(out_dir, "figure1.png")))

    if numeric.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=150)
        ax.scatter(numeric.iloc[:, 0], numeric.iloc[:, 1], s=14, alpha=0.7, color="#c0504d")
        ax.set_xlabel(numeric.columns[0])
        ax.set_ylabel(numeric.columns[1])
        ax.set_title("变量关系")
        ax.grid(alpha=0.25)
        saved.append(save_fig(fig, os.path.join(out_dir, "figure2.png")))

    return saved


def demo_data() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    x = rng.normal(50, 12, size=200)
    y = 1.8 * x + rng.normal(0, 10, size=200)
    return pd.DataFrame({"指标A": x, "指标B": y, "分组": rng.choice(["甲", "乙"], size=200)})


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="数学建模求解骨架")
    p.add_argument("--data", help="输入数据文件（csv/xlsx），不填则用内置示例数据")
    p.add_argument("--sheet", default=0, help="xlsx 的工作表名或序号")
    p.add_argument("--out", default="results", help="结果输出目录")
    p.add_argument("--seed", type=int, default=0, help="随机种子（结果可复现）")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    set_seed(args.seed)
    setup_matplotlib()

    df = read_table(args.data, sheet=args.sheet) if args.data else demo_data()
    metrics = build_model(df)

    out_dir = ensure_dir(args.out)
    figures = make_figures(df, out_dir)

    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics, "figures": figures}, f, ensure_ascii=False, indent=2)

    print(f"[ok] 样本 {metrics['n_rows']} 行 × {metrics['n_cols']} 列")
    print(f"[ok] 指标已写入 {out_dir}/summary.json")
    for p in figures:
        print(f"[ok] 图：{p}")


if __name__ == "__main__":
    main()
