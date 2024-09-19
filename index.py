# coding: utf-8
import eel
import sys
import database
import search

selected = []

@eel.expose
def hello_eel():
    print('Hello Eel')

@eel.expose
def search_keywords(search_keywords):
    qsearch_results = search.search_database(search_keywords)
    search_results = []
    for keyword in search_keywords:
        qsearch_results[keyword] = search.sort_results(qsearch_results[keyword], keyword)
        search_results.append({"keyword": keyword, "result": qsearch_results[keyword], "selected": selected})
    return search_results


if __name__ == '__main__':
    if len(sys.argv) == 0:
        eel.init('build')
        eel.start('index.html')
    elif sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)