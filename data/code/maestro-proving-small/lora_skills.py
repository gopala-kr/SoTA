"""lora_skills.py — H2 preview: fold verified skills into weights with LoRA.

Two adapters on the same open base model, trained for the SAME number of tokens:
  --data skills   verified skills turned into (task → solution) chat examples
  --data generic  an equal-size sample of high-quality public code data
Then rerun skill_eval.py WITHOUT retrieval against each adapter: if the skills
adapter wins on held-out tasks, weights absorbed something retrieval provided.

  pip install transformers peft trl datasets
  python3 lora_skills.py --base <open-model> --data skills  --out adapter-skills
  python3 lora_skills.py --base <open-model> --data generic --out adapter-generic
NOTE: needs a GPU (one 80 GB card is enough for a 7–8B model with LoRA);
it was not executed for this article.
"""
import argparse, json
from datasets import Dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer


def skill_examples(path):
    for line in open(path):
        s = json.loads(line)                       # {"name", "code", "doc", "tests", "task"}
        yield {"messages": [
            {"role": "user", "content": s["task"]},
            {"role": "assistant", "content": f"```python\n{s['code']}\n```"},
        ]}


def generic_examples(path, limit):
    for i, line in enumerate(open(path)):          # {"prompt", "completion"} from a public code set
        if i >= limit:
            break
        r = json.loads(line)
        yield {"messages": [{"role": "user", "content": r["prompt"]},
                            {"role": "assistant", "content": r["completion"]}]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True); ap.add_argument("--data", choices=["skills", "generic"], required=True)
    ap.add_argument("--skills", default="skills_train.jsonl"); ap.add_argument("--generic", default="generic_code.jsonl")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    skills = list(skill_examples(a.skills))
    rows = skills if a.data == "skills" else list(generic_examples(a.generic, len(skills)))
    trainer = SFTTrainer(
        model=a.base,
        train_dataset=Dataset.from_list(rows),
        peft_config=LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, target_modules="all-linear", task_type="CAUSAL_LM"),
        args=SFTConfig(output_dir=a.out, num_train_epochs=2, per_device_train_batch_size=4,
                       gradient_accumulation_steps=8, learning_rate=1e-4, lr_scheduler_type="cosine",
                       warmup_ratio=0.03, bf16=True, logging_steps=10, save_strategy="epoch", seed=0),
    )
    trainer.train()
    trainer.save_model(a.out)
    print(f"saved {a.data} adapter to {a.out} ({len(rows)} examples)")


if __name__ == "__main__":
    main()
