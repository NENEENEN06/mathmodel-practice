# 骨架

复制即用的模板，别每次都从空白开始。

| 目录 | 用途 |
| --- | --- |
| `practice/` | **一场练习的完整目录骨架**：`README.md`（分工与进度）、`REVIEW.md`（复盘）、`code/`（可跑的求解工程）、`paper/`（论文规范与检查表） |
| `paper/` | 三个竞赛的赛制、时间、评分关注点、练手要点 |

## 开一场新练习

```bash
cp -r templates/practice practices/20261015-cumcm2024A
```

然后：

1. 改 `practices/<那一场>/README.md`：题目链接、成员、角色、时间表。
2. `code/main.py` 就是起点，`python main.py --data <数据> --out results` 能直接跑。
3. 论文结构照 `paper/README.md` 走，定稿前过一遍检查表。
