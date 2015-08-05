#!/usr/bin/python

import math, wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob, Word

class TFIDF():

    def __init__(self, file):
        self.foodTagsFile = 'tags/relatedToFood.txt'
        self.stemmer = SnowballStemmer("english")
        self.stop_words = set(stopwords.words('english'))

        self.calculatedScore(file)

    def calculatedScore(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        
        self.foodWords, self.posTag = ['food', 'foodie', 'cuisine'], ['NN', 'NNP']
        self.invertedIndex = {}
        count = 0

        try:

            for line in myFile:
                summary, first = "", True
                infos = line.split('\t')
                toKeep = False
                for tag in infos[1].split('#'):
                    isShort = False
                    tag = self.getEngTag(tag)
                    if self.isFoodTag(tag):
                        tag = TextBlob(tag)
                        tag = tag.words
                        if len(tag) == 1:
                            tag = TextBlob(tag[0].singularize())
                            isShort = True
                        if tag not in self.foodWords:
                            if isShort:
                                if tag.tags[0][1] in self.posTag:
                                    wiki = self.getSummary(tag)
                                    if wiki != None:
                                        toKeep = True
                                        if not first:
                                            summary += " "
                                        first = False
                                        summary += wiki
                            else:
                                tag = " ".join(tag)
                                tag = TextBlob(tag)
                                wiki = self.getSummary(tag)
                                if wiki != None:
                                    toKeep = True
                                    if not first:
                                        summary += " "
                                    first = False
                                    summary += wiki
                                
                if toKeep:
                    self.getInvertedIndex(infos[0], self.getTermFrequence(TextBlob(summary)))
                    count += 1

            tfidf = self.getTFIDF(count, self.invertedIndex)
            self.saveTFIDF("tfidf.txt", tfidf)
        except:
            print "[-] Fail"

    def getEngTag(self, tag):
        tagName = TextBlob(tag.decode('utf-8'))
        tagName = tagName.words[0].singularize()
        
        if len(tagName) >= 3:
            lang = tagName.detect_language()

            if lang != 'en':
                tagName = tagName.translate(from_lang=lang, to='en')

        return tagName.encode('utf-8')     
                
    def isFoodTag(self, tag):
        try:
            myFile = open(self.foodTagsFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        for line in myFile:
            if line.strip() == tag:
                myFile.close()
                return True
        myFile.close()
        return False


    def getSummary(self, tag):
        try:
            summary = wikipedia.summary(str(tag))
        except:
            try:
                definitions = Word(tag).definitions
                summary = " ".join(definitions)
            except:                   
                print "[-] Fail to retrieve the summary of the tag : " + str(tag)
                return None

        text = TextBlob(summary)
        filtered_words = [self.stemmer.stem(w) for w in text.words.lower() if not w in self.stop_words]

        summary = " ".join(filtered_words)

        return summary

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
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False
        
        for key, val in tfidf.items():
            first = True
            myFile.write(str(key))
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
    TFIDF("posts.txt")
