from instagram.client import InstagramAPI
import wikipedia
from textblob import TextBlob, Word
import sys

class InstaFood():

    def __init__(self):
        self.tagsToAvoid = ['like4like', 'likeforlike', 'instafollow', 'follow4follow', 'f4f', 'l4l', '20likes', 'instalike', 'instago', 'instadaily', 'dailygram', 'instagramhub', 'webstagram', 'tagsforlikes', 'tagsforlikesapp', 'followme', 'instagood', 'instacool', 'instagramers', 'picoftheday', 'photooftheday', 'pictureoftheday', 'bestoftheday', 'igers', 'tflers', 'instamood', 'follow', 'like', 'tbt', 'swag', 'iphoneonly', 'nofilter', 'tweegram']
        self.foodWords, self.locationWords = ['food', 'condiment', 'dish', 'cake', 'fruit', 'cuisine', 'meat'], ['country', 'region']
        self.foodTagsFile, self.noFoodTagsFile = 'relatedTags.txt', 'unrelatedTags.txt'
        self.instaBot()
        
    def instaBot(self):
        api = InstagramAPI(client_id='dced40dd759c4019838e1c654ad7ab08', client_secret='428421a5921c4af2ad0fcb5e4e744992')
        #tags, info = api.tag_search('food', 20)

        posts, next = api.tag_recent_media(tag_name='food', count=30)
        temp, max_tag = next.split('max_tag_id=')
        max_tag = str(max_tag)

        for post in posts:
            print post.id
            for tag in post.tags:
                tagName = TextBlob(tag.name)
                tagName = tagName.words[0].singularize()
                if len(tagName) >= 3 and tagName not in self.tagsToAvoid:
                    lang = tagName.detect_language()
                    print tagName, '->', lang
                    if lang != 'en':
                        tagName = tagName.translate(from_lang=lang, to='en')
                        print "Traduction: ", tagName

                    try:
                        definitions = Word(tagName).definitions
                    except:
                        print "[-] This tag doesn't match any definition."
                        self.updateTags(self.noFoodTagsFile, tagName)
                        continue
                        
                    print definitions
                    isRelated = self.isTagRelatedToFood(tag)
                    if isRelated:
                        print "Tag related to food."
                    elif isRelated == False:
                        print "Tag not related to food."
                    else: # isRelated == None
                        if self.isDefRelatedTo(definitions, self.foodWords):
                            self.updateTags(self.foodTagsFile, tagName)
                            print "Tag related to food."
                        else:
                            self.updateTags(self.noFoodTagsFile, tagName)
                            print "Tag not related to food."

                    if self.isDefRelatedTo(definitions, self.locationWords):
                        print "Location"
            print post.user
            try:
                print post.location
            except:
                print "No location"
            print post.created_time
            print post.images['standard_resolution'].url
            print '-------------------'

    def isRelatedToFood(self, tagName):
        try:
            page = wikipedia.WikipediaPage(title=tagName)
        except:
            return False

        count = 0

        for d in [page.categories, [page.summary], Word(tagName).definitions]:
            if self.isDefRelatedTo(d, self.foodWords):
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

        myFile.write(str(tag))
        myFile.write('\n')
        myFile.close()
        return True
    
if __name__ == "__main__":
    InstaFood()
