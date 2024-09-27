import database
import genanki
import time

def create_anki_deck():
    deck_query_results = database.get_anki_deck(deck_ids=[1723547770])[0]

    anki_deck = genanki.Deck(
        deck_id = deck_query_results["Deck_ID"],
        name = deck_query_results["Deck_Name"]
    )

    model_template_query_results = database.get_anki_model_template(model_ids=[1723547904])
    model_fields_query_results = database.get_anki_fields(model_ids=[1723547904])

    model_dict = {}
    model_dict["Model_ID"] = model_template_query_results[0]["Model_ID"]
    model_dict["Model_Name"] = model_template_query_results[0]["Model_Name"]
    model_dict["Fields"] = []
    model_dict["Templates"] = []
    model_dict["Style"] = model_template_query_results[0]["Style"]
    for template in model_template_query_results:
        model_dict["Templates"].append({"name": template["Template_Name"], "qfmt": template["Front"], "afmt": template["Back"]})
    for field in model_fields_query_results:
        model_dict["Fields"].append({"name": field["Name"]})
    
    anki_model = genanki.Model(
        model_id = model_dict["Model_ID"],
        name = model_dict["Model_Name"],
        fields = model_dict["Fields"] ,
        templates = model_dict["Templates"] ,
        css = model_dict["Style"]
    )

    return anki_deck, anki_model

def html_list_of_meanings(term):
    meanings = term["Meanings"]
    if not meanings: return ""
    html_text = "<ol>"
    for meaning in meanings:
        if meaning["Definitions"]:
            html_text += "<li>"
            html_text += ", ".join(meaning["Definitions"][:5])
            html_text += "</li>"
    html_text += "</ol>"
    return html_text

def add_note(note, anki_deck, anki_model):
    qnotes = database.get_anki_note(sort_fields=[note.sort_field], deck_ids=[anki_deck.deck_id], model_ids=[anki_model.model_id])
    if qnotes:
        note.guid = qnotes[0]["GUID"]
    anki_deck.add_note(note)
    if qnotes == []:
        database.insert_anki_note(note_id=note.guid, model_id=anki_model.model_id, deck_id=anki_deck.deck_id, sort_field=note.sort_field)
    return anki_deck


def create_notes(anki_deck, anki_model, terms):
    for term in terms:
        fields = [term["Japanese"], term["Reading"], html_list_of_meanings(term)]
        fields += ["", ""] # example sentences
        
        for i in range(min(5, len(term["Kanji"]))):
            kanji = term["Kanji"][i]
            #TODO sort kunyomi
            kunyomi = [k["Kunyomi"] + "." + k["Ending"] if k["Ending"] else k["Kunyomi"] for k in kanji["Kunyomi"]]
            onyomi = [o["Onyomi"] for o in kanji["Onyomi"]]

            fields.append(kanji["Kanji"])
            fields.append("、".join(kunyomi))
            fields.append("、".join(onyomi))
            fields.append(", ".join(kanji["Definitions"][:5]))
        
        empty_fields = len(anki_model.fields) - len(fields)

        for i in range(empty_fields):
            fields.append("")

        note = genanki.Note(
            model = anki_model,
            fields = fields,
            tags = [],
            guid = int(time.time() * 1000.0)
        )
        time.sleep(0.001) # sleep to prevent clashing guids

        anki_deck = add_note(note, anki_deck, anki_model)

    return anki_deck

def write_to_file(deck, filename):
    genanki.Package(deck).write_to_file(filename)
