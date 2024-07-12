import pandas as pd


def get_account_list(file):
    upload_list = []
    login_list = []
    pwd_list = []
    login = pd.read_excel(file, index_col=None, na_values=['NA'], usecols="A")
    pwd = pd.read_excel(file, index_col=None, na_values=['NA'], usecols="B")
    for i in login:
        for j in login[i].values:
            login_list.append(j)
    for i in pwd:
        for j in pwd[i].values:
            pwd_list.append(j)
    for i in range(len(login_list)):
        upload_list.append([login_list[i], pwd_list[i]])
    return upload_list


def get_code_list(file):
    code_list = []
    code = pd.read_excel(file, index_col=None, na_values=['NA'], usecols="A")
    for i in code:
        for j in code[i].values:
            code_list.append(j)
    return code_list

print(get_code_list('codes.xlsx'))

