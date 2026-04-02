#!/usr/bin/env bash
set -euo pipefail

python -m power_challenger.cli train   --config configs/default.yaml   --output artifacts/models/catboost_pipeline.pkl
