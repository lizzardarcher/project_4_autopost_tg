from main.apps.parser.DataBase import DataBase
from main.apps.parser.parser_main import DataBase
import datetime

# codes = DataBase.get_codes()
# print(codes)
#
# accounts = DataBase.get_accounts()
# print(accounts)
# print(accounts.pop(0))
# print(accounts)
#
# delay = DataBase.get_delay()
# print(delay)
# print(int(DataBase.get_delay())*3600)
# values = (0.0, True, 'XGJY6LWDF4ZNDTND')
DataBase.update_gift_code((0, True, datetime.datetime.now(), 'XGJY6LWDF4ZNDTND'))
print(DataBase.get_checked_gc(('XGPVXK9N5MT5ZKXP',)))
print(0 == False)