# ☄️ Asteroid Path Predictor — Deep Space Hazard Scanner

### 🚀 Live App  
▶️ https://devanshyadav0001-asteroid-path-predictor-app-idnyxs.streamlit.app/

A deployed Machine Learning-powered web app that classifies near-Earth asteroids as **Hazardous** or **Safe** using orbital and physical parameters.  
Supports bulk CSV uploads and single-object evaluations through a clean space-themed UI.

---

## 🌟 Key Features
* **Batch Scan:** Upload .csv files to evaluate multiple asteroid entries in one shot  
* **Single Prediction:** Enter orbital parameters manually  
* **Automatic Preprocessing:** Fills/aligns missing or mismatched columns  
* **Fully Deployed:** Model + UI live on Streamlit  
* **Custom Styling:** Dark space theme, glowing UI accents

---

## 🛠️ Tech Stack
| Layer | Tools |
|------|-------|
| Language | Python 3.8+ |
| ML | Scikit-learn (Random Forest / XGBoost), Joblib |
| UI | Streamlit |
| Data | Pandas, NumPy |
| Theme | Injected custom CSS |

---

## 📂 Project Structure
```bash
├── app.py                # Streamlit UI + prediction logic
├── feature_names.json    # Required feature list
├── model.pkl             # Pretrained ML model
├── requirements.txt      # Dependencies
└── README.md             # Documentation
