import praw
import prawcore
from dotenv import load_dotenv
import os
import csv

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
client_id = os.getenv("CLIENTID")
client_secret = os.getenv("CLIENTSECRET")
user_agent = "MessageSender:v1.0 (by u/AverageAngryPeasant)"
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)

with open('messages.csv', "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        recipient, subject, message = row
        reddit.redditor(recipient).message(subject, message)
