# 真题库

历年赛题**原文**（PDF / 原始格式）都放在这个目录里，按竞赛分：

- `cumcm/` —— 全国大学生数学建模竞赛（国赛）
- `mcm-icm/` —— 美国大学生数学建模竞赛（美赛）
- `shuweibei/` —— 数维杯大学生数学建模挑战赛

文件命名：`<年份>-<题号>.<扩展名>`，例如 `cumcm/2024/2024-A.pdf`。

**附件数据不在仓库里**（国赛附件常有几十到几百 MB），用脚本在本地拉：

```bash
python3 scripts/download_attachments.py --competition cumcm --year 2024
python3 scripts/download_attachments.py --all
```

下载结果放在 `data/attachments/<竞赛>/<年份>/`，已在 `.gitignore` 中，不会提交。

> 下面的索引由 `scripts/build_index.py` 生成，不要手改表格内容；新增题目改
> `problems/meta.json` 后重跑脚本。

<!-- problems-index:start -->
## 概览

| 竞赛 | 全称 | 年份 | 年份范围 | 题量 |
| --- | --- | --- | --- | --- |
| `cumcm` | 全国大学生数学建模竞赛（国赛 CUMCM） | 11 | 2016–2026 | 52 |
| `mcm-icm` | 美国大学生数学建模竞赛（美赛 MCM/ICM） | 6 | 2021–2026 | 36 |
| `shuweibei` | 数维杯大学生数学建模挑战赛 | 7 | 2019–2026 | 20 |

**合计 108 道题。**

## 全国大学生数学建模竞赛（国赛 CUMCM）

- 官网：https://www.mcm.edu.cn/
- 主办：中国工业与应用数学学会（CSIAM）
- 说明：本科组 A/B/C，专科组 D/E（2019 年起才有 E 题）；题目原文来自竞赛官网发布的年度赛题包。

### 2026 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 药材的烘干问题 | 传热、优化 | [打开](cumcm/2026/2026-A.pdf) |
| B | 无线电干扰源的快速自动定位与清除 | 定位、优化 | [打开](cumcm/2026/2026-B.pdf) |
| C | 微网与外部电网电力调控策略 | 优化、调度 | [打开](cumcm/2026/2026-C.pdf) |
| D | 时频冲突检测与消解 | 算法设计、优化 | [打开](cumcm/2026/2026-D.pdf) |
| E | SEM 广告投放策略 | 优化、决策 | [打开](cumcm/2026/2026-E.pdf) |

### 2025 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 烟幕干扰弹的投放策略 | 优化、仿真 | [打开](cumcm/2025/2025-A.pdf) |
| B | 碳化硅外延层厚度的确定 | 数据分析、反问题 | [打开](cumcm/2025/2025-B.pdf) |
| C | NIPT 的时点选择与胎儿的异常判定 | 统计、决策 | [打开](cumcm/2025/2025-C.pdf) |
| D | 矿井突水水流漫延模型与逃生方案 | 仿真、图论 | [打开](cumcm/2025/2025-D.pdf) |
| E | AI 辅助智能体测 | 视觉、数据分析 | [打开](cumcm/2025/2025-E.pdf) |

### 2024 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | “板凳龙”闹元宵 | 几何、仿真 | [打开](cumcm/2024/2024-A.pdf) |
| B | 生产过程中的决策问题 | 决策优化 | [打开](cumcm/2024/2024-B.pdf) |
| C | 农作物的种植策略 | 规划、优化 | [打开](cumcm/2024/2024-C.pdf) |
| D | 反潜航空深弹命中概率问题 | 概率、仿真 | [打开](cumcm/2024/2024-D.pdf) |
| E | 交通流量管控 | 优化、交通仿真 | [打开](cumcm/2024/2024-E.pdf) |

### 2023 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 定日镜场的优化设计 | 几何优化 | [打开](cumcm/2023/2023-A.pdf) |
| B | 多波束测线问题 | 几何优化 | [打开](cumcm/2023/2023-B.pdf) |
| C | 蔬菜类商品的自动定价与补货决策 | 预测、优化 | [打开](cumcm/2023/2023-C.pdf) |
| D | 圈养湖羊的空间利用率 | 优化、仿真 | [打开](cumcm/2023/2023-D.pdf) |
| E | 黄河水沙监测数据分析 | 数据分析 | [打开](cumcm/2023/2023-E.pdf) |

### 2022 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 波浪能最大输出功率设计 | 力学建模、优化 | [打开](cumcm/2022/2022-A.pdf) |
| B | 无人机遂行编队飞行中的纯方位无源定位 | 几何、优化 | [打开](cumcm/2022/2022-B.pdf) |
| C | 古代玻璃制品的成分分析与鉴别 | 聚类、分类 | [打开](cumcm/2022/2022-C.pdf) |
| D | 气象报文信息卫星通信传输 | 图论、优化 | [打开](cumcm/2022/2022-D.pdf) |
| E | 小批量物料的生产安排 | 调度优化 | [打开](cumcm/2022/2022-E.pdf) |

### 2021 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | “FAST”主动反射面的形状调节 | 几何优化 | [打开](cumcm/2021/2021-A.pdf) |
| B | 乙醇偶合制备 C4 烯烃 | 数据拟合、优化 | [打开](cumcm/2021/2021-B.pdf) |
| C | 生产企业原材料的订购与运输 | 供应链、优化 | [打开](cumcm/2021/2021-C.pdf) |
| D | 连铸切割的在线优化 | 优化 | [打开](cumcm/2021/2021-D.pdf) |
| E | 中药材的鉴别 | 分类、判别分析 | [打开](cumcm/2021/2021-E.pdf) |

### 2020 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 炉温曲线 | 微分方程、优化 | [打开](cumcm/2020/2020-A.pdf) |
| B | 穿越沙漠 | 动态规划、博弈 | [打开](cumcm/2020/2020-B.pdf) |
| C | 中小微企业的信贷决策 | 评价、决策 | [打开](cumcm/2020/2020-C.pdf) |
| D | 接触式轮廓仪的自动标注 | 几何、优化 | [打开](cumcm/2020/2020-D.pdf) |
| E | 校园供水系统智能管理 | 数据分析、优化 | [打开](cumcm/2020/2020-E.pdf) |

### 2019 年（5 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 高压油管的压力控制 | 微分方程、优化 | [打开](cumcm/2019/2019-A.pdf) |
| B | “同心协力”策略研究 | 力学建模、仿真 | [打开](cumcm/2019/2019-B.pdf) |
| C | 机场的出租车问题 | 排队论、优化 | [打开](cumcm/2019/2019-C.pdf) |
| D | 空气质量数据的校准 | 统计回归 | [打开](cumcm/2019/2019-D.pdf) |
| E | “薄利多销”分析 | 经济模型、优化 | [打开](cumcm/2019/2019-E.pdf) |

### 2018 年（4 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 高温作业专用服装设计 | 传热、优化 | [打开](cumcm/2018/2018-A.pdf) |
| B | 智能 RGV 的动态调度策略 | 离散事件仿真、优化 | [打开](cumcm/2018/2018-B.pdf) |
| C | 大型百货商场会员画像描绘 | 数据分析、聚类 | [打开](cumcm/2018/2018-C.pdf) |
| D | 汽车总装线的配置问题 | 整数规划、优化 | [打开](cumcm/2018/2018-D.pdf) |

### 2017 年（4 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | CT 系统参数标定及成像 | 反问题、数值计算 | [打开](cumcm/2017/2017-A.pdf) |
| B | “拍照赚钱”的任务定价 | 优化、聚类 | [打开](cumcm/2017/2017-B.pdf) |
| C | 颜色与物质浓度辨识 | 回归、数据拟合 | [打开](cumcm/2017/2017-C.pdf) |
| D | 巡检线路的排班 | 图论、排班优化 | [打开](cumcm/2017/2017-D.pdf) |

### 2016 年（4 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 系泊系统的设计 | 优化、力学建模 | [打开](cumcm/2016/2016-A.pdf) |
| B | 小区开放对道路通行的影响 | 评价、交通仿真 | [打开](cumcm/2016/2016-B.pdf) |
| C | 电池剩余放电时间预测 | 预测、数据拟合 | [打开](cumcm/2016/2016-C.pdf) |
| D | 风电场运行状况分析及优化 | 数据分析、优化 | [打开](cumcm/2016/2016-D.pdf) |

## 美国大学生数学建模竞赛（美赛 MCM/ICM）

- 官网：https://www.comap.com/contests/mcm-icm
- 主办：COMAP
- 说明：MCM：A（连续型）/B（离散型）/C（数据型）；ICM：D/E/F。英文题目原文，2021–2026 共 36 题；绝大多数来自 COMAP 官方下载，个别文件官方端点传输中断，改用公开镜像。

### 2026 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Modeling Smartphone Battery Drain | MCM | [打开](mcm-icm/2026/2026-A.pdf) |
| B | Creating a Moon Colony Using a Space Elevator System | MCM | [打开](mcm-icm/2026/2026-B.pdf) |
| C | Data With The Stars | MCM | [打开](mcm-icm/2026/2026-C.pdf) |
| D | Managing Sports for Success | ICM | [打开](mcm-icm/2026/2026-D.pdf) |
| E | Passive Solar Shading | ICM | [打开](mcm-icm/2026/2026-E.pdf) |
| F | To Gen-AI, or Not To Gen-AI (or how to Gen-AI)? That is the Question! | ICM | [打开](mcm-icm/2026/2026-F.pdf) |

### 2025 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Testing Time: The Constant Wear On Stairs | MCM | [打开](mcm-icm/2025/2025-A.pdf) |
| B | Managing Sustainable Tourism | MCM | [打开](mcm-icm/2025/2025-B.pdf) |
| C | Models for Olympic Medal Tables | MCM | [打开](mcm-icm/2025/2025-C.pdf) |
| D | A Roadmap to a Better City | ICM | [打开](mcm-icm/2025/2025-D.pdf) |
| E | Making Room for Agriculture | ICM | [打开](mcm-icm/2025/2025-E.pdf) |
| F | Cyber Strong? | ICM | [打开](mcm-icm/2025/2025-F.pdf) |

### 2024 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Resource Availability and Sex Ratios | MCM | [打开](mcm-icm/2024/2024-A.pdf) |
| B | Searching for Submersibles | MCM | [打开](mcm-icm/2024/2024-B.pdf) |
| C | Momentum in Tennis | MCM | [打开](mcm-icm/2024/2024-C.pdf) |
| D | Great Lakes Water Problem | ICM | [打开](mcm-icm/2024/2024-D.pdf) |
| E | Sustainability of Property Insurance | ICM | [打开](mcm-icm/2024/2024-E.pdf) |
| F | Reducing Illegal Wildlife Trade | ICM | [打开](mcm-icm/2024/2024-F.pdf) |

### 2023 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Drought-Stricken Plant Communities | MCM | [打开](mcm-icm/2023/2023-A.pdf) |
| B | Reimagining Maasai Mara | MCM | [打开](mcm-icm/2023/2023-B.pdf) |
| C | Predicting Wordle Results | MCM | [打开](mcm-icm/2023/2023-C.pdf) |
| D | Prioritizing the UN Sustainability Goals | ICM | [打开](mcm-icm/2023/2023-D.pdf) |
| E | Light Pollution | ICM | [打开](mcm-icm/2023/2023-E.pdf) |
| F | Green GDP | ICM | [打开](mcm-icm/2023/2023-F.pdf) |

### 2022 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Power Profile of a Cyclist | MCM | [打开](mcm-icm/2022/2022-A.pdf) |
| B | Water and Hydroelectric Power Sharing | MCM | [打开](mcm-icm/2022/2022-B.pdf) |
| C | Trading Strategies | MCM | [打开](mcm-icm/2022/2022-C.pdf) |
| D | Data Paralysis? Use Our Analysis! | ICM | [打开](mcm-icm/2022/2022-D.pdf) |
| E | Forestry for Carbon Sequestration | ICM | [打开](mcm-icm/2022/2022-E.pdf) |
| F | All for One and One (Space) for All! | ICM | [打开](mcm-icm/2022/2022-F.pdf) |

### 2021 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Fungi | MCM | [打开](mcm-icm/2021/2021-A.pdf) |
| B | Fighting Wildfires | MCM | [打开](mcm-icm/2021/2021-B.pdf) |
| C | Confirming the Buzz about Hornets | MCM | [打开](mcm-icm/2021/2021-C.pdf) |
| D | The Influence of Music | ICM | [打开](mcm-icm/2021/2021-D.pdf) |
| E | Re-Optimizing Food Systems | ICM | [打开](mcm-icm/2021/2021-E.pdf) |
| F | Checking the Pulse and Temperature of Higher Education | ICM | [打开](mcm-icm/2021/2021-F.pdf) |

## 数维杯大学生数学建模挑战赛

- 官网：https://www.nmmcm.org.cn/
- 主办：内蒙古创新教育学会
- 说明：分春季赛（国内赛）与秋季赛（国际赛）。官方只公开当年题目，历史真题多为网盘/平台外链，故本库为**尽力收集**：来源含公开仓库、转载重排、官网页面存档，逐份在「备注」里标明；缺口见 shuweibei/SOURCES_AND_GAPS.md。

### 2026 年（3 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 抱轨式磁浮列车的悬浮电磁铁故障检测问题 | 春季赛、国赛 | [打开](shuweibei/2026-春季赛/2026-春季赛-A.pdf) |
| B | 智能办公场景下多源异构文件识别与治理优化 | 春季赛、国赛 | [打开](shuweibei/2026-春季赛/2026-春季赛-B.pdf) |
| C | 我国碳排放数据分析与研究 | 春季赛、国赛 | [打开](shuweibei/2026-春季赛/2026-春季赛-C.pdf) |

### 2025 年（2 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 空中芭蕾——蹦床运动的力学行为分析 | 春季赛、国赛 | [打开](shuweibei/2025-春季赛/2025-春季赛-A.pdf) |
| B | Research on Crop Leaf Disease | 秋季赛、国际赛 | [打开](shuweibei/2025-秋季赛/2025-秋季赛-B.pdf) |

### 2024 年（4 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | Frequency Estimation Problems in Aircraft Laser Velocimetry | 秋季赛、国际赛 | [打开](shuweibei/2024-秋季赛/2024-秋季赛-A.pdf) |
| B | Research on the Collaborative Estimation Method for Spatial Variables | 秋季赛、国际赛 | [打开](shuweibei/2024-秋季赛/2024-秋季赛-B.pdf) |
| C | Modeling of pulsar timing noise deduction and atmospheric time delay deduction of time signals | 秋季赛、国际赛 | [打开](shuweibei/2024-秋季赛/2024-秋季赛-C.pdf) |
| D | Evaluation of Urban Resilience and Sustainable Development Capacity | 秋季赛、国际赛 | [打开](shuweibei/2024-秋季赛/2024-秋季赛-D.pdf) |

### 2022 年（3 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 银行效率评价与破产成因分析 | 春季赛、国赛 | [打开](shuweibei/2022-春季赛/2022-春季赛-A.pdf) |
| B | 大规模新型冠状病毒疫情最优应对策略研究 | 春季赛、国赛 | [打开](shuweibei/2022-春季赛/2022-春季赛-B.pdf) |
| C | 电动汽车充电站的部署优化策略 | 春季赛、国赛 | [打开](shuweibei/2022-春季赛/2022-春季赛-C.pdf) |

### 2021 年（6 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A | 外卖骑手的送餐危机 | 春季赛、国赛 | [打开](shuweibei/2021-春季赛/2021-春季赛-A.pdf) |
| B | 中小城市地铁运营与建设优化设计 | 春季赛、国赛 | [打开](shuweibei/2021-春季赛/2021-春季赛-B.pdf) |
| B | Analysis and prediction for extreme precipitation (2021 “ShuWei Cup” B) | 秋季赛、国际赛 | [打开](shuweibei/2021-秋季赛/2021-秋季赛-B.pdf) |
| C | 运动会优化比赛模式探索 | 春季赛、国赛 | [打开](shuweibei/2021-春季赛/2021-春季赛-C.pdf) |
| C | Future development plans for tourism under the Corona-virus disease (2021 “ShuWei Cup” C) | 秋季赛、国际赛 | [打开](shuweibei/2021-秋季赛/2021-秋季赛-C.pdf) |
| D | Model analysis of box office fluctuations in the 2021 movie market (2021 “ShuWei Cup” D) | 秋季赛、国际赛 | [打开](shuweibei/2021-秋季赛/2021-秋季赛-D.pdf) |

### 2020 年（1 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A/B/C(全套) | 2020“数维杯”大学生数学建模竞赛赛题题目（A题 舆情监测情感倾向分析建模 等） | 春季赛、国赛 | [打开](shuweibei/2020-春季赛/2020-春季赛-全套.pdf) |

### 2019 年（1 题）

| 题号 | 标题 | 主题 | 题目原文 |
| --- | --- | --- | --- |
| A/B/C(全套) | 2019年数维杯大学生数学建模竞赛题目（A题 我国省际生态环境与经济交互状况的综合评价 等） | 春季赛、国赛 | [打开](shuweibei/2019-春季赛/2019-春季赛-全套.pdf) |
<!-- problems-index:end -->
