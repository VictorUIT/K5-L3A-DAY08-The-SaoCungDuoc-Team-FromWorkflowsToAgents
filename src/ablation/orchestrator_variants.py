"""Research card R1 ablation: how many read tools the investigator is given.

One variable changes: the `allowed_tools` list in the handoff. Model (MockLLM),
seeds, corpus, prices, evaluator, host, and the orchestrator's own code are the
same as shape C. Run from `src/`:

    python -m lab8.benchmark --shapes orchestrator_min,orchestrator,orchestrator_wide --extra-shape orchestrator_min=ablation.orchestrator_variants:run_claim_min --extra-shape orchestrator_wide=ablation.orchestrator_variants:run_claim_wide --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_investigator_tools.json
"""

from __future__ import annotations

from lab8.schemas import RunResult
from lab8.shapes.orchestrator import run_with_tools

# 2 tools: only the chain the decision depends on (order -> quote).
MIN_TOOLS = ["lookup_order", "compute_compensation"]
# 5 tools: everything read-only the runner can execute from a handoff.
WIDE_TOOLS = ["get_claim_view", "lookup_order", "lookup_policy", "lookup_refund_history", "compute_compensation"]


def run_claim_min(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    return run_with_tools(claim_id, seed=seed, store_path=store_path, crash_at=crash_at, investigator_tools=MIN_TOOLS)


def run_claim_wide(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    return run_with_tools(claim_id, seed=seed, store_path=store_path, crash_at=crash_at, investigator_tools=WIDE_TOOLS)
