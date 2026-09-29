# Quick start (no tooling required)

Three steps: run it → edit one file → upload the result. No third-party packages needed.

## Step 1 · Run the baseline (see a score and a replay)

| Your computer | What to do |
|---|---|
| macOS | double-click `run_baseline.command` (the Python that ships with macOS is enough; if it "cannot be opened", right-click → Open) |
| Windows | install Python 3.12 from https://www.python.org/downloads/ (tick **Add python.exe to PATH**), then double-click `run_baseline.bat` |
| Linux | run `./run_baseline.sh` in a terminal |

After about 15 seconds a web page opens: the replay of the baseline agent over 180 nights of the public scenario.
The terminal ends with the score, about **12287** for the unmodified kit, with `termination_reason = survey_complete`.

For a first look, use `run_demo_week` (`.command` / `.bat` / `.sh`) instead: same pipeline and same scorer over a
seven-night scenario. It finishes in about two seconds and the replay is short enough to follow night by night.
Its results go to `demo_week_output/`.
Note: `demo-week` and the 180-night scenario use the practice rules, with no hidden anomaly tags; only
`finals-preview` has them (see the end of this page).

## Step 2 · Edit one file

Open `agent/my_strategy.py`. The whole competition fits in its `choose_action` function:

- each decision the platform hands you the candidates that can be observed right now, ranked (index 0 = highest estimated gain);
- return the candidate you want to observe, or `None` to wait for this slot.

The file contains ideas you can uncomment (REQUIRED tiles first, serve observation requests, wait in poor
conditions, remember things in `memory`) and documents every field of a candidate.

Save, double-click `run_baseline` again, and compare the score. When the agent fails, the terminal prints the
last lines of `agent.log` for you.

## Step 3 · Upload (practice)

1. Open the competition website → register → create a team (a team of one is fine).
2. "Submit" page → pick the scenario you ran → drop `run_output/decisions.csv` into the upload box.
3. The score arrives within seconds, with the breakdown and the night-by-night replay.

This CSV upload is for the Playground practice only. The online competition evaluates complete projects:

## Upload to the platform (complete project)

1. In this folder run `python3 pack_agent.py`. It writes `my-agent.zip`: your whole `agent/` folder with
   `observer.project.json` at the ZIP root, which tells the platform to run `python3 -u minimal_agent.py`.
   `.env` is never packed.
2. On the website open **Participate** → Submit a complete project → private ZIP, and upload `my-agent.zip`.
3. Wait for preparation and the public test, check the review, confirm the version, then evaluate it.

The kit's agent works there without any model key (enough to test the flow; awards require LLM-driven agent
techniques in at least two stages, see the site's Rules). Cloud runs never use a key from your files: if your agent
calls a model, set your own API endpoint, model and key on the Participate page. The platform does not provide
model credit for cloud runs.

## Going further

- More weather to practise on: `python3 make_scenario.py --out scenarios/mine --seed 7 --days 30`, then
  `python3 local_runner.py --scenario scenarios/mine --agent agent/minimal_agent.py`.
- Let a language model take part locally: copy `agent/.env.example` to `agent/.env`, set `MODEL_PROVIDER` and
  your own API key, and run as usual. On the platform `.env` is not uploaded; the agent reads `OPENAI_BASE_URL` /
  `OPENAI_API_KEY`, which the platform provides for your key set on the Participate page (see `README.md`,
  "Upload a complete project"). Teams that complete the practice get a sponsor code (such as Kimi Coding Plan)
  for their captain; codes are coming soon.
- Data formats, the protocol and the scoring formula are on the website's Docs page; `README.md` is the
  engineer's version of this guide.

> Practice scenarios keep the pre-anomaly rules (no tags, no repeats, no reports). To rehearse the finals mechanics, run `run_finals_preview` / `scenarios/finals-preview` (baseline about **8214**; the sample agent detects and reports the instrument fault by itself).
