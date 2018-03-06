# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 13:57:57 2018

@author: RIP-OpanasenkoVG
"""

import datetime
from time import sleep
import re
import requests
import pymorphy2


def get_updates_json(request, offset):
    params = {"timeout": 100, "offset": offset}
    response = requests.get(request + "getUpdates", data=params)
    return response.json()

def last_update(data):
    results = data["result"]
    total_updates = len(results) - 1
    return results[total_updates]

def all_updates(data):
    results = data["result"]
    return results

def get_chat_id(update):
    chat_id = update["message"]["chat"]["id"]
    return chat_id

def send_mess(chat, text):
    params = {"chat_id": chat, "text": text}
    response = requests.post(url + "sendMessage", data=params)
    return response

def make_response (msg):
    chat_id = get_chat_id(msg)
    answer = make_answer(msg["message"])
    print("Received: " + msg["message"]["text"])
    send_mess(chat_id, answer)

def is_latin_text(text):
    return re.match(r"[a-zA-Z]", text)

def make_answer(msg):
    vowels = set("уеыаоэяиюё")
    wrds = list(re.findall("\w+", msg["text"], re.UNICODE))
    if "RU" in msg["from"]["language_code"] and not is_latin_text(wrds[len(wrds)-1]):
        answer = "Хуйнаны, а не " + msg["text"].lower()
    else:
        answer = "Хуйнаны. Пиши как русский, епископ!"
    return answer

def send_updates(sent_updates):
    now = datetime.datetime.now()
    if now.hour >= 11 and now.minute >= 0 and now.second >= 0 and not sent_updates:
        for usr in all_users:
            date_diff = datetime.timedelta()
            date_diff = VIEZD_DATE - now
            date_diff_str = str(date_diff.days) + " " + day_str.make_agree_with_number(date_diff.days).word
            text = "Братка, до выезда всего " + date_diff_str
            send_mess(usr, text)
        sent_updates = True
    if now.hour == 0:
        sent_updates = False
    return sent_updates

url = "https://api.telegram.org/bot531357875:AAHi4QESk1pkUkuZ6paId7ef1xqliZqqtMo/"
VIEZD_DATE = datetime.datetime(2018, 3, 15, hour=20, minute=30, second=0)
morph = pymorphy2.MorphAnalyzer()
day_str = morph.parse("день")[0]
sent_updates = False

all_users = []
# список всех юзеров, которым будем отправлять напоминалки
offset = last_update(get_updates_json(url, offset = None))["update_id"]

if __name__ == "__main__":
    while True:
        try:
            for msg in all_updates(get_updates_json(url, offset)):
                offset = msg["update_id"] + 1
                make_response (msg)
            chat_id = msg["message"]["chat"]["id"]
            if not chat_id in all_users:
                all_users.append(chat_id)
            sent_updates = send_updates(sent_updates)
            sleep(1)
        except KeyboardInterrupt:
            exit()