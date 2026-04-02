# Competition summary

## Outcome

This repository documents a **Gold Medal** solution that finished **Top 5** on the IBM SkillsBuild Hydropower Climate Optimisation Challenge.

## What actually won

The final competition recipe was not a single monolithic model. It was a layered forecasting system:

1. **CatBoost leaderboard model** for most sources
2. **Device-level exception handling** for consumer device 18
3. **Small device-specific rescaling** for a few systematic biases
4. **Submission alignment and manual sanity checks** before export

That is exactly the kind of competitive tabular time-series workflow that often performs best in practice: strong supervised baseline, targeted error analysis, and narrow fixes where the baseline clearly breaks.

## Why the device-18 heuristic mattered

In the original notebook exploration, consumer device 18 behaved differently from the rest of the fleet. The generic model underfit a short peak followed by a strong decline. Replacing those rows with a simple, interpretable heuristic improved the final leaderboard behavior.

## Why the refactor matters

The initial repository was effective for experimentation but difficult to read quickly:

- logic duplicated across notebooks
- private file paths mixed with analysis code
- winning pipeline not clearly separated from experiments

The refactor addresses those issues by moving the main path into `src/`, keeping experiments in `notebooks/archive/`, and centralizing paths and knobs in `configs/default.yaml`.
