# 当前最佳平均分代码包 · 2026-10-03

[下载代码与 CNN 权重压缩包](best-numeric-v4-20261003.zip)

配置：`expanded-shortlist_diversity`（光纤网格重排＋质量校准＋多天气训练的互补候选CNN）。源码来自实际服务器实验快照，包含实际选中权重及配对结果。

| 35 个配对开发情景 | 平均分 |
|---|---:|
| 当前最佳数值组合 | **6700.94** |
| 旧混合CNN参考 | 6137.97 |

平均提升 **562.97（9.17%）**，**34/35** 胜出，训练种子17。

**这是开发代理环境分数，不是官方排行榜成绩。** 最强数值组合尚缺预留的episode100/101最终确认，部署入口也没有官方云端得分。

压缩包默认关闭LLM/API以保留数值配置，不能声称已经满足比赛的API/LLM接入要求。不得将未测过的“数值组合＋Agent”的成绩视为6700.94。包内README给出开发复核命令、JSONL入口、依赖和限制。

兼容修正：清单采用`schema_version: observer-project-v1`与`image: python:3.12-slim`，移除了`env`和`protocol`；运行参数由`run_agent.py`设置，算法与权重不变。请重新上传最新ZIP。

包内有`weights/`、`experiments/`、`evidence/`和逐文件哈希。没有API密钥、服务器token、Qwen27B权重或原始调用日志。

SHA-256：`8e2f36ac8a2fd40bb15ec7b9ef79d4a1f9c54b437c2c5eefec41f0f535b1de63`
