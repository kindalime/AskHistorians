import praw
import prawcore
from dotenv import load_dotenv
import os
import sqlite3
import logging

class DigestBot:
    def __init__(self):
        self.reddit = self.reddit_init()
        self.db = self.create_database()
        self.cursor = self.db.cursor()
        if os.getenv("AHDEBUG") in ["TRUE", "true"]:
            logging.basicConfig(filename='digest.log', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='digest.log', level=logging.INFO)

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
            c.execute("CREATE TABLE SUBS ([user] text, [mod] integer)")
        db.commit()
        return db

    def extract_command(self, text):
        text = text.strip()
        if " " not in text:
            return text, ""
        else:
            return text[:text.find(" ")], text[text.find(" ") + 1:]

    def parse_message(self, message):
        command, text = self.extract_command(message.body)
        subject = message.subject
        logging.debug(f"Parsed message with command {command} and text {text}.")
        user = message.author.name

        if user in ["reddit"]: # automated emails
            return

        if command in ["!sub", "!subscribe"]:
            self.add_user(user)
        elif command in ["!unsub", "!unsubscribe"]:
            self.remove_user(user)
        elif command in ["!mod"]:
            self.mod_user(user, text)
        elif command in ["!unmod"]:
            self.unmod_user(user, text)
        elif command in ["!send"]:
            if self.check_mod(user):
                if not text:
                    self.send_pm(user, subject, "Error: must include message to send!")
                else:
                    self.send_digest(subject, text[text.find(" ")+1:])
            else:
                self.send_pm(user, subject, text)
        else:
            text = message.body.strip()
            user = message.author.name
            self.send_pm(user, subject, text)

    def check_user(self, user):
        self.cursor.execute("SELECT user FROM subs where user = '" + user + "'")
        return self.cursor.fetchone() != None

    def check_mod(self, user):
        if user in ["AverageAngryPeasant", "Georgy_K_Zhukov", "AHMessengerBot"]:
            return True

        self.cursor.execute("SELECT user FROM subs where user = '" + user + "' AND mod = 1")
        result = self.cursor.fetchone()
        return result != None

    def add_user(self, user):
        if self.check_user(user):
            logging.info(f"Attempted add failed, {user} is already subbed.")
            return

        self.cursor.execute("INSERT INTO SUBS VALUES ('" + user + "', 0)")
        self.db.commit()
        logging.info(f"Added user {user} successfully.")

    def remove_user(self, user):
        if not self.check_user(user):
            logging.info(f"Attempted remove failed, {user} is already not subbed.")
            return

        self.cursor.execute("DELETE FROM SUBS WHERE user = '" + user + "'")
        self.db.commit()
        logging.info(f"Removed user {user} successfully.")

    def mod_user(self, user, text):
        if not self.check_user(user) or not self.check_mod(user):
            logging.info(f"Attempted mod failed, {user} is not modded.")
            return
        
        if not text:
            text = user

        self.cursor.execute("UPDATE subs SET mod = 1 WHERE user = '" + text + "'")
        self.db.commit()
        logging.info(f"Mod {user} modded user {text} successfully.")

    def unmod_user(self, user, text):
        if not self.check_user(user) or not self.check_mod(user):
            logging.info(f"Attempted unmod failed, {user} is not modded.")
            return

        if not text:
            text = user

        self.cursor.execute("UPDATE subs SET mod = 0 WHERE user = '" + text + "'")
        self.db.commit()
        logging.info(f"Mod {user} unmodded user {text} successfully.")

    def send_digest(self, subject, text):
        users = self.cursor.execute("SELECT user FROM subs")
        for user in users:
            user = user[0]
            self.reddit.redditor(user).message(subject, text)
        logging.info(f"User {user} successfully sent digest.")
        logging.debug(f"Digest had subject {subject} and text {text}.")

    def send_pm(self, user, subject, text):
        if text and text not in ["sub", "subscribe", "unsub", "unsubscribe", "mod", "unmod", "send"] and text[0] != "!":
            text = "User " + user + " has sent you a message through DigestBot:\n\n" + "SUBJECT: " + subject + "\n\n" + text
            self.reddit.redditor("AverageAngryPeasant").message("DigestBot PM", text)
        logging.debug(f"Private message sent by user {user}.")

    def print_db(self):
        self.cursor.execute("SELECT * FROM SUBS")
        logging.debug(self.cursor.fetchall())

    def main(self):
        self.print_db()
        try:
            for message in self.reddit.inbox.stream():
                self.parse_message(message)
                message.mark_read()
        except sqlite3.DatabaseError as err:
            logging.error("Sqlite error: " + str(err))

if __name__ == "__main__":
    bot = DigestBot()
    bot.main()
