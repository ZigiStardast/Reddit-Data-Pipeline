import boto3
import botocore
import configparser
import pathlib
import datetime
import sys

import psycopg2
from validate_input import validate_input
from psycopg2 import sql

# Configuration File
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.parent.parent.resolve()
config_file_name = "configuration.conf"
parser.read(f"{script_path}/{config_file_name}")

# Variabless
RS_USERNAME = parser.get("aws_config", "redshift_username")
RS_PASSWORD = parser.get("aws_config", "redshift_password")
RS_HOSTNAME = parser.get("aws_config", "redshift_hostname")
RS_PORT = parser.get("aws_config", "redshift_port")
RS_ROLE = parser.get("aws_config", "redshift_role")
RS_DB = parser.get("aws_config", "redshift_database")
BUCKET_NAME = parser.get("aws_config", "bucket_name")
ACCOUNT_ID = parser.get("aws_config", "account_id")
TABLE_NAME = "reddit"

try:
    output_file_name = sys.argv[1]
except Exception as e:
    sys.exit(1)
        
# S3 File, Role String
s3_file_path = f"s3://{BUCKET_NAME}/{output_file_name}.csv"
role_string = f"arn:aws:iam::{ACCOUNT_ID}:role/{RS_ROLE}"

# Create Table if doesn't exist
sql_create_table = sql.SQL(
    """ CREATE TABLE IF NOT EXISTS {table} (
                            id varchar PRIMARY KEY,
                            title varchar(max),
                            num_comments int,
                            score int,
                            author varchar(max),
                            created_utc timestamp,
                            url varchar(max),
                            upvote_ratio float,
                            over_18 bool,
                            edited bool,
                            spoiler bool,
                            stickied bool
        );
    """
).format(table=sql.Identifier(TABLE_NAME))

# If table exists remove it and add new with the same id
create_temp_table = sql.SQL("CREATE TEMP TABLE temp_table (LIKE {table});"
                            ).format(table=sql.Identifier(TABLE_NAME))

copy_to_temp_table = f"COPY temp_table FROM '{s3_file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"

delete_from_table = sql.SQL("DELETE FROM {table} USING our_staging_table WHERE {table}.id = our_staging_table.id;"
                            ).format(table=sql.Identifier(TABLE_NAME))

add_to_table = sql.SQL("INSERT INTO {table} SELECT * FROM temp_table;"
                       ).format(table=sql.Identifier(TABLE_NAME))

drop_temp_table = "DROP TABLE temp_table"

def main():
    validate_input(output_file_name)
    rs_conn = connect_to_redshift()
    

def connect_to_redshift():
    try:
        conn = psycopg2.connect(host=RS_HOSTNAME, user=RS_USERNAME, password=RS_PASSWORD, dbname=RS_DB, port=RS_PORT)
        return conn
    except Exception as e:
        print(f"Unable to connect to redshift: {e}")
        sys.exit(1)

def load_data_into_redshift(conn):
    
    with conn:
        cur = conn.cursor()
        cur.execute(sql_create_table)
        cur.execute(create_temp_table)
        cur.execute(copy_to_temp_table)
        cur.execute(delete_from_table)
        cur.execute(add_to_table)
        cur.execute(drop_temp_table)
        
        conn.commit()
    
if __name__ == '__main__':
    main()