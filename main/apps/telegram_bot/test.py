from time import sleep

from database import DataBase
from datetime import date, datetime, time
import sqlite3 as sql
import traceback

from config import DATA_BASE
# # p = DataBase.get_posts((False, 1))
# # b = DataBase.get_bot()
# c = DataBase.get_chats()
# print(c)
# tz = DataBase.get_tz()
#
# for i in p:
#     print(i)
#
# print(b)
# print(c)
# print(tz)

# t = date.today()
# print(t)
# tm = datetime.now().time().strftime('%H:%M')
# print(tm)
# print(datetime.now().strftime('%H:%M'))
# for i in p:
#     post_time = i[3][:5]
#     print(post_time)
#     if post_time == datetime.now().strftime('%H:%M'):
#         print('OK')

# DataBase.update_message_is_sent((False, 1))
# DataBase.update_message_is_sent((False, 2))
# DataBase.update_message_is_sent((False, 3))
# DataBase.update_message_is_sent((False, 4))

# datetime.strftime('2023-05-03', '%Y-%m-%D')
# datetime_object = datetime.strptime('2023-05-03', '%Y-%m-%d')
# print(datetime_object)



# import sys
# print(sys.getfilesystemencoding())
# import locale
# print(locale.getdefaultlocale())

# DataBase.update_chat_id((-1221, 'https://t.me/d12d12d12f'))

def update_chat_day_all(val) -> None:
    try:
        con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
        cur = con.cursor()
        cur.execute('UPDATE home_chat SET day=? WHERE day=?', val)
        con.commit()
        con.close()
    except sql.Error as error:
        print(error, traceback.format_exc())


def get_user_to_mail() -> list:
    data = []
    try:
        con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
        cur = con.cursor()
        data = cur.execute('SELECT id from home_usertomail').fetchall()
        con.close()
    except sql.Error as error:
        print(error, traceback.format_exc())
    return data


print(get_user_to_mail())