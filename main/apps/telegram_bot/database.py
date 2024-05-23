import sqlite3 as sql
import traceback

from config import DATA_BASE


class DataBase:
    db = DATA_BASE

    # ToDo SETTERS ################################################################

    @staticmethod
    def set() -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('INSERT INTO smartphone VALUES (?,?,?)', ())
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def set_new_user(values: tuple) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('INSERT INTO bot_app_user VALUES (?,?,?,?,?)', values)
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def set_new_message(values: tuple) -> None:
        print(values)
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute(
                'INSERT INTO bot_app_messages (id,username,text,photo,city,is_sent,is_allowed,user_id_id,date) VALUES (?,?,?,?,?,?,?,?,?)',
                values)
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def set_new_city(city: str) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute(
                'INSERT INTO bot_app_city (city) VALUES (?)', (city,))
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def set_new_channel(channel: str, title: str) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute(
                'INSERT INTO bot_app_channel (channel, title) VALUES (?,?)', (channel, title))
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def set_user_to_mail(val):
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('INSERT INTO home_usertomail (id) VALUES (?)', (val,))
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    # ToDo GETTERS ################################################################

    @staticmethod
    def get() -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            raw_data = cur.execute('SELECT * FROM smartphone WHERE available LIKE ?', ()).fetchall()
            con.close()
        except:
            print(traceback.format_exc())
        return data

    @staticmethod
    def get_posts(val) -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute(
                'SELECT day, text, media_file, post_time, is_sent, id FROM home_post WHERE is_sent = ? AND day = ?'
                'ORDER BY day', val).fetchall()
            con.close()
        except:
            print(traceback.format_exc())
        # print(data)
        return data

    @staticmethod
    def get_posts_by_bot_id(val) -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute(
                'SELECT day, text, media_file, post_time, is_sent, id FROM home_post WHERE is_sent = ? AND day = ? AND bot_id=?'
                'ORDER BY day', val).fetchall()
            con.close()
        except:
            print(traceback.format_exc())
        # print(data)
        return data


    @staticmethod
    def get_polls(val) -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute(
                'SELECT day, '
                'question, '
                'post_time, '
                'is_sent, '
                'option_1, '
                'option_2, '
                'option_3, '
                'option_4, '
                'option_5, '
                'option_6, '
                'option_7, '
                'option_8, '
                'option_9, '
                'option_10, '
                'is_anonymous, '
                'id '
                'FROM home_poll '
                'WHERE is_sent = ? AND day = ?'
                'ORDER BY day', val).fetchall()
            con.close()
        except:
            print(traceback.format_exc())

        return data

    @staticmethod
    def get_polls_by_bot_id(val) -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute(
                'SELECT day, '
                'question, '
                'post_time, '
                'is_sent, '
                'option_1, '
                'option_2, '
                'option_3, '
                'option_4, '
                'option_5, '
                'option_6, '
                'option_7, '
                'option_8, '
                'option_9, '
                'option_10, '
                'is_anonymous, '
                'id '
                'FROM home_poll '
                'WHERE is_sent = ? AND day = ? AND bot_id=?'
                'ORDER BY day', val).fetchall()
            con.close()
        except:
            print(traceback.format_exc())

        return data

    @staticmethod
    def get_bot():
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute('SELECT token, start_date, is_started, day FROM home_bot', ()).fetchone()
            con.close()
        except:
            print(traceback.format_exc())
        # print(data)
        return data

    @staticmethod
    def get_bots():
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute('SELECT token, start_date, is_started, day, id FROM home_bot', ()).fetchall()
            con.close()
        except:
            print(traceback.format_exc())
        # print(data)
        return data

    @staticmethod
    def get_chats() -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            d = cur.execute('SELECT reference, day, chat_id, title FROM home_chat WHERE chat_id=0 ', ()).fetchall()
            con.close()
            for i in d:
                data.append(['@' + i[0].split('/')[-1], i[1], i[2], i[3]])
        except:
            print(traceback.format_exc())
        # print(data)
        return data


    @staticmethod
    def get_chats_for_post() -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            d = cur.execute('SELECT reference, day, chat_id, title FROM home_chat', ()).fetchall()
            con.close()
            for i in d:
                data.append(['@' + i[0].split('/')[-1], i[1], i[2], i[3]])
        except:
            print(traceback.format_exc())
        # print(data)
        return data

    @staticmethod
    def get_chats_for_post_by_bot(val) -> list:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            d = cur.execute('SELECT reference, day, chat_id, title FROM home_chat WHERE bot_id=?', (val,)).fetchall()
            con.close()
            for i in d:
                data.append(['@' + i[0].split('/')[-1], i[1], i[2], i[3]])
        except:
            print(traceback.format_exc())
        # print(data)
        return data



    @staticmethod
    def get_tz() -> int:
        data = []
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            data = cur.execute('SELECT tz FROM home_usersettings', ()).fetchone()
            con.close()
            data = int(data[0].split(' ')[0].replace('+', ''))
        except:
            print(traceback.format_exc())
        # print(data)
        return data

    @staticmethod
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

    # ToDo UPDATE ################################################################

    @staticmethod
    def update(data: str) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE smartphone SET available=? WHERE model_city LIKE ?', ())
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def update_message_is_sent(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_post SET is_sent=? WHERE id=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_poll_is_sent(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_poll SET is_sent=? WHERE id=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_chat_id(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_chat SET chat_id=? WHERE title=?', val)
            con.commit()
            con.close()
            # if cur.rowcount < 1:
            #     print('Fail', 'UPDATE home_chat SET chat_id=? WHERE reference=?', val)
            # else:
            #     print('Succeed','UPDATE home_chat SET chat_id=? WHERE reference=?', val)
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_bot_day(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_bot SET start_date=?, day=? WHERE id=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_chat_error(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_chat SET error=? WHERE reference=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_chat_day(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_chat SET day=? WHERE reference=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    @staticmethod
    def update_chat_day_all(val) -> None:
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('UPDATE home_chat SET day=? WHERE day=?', val)
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())

    # ToDo DELETE ################################################################

    @staticmethod
    def delete():
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('DELETE FROM smartphone  WHERE model_city ', ())
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def delete_message(msg_id):
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('DELETE FROM bot_app_messages  WHERE id=? ', (msg_id,))
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def delete_city(city):
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('DELETE FROM bot_app_city  WHERE city=? ', (city,))
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def delete_channel(channel):
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('DELETE FROM bot_app_channel WHERE channel=? ', (channel,))
            con.commit()
            con.close()
        except:
            print(traceback.format_exc())

    @staticmethod
    def delete_user_to_mail(val):
        try:
            con = sql.connect(DATA_BASE, check_same_thread=False, timeout=100)
            cur = con.cursor()
            cur.execute('DELETE FROM home_usertomail WHERE id=?', (val,))
            con.commit()
            con.close()
        except sql.Error as error:
            print(error, traceback.format_exc())