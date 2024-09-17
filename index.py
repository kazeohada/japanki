# coding: utf-8
import eel
import sys
import database
import search


@eel.expose
def hello_eel():
    print('Hello Eel')

@eel.expose
def search_keywords(search_keywords):
    search_results = search.search_database(search_keywords)
    selected = {}
    for keyword in search_keywords:
        search_results[keyword] = search.sort_results(search_results[keyword], keyword)
        selected[keyword] = [(search.auto_select(search_results[keyword], keyword))]
    return search_results



if __name__ == '__main__':
    if len(sys.argv) == 0:
        eel.init('build')
        eel.start('index.html')
    elif sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)