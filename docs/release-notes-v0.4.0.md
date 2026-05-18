# v0.4.0 Release Notes

- JSON config workflow: repeatable local backtest and sweep runs can now be defined with `--config`, including the bundled [`examples/configs/split-sweep.json`](../examples/configs/split-sweep.json).
- Override behavior: explicit CLI flags take precedence over config values, so one shared config can be reused while changing output paths, result counts, or other run settings at invocation time.
- Config documentation: [`docs/config-files.md`](config-files.md) describes supported JSON shape, option names, precedence rules, and the bundled split-sweep example.
- Verification commands: run `pytest`, `python scripts/selfcheck.py`, or run the config sample with `market-signal-lab --config examples/configs/split-sweep.json`.
- Research boundary: config files make experiments easier to reproduce; they do not change the research-only scope, market-data assumptions, or no-advice boundaries.
