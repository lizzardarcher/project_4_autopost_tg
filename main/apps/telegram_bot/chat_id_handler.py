import os
import traceback
from time import sleep
from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests
from database import DataBase


def get_chat_id():
    # bot_token = DataBase.get_bot()[0]
    bots = DataBase.get_bots()
    # print(bots)
    # print(chats, bot_token)
    for bot in bots:
        chats = DataBase.get_chats_for_post_by_bot(bot[4])
        # print(chats)
        if chats:
            # r = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates?offset=-100').text
            url = f'https://api.telegram.org/bot{bot[0]}/getUpdates'
            r = requests.get(url).text
            # print(bot_token)
            # print(url)
            try:
                for chat in chats:
                    if not chat[2]:
                        chat_reference = chat[0].replace('@', '')
                        chat_title = chat[3]
                        # print(chat_reference, chat_title)
                        sleep(6)
                        data = json.loads(r)
                        if data['ok']:
                            # chat_id = data['result'][0]['my_chat_member']['chat']['id']
                            # print(data['ok'])
                            for _data in data['result']:
                                try:
                                    chat_id = _data['message']['chat']['id']
                                    # print(chat_id)

                                    try:
                                        chat_username = _data['message']['chat']['username']
                                    except:
                                        chat_username = 'No username'

                                    chat_title_json = _data['message']['chat']['title']
                                    # print(chat_id, chat_username, 'https://t.me/'+chat_reference)
                                    if chat_title_json == chat_title:
                                        # print('SUPER!!!', (chat_id, chat_title))
                                        DataBase.update_chat_id((chat_id, chat_title))
                                    # print(chat_id, chat_title)
                                except Exception as e:
                                    pass
                                    # print(traceback.format_exc())
                        else:
                            print('data not ok')
            except Exception as e:
                # pass
                print(traceback.format_exc())




if __name__ == '__main__':
    try:
        while True:
            get_chat_id()
            sleep(150)
    except KeyboardInterrupt:
        print(KeyboardInterrupt)

# if data['ok']:
#     # chat_id = data['result'][0]['my_chat_member']['chat']['id']
#     print(data['ok'])
#     for _data in data['result']:
#         try:
#             chat_id = _data['my_chat_member']['chat']['id']
#             print(chat_id)
#
#             try:
#                 chat_username = _data['my_chat_member']['chat']['username']
#             except:
#                 chat_username = 'No username'
#
#             chat_title_json = _data['my_chat_member']['chat']['title']
#             print(chat_id, chat_username, 'https://t.me/' + chat_reference)
#             if chat_title_json == chat_title:
#                 print('SUPER!!!', (chat_id, chat_title))
#                 DataBase.update_chat_id((chat_id, chat_title))
#             print(chat_id, chat_title)
#         except Exception as e:
#             # pass
#             print(traceback.format_exc())
# else:
#     print('data not ok')