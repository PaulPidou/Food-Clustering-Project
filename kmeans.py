#!/usr/bin/python

import numpy, scipy

class KMeans():

    def __init__(self, file):
        self.main(file, 5)

    def main(self, file, k):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False


    def getInitCentroids(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        for line in myFile:

        

if __name__ == "__main__":
    KMeans(file)
