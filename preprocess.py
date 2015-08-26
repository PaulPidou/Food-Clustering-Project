#!/usr/bin/python

import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob, Word
import argparse, sys, os

class PreProcess():
    def __init__(self, postsFile, preproceed_postsFile):
        print "[*] Preprocess module starting"
        
        if not os.path.exists('./files'):
            os.makedirs('./files')

        try:
            myFile = open(preproceed_postsFile, 'w')
        except:
            print "[-] Fail to create the file."
            sys.exit(0)
        myFile.close()
                
        self.foodTagsFile = 'tags/relatedToFood.txt'
        self.stemmer = SnowballStemmer("english")
        self.stop_words = set(stopwords.words('english'))

        self.main(postsFile, preproceed_postsFile)

    def main(self, postsFile, preproceed_postsFile):
        "Pre-process the posts file"
        try:
            myFile = open(postsFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        self.foodWords, self.posTag = ['food', 'foodie', 'cuisine'], ['NN', 'NNP']

        for line in myFile:
            summary, first = "", True
            infos = line.split('\t')

            if not self.checkIfNew(preproceed_postsFile, infos[0]):
                print "[*] Already treated this entry."
                continue
            
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
                self.savePost(preproceed_postsFile, infos[0], summary)

        myFile.close()

    def getEngTag(self, tag):
        "Get the tag in English"
        tagName = TextBlob(tag.decode('utf-8'))
        tagName = tagName.words[0].singularize()
        
        if len(tagName) >= 3:
            lang = tagName.detect_language()

            if lang != 'en':
                tagName = tagName.translate(from_lang=lang, to='en')

        return tagName.encode('utf-8')     
                
    def isFoodTag(self, tag):
        "Check if the tag is related to food"
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
        "Get the summary related to a given tag"
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
        "Save the pre-processed posts"
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

    def checkIfNew(self, file, id_post):
        "Check if a given post has been already treated"
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        for line in myFile:
            infos = line.split('\t')

            if infos[0] == id_post:
                myFile.close()
                return False

        myFile.close()
        return True

if __name__ == "__main__":
    directory, postsFile, preproceed_postsFile = "./files/", "posts.txt", "preproceed_posts.txt"

    parser = argparse.ArgumentParser(description='Food clustering project - Preprocess module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-pf', action="store", dest="postsFile", help="Source posts file. By default: posts.txt", nargs=1) 
    parser.add_argument('-ppf', action="store", dest="preprocessFile", help="File to save the preprocess posts. By default: preproceed_posts.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.postsFile != None:
        postsFile = args.postsFile[0]
    if args.preprocessFile != None:
        preproceed_postsFile = args.preprocessFile[0]
        
    PreProcess(directory + postsFile, directory + preproceed_postsFile)
