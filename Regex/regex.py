import re
import json

file = "all_articles.json"

with open(file) as f:
    data = json.load(f)

minutes = 0
seconds = 0
n=0

wc, cc, vc = 0, 0, 0

newdata = []


import spacy
nlp = spacy.load('en_core_web_sm')

for d in data:
    d = d.replace("\n", " ")
    d = d.replace("  ", " ")

    dates = re.compile(r'\d\d\/\d\d\/\d\d\d\d') # Les dates
# <re.Match object; span=(2, 9), match='dd/mm/yyyy'>

    videotime = re.compile(r'watch now\nVIDEO\n(?P<minutes>\d+):(?P<seconds>\d+)')
    
    times = videotime.findall(d)
    updated = re.sub(videotime, "", d)
        
    for couple in times:
        minutes += float(couple[0])
        seconds += float(couple[1])

    sources = re.compile('((\w|-| )+\|)+(\w|-| )')
    src = sources.findall(d)
    updated = re.sub(sources, "", updated)

    newdata += updated
    doc = nlp(updated)

    words = [token.text for token in doc]
    verbs = [token.text for token in doc if token.pos_=="VERB"]
    vc += len(verbs)
    wc += len(words)
    cc += len(updated)
    
    avg = (minutes*60 + seconds) / n
print(avg)

avgw = wc/n
avgc = cc/n
avgv = vc/n

print(avgw, avgc, avgv)
