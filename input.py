"""
Fonctions auxiliaires pour le traitement des données
"""

import re, math


def linguistique_ligne(line, freq, common_words):
    """
    Traitement linguistique pour une ligne
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    token = 0
    for word in words:
        token += 1
        if word not in common_words:
            # maj frequence
            try:
                freq[word] += 1
            except KeyError:
                freq[word] = 1
    return token


def linguistique_author(line, freq, common_words):
    """
    Traitement linguistique pour une ligne d'auteur
    """
    author = line.split(',')[0].lower()
    try:
        freq[author] += 1
    except KeyError:
        freq[author] = 1
    return author


def linguistique_ligneCS276(line, freq, common_words, logT, logM, tokens):
    """
    Traitement linguistique pour une ligne
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    token = tokens
    for word in words:
        token += 1
        if word not in common_words:
            # maj frequence
            try:
                freq[word] += 1
            except KeyError:
                freq[word] = 1
            logT.append(math.log10(token))
            logM.append(math.log10(len(freq)))
    return token


def index_ligne(docID, line, index, wordDic, wordID, common_words):
    """
    Traitement d'une ligne pour la construction de l'index
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    for word in words:
        if word not in common_words:

            # maj words
            if word not in wordDic:
                wordDic[word] = wordID
                wordID += 1
        
            # maj indexß
            w_ID = wordDic[word]
            try:
                if docID in index[w_ID]:
                    index[w_ID][docID] += 1
                else:
                    index[w_ID][docID] = 1
            except KeyError:
                index[w_ID] = {docID:1}
    
    return wordID


def index_author(docID, line, index, wordDic, wordID, common_words):
    """
    Traitement d'une ligne d'auteur pour la construction de l'index
    """
    author = line.split(',')[0].lower()
    if author not in wordDic:
        wordDic[author] = wordID
        wordID += 1

        # maj indexß
    w_ID = wordDic[author]
    try:
        if docID in index[w_ID]:
            index[w_ID][docID] += 1
        else:
            index[w_ID][docID] = 1
    except KeyError:
        index[w_ID] = {docID: 1}

    return wordID


def vbe_index_ligne(docID, line, index, wordDic, wordID):
    """
    Traitement d'une ligne pour la construction de l'index avec la compression Variable Byte Encoding
    """
    words = list(filter(None, re.split(r'[^a-z0-9]', line.lower())))
    for word in words:
        # maj words
        if word not in wordDic:
            wordDic[word] = wordID
            wordID += 1
    
        # maj indexß
        w_ID = wordDic[word]
        try:
            index[w_ID].add(docID)
        except KeyError:
                index[w_ID] = {docID}
    
    return wordID


def parse_qrel(filename):
    parsed_qrel = dict()
    with open(filename, 'r') as f:
        for line in f:
            query, document, _, _ = (int(el) for el in line.split())
            parsed_qrel.setdefault(query, []).append(document)
    return parsed_qrel


def parse_queries(filename, common_words):
    queries = dict()
    reading = False
    with open(filename, "r") as f:
        for line in f:
            if line[0:2] == ".I":
                queryID = int(line.split(' ')[1])
                queries[queryID] = []
            if line[0:2] == ".W":
                reading = True
            elif line[0] == ".":
                reading = False
            elif reading:
                words = list(filter(None, re.split(r'[^a-z0-9/]', line.lower())))
                for word in words:
                    if word not in common_words:
                        queries[queryID].append(word)
    for queryID, query in queries.items():
        queries[queryID]= ' '.join(query)
    return queries

if __name__ == "__main__":
    qrel_real = parse_qrel('data/CACM/qrels.text')
    for k in qrel_real:
        print(k)

    """ --> All requests do not have an answer
    """