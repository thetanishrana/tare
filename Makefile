# Common commands. Run from the repo root. `make test` needs no network and no API keys
# (sandbox tests skip themselves if Docker or the task bundles are missing).
PY := .venv/bin/python

.PHONY: test lint format setup-data oracle bundles references alt-answers sandbox-image sandbox-smoke ollama k1

test:           ## unit tests (golden test needs the sandbox image and task bundles)
	.venv/bin/pytest -q

lint:           ## ruff check and format check
	.venv/bin/ruff check . && .venv/bin/ruff format --check .

format:
	.venv/bin/ruff check --fix . && .venv/bin/ruff format .

setup-data:     ## export SDTM to parquet, build all oracles, then the task bundles and answer keys
	Rscript r/export_sdtm.R && Rscript r/oracle_build.R && $(PY) -c "from tare.tasks import build_all; build_all()"

oracle:         ## rebuild oracle outputs only (data/oracle/)
	Rscript r/oracle_build.R

bundles:        ## rebuild task bundles and answer keys from the YAML/specs
	$(PY) -c "from tare.tasks import build_all; build_all()"

references:     ## every reference solution must score 'correct' (needs Docker + bundles)
	$(PY) scripts/run_references.py

alt-answers:    ## answer keys for the alternative defensible readings (needs Docker + bundles)
	$(PY) scripts/build_alt_answers.py

sandbox-image:  ## build the arm64 sandbox image
	docker build -t tare-sandbox:dev docker

sandbox-smoke:  ## network blocked, inputs read-only, R and Python parquet round trip
	scripts/sandbox_smoke_test.sh

ollama:         ## start the local model server with Tare's settings (16k context)
	scripts/ollama_serve.sh

k1:             ## oracle check (K1)
	Rscript r/k1_oracle_check.R
