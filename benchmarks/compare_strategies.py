"""Offline comparison using the original workflow and scorer; no model calls.

python benchmarks/compare_strategies.py --label baseline --baseline
python benchmarks/compare_strategies.py --label paper
Additional generated scenarios can be passed with --scenarios PATH [PATH ...].
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "agent"))

import decision_graph
from challenge.challenge_workflow import ChallengeWorkflow
from challenge.scoring_core import score_files


class Provider:
    def publish_initial(self, publication):
        self.agent = decision_graph.MinimalDecisionAgent(publication, model=None, top_k=12)

    def __call__(self, snapshot, deadline):
        return self.agent.decide(snapshot)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True)
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--scenarios", nargs="+", default=["scenarios/demo-week", "scenarios/dev-reference", "scenarios/finals-preview"])
    args = parser.parse_args()
    if Path(args.label).name != args.label:
        parser.error("label must be a directory name")
    if args.baseline:
        spec = importlib.util.spec_from_file_location("baseline_strategy", ROOT / "benchmarks/baseline_my_strategy.py")
        baseline = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(baseline)
        decision_graph.my_strategy = baseline
    rows = []
    for item in args.scenarios:
        scenario = (ROOT / item).resolve()
        output = ROOT / "benchmarks/results" / args.label / scenario.name
        if output.exists():
            raise FileExistsError(f"Refusing to overwrite {output}; choose another label")
        started = time.monotonic()
        workflow = ChallengeWorkflow(root=scenario)
        result = workflow.run(Provider(), wallclock_seconds=600)
        workflow.write_outputs(output, result)
        report = score_files(scenario, output / "decisions.csv", output / "score_report.json", result["termination_reason"])
        assert abs(report["score"]["total"] - result["score_report"]["score"]["total"]) < 1e-6
        assert result["termination_reason"] == "survey_complete", result["commit_log"][-1:]
        row = {"scenario": scenario.name, "total": report["score"]["total"],
               "base_science": report["score"]["base_science"],
               "coverage_evenness": report["score"].get("coverage_evenness", 0),
               "completed": len(report["completion"]["completed_tiles"]),
               "required_missing": len(report["completion"]["required_missing"]),
               "penalties": report["score"]["penalties"], "reports": report.get("reports"),
               "seconds": round(time.monotonic() - started, 3)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    (ROOT / "benchmarks/results" / args.label / "summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
