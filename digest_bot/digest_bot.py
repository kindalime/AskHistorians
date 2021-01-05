import praw
import prawcore
from dotenv import load_dotenv
import os
import sqlite3

class DigestBot:
    def __init__(self):
        reddit = self.reddit_init()
        
    def reddit_init(self):
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")
        user_agent = "DigestBot:v1.0 (by u/AverageAngryPeasant)"
        return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

    def parse_message(self, message):
        text = message.body.strip()
        if text in ["!sub", "!subscribe"]:
            pass
        elif text in ["!unsub", "!unsubscribe"]:
            pass
        elif text in ["!mod"]:
            pass
        elif text in ["!unmod"]:
            pass
        else:
            pass

    def main(self):
        for message in self.reddit.inbox.stream():
            self.parse_message(message)
            message.mark_read()
