from pyexpat import model
import psycopg2
from typing import List
import time
from config import CURSOR as cursor

def search_word(keyword: str):
    word_ids = []
    term_ids = []

    # using english
    definitions = get_meaning_definition(definitions=[keyword])
    [word_ids.append(definition["Word_ID"]) for definition in definitions if definition["Word_ID"] not in word_ids]

    # using japanese
    qterms = get_word_term(terms=[keyword], word_ids=word_ids) # with word_ids found above
    [word_ids.append(term["Word_ID"]) for term in qterms if term["Word_ID"] not in word_ids]
    qterms = get_word_term(word_ids=word_ids)
    qmeanings = get_term_meaning(term_ids=[term["Term_ID"] for term in qterms])
    qdefinitions = get_meaning_definition(meaning_ids=[meaning["Meaning_ID"] for meaning in qmeanings])

    words = get_word_popularity(word_ids=word_ids)

    # kanji
    qterm_kanji = get_term_kanji(word_ids=word_ids)
    kanji_list = []
    [kanji_list.append(kanji["Kanji"]) for kanji in qterm_kanji if kanji["Kanji"] not in kanji_list]
    qkanji = search_kanji(kanji_search=kanji_list)

    for word in words:
        word["Terms"] = []
        terms = [term for term in qterms if term["Word_ID"] == word["Word_ID"]]
        for term in terms:
            meanings = [meaning for meaning in qmeanings if meaning["Term_ID"] == term["Term_ID"]]
            term["Meanings"] = []
            definitions = [definition for definition in qdefinitions if definition["Meaning_ID"] in [meaning["Meaning_ID"] for meaning in meanings]]
            current_meaning_id = definitions[0]["Meaning_ID"]
            current_meaning = {}
            current_meaning["Meaning_ID"] = current_meaning_id
            current_meaning["Popularity"] = next(meanings[i]["Popularity"] for i in range(len(meanings)) if meanings[i]["Meaning_ID"] == current_meaning_id)
            current_meaning["Definitions"] = []

            term["Kanji"] = []
            term_kanji = [e["Kanji"] for e in qterm_kanji if e["Term_ID"] == term["Term_ID"]]
            for kanji in term_kanji:
                term["Kanji"].append(next(k for k in qkanji if k["Kanji"] == kanji))

            for definition in definitions:
                if definition["Meaning_ID"] != current_meaning_id:
                    term["Meanings"].append(current_meaning)
                    current_meaning_id = definition["Meaning_ID"]
                    current_meaning = {} 
                    current_meaning["Meaning_ID"] = current_meaning_id
                    current_meaning["Popularity"] = next(meanings[i]["Popularity"] for i in range(len(meanings)) if meanings[i]["Meaning_ID"] == current_meaning_id)
                    current_meaning["Definitions"] = []
                current_meaning["Definitions"].append(definition["Definition"])
                
            term["Meanings"].append(current_meaning)
        word["Terms"] = terms
    

    return words

def search_term(keyword: str):

    term_ids = []    
    # using english
    definitions = get_meaning_definition(definitions=[keyword])

    qterms = get_term_meaning(meaning_ids=[definition["Meaning_ID"] for definition in definitions])
    [term_ids.append(term["Term_ID"]) for term in qterms if term["Term_ID"] not in term_ids]
    
    # using japanese
    terms = get_word_term(terms=[keyword], term_ids=term_ids)
    qmeanings = get_term_meaning(term_ids=[term["Term_ID"] for term in terms])
    qdefinitions = get_meaning_definition(meaning_ids=[meaning["Meaning_ID"] for meaning in qmeanings])


    for term in terms:
        meanings = [meaning for meaning in qmeanings if meaning["Term_ID"] == term["Term_ID"]]
        term["Meanings"] = []
        definitions = [definition for definition in qdefinitions if definition["Meaning_ID"] in [meaning["Meaning_ID"] for meaning in meanings]]
        current_meaning_id = definitions[0]["Meaning_ID"]
        current_meaning = {}
        current_meaning["Meaning_ID"] = current_meaning_id
        current_meaning["Popularity"] = next(meanings[i]["Popularity"] for i in range(len(meanings)) if meanings[i]["Meaning_ID"] == current_meaning_id)
        current_meaning["Definitions"] = []

        for definition in definitions:
            if definition["Meaning_ID"] != current_meaning_id:
                term["Meanings"].append(current_meaning)
                current_meaning_id = definition["Meaning_ID"]
                current_meaning = {} 
                current_meaning["Meaning_ID"] = current_meaning_id
                current_meaning["Popularity"] = next(meanings[i]["Popularity"] for i in range(len(meanings)) if meanings[i]["Meaning_ID"] == current_meaning_id)
                current_meaning["Definitions"] = []
            current_meaning["Definitions"].append(definition["Definition"])
            
        term["Meanings"].append(current_meaning)       

    return terms

def search_kanji(kanji_search: List[str]):
    onyomi_list = get_kanji_onyomi(kanji=kanji_search)
    kunoymi_list = get_kanji_kunyomi(kanji=kanji_search)
    definition_list = get_kanji_defintion(kanji=kanji_search)

    kanji_list = []

    for i in range(len(kanji_search)):
        kanji = {}
        kanji["Kanji"] = kanji_search[i]
        onyomi = []
        kunyomi = []
        definition = []
        [onyomi.append(ony) for ony in onyomi_list if kanji["Kanji"] == ony["Kanji"]]
        [kunyomi.append(kun) for kun in kunoymi_list if kanji["Kanji"] == kun["Kanji"]]
        [definition.append(de["Definition"]) for de in definition_list if kanji["Kanji"] == de["Kanji"]]
        if onyomi:
            kanji["Kanji_ID"] = onyomi[0]["Kanji_ID"]
        else:
            kanji["Kanji_ID"] = kunyomi[0]["Kanji_ID"]

        kanji["Onyomi"] = [{key: on[key] for key in on.keys() & {"Onyomi_ID", "Onyomi"}} for on in onyomi]
        kanji["Kunyomi"] = [{key: kun[key] for key in kun.keys() & {"Kunyomi_ID", "Kunyomi", "Ending"}} for kun in kunyomi]
        kanji["Definitions"] = definition

        kanji_list.append(kanji)

    return kanji_list

def get_word(cursor):
    cursor
    
def get_word_popularity(word_ids: List[str] = []):
    if word_ids == []:
        return []
    
    conditions = []
    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)
    
    statement = f"""SELECT "Word_ID", "Popularity" FROM "Word_Popularity_View" WHERE {' OR '.join(conditions)} ORDER BY "Popularity" DESC;"""

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Popularity"] = res[1]
        result[i] = res_dict

    return result

def get_word_term(term_ids: List[int] = [], word_ids: List[int] = [], main_term_ids: List[int] = [], terms: List[str] = []):
    if term_ids == [] and word_ids  == [] and terms  == []:
        return []

    conditions = []

    if term_ids:
        term_id_condition = f""""Term_ID" IN ({', '.join(f"'{id}'" for id in term_ids)})"""
        conditions.append(term_id_condition)
    
    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)

    # if main_term_ids:
    #     main_term_id_condition = f""""Main_Term_ID" IN ({', '.join(f"'{id}'" for id in main_term_ids)})"""
    #     conditions.append(main_term_id_condition)
    
    if terms:
        term_conditions = [f""""Japanese" = '{term}' OR "Reading" = '{term}'""" for term in terms]
        term_condition = " OR ".join(term_conditions)
        conditions.append(term_condition)

    statement = f"""SELECT DISTINCT "Word_ID", "Term_ID", "Japanese", "Reading" FROM "Word_Term_View" WHERE {' OR '.join(conditions)}"""

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Term_ID"] = res[1]
        res_dict["Japanese"] = res[2]
        res_dict["Reading"] = res[3]
        result[i] = res_dict

    return result

def get_word_main_term(term_ids: List[int] = [], word_ids: List[int] = [], terms: List[str] = []):
    if term_ids == [] and word_ids  == [] and terms  == []:
        return []

    conditions = []
    
    if term_ids:
        term_id_condition = f""""Term_ID" IN ({', '.join(f"'{id}'" for id in term_ids)})"""
        conditions.append(term_id_condition)
    
    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)
    
    if terms:
        term_conditions = [f""""Japanese" = '{term}' OR "Reading" = '{term}'""" for term in terms]
        term_condition = " OR ".join(term_conditions)
        conditions.append(term_condition)

    statement = f"""SELECT "Word_ID", "Term_ID", "Main_Term_ID", "Japanese", "Reading" FROM "Word_Main_Term_View" WHERE {' OR '.join(conditions)}"""

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Term_ID"] = res[1]
        res_dict["Main_Term_ID"] = res[2]
        res_dict["Japanese"] = res[3]
        res_dict["Reading"] = res[4]
        result[i] = res_dict

    return result

def get_term_meaning(word_ids: List[int] = [], term_ids: List[int] = [], terms: List[str] = [], meaning_ids: List[int] = []):
    if word_ids == [] and term_ids == [] and terms == [] and meaning_ids == []:
        return []
    
    conditions = []

    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)

    if term_ids:
        term_id_condition = f""""Term_ID" IN ({', '.join(f"'{id}'" for id in term_ids)})"""
        conditions.append(term_id_condition)
    
    if terms:
        term_conditions = [f""""Japanese" = '{term}' OR "Reading" = '{term}'""" for term in terms]
        term_condition = " OR ".join(term_conditions)
        conditions.append(term_condition)
    
    if meaning_ids:
        meaning_id_condition = f""""Meaning_ID" IN ({', '.join(f"'{id}'" for id in meaning_ids)})"""
        conditions.append(meaning_id_condition)
    
    statement = f"""SELECT DISTINCT "Word_ID", "Term_ID", "Japanese", "Reading", "Meaning_ID", "Popularity" FROM "Term_Meaning_View" WHERE {' OR '.join(conditions)}"""

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Term_ID"] = res[1]
        res_dict["Japanese"] = res[2]
        res_dict["Reading"] = res[3]
        res_dict["Meaning_ID"] = res[4]
        res_dict["Popularity"] = res[5]
        result[i] = res_dict

    return result

def get_meaning_definition(word_ids: List[int] = [], meaning_ids: List[int] = [], definition_ids: List[int] = [], definitions: List[str] = []):
    if word_ids  == [] and definition_ids  == [] and meaning_ids  == [] and definitions  == []:
        return []
    
    conditions = []

    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)
    
    if meaning_ids:
        meaning_id_condition = f""""Meaning_ID" IN ({', '.join(f"'{id}'" for id in meaning_ids)})"""
        conditions.append(meaning_id_condition)

    if definition_ids:
        definition_id_condition = f""""Definition_ID" IN ({', '.join(f"'{id}'" for id in definition_ids)})"""
        conditions.append(definition_id_condition)

    if definitions:
        definition_condition = f""""Definition" IN ({', '.join(f"'{definition}'" for definition in definitions)})"""
        conditions.append(definition_condition)

    statement = f"""SELECT DISTINCT "Word_ID", "Meaning_ID", "Definition_ID", "Definition", "Order" FROM "Meaning_Definition_View" WHERE {' OR '.join(conditions)}
                        ORDER BY "Meaning_ID", "Order" """

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Meaning_ID"] = res[1]
        res_dict["Definition_ID"] = res[2]
        res_dict["Definition"] = res[3]
        res_dict["Order"] = res[4]
        result[i] = res_dict

    return result

def get_term_kanji(word_ids: List[int] = [], term_ids: List[int] = [], kanji_ids: List[int] = [], terms: List[str] = [], kanji: List[str] = []):
    if word_ids == [] and term_ids == [] and kanji_ids == [] and terms == [] and kanji == []:
        return []

    conditions = []

    if word_ids:
        word_id_condition = f""""Word_ID" IN ({', '.join(f"'{id}'" for id in word_ids)})"""
        conditions.append(word_id_condition)

    if term_ids:
        term_id_condition = f""""Term_ID" IN ({', '.join(f"'{id}'" for id in term_ids)})"""
        conditions.append(term_id_condition)
    
    if kanji_ids:
        kanji_id_condition = f""""Kanji_ID" IN ({', '.join(f"'{id}'" for id in kanji_ids)})"""
        conditions.append(kanji_id_condition)
    
    if terms:
        term_conditions = [f""""Japanese" = '{term}' OR "Reading" = '{term}'""" for term in terms]
        term_condition = " OR ".join(term_conditions)
        conditions.append(term_condition)

    if kanji:
        kanji_condition = f""""Kanji" IN ({', '.join(f"'{id}'" for id in kanji)})"""
        conditions.append(kanji_condition)

    statement = f"""SELECT DISTINCT "Word_ID", "Term_ID", "Kanji_ID", "Japanese", "Reading", "Kanji", "Order" FROM "Term_Kanji_View" WHERE {' OR '.join(conditions)}
                    ORDER BY "Term_ID", "Order" """
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Word_ID"] = res[0]
        res_dict["Term_ID"] = res[1]
        res_dict["Kanji_ID"] = res[2]
        res_dict["Japanese"] = res[3]
        res_dict["Reading"] = res[4]
        res_dict["Kanji"] = res[5]
        result[i] = res_dict
    
    return result
    
def get_kanji_onyomi(kanji_ids: List[int] = [], kanji: List[str] = []):
    if kanji_ids == [] and kanji == []:
        return []
    conditions = []

    if kanji_ids:
        kanji_id_condition = f""""Kanji_ID" IN ({', '.join(f"'{id}'" for id in kanji_ids)})"""
        conditions.append(kanji_id_condition)

    if kanji:
        kanji_condition = f""""Kanji" IN ({', '.join(f"'{kanji}'" for kanji in kanji)})"""
        conditions.append(kanji_condition)

    statement = f"""SELECT DISTINCT "Kanji_ID", "Kanji", "Onyomi_ID", "Onyomi", "Order" FROM "Kanji_Onyomi_View" WHERE {' OR '.join(conditions)}
                    ORDER BY "Kanji_ID", "Order" """
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Kanji_ID"] = res[0]
        res_dict["Kanji"] = res[1]
        res_dict["Onyomi_ID"] = res[2]
        res_dict["Onyomi"] = res[3]
        res_dict["Order"] = res[4]
        result[i] = res_dict
    
    return result

def get_kanji_kunyomi(kanji_ids: List[int] = [], kanji: List[str] = []):
    if kanji_ids == [] and kanji == []:
        return []
    conditions = []

    if kanji_ids:
        kanji_id_condition = f""""Kanji_ID" IN ({', '.join(f"'{id}'" for id in kanji_ids)})"""
        conditions.append(kanji_id_condition)

    if kanji:
        kanji_condition = f""""Kanji" IN ({', '.join(f"'{kanji}'" for kanji in kanji)})"""
        conditions.append(kanji_condition)

    statement = f"""SELECT DISTINCT "Kanji_ID", "Kanji", "Kunyomi_ID", "Kunyomi", "Ending", "Order" FROM "Kanji_Kunyomi_View" WHERE {' OR '.join(conditions)}
                    ORDER BY "Kanji_ID", "Order" """
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Kanji_ID"] = res[0]
        res_dict["Kanji"] = res[1]
        res_dict["Kunyomi_ID"] = res[2]
        res_dict["Kunyomi"] = res[3]
        res_dict["Ending"] = res[4]
        res_dict["Order"] = res[5]
        result[i] = res_dict
    
    return result

def get_kanji_defintion(kanji_ids: List[int] = [], kanji: List[str] = [], definitions: List[str] = []):
    if kanji_ids == [] and kanji == [] and definitions == []:
        return []
    
    conditions = []

    if kanji_ids:
        kanji_id_condition = f""""Kanji_ID" IN ({', '.join(f"'{id}'" for id in kanji_ids)})"""
        conditions.append(kanji_id_condition)

    if kanji:
        kanji_condition = f""""Kanji" IN ({', '.join(f"'{kanji}'" for kanji in kanji)})"""
        conditions.append(kanji_condition)
    
    if definitions:
        definition_condition = f""""Definition" IN ({', '.join(f"'{definition}'" for definition in definitions)})"""
        conditions.append(definition_condition)

    statement = f"""SELECT DISTINCT "Kanji_ID", "Kanji", "Definition", "Order" FROM "Kanji_Definition_View" WHERE {' OR '.join(conditions)}
                    ORDER BY "Kanji_ID", "Order" """  
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Kanji_ID"] = res[0]
        res_dict["Kanji"] = res[1]
        res_dict["Definition"] = res[2]
        res_dict["Order"] = res[3]
        result[i] = res_dict
    
    return result

def get_anki_deck(deck_ids: List[int] = [], deck_names: List[str] = []):
    if deck_ids == [] and deck_names == []:
        return []
    
    conditions = []

    if deck_names:
        deck_name_condition = f""""Name" IN ({', '.join(f"'{name}'" for name in deck_names)})"""
        conditions.append(deck_name_condition)

    if deck_ids:
        deck_id_condition = f""""ID" IN ({', '.join(f"'{id}'" for id in deck_ids)})"""
        conditions.append(deck_id_condition)

    statement = f"""SELECT DISTINCT "ID", "Name" FROM "Anki_Deck" WHERE {' OR '.join(conditions)}
                    ORDER BY "ID" """  
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Deck_ID"] = res[0]
        res_dict["Deck_Name"] = res[1]
        result[i] = res_dict

    return result

def get_anki_fields(model_ids: List[int] = []):
    if not model_ids: return []

    conditions = []

    if model_ids:
        model_id_condition = f""""Model_ID" IN ({', '.join(f"'{id}'" for id in model_ids)})"""
        conditions.append(model_id_condition)

    statement = f"""SELECT DISTINCT "ID", "Name", "Model_ID", "Order" FROM "Anki_Fields" WHERE {' OR '.join(conditions)}
                    ORDER BY "Model_ID", "Order" """  
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["ID"] = res[0]
        res_dict["Name"] = res[1]
        res_dict["Model_ID"] = res[2]
        res_dict["Order"] = res[3]
        result[i] = res_dict

    return result

def get_anki_model_template(template_ids: List[int] = [], model_names: List[str] = [], model_ids: List[str] = []):
    if template_ids == [] and model_names == [] and model_ids == []:
        return []

    conditions = []

    if template_ids:
        template_id_condition = f""""Template_ID" IN ({', '.join(f"'{id}'" for id in template_ids)})"""
        conditions.append(template_id_condition)

    if model_names:
        model_name_condition = f""""Model_Name" IN ({', '.join(f"'{name}'" for name in model_names)})"""
        conditions.append(model_name_condition)

    if model_ids:
        model_id_condition = f""""Model_ID" IN ({', '.join(f"'{id}'" for id in model_ids)})"""
        conditions.append(model_id_condition)

    statement = f"""SELECT DISTINCT "Model_ID", "Model_Name", "Template_ID", "Template_Name", "Front", "Back", "Style", "Order" FROM "Model_Template_View" WHERE {' OR '.join(conditions)}
                    ORDER BY "Model_ID", "Order" """  
    
    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["Model_ID"] = res[0]
        res_dict["Model_Name"] = res[1]
        res_dict["Template_ID"] = res[2]
        res_dict["Template_Name"] = res[3]
        res_dict["Front"] = res[4]
        res_dict["Back"] = res[5]
        res_dict["Style"] = res[6]
        res_dict["Order"] = res[7]
        result[i] = res_dict

    return result

def get_anki_note(note_ids: List[int] = [], model_ids: List[int] = [], deck_ids: List[int] = [], sort_fields: List[str] = []):
    if not note_ids and not model_ids and not deck_ids and not sort_fields:
        return []

    conditions = []

    if note_ids:
        note_id_condition = f""""GUID" IN ({', '.join(f"'{id}'" for id in note_ids)})"""
        conditions.append(note_id_condition)
    
    if model_ids:
        model_id_condition = f""""Model_ID" IN ({', '.join(f"'{id}'" for id in model_ids)})"""
        conditions.append(model_id_condition)
    
    if deck_ids:
        deck_id_condition = f""""Deck_ID" IN ({', '.join(f"'{id}'" for id in deck_ids)})"""
        conditions.append(deck_id_condition)
    
    if sort_fields:
        sort_field_conditions = f""""Sort_Field" IN ({', '.join(f"'{field}'" for field in sort_fields)})"""
        conditions.append(sort_field_conditions)

    statement = f"""SELECT DISTINCT "GUID", "Model_ID", "Deck_ID", "Sort_Field" FROM "Anki_Note" WHERE {' AND '.join(conditions)}
                    ORDER BY "Deck_ID", "Model_ID", "Sort_Field" """ 

    cursor.execute(statement)
    result = cursor.fetchall()

    for i in range(len(result)):
        res = result[i]
        res_dict = {}
        res_dict["GUID"] = res[0]
        res_dict["Model_ID"] = res[1]
        res_dict["Deck_ID"] = res[2]
        res_dict["Sort_Field"] = res[3]
        result[i] = res_dict

    return result

def insert_anki_note(note_id: int, model_id: int, deck_id: int, sort_field: str):
    cursor.execute(f""" INSERT INTO "Anki_Note" ("GUID", "Model_ID", "Deck_ID", "Sort_Field")
                        VALUES ('{note_id}', '{model_id}', '{deck_id}', '{sort_field}') """)
        
def load_fields(cursor):
    cursor.execute("""DELETE FROM "Anki_Fields" """)
    fields = [
            {'name': 'Japanese'},{'name': 'Reading'},{'name': 'Meaning'},
            {'name': 'Sentence 1'},{'name': 'Sentence 2'},
            {'name': 'Kanji 1'},{'name': 'Kanji 1 Kunyomi'},{'name': 'Kanji 1 Onyomi'},{'name': 'Kanji 1 Meaning'},
            {'name': 'Kanji 2'},{'name': 'Kanji 2 Kunyomi'},{'name': 'Kanji 2 Onyomi'},{'name': 'Kanji 2 Meaning'},
            {'name': 'Kanji 3'},{'name': 'Kanji 3 Kunyomi'},{'name': 'Kanji 3 Onyomi'},{'name': 'Kanji 3 Meaning'},
            {'name': 'Kanji 4'},{'name': 'Kanji 4 Kunyomi'},{'name': 'Kanji 4 Onyomi'},{'name': 'Kanji 4 Meaning'},
            {'name': 'Kanji 5'},{'name': 'Kanji 5 Kunyomi'},{'name': 'Kanji 5 Onyomi'},{'name': 'Kanji 5 Meaning'}
        ]

    for i in range(len(fields)):
        cursor.execute(f"""
            INSERT INTO "Anki_Fields" ("ID", "Name", "Model_ID", "Order")
            VALUES ('{int(time.time())}', '{fields[i]['name']}', '{1723547904}', '{i+1}')
        """)
        time.sleep(2)
    