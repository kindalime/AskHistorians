import praw
import prawcore
from dotenv import load_dotenv
import os
import sys
import datetime
import pytz
from utils import *
import csv

class SaveFetcher():
    def __init__(self):
        pass

    def reddit_signin(self, username, password):
        load_dotenv()
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")

        user_agent = "SaveFetcher:v0.0.1 (by u/AverageAngryPeasant)"
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)
        
        try:
            self.reddit.user.me()
        except prawcore.ResponseException:
            return False, "Error: invalid credentials!"
        except Exception as e:
            print(e)
            if hasattr(e, 'message'):
                return False, e.message
            else:
                return False, str(e)
        else:
            return True, None

    def create_stamps(self, from_date, to_date):
        self.from_stamp = get_unix_time(from_date)
        self.to_stamp = get_unix_time(to_date)
        return True, None
        
    def saved_posts(self):
        try:
            saved = [post for post in self.reddit.user.me().saved(limit=None)]
            with open("results.csv", "w") as f:
                writer = csv.writer(f)
                writer.writerow("Post Author", "Post Permalink", "Post Score", "Submission Author", "Submission Permalink", "Submission Score")
                for post in saved:
                    if type(post) is praw.models.Comment:
                        if post.subreddit.display_name == "AskHistorians" and self.from_stamp < post.created_utc < self.to_stamp:
                            line = [post.author.name, post.permalink, post.score, post.submission.author.name, post.submission.permalink, post.submission.score]
                            writer.writerow(line)
                            post.unsave()
        except Exception as e:
            print(e)
            if hasattr(e, 'message'):
                return e.message
            else:
                return str(e)
        else:
            return "Success! Check this program's location for results."
