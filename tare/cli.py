"""`tare` command line."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
import yaml

from tare.cli_clients import make_client
from tare.pair_runs import run_pair_experiment
from tare.runs import run_experiment

app = typer.Typer(help="Tare: independent AI double programming for clinical trial datasets.")


@app.callback()
def main() -> None:
    """Tare command line."""


@app.command()
def run(config: Annotated[Path, typer.Option("--config", help="Experiment config YAML")]) -> None:
    """Run a single-programmer experiment from a config file."""
    cfg = yaml.safe_load(config.read_text())
    if cfg.get("mode") == "pair":
        run_pair_experiment(cfg)
    else:
        run_experiment(cfg, make_client(cfg))


if __name__ == "__main__":
    app()
