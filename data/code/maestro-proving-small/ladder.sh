#!/bin/sh
# ladder.sh — train four sizes on the same data budget, collect "params loss" for scaling_fit.py
rm -f ladder.txt ckpt_*.pt
for size in xs s sm m; do
  python3 train_tiny.py --size $size --steps 1500 --ckpt ckpt_$size.pt | tee log_$size.txt
  grep final_val log_$size.txt | awk '{print $4, $2}' >> ladder.txt
done
python3 scaling_fit.py ladder.txt
