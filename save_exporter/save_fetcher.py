import praw
from dotenv import load_dotenv
import os
import sys
import datetime
import pytz

class SaveFetcher():
    def __init__(self, username, password, client_id, client_secret):
        user_agent = "SaveFetcher:v0.0.1 (by u/AverageAngryPeasant)"
        self.reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)
        self.redditor = self.reddit.redditor(name=username)
        
    def get_saved_posts(self):
        saved = [post for post in self.reddit.user.me().saved(limit=None)]
        for post in saved:
            if type(post) is praw.models.Comment:
                if self.from_stamp < post.created_utc < self.to_stamp:
                    print(post.author.name)
                    print(post.permalink)
                    print(post.submission.name)
                    print(post.submission.permalink)
                    print(post.submission.score)
                    print(post.score)
        return saved
 
    def get_unix_time(self, year, month, day, timezone):
        date = datetime.datetime(year, month, day)
        date = timezone.localize(date)
        stamp = date.timestamp()
        return stamp

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    client_id = os.getenv("CLIENTID")
    client_secret = os.getenv("CLIENTSECRET")
    s = SaveFetcher(username, password)
    # s.get_saved_posts()
    stamp = s.get_unix_time(2020, 12, 30, pytz.timezone("America/New_York"))
    print(datetime.datetime.fromtimestamp(stamp, tz=datetime.timezone.utc))