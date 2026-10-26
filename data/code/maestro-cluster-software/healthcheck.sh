#!/bin/bash
# healthcheck.sh — Slurm HealthCheckProgram, runs every 5 minutes on each node
# (slurm.conf: HealthCheckProgram=/etc/slurm/healthcheck.sh
#              HealthCheckInterval=300  HealthCheckNodeState=ANY)
# Cheap checks only: a node that fails is drained, never rebooted from here.
H=$(hostname -s)
drain() { scontrol update nodename=$H state=drain reason="hc: $1"; exit 0; }

[ "$(nvidia-smi -L | wc -l)" -eq 8 ]            || drain "gpu count"
nvidia-smi -q -d ECC | grep -q "Pending Page Blacklist *: Yes" && drain "ecc retire pending"
dmesg -T --since "-10min" | grep -qE "NVRM: Xid.*(48|63|64|74|79|94|95)" && drain "xid $(dmesg | grep -oE 'Xid[^,]*' | tail -1)"
[ "$(ibstat | grep -c 'State: Active')" -ge 8 ] || drain "ib link down"
df -P /checkpoints >/dev/null 2>&1              || drain "checkpoint fs"
T=$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader | sort -n | tail -1)
[ "$T" -lt 87 ]                                 || drain "gpu temp $T"
exit 0
