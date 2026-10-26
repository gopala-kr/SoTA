# Maestro-1 — model card (outline)
## Model
- Developer: Maestro (start-up) · Version: 1.0 · Date: month 13
- Architecture: mixture-of-experts, 65.2B total / 11.7B active parameters
- Training compute: ~7.2e23 FLOPs (6·N·D estimate) · Context: 64K tokens
## Intended use
- Software-engineering assistance inside customers' own repositories, through agents with a tool guard
- Not intended for: unsupervised production changes, medical/legal advice, decisions about people
## Training data
- ~10T tokens: filtered web, permissively licensed code, maths, books, multilingual, verified skills
- Public summary: see data-summary.pdf (EU template) · opt-outs honoured
## Evaluation (harness v3, contamination-checked, 95% CIs)
- Partner held-out tasks: pass@1 ... [CI] vs Maestro-0 ... [CI]
- Public benchmarks: ... (with contamination notes)
## Safety
- Red-team attack success by category with Wilson intervals; known weaknesses listed
## Limitations
- Below frontier models on general knowledge; English-first; can still write insecure code
## Contact
- security@ and incidents@ addresses, response times
