# IBM SkillsBuild Hydropower Climate Optimisation Challenge

> **🥇 Gold Medal solution · Top 5 finalist on Zindi**  
> A modular forecasting project for micro-hydropower load prediction, rebuilt from the original research notebooks into a cleaner, senior-ML-engineer-style repository.

## Highlights

- **Competition result:** Gold Medal and **Top 5** finish
- **Problem:** forecast daily `kwh` generation for micro-hydropower plants in the Kalam region of Pakistan
- **Core winning recipe:** CatBoost for the main leaderboard submission, a targeted device-18 heuristic, and light post-processing for systematic device-level bias
- **Repository upgrade:** packaged source code, reproducible config, CLI entrypoints, tests, docs, and archived notebooks

## Repository layout

```text
power-challenger/
├── artifacts/                  # trained models and submissions
├── configs/                    # YAML experiment configuration
├── data/
│   ├── external/               # competition files you add locally
│   └── reference/              # shipped metadata + aggregated training sample
├── docs/                       # competition summary and engineering notes
├── notebooks/archive/          # original exploration notebooks
├── scripts/                    # convenience shell entrypoints
├── src/power_challenger/       # production-style Python package
└── tests/                      # lightweight regression tests
```

## Competition framing

Micro-hydropower plants are a critical off-grid energy source, but output changes quickly with climate, seasonality, and plant-specific operating patterns. The competition task was to forecast the next 30 days of energy load generation using a mix of operational data and climate measurements.

This refactor keeps the original competition intuition while presenting it like a maintainable ML project rather than a loose collection of notebooks.

## Final solution at a glance

### 1. Daily training frame
- aggregate and clean the plant-level `kwh` history
- parse `Source -> consumer_device / data_user`
- merge source metadata (`voltage`, source type)
- merge daily climate aggregates when the climate workbook is available
- add cyclical calendar features

### 2. Main supervised model
- **CatBoostRegressor** trained on all devices except `consumer_device_18`
- targeted trimming of early history for high-variance / high-kWh sources
- strong tabular baseline that handles nonlinear interactions well

### 3. Device-specific exception handling
- `consumer_device_18` showed a rising-then-declining pattern that general models handled poorly
- the final leaderboard submission replaced those predictions with a custom **peak-then-decline heuristic**
- additional post-processing scaled devices `13` and `21` to correct systematic bias

### 4. Submission generation
- load the official sample submission
- build inference features for every `(date, consumer_device, data_user)` row
- predict with CatBoost where appropriate
- overwrite device-18 rows with the heuristic forecast
- align to the sample submission and export the final CSV

## Quick start

### 1) Create the environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[classic,dev]"
```

### 2) Add the private competition files

Place these in `data/external/`:

```text
data/external/Kalam Climate Data.xlsx
data/external/SampleSubmission.csv
```

### 3) Train the main model

```bash
python -m power_challenger.cli train   --config configs/default.yaml   --output artifacts/models/catboost_pipeline.pkl
```

### 4) Generate the final submission

```bash
python -m power_challenger.cli predict   --config configs/default.yaml   --model-path artifacts/models/catboost_pipeline.pkl   --output artifacts/submissions/gold_submission.csv
```

### 5) Run a simple holdout validation

```bash
python -m power_challenger.cli validate   --config configs/default.yaml   --split-date 2024-09-13
```

## Why this version reads better

The original repo captured a lot of strong competitive work, but it spread the logic across many notebooks. This version makes the winning path obvious:

- **`src/power_challenger/pipelines/training.py`** builds the leaderboard training frame
- **`src/power_challenger/pipelines/predict.py`** assembles the final submission
- **`src/power_challenger/models/heuristics.py`** contains the device-18 override and post-processing logic
- **`notebooks/archive/`** preserves the original exploration for transparency

## Archived experimentation

The notebook archive includes:
- CatBoost / boosting experiments
- ARIMA and SARIMA baselines
- GRU and LSTM forecasting experiments
- feature engineering playgrounds
- clustering / source profiling analysis

These are intentionally preserved as research history, while the package exposes the cleaner production path.

## Results

| Achievement | Summary |
|---|---|
| Public recognition | **Gold Medal** |
| Final placement | **Top 5 finalist** |
| Delivery style | notebook-to-project refactor with reproducible structure |

## Engineering notes

- Optional dependencies are imported lazily so the repository remains readable even without every heavyweight package installed.
- The shipped `aggday.csv` and source metadata tables allow the structure to be inspected immediately.
- Competition-only files remain external to keep the repository portable and Git-friendly.

## Bibliography

1. Dorogush, A. V., Ershov, V., & Gulin, A. (2018). *CatBoost: gradient boosting with categorical features support*. NeurIPS ML Systems Workshop.
2. Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice* (3rd ed.). OTexts.
3. Hochreiter, S., & Schmidhuber, J. (1997). *Long Short-Term Memory*. Neural Computation, 9(8), 1735–1780.
4. Cho, K. et al. (2014). *Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation*. EMNLP.
5. Zindi. *IBM SkillsBuild Hydropower Climate Optimisation Challenge*. Competition page and dataset documentation.

## Acknowledgment

Hosted by **Zindi** and sponsored by **IBM SkillsBuild**.  
Data attribution in the original notebook credits **CISNR (Center for Intelligent Systems and Networks Research, UET Peshawar)**.
