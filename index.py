# coding: utf-8
import eel
import sys


@eel.expose
def hello():
    print('hello')


if __name__ == '__main__':
    if len(sys.argv) == 0:
        eel.init('build')
        eel.start('index.html')
    elif sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)