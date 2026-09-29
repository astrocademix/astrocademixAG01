# Agent Observer — starter kit (challenge v3)

> New to this? Read **[QUICKSTART.md](QUICKSTART.md)** / **[QUICKSTART_ZH.md](QUICKSTART_ZH.md)**（中文）: double-click `run_baseline`, edit
> `agent/my_strategy.py`, upload the `decisions.csv` for practice, or pack `agent/` with `pack_agent.py` and upload the ZIP
> as a complete project. This README is the detailed engineering version.

Everything in this folder is what the evaluation platform runs: the same workflow, the same JSON-Lines
transport, the same scorer. A local run on a public scenario reproduces the platform's `score_report.json`
for the same `decisions.csv`.

Windows, macOS and Linux are supported (verified on Windows 11 with Python 3.12 from python.org: same scores, byte-identical generated scenarios; the runner uses a thread-based transport there). Python 3.9 or newer and the standard library are enough: the `python3` that ships with macOS works as is; on Windows install Python 3.12 from python.org (tick "Add python.exe to PATH"). Only an LLM-backed agent needs the optional packages in
`agent/requirements.txt`.

| Path | Purpose |
|---|---|
| `agent/` | Your agent. `my_strategy.py` is the one file most teams edit (`choose_action`); `minimal_agent.py` is the entry script; `decision_graph.py` holds the full pipeline and `anomaly_detection.py` the reference anomaly-reporting layer for those who want more. |
| `run_baseline.command` / `.bat` / `.sh` | Double-click launchers: run the baseline on the bundled scenario and open the replay. |
| `run_demo_week.command` / `.bat` / `.sh` | Same launchers on the seven-night demo scenario: about two seconds, replay short enough to read night by night. |
| `run_finals_preview.command` / `.bat` / `.sh` | Same launchers on `scenarios/finals-preview/`: the finals mechanics rehearsal. |
| `challenge/` | The public environment: contracts, calendar, tile geometry, weather, requests, workflow, scorer, replay renderer. Do not edit. |
| `scenarios/dev-reference/` | Public reference scenario: 180 nights, 7,928 slots, 64 tiles, weather truth included. |
| `scenarios/demo-week/` | Public one-week demo scenario: 7 nights, 294 slots, 64 tiles, 1 observation request, weather truth included. |
| `scenarios/finals-preview/` | Finals-mechanics rehearsal: 7 nights with hidden nova/reddening tags (`tile_anomalies.csv` shipped here so local scoring works), an instrument fault, per-slot efficiency jitter, score feedback, the report channel and the coverage-evenness term. The unmodified kit scores about 8214.26 here and reports the fault correctly. |
| `local_runner.py` | Runs an agent through the platform transport on a scenario and scores it. |
| `score_decisions.py` | Re-scores a `decisions.csv` (public scenarios only), including its `report_*` rows. |
| `make_scenario.py` | Generates new public practice scenarios from a seed. |
| `fetch_scenario.py` | Downloads any scenario the platform publishes (`--list`, then `fetch_scenario.py dev-fortnight`) into `scenarios/<slug>/`. |
| `pack_agent.py` | Zips `agent/` into a complete-project ZIP (with `observer.project.json` at its root) and validates it. |
| `sac_submit.py` | Uploads a practice results file (`decisions.csv`) to the platform and waits for the score. |
| `SKILL.md` | Step-by-step instructions an AI coding assistant can follow. |

## Two rule sets, one kit

The platform's **practice phase** still runs the pre-anomaly rules: its scenarios (`dev-reference`,
`demo-week`, `dev-fortnight`) carry no anomaly tags, publish no score feedback, accept no reports, and a
repeat observation of a completed tile stays invalid there — local runs on the bundled copies reproduce the
platform's practice scores exactly. The **online competition** scenarios enable the full mechanics described
in this README (hidden tags, instrument faults, repeat observations banking the per-tile maximum, the
`report` channel). `scenarios/finals-preview/` is the rehearsal copy of those rules; the kit's agent and
runner speak both generations automatically, so one agent works everywhere.

## Quick start

```bash
unzip agent-observer-starter-kit.zip && cd agent-observer-starter-kit
python3 local_runner.py --scenario scenarios/demo-week --agent agent/minimal_agent.py --wallclock 900 --out demo_week_output   # 7 nights, ~2 s
python3 local_runner.py --scenario scenarios/dev-reference --agent agent/minimal_agent.py --wallclock 600 --out run_output      # 180 nights, ~15 s
```

Standard output ends with a JSON summary (with `--quiet` it is the only output); on the reference scenario the shipped deterministic agent completes
the survey (`"termination_reason": "survey_complete"`) with `total` ≈ 12287.48 in about 15 s of wall clock.
`run_output/` holds `decisions.csv` (the whole trace — anomaly reports appear as `report_*` action rows right
after their carrier decision), `workflow_result.json`, `score_report.json`, `agent.log` (your agent's
stderr) and `decision_replay.html` (open it in a browser to step through every night).

More scenarios keep a strategy from tuning to one weather sequence:

```bash
python3 make_scenario.py --out scenarios/mine --seed 7 --days 30 --start-date 2026-10-05
python3 local_runner.py --scenario scenarios/mine --agent agent/minimal_agent.py --out run_mine
python3 score_decisions.py --scenario scenarios/mine --decisions run_mine/decisions.csv
python3 fetch_scenario.py --list                     # scenarios published by the platform
python3 fetch_scenario.py dev-fortnight              # -> scenarios/dev-fortnight/, ready for local_runner.py
```

## Scenario directory

Every scenario (the shipped `scenarios/dev-reference/`, anything `make_scenario.py` writes, and the platform's
hidden competition scenarios) has the same layout. `local_runner.py` and `score_decisions.py` read it directly.

| Path | Contents |
|---|---|
| `config/scenario_config.json` | scenario id, seed, `competition.global_wallclock_seconds` |
| `config/calendar_config.json` | site (latitude 31.9634°, longitude −111.599°, UTC−7, sun altitude limit −12°), survey start, days, `slot_seconds` 900 |
| `config/tile_config.json` | 8 regions × 8 tiles, 2 REQUIRED per region (one available for 14 days only), altitude limit 30°, lunar model, target classes, hidden anomaly-tag counts |
| `config/weather_config.json` | quality processes (instrument efficiency jitters per slot in [0.90, 1.00]), closure model, forecast horizon and error model (12 % misses, 6 false positives), event catalogue |
| `config/request_config.json` | request cadence (every 7 nights, p = 0.55), deadline classes `ONE_WEEK` / `TWO_WEEKS` / `ONE_MONTH`, completion modes `ALL` / `AT_LEAST_N`, reward 140 and miss penalty 190 per required tile |
| `config/workflow_config.json` | `global_wallclock_seconds`, weekly horizon 7 days, tile-window horizon 7 days, `per_decision_timeout_seconds: null`, clock starts after the initial publication |
| `config/score_config.json` | `challenge-score-v3` thresholds, program bonus, penalties, FLEXIBLE quota |
| `outputs/reference/night_calendar.csv`, `slots.csv` | the shared time axis: solar dusk/dawn per night, 900 s slots |
| `outputs/reference/tiles.csv`, `targets.csv`, `tile_windows.csv` | catalogue, per-target science weights, per-night visibility windows |
| `outputs/reference/observation_requests.csv`, `observation_request_tiles.csv` | pre-generated requests and their tiles |
| `outputs/reference/weather.csv` | site baseline weather per slot (public on practice scenarios only) |
| `outputs/reference/weather_forecasts.csv` | uncertain, daily-revised forecasts (the snapshots only show revisions issued so far) |
| `outputs/reference/weather_events.csv` | directional events: `rainy`, `cloudy`, `smoggy`, `rocket_launch`, `cold_wave`, `tornado`, `instrument_fault` with scope `ALL` / `REGION_SET` / `SKY_CAP_ICRS` / `HORIZON_SECTOR`, `force_close` and quality multipliers (hidden on competition scenarios; faults never appear in forecasts) |
| `outputs/reference/tile_anomalies.csv` | hidden per-tile truth tags (`nova` ×1.5, `reddening` ×0.8 on the tile's score); never shown to the agent, auditable after the fact |
| `outputs/reference/scenario_manifest.json`, `*_metadata.json` | row counts and SHA-256 of every file |

The platform never mounts this directory into your agent's sandbox: the only weather an agent sees is the
`current_site_weather` and per-candidate `effective_weather` of each snapshot, plus the forecast revisions in
`weekly`. A `decisions.csv` scored with `score_decisions.py` reports `termination_reason = trace_complete`; a
live run reports `survey_complete`, `global_wallclock_expired`, `agent_error` or `agent_initialization_error`.

## How a run works

1. The platform starts your program once with the `run` command of `observer.project.json`
   (`python3 -u minimal_agent.py` for the kit; cwd = your project folder, a scrubbed environment plus the
   manifest's `environment` and the model-proxy variables `OPENAI_BASE_URL` / `OPENAI_API_KEY`; stderr is
   captured to the run log). `local_runner.py` mirrors this and also loads your local `agent/.env`.
2. It writes one `initialize` line: the immutable catalogs (tiles with `tile_science_value`, targets, calendar,
   site) and the exact `scoring_contract` (`challenge-score-v3` config, weather score interface, lunar model).
   No reply is expected. Up to 30 s are allowed for the process to accept it.
3. The global wall clock starts. For every decision opportunity the platform writes one `decision_request`
   line and waits for one `decision_response` line with the same `decision_sequence`. Reading a snapshot never
   advances simulated time; a committed action does.
4. The run ends when the survey is complete, when the wall clock expires (an in-flight response is ignored),
   or when the agent exits / answers with something unparseable
   (`agent_error`: the remaining survey stays unobserved, so every remaining REQUIRED tile counts as missed).
   On the two normal endings the agent first receives one `finish` message and 30 grace seconds to write a
   summary and exit on its own (see "The finish message" below); only then is a still-running process stopped.
5. The platform replays `decisions.csv` with the public scorer and stores `score_report.json`.

The wall clock is the only time rule: no per-decision timeout, no synthetic fallback action. The reference
scenario's budget is 7200 s locally; on the platform each formal scenario has 3600 s and each Playground
complete-project scenario 18000 s. Every run publishes its budget in `initialize.global_wallclock_seconds`
and in the `SAC_WALLCLOCK_SECONDS` environment variable.

### Envelopes (`participant-agent-protocol-v2`)

```jsonc
// platform -> agent, once
{"protocol_version":"participant-agent-protocol-v2","message_type":"initialize",
 "payload":{"schema_version":"initial-publication-v2","calendar":{...},"site":{...},
            "tile_catalog":{"tile_count":64,"required_tile_ids":[...],"region_ids":[...],"tiles":[...]},
            "target_catalog":[...],"scoring_contract":{"score_config":{...},"weather_score_interface":{...},"lunar_model":{...}},
            "global_wallclock_seconds":7200.0}}
// platform -> agent, per decision
{"protocol_version":"participant-agent-protocol-v2","message_type":"decision_request","decision_sequence":17,
 "payload":{"schema_version":"decision-snapshot-v3","decision_sequence":17,
            "cursor":{"slot_id":"...","night_id":"...","timestamp_utc":"2026-09-07T03:15:00Z","slot_offset_seconds":0},
            "current_site_weather":{"is_observable":true,"seeing_arcsec":1.1,"transparency":0.9,"sky_quality":1.0},
            "tile_last_finished":{"tile_id":"T00037","score":121.5} /* or null */,
            "candidate_tiles":[{"tile_id":"...","region_id":"...","scheduling_class":"REQUIRED|FLEXIBLE","nominal_exptime_seconds":900,
                                "tile_science_value":123.4,"window_start_utc":"...","window_end_utc":"...",
                                "geometry":{"altitude_deg":..,"azimuth_deg":..,"airmass":..,"lunar_quality_factor":..},
                                "effective_weather":{...},"already_completed":false}],
            "active_requests":[{"request_id":"...","deadline_utc":"...","completion_reward":..,"miss_penalty":..,
                                "tile_requirements":[{"tile_id":"...","required_visits":1,"completed_visits":0,"remaining_visits":1}],
                                "is_complete":false}],
            "night_start":{"night":{...},"tile_windows":[...]} /* or null */, "weekly":{"weather_forecast":[...],"tile_windows":[...],"observation_requests":[...]} /* or null */,
            "progress":{"completed_tile_ids":[...],"flexible_completed_by_region":{...}}}}
// agent -> platform, one line per request; "reports" is optional
{"protocol_version":"participant-agent-protocol-v2","message_type":"decision_response","decision_sequence":17,
 "action":"observe","tile_id":"...","program":"DARK","request_id":"","reason":"short text",
 "reports":[{"kind":"NOVA","tile_id":"T00037"},{"kind":"Instrument_Failure"}]}
```

`action` is `observe` or `wait`. `program` is `DARK`, `BRIGHT` or `BACKUP`; `request_id` may be empty. Only
stdout carries protocol lines; print diagnostics to stderr.

Snapshot feedback and publications:

* `tile_last_finished` — the realized official score (`base + program_bonus`) of your most recently finished
  exposure, or `null` before the first one. Interrupted exposures report 0. Waits and invalid actions produce
  no update. Compare it against the public-formula estimate to detect hidden anomalies.
* `fault_status` — present only on the first decision of a night, and only after a fault report of yours was
  correct: one simulated day after the report it appears as
  `{"status":"fault","event_id":...,"spatial_scope_type":...,"spatial_scope_payload":{...},"instrument_efficiency_multiplier":...,"reported_at_utc":...,"published_at_utc":...,"repair_complete_utc":...}`,
  is re-published nightly while the repair is running, and disappears once `repair_complete_utc` passes
  (two simulated days after the report). A fault report with no active fault gets, on the same one-day
  schedule, a one-night `{"status":"normal","reference_report_id":...}` answer instead.

`reports` rides on a `decision_response`: zero or more entries, each `{"kind":"Instrument_Failure"}` or
`{"kind":"NOVA"|"Reddening","tile_id":"..."}`. Reports never consume slot time. Malformed entries are dropped
(the action still counts); duplicates are tolerated and deduplicated at settlement. Each accepted report lands
in `decisions.csv` as a `report_instrument_failure` / `report_nova` / `report_reddening` action row immediately
after its carrier decision (sharing the incrementing `decision_id` sequence), so the single file replays
everything. Settlement: a correct
NOVA/Reddening tag earns +100, a wrong one −150 (first report per tile and tag counts; both tags may be
reported on one tile). For faults: reporting while an unacknowledged fault is active is *correct* (it triggers
the `fault_status` publication and the repair clock); with no active fault it is a *misreport* — one misreport
between two correct reports is free, each further one costs 100; re-reporting an acknowledged fault under
repair is neutral.

### The finish message

When an evaluation ends (all slots done, or the global time limit reached), the platform sends your program one last message:

```json
{"protocol_version": "…", "message_type": "finish", "payload": {"termination_reason": "survey_complete", "last_decision_sequence": 1234, "grace_seconds": 30}}
```

- Do not reply. Anything written to stdout after this message is ignored.
- The platform then closes your program's stdin. Your program has 30 seconds to collect data and write a summary, and should then exit on its own. If it is still running after 30 seconds, the platform stops it.
- These 30 seconds do not count against the scenario time limit and do not affect the score. The score is final before this message is sent.
- Anything written to stderr during this time is saved in agent.log in your result ZIP.
- termination_reason is survey_complete (all slots done) or global_wallclock_expired (time limit reached).
- Programs that do not recognise this message keep working; even if one fails on it, the score is not affected.

## Scoring (`challenge-score-v3`, public)

For each exposure segment: `A = instrument_efficiency * transparency * sky_quality / (seeing_arcsec * airmass)`,
`A_used = A * lunar_quality_factor`, `S = V_tile * (segment_seconds / nominal_exptime_seconds) * A_used * (1 + program_bonus)`.
Program bands are determined on the efficiency-free quality (`A` without the efficiency factor), so the preview
and the replay always agree on the band; efficiency still scales the score itself.
`V_tile` is the sum of the tile's target `science_weight`s (published as `tile_science_value`). The program bonus
applies only when the chosen program matches the quality band of `A_used` (DARK ≥ 0.65, BRIGHT ≥ 0.40, else
BACKUP; bonuses 0.25 / 0.15 / 0.08). Repeat observations are legal: a tile's science score is the **maximum**
over its observations (a worse repeat never lowers it), completion still banks on the first legal observation,
and a request-tagged observation scores normally — a request naming an already-observed tile needs a new
post-issue observation to count a visit. Hidden tile tags multiply a tile's score silently: `nova` ×1.5,
`reddening` ×0.8 (both may stack); the published `tile_science_value` stays the untagged baseline.

`total = science + program_bonus + completed_request_reward + coverage_bonus + report_reward − penalties`, where the penalties are:

| Penalty | Amount |
|---|---|
| unsafe observation (starting while `is_observable` is false) | 2000 per action |
| invalid action (unknown or out-of-window tile, bad program / request) | 100 per action |
| avoidable wait (waiting while a score-improving observation existed) | 0.001 per second |
| REQUIRED tile never completed | 1000 per tile |
| FLEXIBLE region below its quota of 4 completed tiles | 100 per missing tile |
| observation request expired without completion | the request's `miss_penalty` (waived when no legal opportunity existed) |
| wrong NOVA/Reddening report | 150 per report (a correct one earns +100 in `report_reward`) |
| fault misreports beyond the free allowance of one per correct report | 100 per misreport |

`agent/scoring_preview.py` applies this formula to the current snapshot without side effects — except that
snapshots never carry `instrument_efficiency`, so the preview baseline is efficiency-free: the gap between a
preview estimate and the realized `tile_last_finished` score isolates the hidden instrument side (efficiency
jitter × fault multiplier × tag multiplier). The authoritative
scorer integrates the real exposure segments during replay. The shipped deterministic minimal agent reaches
about 12287 on the reference scenario (64 of 64 tiles, 17 of 18 requests, no penalties); a random feasible
policy scores far lower, mostly through missed REQUIRED tiles and invalid actions.

## Editing the agent

* `agent/decision_graph.py` — the decision logic (`_prepare`, `_model_node`, `_finalize`). The deterministic
  path ranks `preview_actions(...)` by estimated gain and observes the best; `wait` only when nothing can be
  completed. Add your own planning, memory across decisions, or candidate filtering here.
* `agent/model_factory.py` and `agent/.env` — optional LLM. Locally: copy `.env.example` to `.env`, set
  `MODEL_PROVIDER`, `MODEL_NAME` and the provider key, and install `agent/requirements.txt`
  (`python3 -m pip install -r agent/requirements.txt`). On the platform `.env` is never uploaded: every run gets
  `OPENAI_BASE_URL` (the platform's OpenAI-compatible model proxy) and `OPENAI_API_KEY` (a temporary run
  credential, not your key). `model_factory.py` reads these two first and falls back to `MODEL_BASE_URL` and the
  provider keys (`ZAI_API_KEY`, `DEEPSEEK_API_KEY`, ...) for local runs. The model name comes from `OPENAI_MODEL`
  or `MODEL_NAME`; on the platform it may be left empty, because the proxy uses the endpoint, model and key your
  team set on the Participate page. The proxy speaks chat completions, so OpenAI-compatible profiles use the chat
  API there.
* Keep `minimal_agent.py` / `protocol.py` compatible with the envelopes above; the platform validates every
  response.
* Anything your agent imports must live inside `agent/`. The kit's `challenge/` package is not available on
  the platform; `scoring_preview.py` is copied into `agent/` for that reason.

## Upload a complete project

`agent/` already is a complete project: `agent/observer.project.json` tells the platform how to run it, so no
automatic adapter (and no model key) is needed to prepare it.

```json
{
  "schema_version": "observer-project-v1",
  "protocol": "jsonl-v2",
  "image": "python:3.12-slim",
  "build": [],
  "run": ["python3", "-u", "minimal_agent.py"],
  "working_directory": ".",
  "environment": {"PYTHONDONTWRITEBYTECODE": "1", "MODEL_PROVIDER": "deterministic"}
}
```

1. `python3 pack_agent.py` writes `my-agent.zip` with the manifest at its root. It checks the manifest the way the
   platform does and leaves `.env` out (the platform rejects ZIPs with `.env`; `--include-env` exists only for a
   local copy and prints a warning).
2. On the website open **Participate** → Submit a complete project → private ZIP, upload `my-agent.zip`, wait for
   preparation and the public test, review and confirm the version, then evaluate it.
3. The shipped agent is deterministic and works without any model key; that is enough to test the flow, but
   awards require agent (LLM-driven) techniques in at least two stages (see the site's Rules). The image tag is
   resolved to a fixed digest during preparation.

To let a model take part on the platform, set your endpoint, model and key on the Participate page (never in the
ZIP), then install the packages in a build step and switch the provider, for example:

```json
  "build": [["python3", "-m", "pip", "install", "--no-cache-dir", "--disable-pip-version-check",
             "--target", ".deps", "-r", "requirements.txt"]],
  "environment": {"PYTHONPATH": ".deps", "PYTHONDONTWRITEBYTECODE": "1", "MODEL_PROVIDER": "openai"}
```

Build steps run in the same image with network access, as a non-root user whose only writable places are the
project folder and `/tmp`, hence `--target .deps`. The manifest `environment` must not contain keys or tokens.

## Submit

The formal competition (`online`, Oct 5–7) evaluates complete projects only: upload your project on the site
(`/compete`). The platform runs it step by step on three fixed formal scenarios (A, B, C), the same for every team;
their files, weather, forecasts and events are never published, and observations arrive one step at a time. Result
ZIPs of your own evaluations (including `agent.log`) remain downloadable. Evaluate freely within the daily limit
(10 batches per team per day, 3600 s per scenario), then mark one confirmed version as your team's **final
version** (changeable until the phase ends; default: the version of your best online batch). After the phase ends the organizers evaluate each final version once on one hidden scenario, and only
that hidden score decides the final ranking. If your program calls a model, switch the model API to "Save encrypted"
before the phase ends: the hidden run has no open page, so a key that is not saved cannot be used. There is no CSV path for the formal phase.
Awards require agent (LLM-driven) techniques in at least two of: natural-language understanding, data parsing,
task planning, action decision-making, tool calling, plan adaptation.

Before the competition, the Playground complete-project track (`practice-projects`) runs the same cloud flow on
`dev-fortnight` and `dev-reference`: 5 evaluations per team per day, 18000 s per scenario, separate board.

The Playground `practice` phase still accepts the `decisions.csv` your local run produced:

```bash
python3 sac_submit.py --url https://<ref>.supabase.co --key <anon key> --email you@x.org --password '...' \
    --phase practice --kind results --scenario dev-reference --file run_output/decisions.csv --wait
```

The URL and anon key are on the platform's Resources page.

## 中文说明

参赛 Agent 的中文说明（责任边界、启用各家 LLM 的 `.env` 配置、JSON-Lines 协议、评分参数与回退保障）见
[`agent/README_ZH.md`](agent/README_ZH.md)。本地流程：`local_runner.py` 跑基线 → `make_scenario.py` 生成更多场景 →
修改 `agent/decision_graph.py` → `pack_agent.py` 打包成完整项目 ZIP（根目录含 `observer.project.json`，不含 `.env`），在「参赛」页上传；
默认的确定性智能体不需要任何模型密钥，可用来跑通流程，但评奖要求至少两个环节采用智能体（大模型驱动）技术。平台运行时注入 `OPENAI_BASE_URL` / `OPENAI_API_KEY`（平台模型代理和临时凭证），
`model_factory.py` 优先读取它们，本地运行时再回退到 `MODEL_BASE_URL` 与各服务商密钥。练习阶段可用 `sac_submit.py` 提交 `decisions.csv`。正式比赛（`online`，10 月 5–7 日）只评测完整项目：在网站上传项目，平台在三个固定的正式场景（A、B、C，所有队伍相同；场景文件、天气、预报和事件不公开）上逐步评测，每队每天 10 批，每个场景 3600 秒，本队评测的结果 ZIP（含 `agent.log`）可下载，不接受 CSV。每日次数内可自由评测，并选定一个已确认版本作为本队**最终版本**（比赛结束前可更改；未选择时默认用线上最高分批次的版本）。比赛结束后，主办方在一个隐藏场景上对每队最终版本评测一次，最终排名只看这个成绩。程序会调用大模型的队伍，须在比赛结束前把模型 API 改为「加密保存」，否则隐藏评测时模型调用会失败。
