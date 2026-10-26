# input_output_filter.py — classifier layer around the model (sketch). A safety
# classifier (for example an open Llama Guard-style model served next to
# Maestro-1) labels each user message and each answer against a policy.
from serving import classify, generate          # internal clients (Part 15)

POLICY = ["violent crime", "weapons of mass harm", "child safety", "privacy / personal data",
          "malicious code meant to harm others", "self-harm"]

def respond(conversation):
    verdict = classify(conversation, policy=POLICY, role="user")
    if verdict.unsafe:
        return refusal(verdict.category)             # short, non-judgemental, logged
    answer = generate(conversation)
    if classify(conversation + [answer], policy=POLICY, role="assistant").unsafe:
        log_incident(conversation, answer)           # reviewed weekly; feeds red-team set
        return refusal("output")
    return answer
