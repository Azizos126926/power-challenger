#!/usr/bin/env bash
set -euo pipefail

python -m power_challenger.cli predict   --config configs/default.yaml   --model-path artifacts/models/catboost_pipeline.pkl   --output artifacts/submissions/gold_submission.csv
