#!/usr/bin/env bash
# Sandbox smoke test: R and Python read a parquet input, write a parquet output, network is blocked,
# inputs are read-only. Uses the same run flags as the harness. Needs the tare-sandbox:dev image.
set -euo pipefail
cd "$(dirname "$0")/.."
IMAGE="${IMAGE:-tare-sandbox:dev}"
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
mkdir -p "$W/inputs" "$W/out"; chmod 777 "$W/out"

.venv/bin/python - "$W/inputs/x.parquet" <<'PY'
import sys, pandas as pd
pd.DataFrame({"USUBJID": ["a", "b", "c"], "AGE": [30, 70, 17]}).to_parquet(sys.argv[1])
PY

cat > "$W/code.R" <<'R'
suppressPackageStartupMessages({library(arrow); library(dplyr)})
x <- read_parquet("/work/inputs/x.parquet")
write_parquet(x %>% mutate(AGEGR1 = if_else(AGE < 18, "<18", if_else(AGE <= 64, "18-64", ">64"))), "/work/out/r.parquet")
R
cat > "$W/code.py" <<'PY'
import pandas as pd
x = pd.read_parquet("/work/inputs/x.parquet")
x["AGEGR1"] = pd.cut(x["AGE"], [-1, 17, 64, 200], labels=["<18", "18-64", ">64"]).astype(str)
x.to_parquet("/work/out/py.parquet")
PY
cat > "$W/net.py" <<'PY'
import socket
try:
    socket.create_connection(("1.1.1.1", 53), timeout=3)
    print("NETWORK OPEN")
except OSError as e:
    print("network blocked:", e)
PY
cat > "$W/ro.py" <<'PY'
try:
    open("/work/inputs/new.txt", "w")
    print("INPUTS WRITABLE")
except OSError as e:
    print("inputs read-only:", e)
try:
    open("/work/code_edit.txt", "w")
    print("ROOT FS WRITABLE")
except OSError as e:
    print("root fs read-only:", e)
PY

run() {  # run <command...>
  docker run --rm --network none --read-only --tmpfs /tmp --memory 2g --cpus 2 --pids-limit 256 \
    -v "$W/inputs:/work/inputs:ro" -v "$W/out:/work/out" -v "$W/code.R:/work/code.R:ro" \
    -v "$W/code.py:/work/code.py:ro" -v "$W/net.py:/work/net.py:ro" -v "$W/ro.py:/work/ro.py:ro" \
    "$IMAGE" "$@"
}
run Rscript /work/code.R
run python /work/code.py
run python /work/net.py
run python /work/ro.py
.venv/bin/python - "$W/out" <<'PY'
import sys, pandas as pd
r = pd.read_parquet(f"{sys.argv[1]}/r.parquet"); p = pd.read_parquet(f"{sys.argv[1]}/py.parquet")
print(r.to_string(index=False)); print(p.to_string(index=False))
assert list(r["AGEGR1"]) == list(p["AGEGR1"]) == ["18-64", ">64", "<18"], "unexpected output"
print("SMOKE TEST PASSED")
PY
