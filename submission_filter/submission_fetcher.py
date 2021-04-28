import os
import praw
import psaw
import prawcore
import datetime
from dotenv import load_dotenv

class SubmissionFetcher:
    def __init__(self):
        self.reddit = self.reddit_init()
        self.ps = psaw.PushshiftAPI(self.reddit)

    def reddit_init(self):
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")
        user_agent = "SubmissionFetcher:v1.0 (by u/AverageAngryPeasant)"
        return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

    def fetch_submissions(self, subreddit, limit=None):
        cache = []
        gen = self.ps.search_submissions(subreddit=subreddit)
        for c in gen:
            cache.append(c)

            if len(cache) % 100 == 0:
                print(f"Reached {len(cache)} submissions!")
                print("Time: " + datetime.datetime.now().strftime("%I:%M %p"))
            if limit and len(cache) == limit:
                break

        return cache