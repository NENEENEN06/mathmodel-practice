"""层次分析法（AHP）：主观赋权的标准做法。

解决什么问题
    多指标决策里，指标之间没有客观数据、或需要体现专家/队伍的主观偏好时，
    用成对比较矩阵把"哪个更重要"量化成权重。

输入
    A : (n, n) 判断矩阵，a[i][j] 用 1-9 标度表示"指标 i 相对指标 j 的重要程度"，
        满足 a[j][i] = 1/a[i][j]，a[i][i] = 1。

输出
    w : (n,) 权重（和为 1），CR 一致性比率，是否通过（CR < 0.1）。

算法
    1. 列归一化后按行求均值（和积法）得到权重，等价于主特征向量的近似；
    2. λ_max ≈ Σ (Aw)_i / (n * w_i)
    3. CI = (λ_max - n) / (n - 1)，CR = CI / RI，RI 查表（Saaty 随机一致性指标）。

用法
    python ahp.py            # 跑内置例子
    >>> from ahp import ahp
    >>> w, cr = ahp([[1, 3, 5], [1/3, 1, 3], [1/5, 1/3, 1]])
"""
from __future__ import annotations

import numpy as np

# Saaty 随机一致性指标（n = 1..11）
RI_TABLE = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24,
            7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}


def ahp(matrix, verbose: bool = True):
    """返回 (权重向量, 一致性比率 CR)。CR < 0.1 认为判断矩阵可接受。"""
    A = np.asarray(matrix, dtype=float)
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("判断矩阵必须是方阵")
    if not np.allclose(np.diag(A), 1.0):
        raise ValueError("判断矩阵对角线必须为 1")

    # 和积法求权重
    col_sum = A.sum(axis=0)
    w = (A / col_sum).mean(axis=1)
    w = w / w.sum()

    # 一致性检验
    Aw = A @ w
    lam_max = float(np.mean(Aw / w))
    ci = (lam_max - n) / (n - 1) if n > 1 else 0.0
    ri = RI_TABLE.get(n, 1.51)
    cr = ci / ri if ri > 0 else 0.0

    if verbose:
        print(f"权重 w = {np.round(w, 4)}")
        print(f"λ_max = {lam_max:.4f}, CI = {ci:.4f}, RI = {ri}, CR = {cr:.4f}")
        print("一致性：" + ("通过（CR < 0.1）" if cr < 0.1 else "不通过，需要调整判断矩阵"))

    return w, cr


def build_from_triples(pairs, n):
    """用 (i, j, 值) 三元组构造判断矩阵，只填上三角，下三角取倒数。

    >>> build_from_triples([(0, 1, 3), (0, 2, 5), (1, 2, 2)], 3)
    """
    A = np.ones((n, n))
    for i, j, v in pairs:
        A[i, j] = v
        A[j, i] = 1.0 / v
    return A


if __name__ == "__main__":
    # 例子：选方案要考虑"成本、效果、可靠性"三个指标
    # 判断：效果 > 成本 > 可靠性
    pairs = [(0, 1, 1 / 2), (0, 2, 2.0), (1, 2, 3.0)]  # 0=成本 1=效果 2=可靠性
    A = build_from_triples(pairs, 3)
    names = ["成本", "效果", "可靠性"]
    print("判断矩阵：")
    print(np.round(A, 3))
    w, cr = ahp(A)
    print("指标权重：", {f"{k}": round(float(v), 4) for k, v in zip(names, w)})
    assert abs(w.sum() - 1) < 1e-9 and cr < 0.1
