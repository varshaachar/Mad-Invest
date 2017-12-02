# praw to use reddit
import praw  # pip install praw
from datetime import datetime


CLIENT_ID = "Vau1RZY26a53fA"
CLIENT_SECRET = "AaiSrWmjaPXVf5jfqxxdBXNRfI8"

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, password='myreddit01!', user_agent='testscript by /u/varsha_achar',
                     username='varsha_achar')

i = 0  # to count number of posts
for submission in reddit.subreddit('bitcoin').hot(limit=900):
    i += 1

    # output date as datetimeobj instead of timestamp
    date = datetime.fromtimestamp(submission.created)
    print(submission.title, date)

print("\n")
print("There were", i, "number of posts") # only for information purposes.