import re

def getSentences(content):
    #Split content by sentence-ending punctuation: . ! ? ; : followed by space
    return re.split(r"[.!?;:\s]\s", content)


def getWords(sentence):
    #Return list of all strings containing a-Z characters including - and '
    return re.findall(r"\b[a-zA-Z]+(?:\-[a-zA-Z']+)?", sentence)
