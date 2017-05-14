import pickle
import sys
import re

def processQuery(index, query):
    pLists = []
    for word in query:
        pLists.append(index.get(word, []))

    pLists = sorted(pLists, key=len)
    res = pLists.pop(0)
    while len(pLists) > 0:
        l1 = res
        l2 = pLists.pop(0)
        res = []
        x = y = 0
        while x < len(l1) and y < len(l2):
            (d1, p1) = l1[x]
            (d2, p2) = l2[y]
            if d1 > d2:
                y += 1
            elif d1 < d2:
                x += 1
            elif p1 > p2:
                y += 1
            elif p1 < p2:
                x += 1
            else:
                res.append((d1, p1))
                x += 1
                y += 1
    return res

def procesarNoticia(texto):
    texto = "".join([c if c.isalpha() else " " for c in texto])
    return [w.lower() for w in re.split(delimiter_word, texto)]

def snippet(text, wordlist):
    words = procesarNoticia(text);
    #words = re.split(delimiter_word,text)
    snippet = ""
    for i in range(0,len(words)):
        word = words[i]
        if word in wordlist:
            snippet = snippet + "..."
            for j in range(max(0,i-3),min(len(words),i+4)):
                snippet = snippet + words[j] + " "
            snippet = snippet + "...\n"
    return snippet

# Process arguments
if len(sys.argv) != 2:
    print("Usage: python SAR_searcher.py index_file")
    exit(-1)
index_file = sys.argv[1]

# Retrieve data from file
with open(index_file, "rb") as f:
    (index, docIndex) = pickle.load(f)


delimiter_noticia = re.compile("<DOC>")
delimiter_text = re.compile("</?TEXT>")
delimiter_title = re.compile("</?TITLE>")
delimiter_word = re.compile("[\n\t ]")

# Infinite query loop (end with '')
print("TIP: you can write !! to insert your previous query")
prev = ""
query = input("Your query > ")
while query != '':
    query = query.replace("!!", prev)
    prev = query
    wordlist = query.lower().split()
    res = processQuery(index, wordlist)
    dant = -1

    cont = 0
    for (d,p) in res:
        if(cont>9):
            continue
        if dant != d:
            data = open(docIndex.get(d)).read()
            dant = d
        news_list = re.split(delimiter_noticia, data)
        new = news_list[p+1]
        title = re.split(delimiter_title,new)
        if len (title)>1:
            print(title[1])
        if len(res)<3:
            text = re.split(delimiter_text,new)
            if len (title)>1:
                print(text[1])
        elif len(res)<6:
            text = re.split(delimiter_text,new)
            print(snippet(text[1], wordlist))
        cont+=1

    query = input("Your query > ")

print("The program will now end.")
