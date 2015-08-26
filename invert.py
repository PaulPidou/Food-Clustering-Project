#!/usr/bin/python

import argparse, sys, os

class Invert():
    def __init__(self, tfidfFile, scorePostsFile):
        print "[*] Invert index module starting"
        
        if not os.path.exists('./files'):
            os.makedirs('./files')
                
        self.invert(tfidfFile, scorePostsFile)

    def invert(self, tfidfFile, scorePostsFile):
        "Invert the given TF-IDF file"
        try:
            myFile = open(tfidfFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        invertedIndex = {}
        for line in myFile:
            infos = line.split('\t')
            for tup in infos[1].split('#'):
                couple = tup.split(':')
                invertedIndex.setdefault(couple[0], [])
                invertedIndex[couple[0]].append((infos[0], couple[1]))
        myFile.close()

        normIndex = {}
        for key, val in invertedIndex.items():
            values = []
            for tup in val:
                values.append(float(tup[1]))
            normValues = self.normalizeL2(values)

            normIndex.setdefault(key, [])
            for i in range(len(val)):
                normIndex[key].append((val[i][0], normValues[i]))

        self.saveInvert(scorePostsFile, normIndex)
        return True


    def normalizeL2(self, values):
        "Apply a l2 normalization on the given array"
        l2norm, normValues = 0, []

        for val in values:
            l2norm += val * val

        if l2norm == 0:
            normValues = 1 * len(values)
        else:
            for val in values:
                normValues.append(float(val / l2norm))

        return normValues

    def saveInvert(self, file, index):
        "Save the inverted file"
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False
        
        for key, val in index.items():
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
    directory, tfidfFile, scoredPostsFile = "./files/", "tfidf.txt", "scored_posts.txt"

    parser = argparse.ArgumentParser(description='Food clustering project - Invert index module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-tf', action="store", dest="tfidfFile", help="Source TFIDF file. By default: tfidf.txt", nargs=1)
    parser.add_argument('-spf', action="store", dest="scoredPostsFile", help="File to save the scored posts. By default: scored_posts.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.tfidfFile != None:
        tfidfFile = args.tfidfFile[0]
    if args.scoredPostsFile != None:
        scoredPostsFile = args.scoredPostsFile[0]
        
    Invert(directory + tfidfFile, directory + scoredPostsFile)
