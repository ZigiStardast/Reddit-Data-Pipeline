import configparser
import pathlib
import praw
import sys
import datetime
import pandas as pd
import numpy as np
from validate_input import validate_input

# Read Configuraton File
parser = configparser.ConfigParser()
script_path = pathlib.Path(__file__).parent.parent.parent.resolve()
config_file_name = "configuration.conf"
parser.read(f"{script_path}/{config_file_name}")


# Variables
CLIENT_ID = parser.get("REDDIT_CONFIG", "ClientID")
CLIENT_SECRET = parser.get("REDDIT_CONFIG", "ClientSecret")

SUBREDDIT_NAME = 'dataengineering'
TIME_FILTER = 'day'
LIMIT = None

# Attributes from Reddit Submission
ATTRIBUTES = (
    "id",
    "title",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "upvote_ratio",
    "over_18",
    "edited",
    "spoiler",
    "stickied",
)


try:
    output_file_name = sys.argv[1]
except Exception as e:
    sys.exit(1)

         
validate_input(output_file_name)
date_for_dag_run = datetime.datetime.strptime(output_file_name, "%Y%m%d")


def main():
    reddit_instance = reddit_api()
    df = extract_data(reddit=reddit_instance)
    transformed_df = transform_data(df)
    load_to_csv(transformed_df)
    


def reddit_api() -> praw.Reddit:
    try:
        user_agent = "My User Agent"
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=user_agent,
            )
        return reddit
    except Exception as e:
        print(f"Unable to connect to API. Error: {e}")
        sys.exit(1)
 
def extract_data(reddit) -> pd.DataFrame:
    list_of_posts = []
    subreddit_name = reddit.subreddit(SUBREDDIT_NAME)
    try:
        posts = subreddit_name.top(time_filter=TIME_FILTER, limit=LIMIT)
        for submission in posts:
            sub_dict_all_attributes = vars(submission)
            sub_dict = {ATTRIBUTE:sub_dict_all_attributes[ATTRIBUTE] for ATTRIBUTE in ATTRIBUTES}
            list_of_posts.append(sub_dict)
        df = pd.DataFrame(list_of_posts)
        return df
    except Exception as e:
        print(f"An error occured (extract_data), {e}")
        sys.exit(1)
        
def transform_data(df: pd.DataFrame):
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    
    df['over_18'] = np.where(
        (df['over_18'] == 'False') | (df['over_18'] == False), False, True
    ).astype(bool)
    
    df['spoiler'] = np.where(
        (df['spoiler'] == 'False') | (df['spoiler'] == False), False, True
    ).astype(bool)
    
    df['stickied'] = np.where(
        (df['stickied'] == 'False') | (df['stickied'] == False), False, True
    ).astype(bool)
    
     # TODO: For edited line, rather than force as boolean, keep date-time of last
     # edit and set all else to None.
    df['edited'] = np.where(
        (df['edited'] == 'False') | (df['edited'] == False), False, True
    ).astype(bool)
    
    return df
    
def load_to_csv(df: pd.DataFrame):
    try:
        df.to_csv(f'tmp/{output_file_name}.csv', index=False)
    except Exception as e:
        print(f"Error (load_to_csv), {e}")
        sys.exit(1)
        
        
if __name__ == "__main__":
    main()