import os

def getTextFiles(path):

    text_files = []

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join(root, file))

    return text_files
