# Asteroid-Path-Predictor
# ☄️ Deep Space Hazard Scanner (Asteroid Predictor)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange)

A Machine Learning-powered web application that predicts whether an asteroid poses a potential threat to Earth. This tool analyzes orbital and physical parameters to classify objects as **Hazardous** or **Safe**, wrapped in an immersive space-themed user interface.

## 🌟 Key Features

* **Batch Analysis:** Upload a CSV file containing asteroid data to scan multiple objects at once.
* **Manual Trajectory Input:** Input specific orbital parameters (Velocity, Eccentricity, etc.) manually for single-object analysis.
* **Immersive UI:** Custom CSS styling featuring a deep-space background and neon-styled elements for a "Mission Control" aesthetic.
* **Robust Preprocessing:** Automatically handles missing features in user uploads to ensure model compatibility.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (Random Forest/XGBoost - *depending on your specific model*), Joblib
* **Styling:** Custom CSS injection

## 📂 Project Structure

```bash
├── app.py                # Main application logic and UI
├── feature_names.json    # List of features required by the ML model
├── model.pkl             # Pre-trained Machine Learning model
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation