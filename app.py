import streamlit as st
import pandas as pd
import json
import joblib
import base64

# 1. Page Configuration
st.set_page_config(
    page_title="Asteroid Hazard Predictor", 
    layout="wide",
    page_icon="☄️"
)

# ==========================================
# 2. CUSTOM SPACE THEME (CSS)
# ==========================================
def set_space_theme():
    st.markdown("""
    <style>
    /* Main Background - Deep Space Blue/Black */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2000&auto=format&fit=crop");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Transparent container for content readability */
    .block-container {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #444;
    }

    /* Headings */
    h1, h2, h3 {
        color: #00e6ff !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px #00e6ff;
    }
    
    /* Text Color */
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }

    /* Input Boxes */
    .stNumberInput input {
        background-color: #1c1c1c;
        color: #00ffcc;
        border: 1px solid #00e6ff;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 20, 0.9);
        border-right: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

set_space_theme()

# ==========================================
# 3. LOAD ASSETS
# ==========================================
@st.cache_data
def load_feature_names():
    with open('feature_names.json', 'r') as f:
        return json.load(f)

@st.cache_resource
def load_model():
    return joblib.load('model.pkl')

all_features = load_feature_names()
model = load_model()

# ==========================================
# 4. SIDEBAR - FILE UPLOAD
# ==========================================
st.sidebar.title("🛸 Mission Control")
st.sidebar.write("Upload a CSV file for batch analysis.")

uploaded_file = st.sidebar.file_uploader("Upload Asteroid Data (CSV)", type=["csv"])

# Define the important manual inputs (if no file is uploaded)
IMPORTANT_FEATURES = [
    "Relative Velocity km per sec", 
    "Orbit Uncertainty", 
    "Eccentricity", 
    "Semi Major Axis", 
    "Inclination",
    "Perihelion Distance",
    "Mean Anomaly",
    "Absolute Magnitude"
]

# ==========================================
# 5. MAIN LOGIC
# ==========================================

st.title("☄️ Deep Space Hazard Scanner")

# CASE A: CSV IS UPLOADED

# CASE A: CSV IS UPLOADED
if uploaded_file is not None:
    st.info("📂 File Uploaded! Analyzing Batch Data...")
    
    try:
        # Read the CSV
        input_df = pd.read_csv(uploaded_file)
        
        # DEBUG: Show what columns were found
        # st.write("Columns found in CSV:", input_df.columns.tolist()) 
        
        # 1. Align columns: Create a DataFrame with ONLY the columns the model needs
        model_input = pd.DataFrame()
        
        # Loop through the 32 features the MODEL expects
        for feature in all_features:
            if feature in input_df.columns:
                # If CSV has it, copy it
                model_input[feature] = input_df[feature]
            else:
                # If CSV is missing it, fill with 0 (Safe Default)
                model_input[feature] = 0.0
                
        # Handle "Orbiting Body" text-to-number conversion
        if "Orbiting Body" in model_input.columns:
            # Force all values to 0 (Earth) to prevent text errors
            model_input["Orbiting Body"] = 0

        # 2. Predict
        # We use a try/except specifically for the prediction step
        try:
            predictions = model.predict(model_input)
            
            # 3. Add results to the view
            # Create a clean result table
            results_df = input_df.copy()
            results_df['Hazard_Prediction'] = predictions
            
            # Map 0/1 to Text
            results_df['Hazard_Label'] = results_df['Hazard_Prediction'].apply(
                lambda x: "⚠️ HAZARDOUS" if (x == 1 or x == True) else "✅ Safe"
            )
            
            # 4. Show Stats
            hazardous_count = results_df['Hazard_Prediction'].sum()
            st.metric("Potentially Hazardous Objects Found", f"{int(hazardous_count)} / {len(results_df)}")
            
            # 5. Show Data (Move Label to the front)
            cols = ['Hazard_Label'] + [c for c in results_df.columns if c != 'Hazard_Label']
            st.dataframe(results_df[cols])
            
        except Exception as pred_error:
            st.error(f"Model Prediction Failed. Check if your CSV data is numeric. Error: {pred_error}")
            
    except Exception as e:
        st.error(f"Error processing CSV file: {e}")

# CASE B: MANUAL ENTRY (No CSV)
else:
    st.markdown("### Manual Trajectory Input")
    st.write("Enter parameters manually below.")
    
    input_data = {}
    
    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]

        for i, feature in enumerate(IMPORTANT_FEATURES):
            current_col = cols[i % 3]
            # Check if feature exists in model list
            if feature in all_features:
                input_data[feature] = current_col.number_input(
                    label=feature, 
                    value=0.0, 
                    format="%.6f"
                )

        # Fill hidden features
        for feature in all_features:
            if feature not in input_data:
                input_data[feature] = 0.0

        st.write("---")
        submitted = st.form_submit_button("Initiate Scan", type="primary")

    if submitted:
        df = pd.DataFrame([input_data])
        df = df[all_features]
        
        if "Orbiting Body" in df.columns:
            df["Orbiting Body"] = 0 
            
        pred = model.predict(df)[0]
        
        st.write("---")
        if pred == 1:
            st.error("⚠️ ALERT: OBJECT CLASSIFIED AS HAZARDOUS")
            st.markdown("**Action:** Review trajectory immediately.")
        else:
            st.success("✅ STATUS: OBJECT IS SAFE")
            st.markdown("**Action:** No threat detected.")
