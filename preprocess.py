#!/usr/bin/python

import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob, Word

class PreProcess():

    def __init__(self, file):
        self.foodTagsFile = 'tags/relatedToFood.txt'
        self.stemmer = SnowballStemmer("english")
        self.stop_words = set(stopwords.words('english'))

        self.main(file)

    def main(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        self.foodWords, self.posTag = ['food', 'foodie', 'cuisine'], ['NN', 'NNP']

        for line in myFile:
            summary, first = "", True
            infos = line.split('\t')
            toKeep = False
            for tag in infos[1].split('#'):
                isShort = False
                tag = self.getEngTag(tag)
                if self.isFoodTag(tag):
                    tag = TextBlob(tag)
                    try:
                        tag = tag.words
                    except:
                        continue
                    if len(tag) == 1:
                        tag = TextBlob(tag[0].singularize())
                        isShort = True
                    else:
                        tag = " ".join(tag)
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
                            tag = TextBlob(tag)
                            wiki = self.getSummary(tag)
                            if wiki != None:
                                toKeep = True
                                if not first:
                                    summary += " "
                                first = False
                                summary += wiki
                            
            if toKeep:
                self.savePost("preproceed_posts.txt", infos[0], summary)

        myFile.close()

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

    def savePost(self, file, post_id, summary):
        try:
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False
        
        first = True
        myFile.write(str(post_id))
        myFile.write('\t')
        myFile.write(summary.encode('utf-8'))
        myFile.write("\n")
            
        myFile.close()
        return True

if __name__ == "__main__":
    PreProcess("posts.txt")
