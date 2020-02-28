from fileUtils import getTextFiles
from textUtils import getSentences, getWords
from itertools import combinations
import matplotlib.pyplot as plt
import os
import networkx as nx

def main():

    MAX_FILE_SIZE_GB = 5
    CORPUS_PATH = "OANC-GrAF"

    #Initialize language graph and directory to save it to
    G = nx.MultiGraph([])

    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    graph_file_path = "graphs/%s_language_graph.gml" % CORPUS_PATH
    nx.write_gml(G, graph_file_path)

    #Get .txt file paths recursively from corpora folder
    text_files = getTextFiles(CORPUS_PATH)
    num_files = len(text_files)

    #Plot word acquisition along the way
    num_words = []

    #Iterate through text files
    for i, file in enumerate(text_files, start=1):

        print("Scanning %d of %d files: %s" % (i, num_files, os.path.basename(file)))

        #Open file, if error thrown, continue to next file
        try:
            text = open(file).read()
        except:
            continue


        for s in getSentences(text):

            words = [w.lower() for w in getWords(s)]

            #Update base word counts
            for w in words:

                #If new word, intialize in graph
                if (w not in G.nodes):
                    G.add_node(w)
                    G.nodes[w]["count"] = 1
                #Otherwise, update counts for all of the words
                else:
                    G.nodes[w]["count"] += 1

            #Iterate through all combinations of words in sentence
            for w1, w2 in combinations(words, 2):

                #Get current count
                edge_data = G.get_edge_data(w1, w2, key="co-occurance")

                #If none, initialize the count
                if(edge_data == None):
                    G.add_edge(w1, w2, key="co-occurance", count=1)
                #Otherwise, update all counts
                else:
                    prev_count = edge_data["count"]
                    G.add_edge(w1, w2, key="co-occurance", count=prev_count + 1)

        #Save language graph file and check for maximum file size
        if (os.path.getsize(graph_file_path) > MAX_FILE_SIZE_GB*1000000000):
            print("Saving and quitting: Maximum file size reached.")
            break

        #Every once in a while, save graph and display word acquisition trend
        num_words.append(len(G.nodes))
        if (i % 250 == 0):
            #Save graph
            print("Saving graph...")
            nx.write_gml(G, graph_file_path)
            print("Current file size:", os.path.getsize(graph_file_path)/1000000000, "GB")

            #Plot word count
            plt.title("Word Acquisition")
            plt.xlabel("Files Scanned")
            plt.ylabel("Words in Graph")
            plt.xlim(0, i)
            plt.ylim(0,len(G.nodes))
            plt.plot(range(i), num_words)
            plt.show()

    #Save and exit
    nx.write_gml(G, graph_file_path)

    return 0

if __name__ == "__main__":
    main()
