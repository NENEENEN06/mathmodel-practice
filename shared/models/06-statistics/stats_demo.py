"""统计检验与数据分析：结论要"显著"才敢写进论文。

解决什么问题
    数据有了，要回答：两组东西真的有差别吗？几个因素谁影响大？两个变量
    相关吗？数据服从正态吗？（这决定你后面能用什么方法）

本文件给的示例
    1. 正态性检验（Shapiro / K-S）
    2. 两样本 t 检验（含方差齐性检验）与 Mann-Whitney 非参替代
    3. 单因素方差分析（ANOVA）与事后多重比较（Tukey HSD）
    4. 相关分析（Pearson / Spearman）+ 相关系数显著性
    5. 卡方独立性检验（分类变量的关联）

用法
    python stats_demo.py
"""
from __future__ import annotations

import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def normality_test(x, name="数据", verbose=True):
    """正态性：p > 0.05 表示"没有足够证据说它不正态"（可以按正态处理）。"""
    x = np.asarray(x, dtype=float)
    stat, p = stats.shapiro(x) if x.size <= 5000 else stats.kstest(
        (x - x.mean()) / x.std(ddof=1), "norm")
    if verbose:
        print(f"{name}：Shapiro p = {p:.4f} → "
              + ("可认为近似正态" if p > 0.05 else "偏离正态，改用非参数方法"))
    return float(p)


def two_sample_test(a, b, verbose=True):
    """两样本比较：先查方差齐性，再选 t 检验或 Welch t 检验；不正态就用 Mann-Whitney。"""
    a, b = np.asarray(a, float), np.asarray(b, float)
    lev_p = stats.levene(a, b).pvalue                     # >0.05 认为方差齐
    equal_var = lev_p > 0.05
    t_stat, t_p = stats.ttest_ind(a, b, equal_var=equal_var)
    u_stat, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")
    if verbose:
        print(f"方差齐性 Levene p = {lev_p:.4f} → 用 {'标准' if equal_var else 'Welch'} t 检验")
        print(f"t 检验：t = {t_stat:.4f}, p = {t_p:.4f} → "
              + ("差异显著" if t_p < 0.05 else "差异不显著"))
        print(f"（非参对照）Mann-Whitney p = {u_p:.4f}")
        print(f"均值：A = {a.mean():.3f}, B = {b.mean():.3f}，差值 {a.mean() - b.mean():.3f}")
    return dict(t_p=float(t_p), u_p=float(u_p), equal_var=bool(equal_var))


def anova_test(groups, labels=None, verbose=True):
    """单因素方差分析 + Tukey 事后比较：三个以上组比均值。"""
    F, p = stats.f_oneway(*groups)
    if verbose:
        print(f"ANOVA：F = {F:.4f}, p = {p:.4f} → "
              + ("组间差异显著" if p < 0.05 else "组间无显著差异"))
        print(f"各组均值：" + ", ".join(
            f"{lab}={np.mean(g):.3f}" for lab, g in zip(labels or range(len(groups)), groups)))
    if p < 0.05:
        values = np.concatenate(groups)
        tags = np.concatenate([[lab] * len(g) for lab, g in
                               zip(labels or range(len(groups)), groups)])
        tukey = pairwise_tukeyhsd(values, tags)
        if verbose:
            print(tukey.summary().as_text().split("\n", 3)[-1])
    return dict(F=float(F), p=float(p))


def correlation_test(x, y, verbose=True):
    """相关分析：Pearson（线性）与 Spearman（单调）；非线性关系别只看 Pearson。"""
    x, y = np.asarray(x, float), np.asarray(y, float)
    r, p_r = stats.pearsonr(x, y)
    rho, p_rho = stats.spearmanr(x, y)
    if verbose:
        print(f"Pearson r = {r:.4f} (p = {p_r:.4g})，Spearman ρ = {rho:.4f} (p = {p_rho:.4g})")
        if abs(r - rho) > 0.2:
            print("两者差距较大：可能存在非线性单调关系，Spearman 更可信")
    return dict(pearson=(float(r), float(p_r)), spearman=(float(rho), float(p_rho)))


def chi2_test(table, verbose=True):
    """卡方独立性检验：两个分类变量是否相关（table 为列联表）。"""
    chi2, p, dof, expected = stats.chi2_contingency(np.asarray(table))
    if verbose:
        print(f"卡方 = {chi2:.4f}, 自由度 = {dof}, p = {p:.4f} → "
              + ("两个变量不独立（有关联）" if p < 0.05 else "无法拒绝独立假设"))
        if (expected < 5).any():
            print("  注意：有格子期望频数 < 5，卡方近似不可靠，考虑 Fisher 精确检验")
    return dict(chi2=float(chi2), p=float(p))


if __name__ == "__main__":
    rng = np.random.default_rng(0)

    print("== 1. 正态性检验")
    normality_test(rng.normal(0, 1, 200), "标准正态样本")

    print("\n== 2. 两样本 t 检验")
    a = rng.normal(50, 8, 60)
    b = rng.normal(54, 8, 60)
    two_sample_test(a, b, )

    print("\n== 3. 单因素方差分析")
    groups = [rng.normal(m, 5, 40) for m in (30, 32, 38)]
    anova_test(groups, labels=["甲", "乙", "丙"])

    print("\n== 4. 相关分析")
    x = rng.uniform(0, 10, 100)
    y = np.exp(0.3 * x) + rng.normal(0, 0.5, 100)     # 单调但非线性
    correlation_test(x, y)

    print("\n== 5. 卡方检验")
    chi2_test([[45, 15], [30, 30]])
