import os
import csv
import praw
import psaw
import prawcore
import datetime
from submission_fetcher import SubmissionFetcher
from dotenv import load_dotenv

class SubmissionFilter:
    def __init__(self):
        self.reddit = self.reddit_init()

    def reddit_init(self):
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")
        user_agent = "SubmissionFilterer:v1.0 (by u/AverageAngryPeasant)"
        return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

    def filter_submissions(self, record="filtered.csv", delete=False):
        subs = SubmissionFetcher().fetch_submissions("askhistorians")
        with open(record, "w") as f:
            for sub in subs:
                to_delete = True
                for comm in sub.comments.replace_more(limit=None):
                    if not comm.distinguished:
                        to_delete = False
                        break
                if to_delete:
                    if delete:
                        # sub.delete()
                        pass
                    else:
                        print(sub.title)
                    # write line here