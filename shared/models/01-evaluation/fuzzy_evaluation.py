"""模糊综合评价：指标"好不好"说不清时用的评价法。

解决什么问题
    评价带模糊性（"服务质量好/较好/一般/差"），或指标本身是定性描述，
    用隶属度把它量化，再按权重合成，最后按最大隶属度定级。

输入
    R : (n_indicator, n_level) 隶属度矩阵，每行是某指标对各评价等级的隶属度（行和为 1）
    W : (n_indicator,) 指标权重（可用 AHP 或熵权法得到）

输出
    综合隶属度向量 B 与最终等级

用法
    python fuzzy_evaluation.py
"""
from __future__ import annotations

import numpy as np


def fuzzy_evaluate(R, W, levels=None, verbose=True):
    """B = W · R，按最大隶属度原则定级。"""
    R = np.asarray(R, dtype=float)
    W = np.asarray(W, dtype=float)
    W = W / W.sum()
    if R.shape[0] != W.size:
        raise ValueError("隶属度矩阵行数必须等于权重个数")

    B = W @ R
    idx = int(np.argmax(B))
    levels = levels or [f"等级{i+1}" for i in range(R.shape[1])]

    if verbose:
        print("指标权重：", np.round(W, 4))
        print("综合隶属度：", {lv: round(float(v), 4) for lv, v in zip(levels, B)})
        print(f"结论：{levels[idx]}（隶属度 {B[idx]:.4f}）")
    return B, levels[idx]


def triangular_membership(x, a, b, c):
    """三角隶属函数：中间 b 处为 1，两端 a、c 处为 0。"""
    x = np.asarray(x, dtype=float)
    left = np.where(b != a, (x - a) / (b - a), 1.0)
    right = np.where(c != b, (c - x) / (c - b), 1.0)
    return np.clip(np.minimum(left, right), 0, 1)


if __name__ == "__main__":
    # 例子：三个指标（教学/科研/服务）在"优、良、中、差"四个等级上的隶属度
    R = np.array([
        [0.60, 0.30, 0.10, 0.00],
        [0.40, 0.35, 0.20, 0.05],
        [0.25, 0.40, 0.25, 0.10],
    ])
    W = np.array([0.45, 0.35, 0.20])          # 可以换成 AHP/熵权法算出来的权重
    B, level = fuzzy_evaluate(R, W, levels=["优", "良", "中", "差"])
    assert abs(B.sum() - 1) < 1e-9
