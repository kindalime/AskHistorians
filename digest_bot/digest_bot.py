import praw
import prawcore
from dotenv import load_dotenv
import os
import sqlite3

class DigestBot:
    def __init__(self):
        self.reddit = self.reddit_init()
        self.db = self.create_database()
        self.cursor = self.db.cursor()

    def reddit_init(self):
        load_dotenv()
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        client_id = os.getenv("CLIENTID")
        client_secret = os.getenv("CLIENTSECRET")
        user_agent = "DigestBot:v1.0 (by u/AverageAngryPeasant)"
        return praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

    def create_database(self):
        db = sqlite3.connect("users.db")
        c = db.cursor()
        c.execute("CREATE TABLE SUBS ([username] text UNIQUE, [mod] integer)")
        db.commit()
        return db

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

    def add_user(self, username):
        self.cursor.execute("INSERT INTO SUBS (username, mod) VALUES (" + username + ", 0)")
        self.db.commit()

    def remove_user(self, username):
        self.cursor.execute("DELETE FROM SUBS WHERE username = " + username)
        self.db.commit()

    def mod_user(self, username):
        self.cursor.execute("UPDATE subs SET mod = 1 WHERE username = " + username)
        self.db.commit()

    def unmod_user(self, username):
        self.cursor.execute("UPDATE subs SET mod = 0 WHERE username = " + username)
        self.db.commit()

    def send_pm(self, message):
        pass

    def main(self):
        for message in self.reddit.inbox.stream():
            self.parse_message(message)
            message.mark_read()
