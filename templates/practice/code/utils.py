"""公用小工具：读取数据、随机种子、中文绘图、保存图片。"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

# 常见中文字体（Windows / Linux / macOS），有就用，没有就退回默认
_CJK_FONTS = [
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "WenQuanYi Zen Hei",
    "Microsoft YaHei",
    "SimHei",
    "PingFang SC",
    "Heiti SC",
    "Arial Unicode MS",
]


def set_seed(seed: int = 0) -> None:
    """固定随机种子：论文里的结果必须能复现。"""
    np.random.seed(seed)
    try:
        import random

        random.seed(seed)
    except Exception:
        pass
    try:
        import torch  # 用得到才装

        torch.manual_seed(seed)
    except Exception:
        pass


def setup_matplotlib(dpi: int = 150) -> None:
    """统一字体与字号，避免出图中文变方块。"""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["figure.dpi"] = dpi
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + ["DejaVu Sans"]
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.25
    plt.rcParams["font.size"] = 11


def read_table(path: str, sheet=0, **kwargs) -> pd.DataFrame:
    """读 csv/xlsx，编码和分隔符自作主张处理一下。"""
    if path is None:
        raise ValueError("path 不能为空")
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=sheet, **kwargs)
    for enc in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, encoding="utf-8", errors="replace", **kwargs)


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def save_fig(fig, path: str, dpi: int = 300, close: bool = True) -> str:
    """保存图片：统一 300dpi、紧凑布局，论文直接能用。"""
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    if close:
        import matplotlib.pyplot as plt

        plt.close(fig)
    return path
