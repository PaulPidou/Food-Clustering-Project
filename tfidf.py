#!/usr/bin/python

import math
from textblob import TextBlob, Word
import numpy as np

class TFIDF():

    def __init__(self, file):
        self.calculatedScore(file)

    def calculatedScore(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        self.invertedIndex = {}
        count = 0

        for line in myFile:
            infos = line.split('\t')
            self.getInvertedIndex(infos[0], self.getTermFrequence(TextBlob(infos[1].decode('utf-8'))))
            count += 1

        myFile.close()

        tfidf = self.getTFIDF(count, self.invertedIndex)
        self.saveTFIDF("tfidf.txt", tfidf)

    def getTermFrequence(self, summary):
        termFreq = {}
        for word in summary.words:
            termFreq.setdefault(word, summary.word_counts[word])

        return termFreq

    def getInvertedIndex(self, post_id, termFreq):
        for key, val in termFreq.items():
            self.invertedIndex.setdefault(key, [])
            self.invertedIndex[key].append((post_id, val))

    def getTFIDF(self, count, invertedIndex):
        tfidf = {}
        for key, val in invertedIndex.items():
            tfidf.setdefault(key, [])
            for tup in val:
                score = float(tup[1] * math.log(float(count) / len(val)))
                tfidf[key].append((tup[0], score))

        return tfidf

    def saveTFIDF(self, file, tfidf):
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False
        
        for key, val in tfidf.items():
            first = True
            myFile.write(key.encode('utf-8'))
            myFile.write('\t')
            for tup in val:
                if not first:
                    myFile.write("#")
                first = False
                myFile.write(str(tup[0]))
                myFile.write(":")
                myFile.write(str(tup[1]))
            myFile.write("\n")
            
        myFile.close()
        return True

if __name__ == "__main__":
    TFIDF("copy.txt")
