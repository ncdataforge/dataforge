import os
import pandas as pd

from flask import Blueprint, request, jsonify
from .model import generate_data_from_prediction
from .send_res import save_file_from_request, download_result_from_prediction

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return {"status": "success", "message": "Bank Account Opening Fraud Detection is active"}

@main.route('/predict', methods=['POST'])
def predict():
    error_response = {
        "status": "failed"
    }
    
    # Verify "file" data in Body request
    if 'file' not in request.files:
        error_response['error'] = "Any file hasn't been uploaded"
        return jsonify(error_response), 400
    
    file = request.files['file']
    
    # Verify if file is in a CSV format
    try:
        data_df = pd.read_csv(file)
    except Exception as e:
        error_response['error'] = f"There are problems when reading CSV file: {str(e)}"
        return jsonify(error_response), 400

    if 'id_client' not in data_df.columns:
        error_response['error'] = f"CSV file must include id_client"
        return jsonify(error_response), 400

    # Generate a new file with data predicted and upload it to a S3 bucket 
    data_predicted_df, file_error = generate_data_from_prediction(data_df)
    if file_error is not None:
        error_response['error'] = file_error['error']
        return jsonify(error_response), 400

    file_ready_for_download, upload_error = save_file_from_request(data_df, data_predicted_df)
    if upload_error is not None:
        error_response['error'] = upload_error['error']
        return jsonify(error_response), 400

    # Generate link for download results from prediction
    get_s3_link_from_prediction, link_error = download_result_from_prediction(file_ready_for_download)
    if link_error is not None:
        error_response['error'] = link_error['error']
        return jsonify(error_response), 400

    success_response = {
        "status": "success",
        "filename": file_ready_for_download,
        "download_url": get_s3_link_from_prediction
    }

    return jsonify(success_response), 200

@main.teardown_app_request
def cleanup(exception=None):
    try:
        for file in os.listdir('/tmp/data_original_predicted'):
            if file.startswith("org-") or file.startswith("res-"):
                os.remove(os.path.join('/tmp/data_original_predicted', file))
    except Exception as err:
        print(f"Error cleaning up temp files: {err}")