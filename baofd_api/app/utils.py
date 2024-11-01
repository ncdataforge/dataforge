import os
import pandas as pd
import numpy as np

def generate_tmp_csv_file(df: pd.DataFrame, filename: str, filepath: str) -> str:
    tmp_directory = filepath
    os.makedirs(tmp_directory, exist_ok=True)
    tmp_filepath = os.path.join(tmp_directory, filename)

    df.to_csv(tmp_filepath, index=False)

    return tmp_filepath

def generate_file_for_download(df_1: pd.DataFrame, df_2: pd.DataFrame, filename: str, filepath: str) -> str:
    tmp_directory = filepath
    os.makedirs(tmp_directory, exist_ok=True)
    tmp_filepath = os.path.join(tmp_directory, filename)

    id_clients = df_1['id_client']
    result_df = pd.concat([id_clients, df_2], axis=1)

    result_df['fraud_status'] = np.where(result_df['predictions'] == 1, 'Fraud', 'Not Fraud')

    result_df.to_excel(tmp_filepath, index=False)

    return tmp_filepath

