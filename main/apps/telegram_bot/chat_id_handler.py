import os
import traceback
from time import sleep
from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests
from database import DataBase


def get_chat_id():
    bots = DataBase.get_bots()
    for bot in bots:
        chats = DataBase.get_chats_for_post_by_bot(bot[4])
        if chats:
            url = f'https://api.telegram.org/bot{bot[0]}/getUpdates'
            r = requests.get(url).text
            try:
                for chat in chats:
                    if not chat[2]:
                        chat_reference = chat[0].replace('@', '')
                        chat_title = chat[3]
                        sleep(6)
                        data = json.loads(r)
                        if data['ok']:
                            for _data in data['result']:
                                try:
                                    chat_id = _data['message']['chat']['id']
                                    try:
                                        chat_username = _data['message']['chat']['username']
                                    except:
                                        chat_username = 'No username'
                                    chat_title_json = _data['message']['chat']['title']
                                    if chat_title_json == chat_title:
                                        DataBase.update_chat_id((chat_id, chat_title))
                                except Exception as e:
                                    pass
                        else:
                            print('data not ok')
            except Exception as e:
                print(traceback.format_exc())

if __name__ == '__main__':
    try:
        while True:
            get_chat_id()
            sleep(150)
    except KeyboardInterrupt:
        print(KeyboardInterrupt)
