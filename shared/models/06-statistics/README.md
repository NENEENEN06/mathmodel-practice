# 06 统计与数据分析

**什么时候来这儿**：手里是一堆表格数据，要判断"差异是否真实"、"变量是否相关"、"怎么分组/降维"。

| 文件 | 内容 | 典型题目 |
| --- | --- | --- |
| `stats_demo.py` | 正态性、t 检验、ANOVA、相关、卡方 | 试验对比、因素影响分析、问卷数据分析 |
| `clustering_pca.py` | K-means、层次聚类、PCA、DBSCAN | 样品分类、地区分级、指标压缩、画像 |

## 做数据分析的固定顺序

1. **描述统计**：均值、标准差、分位数、缺失值、异常值（先看图）。
2. **前提检验**：要比较均值 → 先看正态性和方差齐性；不满足就换非参数方法。
3. **检验/建模**：t 检验 / ANOVA / 回归 / 聚类。
4. **多重比较校正**：比较多个组时，p 值要校正（Bonferroni 或 Tukey HSD），否则假阳性一堆。
5. **报告**：写出统计量、自由度、p 值、效应量；p 值不是全部，差多少也要说。

## 坑（这些在评审眼里都是硬伤）

- **p 值滥用**：p > 0.05 只能说"没有足够证据"，不能说"证明没有差异"。
- **相关 ≠ 因果**：论文里别写成因果，除非你有实验设计支撑。
- **聚类前不标准化**：量纲大的指标独占权重。
- **簇数拍脑袋**：必须给依据（肘部/轮廓系数/树状图/业务含义）。
- **样本不平衡**：分类问题里准确率会骗人，要看混淆矩阵、召回率。
- **卡方检验的期望频数 < 5**：近似失效，改 Fisher 精确检验。
- 数据预处理（缺失、异常、标准化）一定要在论文里写明方法，否则结果无法复现。

## 跑一遍

```bash
python stats_demo.py            # 5 类检验示例，每类都打印判读结论
python clustering_pca.py        # 选 k → K-means → 层次 → PCA → DBSCAN
```

## 相关开源

scikit-learn：https://github.com/scikit-learn/scikit-learn ；
statsmodels（统计推断更全）：https://github.com/statsmodels/statsmodels ；
SciPy `stats` 模块：https://docs.scipy.org/doc/scipy/reference/stats.html ；
可视化：Seaborn https://github.com/mwaskom/seaborn （`sns.heatmap` 画相关矩阵、`pairplot` 看分布关系）。
