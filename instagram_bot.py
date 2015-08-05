#!/usr/bin/python

from instagram.client import InstagramAPI
import wikipedia
from textblob import TextBlob, Word
import time, sys
import operator

class InstaFood():

    def __init__(self):
        self.foodWords, self.locationWords = ['food', 'condiment', 'dish', 'cake', 'fruit', 'cuisine', 'meat'], ['country', 'region']
        self.foodTagsFile, self.noFoodTagsFile = 'tags/relatedToFood.txt', 'tags/unrelatedToFood.txt'
        self.instaBot()
        
    def instaBot(self):
        api = InstagramAPI(client_id='dced40dd759c4019838e1c654ad7ab08', client_secret='428421a5921c4af2ad0fcb5e4e744992')
        
        posts, next = api.tag_recent_media(tag_name='food', count=30)
        temp, max_tag = next.split('max_tag_id=')
        max_tag = str(max_tag)

        while True:
            print "[*] " + str(len(posts)) + " posts retrieved."
            for post in posts:
                if self.isNewPost("log/posts.log", post.id):
                    count = 0
                    langs = {}
                    print post.id
                    
                    for tag in post.tags:                       
                        tagName = TextBlob(tag.name)
                        tagName = tagName.words[0].singularize()
                        
                        if len(tagName) >= 3 and tagName != 'food':
                            lang = tagName.detect_language()
                            print tagName, '->', lang
                            langs.setdefault(lang, 0)
                            langs[lang] += 1
                            
                            if lang != 'en':
                                tagName = tagName.translate(from_lang=lang, to='en')
                                print "Traduction: ", tagName

                            tagRelatedToFood = self.isTagRelatedToFood(tagName)
                            if tagRelatedToFood:
                                count += 1
                                print "[+] Tag related to food."
                            elif tagRelatedToFood == False:
                                print "[-] Tag not related to food."
                            else: # tagRelatedToFood == None
                                if self.isRelatedTo(tagName, self.foodWords):
                                    count += 1
                                    self.updateTags(self.foodTagsFile, tagName)
                                    self.writeTagLog("log/newTags.log", tag, True)
                                    print "[+] Tag related to food."
                                else:
                                    self.updateTags(self.noFoodTagsFile, tagName)
                                    self.writeTagLog("log/newTags.log", tag, False)
                                    print "[-] Tag not related to food."
                    if count > 0:
                        self.savePost("posts.txt", post)
                        self.writePostLog("log/posts.log", post, langs, True)
                        print "[+] Post saved."
                    else:
                        self.writePostLog("log/posts.log", post, langs, False)
                        print "[-] Post forget."
                    print '-------------------'
                
            posts, next = api.tag_recent_media(tag_name='food', max_tag_id=max_tag)
            temp, max_tag = next.split('max_tag_id=')
            max_tag = str(max_tag)

            if not next:
                break

    def isRelatedTo(self, tagName, wordsList):
        try:
            page = wikipedia.WikipediaPage(title=tagName)
            definitions = Word(tagName).definitions
        except:
            return False

        count = 0

        for d in [page.categories, [page.summary], definitions]:
            if self.isDefRelatedTo(d, wordsList):
                count += 1

        if count > 1:
            return True
        else:
            return False        

    def isDefRelatedTo(self, definitions, wordsList):
        for definition in definitions:
            d = TextBlob(definition)
            for word in d.words:
                if word.lower() in wordsList:
                    return True
        return False

    def isTagRelatedToFood(self, tag):
        try:
            myFile = open(self.foodTagsFile, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        for line in myFile:
            if line.strip() == tag:
                myFile.close()
                return True
        myFile.close()

        try:
            myFile = open(self.noFoodTagsFile, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        for line in myFile:
            if line.strip() == tag:
                myFile.close()
                return False
        myFile.close()
        return None
            
    def updateTags(self, file, tag):
        try:
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False

        try:
            myFile.write(str(tag))
        except:
            myFile.write(tag.encode('utf-8'))
        myFile.write('\n')
        myFile.close()
        return True

    def isNewPost(self, file, post_id):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return True

        for line in myFile:
            column = line.split('\t')
            if column[2] == str(post_id):
                myFile.close()
                return False
        myFile.close()
        return True

    def savePost(self, file, post):
        try:
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False

        first = True

        myFile.write(str(post.id))
        myFile.write('\t')
        for tag in post.tags:
            if not first:
                myFile.write('#')
            first = False
            try:
                myFile.write(str(tag.name))
            except:
                myFile.write(tag.name.encode('utf-8'))
        myFile.write('\t')
        myFile.write(str(post.user))
        myFile.write('\t')
        try:
            myFile.write(str(post.location))
        except:
            myFile.write("None")
        myFile.write('\t')
        myFile.write(str(post.created_time))
        myFile.write('\t')
        myFile.write(str(post.images['standard_resolution'].url))
        myFile.write('\n')
        myFile.close()
        return True

    def writeTagLog(self, file, tag, related):
        try:
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False

        myFile.write(str(time.time()))
        myFile.write('\t')
        if related:
            myFile.write("[+] ")
        else:
            myFile.write("[-] ")
        try:
            myFile.write(str(tag))
        except:
            myFile.write(tag.encode('utf-8'))
        myFile.write('\n')
        myFile.close()
        return True

    def writePostLog(self, file, post, langs, related):
        try:
            myFile = open(file, 'a')
        except:
            print "[-] Fail to open the file."
            return False

        first = True
        myFile.write(str(time.time()))
        myFile.write('\t')
        if related:
            myFile.write("[+]\t")
        else:
            myFile.write("[-]\t")
        myFile.write(str(post.id))
        myFile.write('\t')

        sorted_lang = sorted(langs.items(), key=operator.itemgetter(1))
        sorted_lang.reverse()

        for lang, val in sorted_lang:
            if not first:
                myFile.write("@")
            first = False
            myFile.write(str(lang) + ":" + str(val))
        myFile.write('\t')
        myFile.write(str(post.images['standard_resolution'].url))
        myFile.write('\n')
        myFile.close()
        return True
        
    
if __name__ == "__main__":
    InstaFood()
