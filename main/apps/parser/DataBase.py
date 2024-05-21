import sqlite3 as sql
import traceback
from sqlite3 import Error as SqlError
from main.apps.parser import config


DATA_BASE = config.DATA_BASE


class DataBase:

    @staticmethod
    def update_gift_code(val) -> None:
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                cur.execute('UPDATE home_giftcode SET balance=?, is_checked=?, report=?, date=?  WHERE code=?', (val[0], val[1], val[2], val[3], val[4]))
                con.commit()
                print('Gift code is Checked', val)
                code = cur.execute('SELECT * FROM home_giftcode WHERE code=?', (val[3],)).fetchone()
                print(code)
        except SqlError:
            print(traceback.format_exc(), val)
            try: print(val[0], val[1], val[2], val[3])
            except: pass

    @staticmethod
    def get_codes():
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                # codes = cur.execute('SELECT code FROM home_giftcode').fetchall()
                codes = cur.execute('SELECT code FROM home_giftcode WHERE is_checked=?', (False,)).fetchall()
                # print('Gift codes Fetched Successfully! Total:', len(codes), ' codes')
        except SqlError:
            codes = []
            print(traceback.format_exc())
        return codes

    @staticmethod
    def get_accounts():
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                accounts = cur.execute('SELECT login, password FROM home_appleaccount WHERE is_active=?', (True,)).fetchall()
                # print('Accounts Fetched Successfully! Total:', len(accounts), ' accounts')
        except SqlError:
            accounts = []
            print(traceback.format_exc())
        return accounts

    @staticmethod
    def get_delay() -> int:
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                delay = cur.execute('SELECT start_time FROM home_usersettings').fetchone()[0]
        except SqlError:
            delay = 12
            print(traceback.format_exc())
        return delay

    @staticmethod
    def update_account_report(val) -> None:
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                cur.execute('UPDATE home_appleaccount SET is_active=?, report=? WHERE login=?', val)
                con.commit()
        except SqlError:
            print(traceback.format_exc())

    @staticmethod
    def update_gc_report(val) -> None:
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                cur.execute('UPDATE home_giftcode SET report=?, is_checked=?, date=? WHERE code=?', val)
                con.commit()
        except SqlError:
            print(traceback.format_exc())

    @staticmethod
    def set_all_gc_unchecked() -> None:
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                cur.execute('UPDATE home_giftcode SET is_checked=?', (False,))
                con.commit()
        except SqlError:
            print(traceback.format_exc())

    @staticmethod
    def get_checked_gc(val):
        try:
            with sql.connect(DATA_BASE, check_same_thread=False, timeout=100) as con:
                cur = con.cursor()
                checked = cur.execute('SELECT is_checked FROM home_giftcode WHERE code=?', val).fetchone()[0]
        except SqlError:
            checked = 1
            print(traceback.format_exc())
        return checked




