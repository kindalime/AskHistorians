import os
import sys
import csv
import praw
import psaw
import prawcore
import datetime as dt
import pytz
from dotenv import load_dotenv
from utils import *

class Submission_Filter:
    """Class that handles all of the internal work with reddit for fetching saves."""

    def __init__(self):
        pass

    def create_dates(self, from_date, to_date):
        """Method that creates unix timestamps from dates, taking time zone into account."""

        self.from_stamp = int(dt.datetime.combine(from_date, dt.time()).timestamp())
        self.to_stamp = int(dt.datetime.combine(to_date, dt.time()).timestamp())
        if self.to_stamp < self.from_stamp:
            return False, "Error: from date after to date!"
        return True, None

    def reddit_signin(self, username, password, twofac):
        """Method that handles reddit authentication with praw."""

        if not username or not password:
            return False, "Error: blank username/password!"

        load_dotenv()
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")

        if twofac:
            password = password + ":" + twofac

        user_agent = "SaveFetcher:v1.0 (by u/AverageAngryPeasant)"
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)
        self.ps = psaw.PushshiftAPI(self.reddit)

        try:
            self.reddit.user.me()
        except prawcore.ResponseException:
            return False, "Error: invalid credentials!"
        except Exception as e:
            print(e)
            if hasattr(e, 'message'):
                return False, "Error: " + e.message
            else:
                return False, "Error: " + str(e)
        else:
            return True, None
        
    def fetch_submissions(self, subreddit, limit=None):
        cache = []
        gen = self.ps.search_submissions(subreddit=subreddit, after=self.from_stamp, before=self.to_stamp, limit=limit)
        for c in gen:
            cache.append(c)

            if len(cache) % 100 == 0:
                print(f"Reached {len(cache)} submissions!")
                print("Time: " + dt.datetime.now().strftime("%I:%M:%S %p"))
            if limit and len(cache) == limit:
                break

        return cache

    def filter_submissions(self, record, delete=False):
        if not record:
            name = "results.csv"
        else:
            name = record + ".csv"

        posts = self.fetch_submissions("askhistorians")
        with open(name, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Post Author", "Post Title", "Post Score", "Post Permalink", "Post Creation Time"])
            for post in posts:
                to_delete = True
                for comm in post.comments.replace_more(limit=None):
                    if not comm.distinguished:
                        to_delete = False
                        break
                if to_delete:
                    line = [post.author, post.title, post.score, post.permalink, dt.datetime.fromtimestamp(post.created_utc)]
                    writer.writerow(line)

                    if delete:
                        post.delete()
                    else:
                        print(post.title)
        return "Filtering complete!"
