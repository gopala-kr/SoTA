#!/bin/bash
# launch_megatron.sh — Maestro-1 layout on 128 nodes (sketch; flag names follow
# Megatron-LM's documented arguments, verify against your version).
#SBATCH --partition=main --nodes=128 --gpus-per-node=8 --exclusive
export NCCL_IB_HCA=mlx5 CUDA_DEVICE_MAX_CONNECTIONS=1
srun python pretrain_gpt.py \
  --num-layers 40 --hidden-size 4096 --num-attention-heads 32 \
  --group-query-attention --num-query-groups 8 --swiglu \
  --num-experts 64 --moe-router-topk 8 --moe-shared-expert-intermediate-size 2048 \
  --moe-ffn-hidden-size 2048 --moe-router-load-balancing-type aux_loss --moe-aux-loss-coeff 1e-3 \
  --tensor-model-parallel-size 2 --pipeline-model-parallel-size 1 \
  --expert-model-parallel-size 8 --sequence-parallel --use-distributed-optimizer \
  --seq-length 8192 --global-batch-size 2048 --micro-batch-size 1 \
  --bf16 --recompute-granularity selective \
  --lr 3e-4 --min-lr 3e-5 --lr-warmup-iters 2000 --train-iters 600000 \
  --save /checkpoints/maestro-1 --save-interval 500 --async-save \
  --data-path $(cat /data/mixture/maestro1_blend.txt)
