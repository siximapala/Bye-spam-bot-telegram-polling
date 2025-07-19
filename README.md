# Bye Spam Bot

Sometimes in your Telegram chat there are useful, interesting, or popular bots.  
For example, in my friends’ chat there is a bot that lets you raise a pig; by pressing the `/grow` command every day, it loses or gains weight.  
It’s fun, but there is one catch: these bots often use their ability to send messages to the chat and post 5–6 ads per day. To get rid of the ads, let’s use this Bye-spam bot.

## Rules

The script works as follows — most likely you already know one of two options:

1) Which words the bot DEFINITELY must NOT use (for example, the word "Subscribe" from "Subscribe to the bot developer’s Telegram channel").

2) Which words the bot can send ONLY WITH (for example, it always writes "Your pig has grown by 10 kilograms." If the message contains "grown" or "kilograms", which do not usually appear in ads, then this is the message we want to keep).

Accordingly, the bot has the following configuration parameters:

```python
GRAY_LIST = [11111111111, 2222222222]

ALLOWED_WORDS = ["hello", "bye", "how", "are", "you"]

FORBIDDEN_WORDS = ["ad", "spam", "18+"]

CHECK_ALLOWED    = True      # Toggle Allowed-Words mode
CHECK_FORBIDDEN  = False     # Toggle Forbidden-Words mode
```

- `GRAY_LIST` — the user_id of the bot or user we are monitoring (you can find it using @UserInfoBot or any similar bot).  
- `CHECK_ALLOWED` — if True, the bot checks whether the message contains any word from `ALLOWED_WORDS`; without such words, the message is deleted.  
- `CHECK_FORBIDDEN` — if True, the bot checks whether the message contains any word from `FORBIDDEN_WORDS`; if so, the message is deleted.

Before using this bot script, fill in these parameters to suit your needs. Choose one mode or use both to be sure. Before running the filter, decide which approach best fits you and which words trigger ads or other unwanted content, then add them to the lists.

## Example

### Mode A: `CHECK_ALLOWED = True`, `CHECK_FORBIDDEN = False`
```python
GRAY_LIST = [11111111111, 2222222222]

ALLOWED_WORDS = ["hello", "bye", "how", "are", "you"]

FORBIDDEN_WORDS = ["ad", "spam", "18+"]

CHECK_ALLOWED = True  #!
CHECK_FORBIDDEN = False
```
Examples of messages that will be filtered for the bot/user in the gray list:
1. "Hello everyone!" — **deleted**
2. "Hello to all" — **not deleted**
3. "Hello bye everyone" — **not deleted**
4. "Ad spam 18+ bye" — **not deleted**
5. "A very long text about the cultural value of the brat Charli xcx album" — **deleted**
6. "A very long text about the cultural value of the brat Charli xcx album hello" — **not deleted**
7. "A very long text about the cultural value of the brat Charli xcx album ad" — **deleted**

### Mode B: `CHECK_ALLOWED = False`, `CHECK_FORBIDDEN = True`
```python
GRAY_LIST = [11111111111, 2222222222]

ALLOWED_WORDS = ["hello", "bye", "how", "are", "you"]

FORBIDDEN_WORDS = ["ad", "spam", "18+"]

CHECK_ALLOWED = False
CHECK_FORBIDDEN = True  #!
```
Examples of messages that will be filtered:
1. "Hello everyone!" — **not deleted**
2. "Hello to all" — **not deleted**
3. "Hello bye everyone" — **not deleted**
4. "Ad spam 18+ bye" — **deleted**
5. "A very long text about the cultural value of the brat Charli xcx album" — **not deleted**
6. "A very long text about the cultural value of the brat Charli xcx album hello" — **not deleted**
7. "A very long text about the cultural value of the brat Charli xcx album ad" — **deleted**

### Mode C: `CHECK_ALLOWED = True`, `CHECK_FORBIDDEN = True`
```python
GRAY_LIST = [11111111111, 2222222222]

ALLOWED_WORDS = ["hello", "bye", "how", "are", "you"]

FORBIDDEN_WORDS = ["ad", "spam", "18+"]

CHECK_ALLOWED = True  #!
CHECK_FORBIDDEN = True  #!
```
Examples of messages that will be filtered:
1. "Hello everyone!" — **deleted**
2. "Hello to all" — **not deleted**
3. "Hello bye everyone" — **not deleted**
4. "Ad spam 18+ bye" — **deleted**
5. "A very long text about the cultural value of the brat Charli xcx album" — **deleted**
6. "A very long text about the cultural value of the brat Charli xcx album hello" — **not deleted**
7. "A very long text about the cultural value of the brat Charli xcx album ad" — **deleted**

## Installation

0. In the bot directory, run:
   ```bash
   pip install -r .\requirements.txt
   ```
   (install Python and Pip if not already installed)

1. Create your bot in @BotFather and get its token.
2. In the bot directory, create a `.env` file (based on `.env-example`) and paste in the token.
3. Open the script and define the filtering rules in the "Rules" section of this README.
4. Add your new bot to your Telegram group.
5. Grant the bot admin rights.
   5.1. Make sure `/setprivacy` is set to `Disable` in @BotFather.
6. Run the `.py` file:
   ```bash
   python bot.py
   ```
