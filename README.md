⚡ Micro-Hydropower Load Forecasting
🌍 Zindi Competition: Forecasting Climate & Operational Effects on Load Generation
This repository contains my solution for the IBM SkillsBuild Hydropower Climate Optimisation Challenge on Zindi. The goal is to develop a machine learning model that predicts energy load generation (in kWh) for micro-hydropower plants (MHPs) in off-grid communities.

📌 Problem Statement
In the remote Kalam region of Pakistan, micro-hydropower plants are crucial for energy generation. However, fluctuating water flow, climate variations, and maintenance schedules make load forecasting challenging.

This project leverages MHP operational data (voltage, current, power factor, etc.) along with climate indicators (temperature, precipitation, wind speed) to improve energy forecasting and system reliability.

📊 Data
The dataset includes:
https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge/data
MHP operational metrics: Voltage, current, power factor, energy readings...

Climate data: Temperature, dew point, precipitation, wind speed, snowfall...

🔗 Competition data: Zindi Dataset

🏆 Evaluation Metric
Submissions are evaluated using Root Mean Squared Error (RMSE).

🚀 Approach
Data Preprocessing – Handling missing values, feature engineering, scaling.

Exploratory Data Analysis (EDA) – Understanding trends, correlations, and distributions.

Modeling – Training various ML models (e.g., Random Forest, XGBoost, LSTMs).

Hyperparameter Tuning – Optimizing for best RMSE performance.

Submission & Evaluation – Generating predictions for Zindi submission.

📌 Status
✅ Ongoing – Experimenting with different models and feature selection techniques.

📢 Acknowledgment
This competition is hosted on Zindi and sponsored by IBM SkillsBuild. Data is provided by CISNR (Center for Intelligent Systems and Networks Research, UET Peshawar).
