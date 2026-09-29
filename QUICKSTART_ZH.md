# 快速上手（零基础版） · Quick start in Chinese

不需要装任何第三方库。三步：跑起来 → 改一个文件 → 上传结果。

## 第 1 步 · 跑起来（看到分数和回放）

| 你的电脑 | 做什么 |
|---|---|
| macOS | 双击 `run_baseline.command`（系统自带的 Python 就够用；若提示"无法打开"，右键 → 打开） |
| Windows | 先到 https://www.python.org/downloads/ 安装 Python 3.12（安装时勾选 **Add python.exe to PATH**），然后双击 `run_baseline.bat` |
| Linux | 终端里运行 `./run_baseline.sh` |

大约 15 秒后会弹出一个网页：这是基线智能体在公开场景上 180 个观测夜的回放。
终端里最后一段是分数，基线约 **12287 分**，`termination_reason` 应为 `survey_complete`。

只想先看一眼的话，把上面的文件名换成 `run_demo_week`（`.command` / `.bat` / `.sh`）：同样的流程、同样的评分器，场景只有 7 个观测夜，约 2 秒跑完，回放页也更容易逐夜看清楚。结果写在 `demo_week_output/`。

注意：`demo-week` 和 180 晚的 `dev-reference` 按练习赛规则计分，没有隐藏异常标签；只有 `finals-preview` 带异常机制（见本页末尾）。

## 第 2 步 · 改一个文件

打开 `agent/my_strategy.py`。整个比赛你只需要改这一个文件里的 `choose_action` 函数：

- 平台每次把"现在能观测的候选"排好序交给你（第 0 个是估计收益最高的），
- 你返回想观测的那个候选，或者返回 `None` 表示这一时隙先等待。

文件里已经写好了几个可以直接取消注释的思路（优先 REQUIRED 瓦片、优先观测请求、条件差就等待、用 `memory` 记住做过什么）。
每个候选带有的字段和含义也写在文件开头。

改完保存，再双击一次 `run_baseline`，看分数有没有变高。运行出错时，终端会直接打印 `agent.log` 的最后几行。

## 第 3 步 · 上传（练习赛）

1. 打开比赛网站 → 注册 → 创建队伍（一个人也可以）。
2. 「提交」页 → 选你本地跑的那个场景 → 把 `run_output/decisions.csv` 拖进上传框。
3. 几秒钟出分；分数分解、每晚回放都在提交页。

上传 CSV 只用于 Playground 练习赛。正式比赛评测完整项目：

## 上传到平台（完整项目）

1. 在本目录运行 `python3 pack_agent.py`，生成 `my-agent.zip`：整个 `agent/` 文件夹，ZIP 根目录带 `observer.project.json`，
   告诉平台运行 `python3 -u minimal_agent.py`。`.env` 不会被打包。
2. 打开网站「参赛」页 → 提交完整项目 → 私有 ZIP 上传，选择 `my-agent.zip`。
3. 等待准备和公开场景测试完成，检查接口、确认版本，再开始评测。

入门包自带的智能体在平台上不需要任何模型密钥（足够跑通流程；评奖要求至少两个环节采用大模型驱动的智能体技术，见网站规则页）。云端运行不会使用你文件里的密钥：程序需要调用大模型时，
请在「参赛」页设置自己的 API 地址、模型和密钥；平台不为云端运行提供模型额度。

## 想更进一步

- 想在本地试更多天气：`python3 make_scenario.py --out scenarios/mine --seed 7 --days 30`，再运行 `python3 local_runner.py --scenario scenarios/mine --agent agent/minimal_agent.py`。
- 想让大模型参与决策：本地运行时复制 `agent/.env.example` 为 `agent/.env`，填 `MODEL_PROVIDER` 与自己的 API key。平台上不上传 `.env`，智能体读取平台注入的 `OPENAI_BASE_URL` / `OPENAI_API_KEY`（对应你在「参赛」页设置的密钥），做法见 `README.md` 的 "Upload a complete project"。跑通练习赛的队伍，队长可领取赞助兑换码（如 Kimi Coding Plan），兑换码即将发放。
- 完整的数据格式、协议和评分公式见网站「文档」页；`README.md` 是给工程师看的详细版。

> 练习场景仍按旧规则计分（无异常标签、不能重复观测、不接受上报）；想演练正式赛的新机制，跑 `run_finals_preview` 或 `scenarios/finals-preview`（基线约 **8214 分**，示例智能体会自己发现并上报那次仪器故障）。
