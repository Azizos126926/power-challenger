# 🏆 IBM SkillsBuild Hydropower Climate Optimisation Challenge  
# TEAM: Aziz Karaborni & Ahmed Soumer
**🥇 Result: Gold Medal — Top 5 Finalist on Zindi**
<p align="center">
  <img src="https://github.com/user-attachments/assets/93afeaba-7d93-48d8-be4e-6ef45f5be31c" alt="mugiwara-IBM SkillsBuild Hydropower Climate Optimisation Challenge" width="300"/>
</p>

## ⚡ Micro-Hydropower Load Forecasting  
🌍 **Zindi Competition**: Forecasting Climate & Operational Effects on Load Generation

This repository contains my solution to the **IBM SkillsBuild Hydropower Climate Optimisation Challenge** hosted on Zindi.  
The objective is to develop a machine learning model that predicts **energy load generation (kWh)** for micro-hydropower plants (MHPs) in off-grid communities.

---

## 📌 Problem Statement

In the remote **Kalam region of Pakistan**, micro-hydropower plants are essential for local energy supply. However, **fluctuating water flow**, **climate variation**, and **maintenance schedules** create challenges in forecasting load.

This project uses both **MHP operational data** (e.g., voltage, current, power factor) and **climate data** (e.g., temperature, precipitation, wind speed) to enhance energy forecasting and ensure system reliability.

---

## 📊 Dataset

🔗 [Competition Data on Zindi](https://zindi.africa/competitions/ibm-skillsbuild-hydropower-climate-optimisation-challenge/data)

- **Operational Metrics**: Voltage, current, power factor, energy readings...
- **Climate Data**: Temperature, dew point, precipitation, wind speed, snowfall...

---

## 🧪 Evaluation Metric

📏 **Root Mean Squared Error (RMSE)** was used to evaluate submissions on the leaderboard.

---

## 🚀 Approach

- **Data Preprocessing** – Handled missing values, created features, normalized input data.
- **Exploratory Data Analysis (EDA)** – Analyzed seasonal patterns, correlations, and anomalies.
- **Modeling** – Built and compared multiple ML models:
  - ARIMA/SARIMA/Prophet
  - Gradient Boosting (Catboost, XGboost...)
  - LSTM/RNN/GRU
- **Hyperparameter Tuning** – Grid search and cross-validation for optimal RMSE.
- **Submission & Evaluation** – Generated predictions for Zindi's submission format.

---

## 📌 Project Status

✅ **Completed** – Finalized models and submitted results  
🔍 **Exploration Ongoing** – Further experimenting with time series ensembles and postprocessing adjustments

---

## 🙏 Acknowledgment

This competition was hosted by **Zindi** and sponsored by **IBM SkillsBuild**.  
Data was provided by **CISNR (Center for Intelligent Systems and Networks Research, UET Peshawar).**

---

