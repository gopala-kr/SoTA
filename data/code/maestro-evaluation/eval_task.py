# eval_task.py — one harness task in the style of the UK AI Security Institute's
# open-source Inspect framework (names follow its documentation; check them
# against the version you install).
from inspect_ai import Task, task
from inspect_ai.dataset import json_dataset
from inspect_ai.solver import basic_agent, system_message
from inspect_ai.tool import bash, python
from inspect_ai.scorer import scorer, accuracy, stderr, Score, CORRECT, INCORRECT

@scorer(metrics=[accuracy(), stderr()])
def hidden_tests():
    async def score(state, target):
        ok = await run_hidden_tests(state.metadata["task_id"], state.output.completion)  # sandboxed
        return Score(value=CORRECT if ok else INCORRECT)
    return score

@task
def partner_heldout():
    return Task(
        dataset=json_dataset("private/partner_heldout_v3.jsonl"),   # never published, never trained on
        solver=basic_agent(init=system_message(SYSTEM), tools=[bash(timeout=120), python()], max_attempts=1),
        scorer=hidden_tests(),
        sandbox="docker",
        epochs=5,                     # 5 samples per task -> pass@1 and pass@5 (pass_at_k.py)
    )
