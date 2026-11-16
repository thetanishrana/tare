# Tare sandbox: model-written R and Python code runs here and nowhere else.
# arm64 (Apple Silicon). Run flags are set by the harness, not here:
#   --network none --read-only --tmpfs /tmp --memory 2g --cpus 2 --pids-limit 256
FROM rocker/r-ver:4.6.1

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv \
 && rm -rf /var/lib/apt/lists/*

RUN Rscript -e 'install.packages(c("dplyr", "lubridate", "stringr", "admiral", "arrow"))' \
 && Rscript -e 'for (p in c("dplyr", "lubridate", "stringr", "admiral", "arrow")) library(p, character.only = TRUE)'

RUN python3 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir pandas pyarrow numpy
ENV PATH="/opt/venv/bin:${PATH}"

RUN useradd --create-home --uid 10001 sandbox
USER sandbox
WORKDIR /work
