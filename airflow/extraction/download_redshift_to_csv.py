import configparser
import pathlib
import sys
import psycopg2
from psycopg2 import sql
import csv

"""
Download Redshift table to CSV file. Will be stored under /tmp folder.
"""

# Configuration file
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.resolve()
conf_file_name = "configuration.conf"
parser.read(f'{script_path}/{conf_file_name}')

# Variabless
RS_USERNAME = parser.get("aws_config", "redshift_username")
RS_PASSWORD = parser.get("aws_config", "redshift_password")
RS_HOSTNAME = parser.get("aws_config", "redshift_hostname")
RS_PORT = parser.get("aws_config", "redshift_port")
RS_ROLE = parser.get("aws_config", "redshift_role")
RS_DB = parser.get("aws_config", "redshift_database")
TABLE_NAME = "reddit"

def main():
    conn = connect_to_redshift()
    download_data_to_csv(conn)

def connect_to_redshift():
    try:
        conn = psycopg2.connect(host=RS_HOSTNAME, user=RS_USERNAME, password=RS_PASSWORD, dbname=RS_DB, port=RS_PORT)
        return conn
    except Exception as e:
        print(f"Unable to connect to redshift: {e}")
        sys.exit(1)
        
def download_data_to_csv(rs_conn):
    """Download data from Redshift table to CSV"""
    with rs_conn:
        cur = rs_conn.cursor()
        cur.execute(
            sql.SQL("SELECT * FROM {table};").format(table=sql.Identifier(TABLE_NAME))
        )
        result = cur.fetchall()
        headers = [col[0] for col in cur.description]
        result.insert(0, tuple(headers))
        fp = open("redshift_output.csv", "w")
        myFile = csv.writer(fp)
        myFile.writerows(result)
        fp.close()
        
if __name__ == '__main__':
    main()
    