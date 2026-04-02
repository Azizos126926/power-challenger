# Modeling notes

## Main model family

The winning path centered on **CatBoostRegressor** over a feature table built from:

- source identity
- calendar features
- climate aggregates
- metadata tables for source voltage and source type

CatBoost is a strong fit here because the task is a medium-scale, structured forecasting problem with nonlinear interactions and limited history for some sources.

## Alternative baselines preserved in the archive

The notebook archive also includes:

- ARIMA / SARIMA baselines
- gradient boosting variants
- LSTM and GRU experiments
- feature prediction experiments
- source clustering experiments

These are valuable for the project story, but they are not the cleanest mainline to expose at the root of the repository.
