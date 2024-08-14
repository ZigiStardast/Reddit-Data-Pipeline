import boto3
import botocore
import configparser
import pathlib
import datetime
import sys
from validate_input import validate_input

# Read Configuration File
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.parent.parent.resolve()
config_file_name = "configuration.conf"
parser.read(f"{script_path}/{config_file_name}")


# Variables
BUCKET_NAME = parser.get("aws_config", "bucket_name")
AWS_REGION = parser.get("aws_config", "aws_region")

try:
    output_file_name = sys.argv[1]
except Exception as e:
    sys.exit(1)

# S3 File Name
FILENAME = f"{output_file_name}.csv"

def main():
    validate_input(output_file_name)
    s3_conn = connect_to_s3()
    create_bucket_if_not_exists(s3_conn)
    upload_to_s3(s3_conn)
    
def connect_to_s3():
    try:
        conn = boto3.resource('s3')
        return conn
    except Exception as e:
        print(f"Can't connect to S3. Error: {e}")
        sys.exit(1)
        
def create_bucket_if_not_exists(conn):
    exists = True
    try:
        conn.meta.client.head_bucket(Bucket=BUCKET_NAME)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False
    if exists == False:
        conn.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={
            'LocationConstraint': AWS_REGION})
        
def upload_to_s3(conn):
    conn.meta.client.upload_file(
        Filename='/tmp/' + FILENAME,
        Bucket=BUCKET_NAME,
        Key=FILENAME # putanja unutar bucket-a
    )
    
if __name__ == '__main__':
    main()