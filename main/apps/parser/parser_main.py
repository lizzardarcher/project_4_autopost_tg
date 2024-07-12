from time import sleep
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium_stealth import stealth
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

from main.apps.parser.DataBase import DataBase


DEBUG = True
start_url = 'https://www.apple.com'
# start_url = 'https://www.google.com'
balance_url = 'https://secure5.store.apple.com/shop/giftcard/balance'
urls = [start_url, balance_url]
LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'
invalid = 'The PIN or gift card number you entered is invalid.'


def get_webdriver():
    options = Options()
    options.add_argument("--window-size=1366,768")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        # "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/ 537.36(KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"
    )
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(
        # executable_path='chromedriver',
        # options=options
    )
    # driver.delete_all_cookies()
    # driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    #     "origin": '*',
    #     "storageTypes": 'all',
    # })
    # driver.implicitly_wait(5)
    return driver


def parse_apple_gc(urls: list, code: str, account: tuple) -> str:
    driver = get_webdriver()
    driver.get(url=urls[0])
    sleep(1)
    try:
        if DEBUG == True: print('Got to ', urls[0])
        sleep(1)
        elements = {
            # 'bag': 'ac-gn-bag',
            'bag': 'globalnav-menubutton-link-bag',
            # 'initial_sign_in': 'ac-gn-bagview-nav-item-signIn',
            'initial_sign_in': '/html/body/div[1]/nav/div/ul/li[4]/div[2]/div/div/div/div[1]/div/div/a',
            'login': 'account_name_text_field',
            'password': 'password_text_field',
            'accept-sign-in-first': 'sign-in',
            'accept-sign-in-second': 'sign-in',
            'input_code': 'giftCardBalanceCheck.giftCardPin',
            'check_balance': 'balanceCheck-balance',
        }

        # select bag, to open profile menu
        bag = driver.find_element(By.ID, elements['bag'])
        bag.click()
        sleep(1)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass bag')

        # select sign-in btn, to enter sign-in menu
        initial_sign_in = driver.find_element(By.XPATH, elements['initial_sign_in'])
        initial_sign_in.click()
        sleep(1)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass initial_sign_in')

        # switch to sign-in iframe
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
        sleep(1)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass iframe')

        # select and fill login field
        login = driver.find_element(By.ID, elements['login'])
        login.click()
        login.send_keys(account[0])
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass login')

        # select next symbol
        sign_in = driver.find_element(By.ID, elements['accept-sign-in-first'])
        sign_in.click()
        sleep(1)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass accept-sign-in-first')

        # select and password field
        pwd = driver.find_element(By.ID, elements['password'])
        pwd.click()
        pwd.send_keys(account[1])
        sleep(1)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass password')

        # confirm sign-in
        sign_in = driver.find_element(By.ID, elements['accept-sign-in-second'])
        sign_in.click()
        sleep(5)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass accept-sign-in-second')

        try: twofa = driver.find_element(By.ID, 'sec-code-wrapper')
        except: twofa = None
        if twofa: DataBase.update_account_report((False, '2fa needed.', account[0]))

        try: error_msg = driver.find_element(By.ID, 'errMsg')
        except: error_msg = None
        if error_msg: DataBase.update_account_report((False, 'Apple ID or pwd is incorrect.', account[0]))

        try: security_1 = driver.find_element(By.XPATH, '/html/body/div[1]/appleid-repair/idms-widget/div/div/div/privacy-consent/div/idms-step/div/div/div/div[2]')
        except: security_1 = None

        if security_1: security_1.click()
        sleep(2)

        # get to GC balance page
        driver.get(urls[1])
        sleep(2)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Got to ', urls[1])

        # input card code
        input_code = driver.find_element(By.ID, elements['input_code'])
        input_code.click()
        input_code.send_keys(code)
        sleep(4)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass input_code')

        # click to get balance check page
        check_balance = driver.find_element(By.ID, elements['check_balance'])
        check_balance.click()
        sleep(3)
        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
        if DEBUG == True: print('Pass check_balance')

        soup = BeautifulSoup(driver.page_source.encode('utf-8'), "html.parser").text
        if invalid.lower() in soup.lower():
            if DEBUG == True: print('code inavlid TRUE!!!')
            DataBase.update_gc_report(('code is incorrect.', True, datetime.now(), code))

        html = driver.page_source.encode('utf-8')
    except:
        html = ''
        driver.close()
        sleep(1)
        driver.quit()
    driver.close()
    sleep(1)
    driver.quit()
    return html


def get_balance(html: str):
    soup = BeautifulSoup(html, "html.parser")
    total = soup.find('div', {"class": "rs-gcbalance-balance"}).text
    total = float(total.replace('$', '').replace(',', '.'))
    if DEBUG == True: print('Balance is: $', total)
    return total


def run_parser():
    accounts = DataBase.get_accounts()
    codes = DataBase.get_codes()
    counter = 0
    while codes:
        for account in accounts:
            if DEBUG == True: print(account)
            for code in codes:
                if DEBUG == True: print(len(codes), 'Current code is:', code[0].encode('utf-8'))
                try:
                    try:
                        if DEBUG == True: print('Get balance ...')
                        balance = get_balance(parse_apple_gc(urls=urls, code=code[0], account=account))
                        # if DEBUG == True: print(LINE_UP, end=LINE_CLEAR)
                        if DEBUG == True: print('Passing Get balance ...')
                    except:
                        if DEBUG == True: print(traceback.format_exc())
                        if 'error' in traceback.format_exc():
                            break
                        else:
                            is_checked = DataBase.get_checked_gc((code[0],))
                            if DEBUG == True: print('is_checked', is_checked)
                            if not is_checked:
                                DataBase.update_gc_report(('Inactive', True, datetime.now(), code[0]))
                            codes.remove(code)
                            break
                    values = (balance, True, '', datetime.now(), code[0])
                    DataBase.update_gift_code(values)
                    codes.remove(code)
                    counter += 1
                    if counter == 3:
                        counter = 0
                        break
                except:
                    if DEBUG == True: print(traceback.format_exc())
                    # codes.remove(code[0])
                    break


if __name__ == '__main__':
    while True:
        try:
            run_parser()
            DataBase.set_all_gc_unchecked()
            sleep(int(DataBase.get_delay())*60)
        except:
            if DEBUG == True: print(traceback.format_exc())
            sleep(int(DataBase.get_delay())*60)
