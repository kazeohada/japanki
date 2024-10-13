# coding: utf-8
import eel
import sys
import database
import anki
import search

keywords = []
search_results = {}
selected_terms = {}


@eel.expose
def hello_eel():
    print('Hello Eel')

@eel.expose
def search_keywords(k):
    global keywords
    global search_results

    keywords = k

    qsearch_results = search.search_database(keywords)
    for keyword in keywords:
        if qsearch_results[keyword]:
            qsearch_results[keyword] = search.sort_results(qsearch_results[keyword], keyword)
            search_results[keyword] = qsearch_results[keyword]
            selected_terms[keyword] = search.auto_select(qsearch_results[keyword], keyword)
        else:
            search_results[keyword] = []
    return search_results

@eel.expose
def generate_anki():
    global selected_terms

    anki_deck, anki_model = anki.create_anki_deck()

    selected_list = []

    for key in selected_terms.keys():
        selected_list += selected_terms[key]

    anki_deck = anki.create_notes(anki_deck, anki_model, selected_list)
    anki.write_to_file(anki_deck, "japanki.apkg")
    # conn.commit()
    return

@eel.expose
def get_selected(): # TODO? add parameters
    return selected_terms

@eel.expose
def add_selected(term, keyword):
    selected_terms[keyword].append(term)
    return selected_terms

@eel.expose
def remove_selected(term, keyword):
    selected_terms[keyword].remove(term)
    return selected_terms


if __name__ == '__main__':
    if len(sys.argv) == 0:
        eel.init('build')
        eel.start('index.html')
    elif sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)