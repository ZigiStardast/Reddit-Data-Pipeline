import datetime
import sys

def validate_input(input_date: str):
    try:
        datetime.datetime.strptime(input_date, "%Y%m%d")
    except ValueError as e:
        raise ValueError("Input should be in format YYYYmmdd")
        sys.exit(1)  
