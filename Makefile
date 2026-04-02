.PHONY: install test train predict

install:
	pip install -e ".[classic,dev]"

test:
	pytest -q

train:
	python -m power_challenger.cli train --config configs/default.yaml --output artifacts/models/catboost_pipeline.pkl

predict:
	python -m power_challenger.cli predict --config configs/default.yaml --model-path artifacts/models/catboost_pipeline.pkl --output artifacts/submissions/gold_submission.csv
