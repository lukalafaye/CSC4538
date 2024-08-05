import re
import json
import spacy
from collections import Counter
import math
import bisect
import numpy as np

class InvertedIndex:
    def __init__(self):
        self.sorted_docs = {} # key: term, value: sorted list of docs
        self.document_frequencies = {} # key: term, value: number of docs containing term 
        self.term_ids = {} # key: term; value: term id
        self.documents = [] # list of documents, doc id is index in list

    def clean(self, text):
        d = d.replace("\n", " ")
        d = d.replace("  ", " ")
        videotime = re.compile(r'watch now\nVIDEO\n(?P<minutes>\d+):(?P<seconds>\d+)')
        times = videotime.findall(d)
        updated = re.sub(videotime, "", d)
        sources = re.compile('((\w|-| )+\|)+(\w|-| )')
        src = sources.findall(d)
        updated = re.sub(sources, "", updated)
        return updated

    def normalize(self, text):
        text = self.clean(text)
        doc = nlp(text)
        words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return words

    def add_document(self, document):
        self.documents.append(doc)
        doc_id = len(self.documents)-1
        words = normalize(document)
        terms = set(words)
        
        for term in terms:
            if term not in self.sorted_docs.keys():
                self.sorted_docs[term] = [doc_id]
            else:
                bisect.insort(self.sorted_docs[term], doc_id)
            
            self.document_frequencies[term] += 1
            
            if term not in self.term_ids.values():
                self.term_ids[term] = len(self.term_ids)

    def save(self, filename):
        data = {
            "sorted_docs": dict(self.sorted_docs),
            "documentFrequencies": self.document_frequencies,
            "term_ids": self.term_ids,
            "documents": self.documents
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.sorted_docs = defaultdict(list, {k: v for k, v in data['sorted_docs'].items()})
            self.document_frequencies = defaultdict(int, data['documentFrequencies'])
            self.term_ids = data['term_ids']
            self.documents = data['documents']

    def merge_conjunction(self, l1, l2):
        docs_l1 = self.sorted_docs[l1]
        docs_l2 = self.sorted_docs[l2]

        if len(docs_l1) == 0:
            return docs_l2

        if len(docs_l2) == 0:
            return docs_l1

        i, j = 0, 0
        result = set()

        while i < len(docs_l1) and j < len(docs_l2):
            if docs_l1[i] == docs_l2[j]:
                result.add(docs_l1[i])
                i += 1
                j += 1
            elif docs_l1[i] < docs_l2[j]:
                i += 1
            else:
                j += 1

        return result
    
    def search_conjunction(self, words):
        if len(words) == 0:
            return []

        current = words[0]
        result = set()

        for word in words[1:]:
            result = result.intersection(self.merge_conjunction(current, word))
            current = word

        return result

    def get_cosine_similarity(self, u, v):
        return np.sum(np.dot(u, v)) / (np.linalg.norm(a) * np.linalg.norm(b))

    def get_bow(self, text, vocab, to_idx):
        bow = [0] * len(vocab)
        for word in text:
            if word in to_idx:
                bow[to_idx[word]] += 1
        return bow

    def get_tfidf(self, text, bow, idf):
        tfidf = [0] * len(bow)
        for idx, count in enumerate(bow):
            tfidf[idx] = count * idf[idx]
        return tfidf


inverted = InvertedIndex()

a = [0, 1]
b = [3, 4]
    
print(inverted.get_cosine_similarity(a, b))
