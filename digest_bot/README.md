# DigestBot

DigestBot is a reddit bot where users can subscribe to receive messages; in this case, it is being used to receive digests from the r/AskHistorians mods.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this script's requirements.
```bash
pip install -r requirements.txt
```

Then, run digest_bot.py using python.
```bash
python digest_bot.py
```

Note that you must place a .env file in this directory with the proper CLIENTID and CLIENTSECRET variables before using this script, as well as the bot account's USERNAME and PASSWORD.

## Commands

As of now, DigestBot has only a few commands. Use these commands by sending them through private message to u/AHMessengerBot on reddit.

* !sub or !subscribe: Subscribes to the bot.
* !unsub or !unsubscribe: Unsubscribes to the bot.
* !mod \[user\]: Mods a user. Must have mod permissions. Default value for user is the sender.
* !unmod \[user\]: Unmods a user. Must have mod permissions. Default value for user is the sender.
* !send: Copies the rest of the message text and its subject and sends that as a new message to all subs.
* !export_mods: Responds with the usernames of all modded users. Must have mod permissions.

For the !send command, format your message the same way that you would format any reddit PM: just add "!send " to the front of it. Additionally, for all command except the !send command, the subject of the message does not matter.

Note that commands must be separated from the rest of their text with a space. Messages that are sent to u/AHMessengerBot that do not start with a command will be sent to me through PM.
