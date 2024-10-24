# coding: utf-8
from ast import Or
from multiprocessing.managers import Namespace
from tkinter.font import names
import eel
import sys
import database
import anki
import search
import registry
from collections import OrderedDict
from typing import List

keywords = []
search_results = OrderedDict()
selected_terms = {}
anki_deck = None
anki_model = None


@eel.expose
def hello_eel():
    print('Hello Eel')

@eel.expose
def search_keywords(k):
    global keywords
    global search_results

    to_search = []

    keywords = k
    for keyword in keywords:
        cached = registry.search_results.get(keyword)
        if cached != -1:
            search_results[keyword] = cached
            registry.search_results.put(keyword, cached)
        else: 
            search_results[keyword] = []
            to_search.append(keyword)
            
    
    qsearch_results = search.search_database(to_search)
    for keyword in to_search:
        if qsearch_results[keyword]:
            qsearch_results[keyword] = search.sort_results(qsearch_results[keyword], keyword)
            search_results[keyword] = qsearch_results[keyword]
            selected_terms[keyword] = search.auto_select(qsearch_results[keyword], keyword)
        else:
            search_results[keyword] = []
        registry.search_results.put(keyword, search_results[keyword])
    return search_results

@eel.expose
def generate_anki():
    global selected_terms
    global anki_deck
    global anki_model

    anki_deck, anki_model = anki.create_anki_deck()

    selected_list = []

    for key in selected_terms.keys():
        selected_list += selected_terms[key]

    anki_deck = anki.create_notes(anki_deck, anki_model, selected_list)
    anki.write_to_file(anki_deck, "japanki.apkg")
    # conn.commit()
    return



@eel.expose
def get_selected(keywords : List[str] = []): # TODO? add parameters
    if not keywords:
        return selected_terms
    
    returned = []
    for keyword in keywords:
        if keyword in keywords:
            returned[keyword] = selected_terms[keyword]
    
    return returned

@eel.expose
def add_selected(term, keyword):
    selected_terms[keyword].append(term)
    return selected_terms

@eel.expose
def remove_selected(term, keyword):
    selected_terms[keyword].remove(term)
    return selected_terms


@eel.expose
def get_anki_deck(ids : List[int] = [], names : List[str] = []):
    decks = None
    if ids == [] and names == []:
        decks = database.get_anki_deck(all=True)
    else:
        decks = database.get_anki_deck(deck_ids=ids, deck_names=names)
    return decks

@eel.expose
def get_anki_model(ids : List[int] = [], names : List[str] = []):
    models = None
    if ids == []:
        models = database.get_anki_model(all=True)
    else:
        models = database.get_anki_model(model_ids=ids, model_names=names)
    return models

@eel.expose
def select_anki_deck(id : int) -> int:
    global anki_deck
    if database.get_anki_deck(ids=[id]) != []:
        anki_deck = anki.create_anki_deck(id)
        return id
    return -1

@eel.expose
def select_anki_model(id : int) -> int:
    global anki_model
    if database.get_anki_model(ids=[id]) != []:
        anki_model = anki.create_anki_model(id)
        return id
    return -1



if __name__ == '__main__':
    print(get_anki_model())
    if len(sys.argv) == 0:
        eel.init('build')
        eel.start('index.html')
    elif sys.argv[1] == '--develop':
        eel.init('client')
        eel.start({"port": 3000}, host="localhost", port=8888)