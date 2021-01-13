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
        exists = os.path.isfile("subs.db")
        db = sqlite3.connect("subs.db")
        c = db.cursor()
        if not exists:
            c.execute("CREATE TABLE SUBS ([username] text, [mod] integer)")
        db.commit()
        return db

    def parse_message(self, message):
        text = message.body.strip()
        user = message.author.name

        if text in ["!sub", "!subscribe"]:
            self.add_user(user)
        elif text in ["!unsub", "!unsubscribe"]:
            self.remove_user(user)
        elif text in ["!mod"]:
            self.mod_user(user)
        elif text in ["!unmod"]:
            self.unmod_user(user)
        else:
            self.send_message(message)

    def check_user(self, username):
        self.cursor.execute("SELECT username FROM subs where username = '" + username + "'")
        return self.cursor.fetchone() != None

    def check_mod(self, username):
        if username in ["AngryAveragePeasant", "Georgy_K_Zhukov", "AHMessengerBot"]:
            return True

        self.cursor.execute("SELECT username FROM subs where username = '" + username + "' AND mod = 1")
        result = self.cursor.fetchone()
        return result != None

    def add_user(self, username):
        if self.check_user(username):
            return

        self.cursor.execute("INSERT INTO SUBS VALUES ('" + username + "', 0)")
        self.db.commit()
        print("add user " + username)
        self.print_db()

    def remove_user(self, username):
        if not self.check_user(username):
            return

        self.cursor.execute("DELETE FROM SUBS WHERE username = '" + username + "'")
        self.db.commit()
        print("remove user " + username)
        self.print_db()

    def mod_user(self, username):
        if not self.check_user(username) and not self.check_mod(username):
            return

        self.cursor.execute("UPDATE subs SET mod = 1 WHERE username = '" + username + "'")
        self.db.commit()
        print("mod user " + username)
        self.print_db()

    def unmod_user(self, username):
        if not self.check_user(username) and not self.check_mod(username):
            return

        self.cursor.execute("UPDATE subs SET mod = 0 WHERE username = '" + username + "'")
        self.db.commit()
        print("unmod user " + username)
        self.print_db()

    def send_message(self, message):
        text = message.body.strip()
        user = message.author.name
        subject = message.subject

        if " " not in text or text[:text.find(" ")] != "!send":
            self.send_pm(user, subject, text)

        # checks if there is a mod with the user's name
        if self.check_mod(user):
            if text == "!send":
                self.send_pm(user, subject, "Error: must include message to send!")
            self.send_digest(subject, text[text.find(" ")+1:])
        else:
            self.send_pm(user, subject, text)

    def send_digest(self, subject, text):
        users = self.cursor.execute("SELECT username FROM subs")
        for username in users:
            username = username[0]
            self.reddit.redditor(username).message(subject, text)

    def send_pm(self, user, subject, text):
        if text not in ["sub", "subscribe", "unsub", "unsubscribe", "mod", "unmod", "send"] and text[0] != "!":
            text = "User " + user + " has sent you a message through DigestBot:\n" + "SUBJECT: " + subject + "\n" + text
            self.reddit.redditor("AverageAngryPeasant").message("DigestBot PM", text)

    def print_db(self):
        self.cursor.execute("SELECT * FROM SUBS")
        print(self.cursor.fetchall())

    def main(self):
        self.print_db()
        # what does this return past the intial 100?
        for message in self.reddit.inbox.stream():
            self.parse_message(message)
            message.mark_read()

if __name__ == "__main__":
    bot = DigestBot()
    bot.main()
