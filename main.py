import cli
import anki
import database
import genanki

def search_database(search_keywords):
    incomplete = False
    search_results = {}
    for search_keyword in search_keywords:
        search_result = database.search_word(keyword=search_keyword)
        if not incomplete and search_result == []:
            all_have_results = True
        search_results[search_keyword] = search_result
    
    return search_results, incomplete

def input_search():
    print("Search for words:")
    search_keywords = []
    search_keyword = input("")
    while search_keyword != "":
        search_keywords.append(search_keyword.strip())
        search_keyword = input("")
    
    return search_keywords

def sort_results(search_result, keyword):
    sorted_result = []
    meaning_dict = {}
    for word in search_result:
        terms = word["Terms"]
        meanings = []
        meaning_ids = []
        for term in terms:
            if term["Japanese"] == keyword or term["Reading"] == keyword:
                return search_result
            for meaning in term["Meanings"]:
                if meaning["Meaning_ID"] not in meaning_ids: 
                    meanings.append(meaning["Definitions"])
                    meaning_ids.append(meaning["Meaning_ID"])
        meaning_dict[word["Word_ID"]] = meanings

    pointer = 0
    while search_result != []:
        to_remove = []
        for i in range(len(search_result)):
            result = search_result[i]
            meanings = meaning_dict[result["Word_ID"]]
            meanings = [meaning for meaning in meanings if len(meaning) > pointer]
            if any([keyword in meaning[pointer] for meaning in meanings]):
                sorted_result.append(result)
                to_remove.append(i)
                search_result
        pointer += 1
        dec = 0
        for i in to_remove:
            i -= dec
            search_result.pop(i)
            dec += 1
        search_result
        to_remove = []
    
    total_popularity = 0
    for res in sorted_result:
        total_popularity += res["Popularity"]
    
    mean_popularity = total_popularity // len(sorted_result)
    first_half = []
    second_half = []

    for res in sorted_result:
        if res["Popularity"] >= mean_popularity:
            first_half.append(res)
        else:
            second_half.append(res)
    
    sorted_result = first_half + second_half
    return sorted_result
            
def auto_select(search_result, keyword):
    selected = None
    for i in range(len(search_result)):
        word = search_result[i]
        for j in range(len(word["Terms"])):
            term = word["Terms"][j]
            if term["Reading"] == keyword:
                return [search_result[i]["Terms"][j]]
            if term["Japanese"] == keyword:
                return [search_result[i]["Terms"][j]]
    
    return [search_result[0]["Terms"][0]]

def main():
    search_keywords = list(set(input_search()))
    search_results, incomplete = search_database(search_keywords)
    assert search_keywords == list(search_results.keys())

    selected = {}
    for keyword in search_keywords:
        search_results[keyword] = sort_results(search_results[keyword], keyword)
        selected[keyword] = [(auto_select(search_results[keyword], keyword))]


    selected = cli.main(search_keywords, search_results, selected)

    selected_list = []
    for key in selected.keys():
        selected_list += selected[key]
    
    anki_deck, anki_model = anki.create_anki_deck()

    anki_deck = anki.create_notes(anki_deck, anki_model, selected_list)
    genanki.Package(anki_deck).write_to_file("japanki.apkg")
    # conn.commit()

    
    
if __name__ == '__main__':
    main()