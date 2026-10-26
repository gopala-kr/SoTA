#!/bin/bash
# serve.sh — one Maestro-1 replica on 2 GPUs with an open inference engine
# (vLLM-style flags from its documentation; verify against your version).
vllm serve /models/maestro-1-fp8 \
  --tensor-parallel-size 2 \
  --quantization fp8 --kv-cache-dtype fp8 \
  --max-model-len 65536 \
  --enable-prefix-caching \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 64 \
  --port 8000
# Kubernetes runs 32 of these behind a router that sends a conversation back to
# the replica holding its cached prefix (Part 16's cost model depends on it).
