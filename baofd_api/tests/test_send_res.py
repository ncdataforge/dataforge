import os
import boto3
import pytest

from moto import mock_aws
from dotenv import load_dotenv
from app.send_res import upload_file_s3_ingestion

load_dotenv()

test_data_ingestion_bucket = 'test-baofd-data-ingestion-ml-api'

# Simulate S3 session with moto 
@pytest.fixture(scope="function")
def mock_session_s3():
    with mock_aws():
        yield boto3.client('s3', region_name='us-east-1')

# Fixture to create S3 bucket for testing function
@pytest.fixture
def create_test_bucket(mock_session_s3):
    mock_session_s3.create_bucket(Bucket=test_data_ingestion_bucket)

    response = mock_session_s3.list_buckets(Prefix='test_')
    list_bucket_res = [k_buckets['Name'] for k_buckets in response['Buckets']]

    assert test_data_ingestion_bucket in list_bucket_res, (
        f"Bucket for testing {test_data_ingestion_bucket} has not been created. Available buckets: {list_bucket_res}"
    )

# Testing "save_data_from_request" function with mocked session
def test_save_data_from_request(mock_session_s3, create_test_bucket):
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_home = os.path.join(current_path + '/docs/test_file_result.csv')

    res = upload_file_s3_ingestion(mock_session_s3,
                                   file_home,
                                   test_data_ingestion_bucket,
                                   'test-object-data-ingestion',
                                   'test_file_result.csv')

    response = mock_session_s3.list_objects_v2(Bucket=test_data_ingestion_bucket)
    
    assert res == True
    assert 'Contents' in response
    assert any(obj['Key'] == 'test-object-data-ingestion/test_file_result.csv' for obj in response['Contents'])