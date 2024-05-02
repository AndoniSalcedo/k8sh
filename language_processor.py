from pyparsing import ParseException
from grammar import kubectlCommand
from constants import k8s_all_verbs, k8s_api_resources


# TODO: early detencion
def wagner_fischer(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost,
            )
    return dp[m][n]


def find_closest_word(input_word, vocabulary):
    min_distance = float("inf")
    closest_word = None

    for word in vocabulary:
        if input_word == word:
            return word, 0
        distance = wagner_fischer(input_word, word)
        if distance < min_distance:
            min_distance = distance
            closest_word = word

    return closest_word

def find_word_at_index(text, index):
    if index < 0 or index >= len(text):
        return ""
    start = text.rfind(' ', 0, index) + 1 
    end = text.find(' ', index) 
    if end == -1:  
        end = len(text)
    return text[start:end]

def find_closest_input(line):
    try:
        kubectlCommand.parseString(line, parseAll=True)
        return line
    except ParseException as pe:
        wrong_word = find_word_at_index(line, pe.col)
        if not wrong_word:
            return line
        if "verb" == str(pe.parserElement):
            vocabulary = k8s_all_verbs
        elif "resource" == str(pe.parserElement):
            vocabulary = k8s_api_resources
        else:
            return line

        closest_word = find_closest_word(wrong_word, vocabulary)
        new_line = pe.pstr.replace(wrong_word, closest_word)

        return find_closest_input(new_line)
