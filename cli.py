import sys
from colorama import Fore, Back, Style
import copy
import unicodedata
import re
from getkey import getkey, keys


def trim_text(text, trim):
    total_length = 0

    i = 0
    while i < len(text):
        if text[i] == "\x1b":
            if text[i:i+5] == Fore.GREEN:
                i += 4
            elif text[i:i+4] == Style.RESET_ALL:
                i += 3
        else:
            if total_length >= trim:
                break
            if unicodedata.east_asian_width(text[i]) in 'WF':
                total_length += 2
            else:
                total_length += 1

        i += 1
    if total_length >= trim:
        text = text[:i-3]+"..."
    else:
        text = text + (" " * (trim - total_length))
        
    return text + Style.RESET_ALL

def generate_search_result_display_text(search_result, selected):
    result_text_list = []

    selected

    for i in range(len(search_result)):
        terms_list = []
        definitions_list = []

        selected_terms = []
        selected_definitions = []
        for term in search_result[i]["Terms"]:

            if term["Japanese"] not in terms_list: 
                terms_list.append(term["Japanese"])
            if term["Reading"] not in terms_list and term["Reading"] != "": 
                terms_list.append(term["Reading"])
            
            for meaning in term["Meanings"]:
                [definitions_list.append(definition) for definition in meaning["Definitions"] if definition not in definitions_list]    

            if term["Term_ID"] in [sel["Term_ID"] for sel in selected]:
                
                selected_list = [sel for sel in selected if sel["Term_ID"] == term["Term_ID"]]
                for selected_term in selected_list:
                    selected_terms.append(terms_list.index(selected_term["Japanese"]))
                    if selected_term["Reading"]:
                        selected_terms.append(terms_list.index(selected_term["Reading"]))

                    for meaning in selected_term["Meanings"]:
                        for definition in meaning["Definitions"]:
                            selected_definitions.append(definitions_list.index(definition))
        
        selected_terms = list(set(selected_terms))
        selected_definitions = list(set(selected_definitions))

        for i in selected_terms:
            terms_list[i] = Fore.GREEN + terms_list[i] + Style.RESET_ALL

        for i in selected_definitions:
            definitions_list[i] = Fore.GREEN + definitions_list[i] + Style.RESET_ALL

        terms_text = ", ".join(terms_list)
        definitions_text = ", ".join(definitions_list)
        
        result_text = terms_text + " - " + definitions_text
        result_text = trim_text(result_text, 100) # consider this when colouring!!
        
        result_text_list.append(result_text)
    
    return result_text_list

def generate_search_result_display(result_text_list, pointed, display_bound):
    display_text_list = []
    for i in range(0, pointed):
        display_text_list.insert(i, "   " + result_text_list[i])

    display_text_list.insert(pointed, "-> " + result_text_list[pointed])

    for i in range(pointed + 1, len(result_text_list)):
        display_text_list.insert(i, "   " + result_text_list[i])
    
    for i in range(max(0, 10-len(display_text_list))):
        display_text_list.append((" " * 103))

    results_display = "\n".join(display_text_list[display_bound:display_bound + 10])
    return results_display


def select(selected, to_select):
    [selected.append(term) for term in to_select if term not in selected]
    return selected

def unselect(selected, to_unselect):
    [selected.remove(term) for term in to_unselect if term in selected]
    return selected
    
def interpret_input(input, pointed_word, search_result): # TODO
    if not input: return
    args = input.split(" -")
    func = None
    word_indices = []
    term_indices = []
    kana_term_indices = []

    terms = []

    if args[0] == "s":
        # default: 1st term selected from pointed word - japanese, kana and english
        func = select
        term_indices = [0]
        word_indices = [pointed_word]
    elif args[0] == "u":
        func = unselect
        term_indices = [0]
        word_indices = [pointed_word]
        
    
    if any(arg == "wa" for arg in args[1:]):
        # 1st term selected from all words
        word_indices = [range(len(search_result))]

    selected_term_indices = [int(arg[:1]) for arg in args if re.compile("^(t(\d)+)$").match(arg)]
    if selected_term_indices:
        term_indices = selected_term_indices

    if any(arg == "ta" for arg in args[1:]):
        # all terms selected from word/all words
        "ta" # SELECT ALL TERMS

    if any(arg == "k" for arg in args[1:]):
        kana_term_indices = term_indices

    if any(re.compile("^(k(\d)+)$").match(arg) for arg in args[1:]):
        # kana and english only taken from specific term from word/all words - kana & english only taken from 1st term selected if out of range
        "kn" # SELECT KANA ONLY FOR SPECIFIC TERM

    term_indices = [k for k in term_indices if k not in kana_term_indices]
    for i in word_indices:
        for j in kana_term_indices:
            term = copy.deepcopy(search_result[i]["Terms"][j])
            term["Japanese"], term["Reading"] = term["Reading"], ""
            terms.append(term)
        for j in term_indices:
            terms.append(search_result[i]["Terms"][j])
    
    return func, terms

def display_search_result(keyword, search_result, selected):
    pointed = 0
    result_text_list = []

    display_bound = 0

    result_text_list = generate_search_result_display_text(search_result, selected)
    
    pressed_key = "default"
    header_text = f"Results for \'{keyword}\'"
    header_padding = (94 - len(header_text)) // 2
    print("   " + "<- " + (" " * header_padding) + header_text + (" " * header_padding) + " ->")
    print("=" * 103)
    user_input = ""

    while pressed_key not in (keys.LEFT, keys.RIGHT):

        results_display = generate_search_result_display(result_text_list, pointed, display_bound)

        print(results_display)
        print("=" * 103)
        print(trim_text(user_input, 103), end="")
        sys.stdout.write(f'\x1b[{len(user_input)+1}G')
        sys.stdout.flush()
        pressed_key = getkey()

        if pressed_key == keys.UP:
            pointed = pointed - 1 if pointed > 1 else 0
            if pointed < display_bound:
                display_bound -= 1
        elif pressed_key == keys.DOWN:
            pointed = (pointed + 1) if (pointed < len(search_result) - 1) else (len(search_result) - 1)
            if pointed >= display_bound + 10:
                display_bound += 1
        elif pressed_key == keys.LEFT:
            sys.stdout.write("\033[F" * (11 + 2))
            sys.stdout.flush()
            return -1, selected
        elif pressed_key == keys.RIGHT:
            sys.stdout.write("\033[F" * (11 + 2))
            sys.stdout.flush()
            return 1, selected
        elif pressed_key == keys.ENTER: #TODO
            if user_input == "":
                return 0, selected
            
            func, terms = interpret_input(user_input, pointed, search_result)
            selected = func(selected, terms)
            result_text_list = generate_search_result_display_text(search_result, selected)
            user_input = ""

        elif pressed_key == keys.BACKSPACE:
            if user_input != "":
                user_input = user_input[:-1]
        else: user_input += pressed_key
        
        sys.stdout.write("\033[F" * 11)
        sys.stdout.flush()
    
    return 0, selected

def main(search_keywords, search_results, selected):
    displayed = 0
    while displayed >= 0 and displayed < len(search_keywords):
        keyword = search_keywords[displayed]
        n, selected[keyword] = display_search_result(keyword=keyword, search_result=search_results[keyword], selected=selected[keyword])    
        if n == 0:
            break
        if displayed + n < 0:
            displayed = len(search_keywords) - 1
        elif displayed + n >= len(search_keywords):
            displayed = 0
        else:
            displayed += n
    
    return selected