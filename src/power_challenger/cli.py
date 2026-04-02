from __future__ import annotations

import argparse
import json
from pathlib import Path

from power_challenger.config import load_config
from power_challenger.pipelines.predict import predict_submission_from_config
from power_challenger.pipelines.training import persist_training_artifacts, train_catboost_from_config
from power_challenger.pipelines.validate import holdout_backtest
from power_challenger.utils.logging import get_logger


logger = get_logger()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Power Challenger forecasting CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train = subparsers.add_parser("train", help="Train the CatBoost leaderboard pipeline.")
    train.add_argument("--config", default="configs/default.yaml")
    train.add_argument("--output", default="artifacts/models/catboost_pipeline.pkl")

    predict = subparsers.add_parser("predict", help="Generate a submission CSV.")
    predict.add_argument("--config", default="configs/default.yaml")
    predict.add_argument("--model-path", default="artifacts/models/catboost_pipeline.pkl")
    predict.add_argument("--output", default="artifacts/submissions/gold_submission.csv")

    validate = subparsers.add_parser("validate", help="Run a simple holdout backtest.")
    validate.add_argument("--config", default="configs/default.yaml")
    validate.add_argument("--split-date", default="2024-09-13")

    inspect = subparsers.add_parser("inspect-config", help="Print the resolved configuration.")
    inspect.add_argument("--config", default="configs/default.yaml")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)

    if args.command == "train":
        artifacts = train_catboost_from_config(config)
        persist_training_artifacts(artifacts, args.output)
        logger.info("Saved model to %s", Path(args.output).resolve())
        return

    if args.command == "predict":
        submission = predict_submission_from_config(config, args.model_path)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        submission.to_csv(output, index=False)
        logger.info("Saved submission to %s", output.resolve())
        return

    if args.command == "validate":
        metrics = holdout_backtest(config, split_date=args.split_date)
        logger.info(json.dumps(metrics, indent=2))
        return

    if args.command == "inspect-config":
        print(json.dumps(config.raw, indent=2))
        return

    parser.error(f"Unknown command: {args.command}")
