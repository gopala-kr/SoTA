#!/bin/bash
# burnin.sh NODE — day-zero acceptance for one 8-GPU node.
# Every step must pass; any failure keeps the node out of the pool.
set -euo pipefail
N=$1; LOG=/acceptance/$N; mkdir -p $LOG
run() { echo "== $1"; ssh $N "$2" > $LOG/$1.log 2>&1 || { echo "FAIL $1 on $N"; exit 1; }; }

run inventory  "nvidia-smi --query-gpu=index,serial,vbios_version,memory.total --format=csv"
run firmware   "nvidia-smi -q | grep -E 'VBIOS|Inforom' ; ibstat | grep -E 'Firmware|Rate'"
run topology   "nvidia-smi topo -m"                 # 8 GPUs on NVSwitch, NICs on the right PCIe roots
run ecc        "nvidia-smi -q -d ECC | grep -E 'Pending|Uncorr'"
run dcgm_long  "dcgmi diag -r 3"                    # memory, PCIe, NVLink, stress (~30-60 min)
run ib_links   "ibstat | grep -c 'State: Active'"   # expect one per compute NIC
run nccl_local "all_reduce_perf -b 8 -e 8G -f 2 -g 8"   # NVLink only, single node
run burn_24h   "dcgmi diag -r 4 || gpu_burn 86400"      # thermals under sustained load
grep -q "Fail" $LOG/dcgm_long.log && { echo "FAIL dcgm on $N"; exit 1; }
echo "PASS $N"
