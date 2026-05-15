from pyparsing import ParseException
from grammar import kubectlCommand
from constants import k8s_all_verbs, k8s_api_resources


# TODO: early detencion
import difflib

def find_closest_word(input_word, vocabulary):
    matches = difflib.get_close_matches(input_word, vocabulary, n=1, cutoff=0.3)
    if matches:
        return matches[0]
    return None

def find_word_at_index(text, index):
    if index < 0 or index >= len(text):
        return ""
    start = text.rfind(' ', 0, index) + 1 
    end = text.find(' ', index) 
    if end == -1:  
        end = len(text)
    return text[start:end]

def find_closest_input(line, depth=0):
    if depth > 5:  # Prevent infinite recursion
        return line
    try:
        kubectlCommand.parse_string(line, parse_all=True)
        return line
    except ParseException as pe:
        wrong_word = find_word_at_index(line, pe.loc)
        if not wrong_word:
            return line
        if getattr(pe.parser_element, "name", None) == "verb":
            vocabulary = k8s_all_verbs
        elif getattr(pe.parser_element, "name", None) == "resource":
            vocabulary = k8s_api_resources
        else:
            return line

        closest_word = find_closest_word(wrong_word, vocabulary)
        if not closest_word or closest_word == wrong_word:
            return line

        # Replace only the specific occurrence
        start = line.rfind(' ', 0, pe.loc) + 1
        end = line.find(' ', pe.loc)
        if end == -1:
            end = len(line)
            
        new_line = line[:start] + closest_word + line[end:]

        return find_closest_input(new_line, depth + 1)
