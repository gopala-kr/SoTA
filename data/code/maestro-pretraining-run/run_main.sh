#!/bin/bash
# run_main.sh — the restart wrapper around the main run (Part 7's policy).
# Requeues from the latest good checkpoint, excluding drained nodes,
# and stops after 3 restarts in an hour so a human looks first.
set -u
RESTARTS=()
while true; do
  BAD=$(sinfo -h -N -t drain,down -o %N | paste -sd, -)
  sbatch --wait --exclude="${BAD}" launch_megatron.sh --load /checkpoints/maestro-1
  rc=$?
  [ $rc -eq 0 ] && { echo "run finished"; exit 0; }
  now=$(date +%s); RESTARTS+=($now)
  recent=$(for t in "${RESTARTS[@]}"; do [ $((now - t)) -lt 3600 ] && echo x; done | wc -l)
  [ "$recent" -ge 3 ] && { echo "3 restarts in 1 h: paging a human"; ./page.sh "main run unstable"; exit 1; }
  sleep 60
done
