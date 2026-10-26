# grpo_config.py — RL with verifiable rewards on Maestro-0/1 (sketch using
# Hugging Face TRL's GRPOTrainer; argument names follow TRL's documentation,
# check them against your installed version).
from trl import GRPOConfig, GRPOTrainer
from maestro.verify import run_hidden_tests      # sandboxed test runner (Agent Layer Part 2)

def reward(completions, task_ids, **kw):
    # 1.0 only if the patch passes the task's tests in a sandbox; no partial credit
    return [1.0 if run_hidden_tests(t, c) else 0.0 for t, c in zip(task_ids, completions)]

cfg = GRPOConfig(
    output_dir="ckpt/maestro-1-rl", num_generations=16,   # the "group" in GRPO
    max_completion_length=4096, learning_rate=1e-6, beta=0.02,  # KL penalty keeps it near the SFT model
    per_device_train_batch_size=4, gradient_accumulation_steps=8, bf16=True,
    logging_steps=10, save_steps=200,
)
trainer = GRPOTrainer(model="ckpt/maestro-1-sft", reward_funcs=[reward],
                      args=cfg, train_dataset=load_verified_tasks("train"))
trainer.train()   # every saved checkpoint is a CANDIDATE: it must pass gate.py before use
