import os
import sys
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler

# File path for model
model_path = os.path.join(os.getcwd() + '/app/modelo_fraudev3.pkl')

# Load model if "pkl" file exists
if os.path.exists(model_path):
    modelo = joblib.load(model_path)
else:
    print(f"Archivo de modelo no encontrado. Path: {model_path}")
    sys.exit(1)

# Initialize scaler
scaler = StandardScaler()

# Define important columns which were used for traning
model_cols = [
        'income', 'name_email_similarity',
       'current_address_months_count', 'customer_age', 'days_since_request',
       'bank_branch_count_8w', 'date_of_birth_distinct_emails_4w',
       'credit_risk_score', 'email_is_free', 'phone_home_valid',
       'phone_mobile_valid', 'bank_months_count', 'has_other_cards',
       'proposed_credit_limit', 'foreign_request', 'session_length_in_minutes',
       'keep_alive_session', 'device_distinct_emails_8w', 'payment_type_AA',
       'payment_type_AB', 'payment_type_AC', 'payment_type_AD',
       'payment_type_AE', 'employment_status_CA', 'employment_status_CB',
       'employment_status_CC', 'employment_status_CD', 'employment_status_CE',
       'employment_status_CF', 'employment_status_CG', 'housing_status_BA',
       'housing_status_BB', 'housing_status_BC', 'housing_status_BD',
       'housing_status_BE', 'housing_status_BF', 'housing_status_BG',
       'source_INTERNET', 'source_TELEAPP', 'device_os_linux',
       'device_os_macintosh', 'device_os_other', 'device_os_windows',
       'device_os_x11'
]

# Verify if required columns are in the DataFrame
def __prepare_dataframe(df: pd.DataFrame):
    missing_cols = [col for col in model_cols if col not in df.columns]
    if missing_cols:
        return None, f"Missing columns: {', '.join(missing_cols)}"
    
    filtered_df = df[model_cols].copy()
    return filtered_df, None

# Pre-process DataFrame using StandardScaler
def __preprocessing_data(data_df: pd.DataFrame) -> pd.DataFrame:
    normalized_data_df = scaler.fit_transform(data_df)
    return pd.DataFrame(normalized_data_df, columns=data_df.columns)

def generate_data_from_prediction(data_df: pd.DataFrame) -> tuple[pd.DataFrame | None, dict | None]:
    try:
        # Prepare DataFrame for prediction
        prepared_data_df, error = __prepare_dataframe(data_df)
        if error:
            return None, {'error': error}
        
        preprocessed_data_df = __preprocessing_data(prepared_data_df)

        ml_prediction = modelo.predict(preprocessed_data_df)

        res_df = pd.DataFrame(data={'predictions': ml_prediction})

        return res_df, None
    except Exception as err:
        return None, {'error': str(err)}