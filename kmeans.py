#!/usr/bin/python

import random, math

class KMeans():

    def __init__(self, file):
        self.main(file, 5)

    def main(self, file, k):
        centroid_ids = self.getInitCentroids(file, k)
        coordinates = self.getCoordinatesById(file, centroid_ids)

    def getInitCentroids(self, file, k):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        randoms = [0] * k
        centroid_ids = [None] * k
        for line in myFile:
            currentMin = min(randoms)
            r = random.random()
            if r > currentMin:
                infos = line.split('\t')
                
                i = randoms.index(currentMin)
                randoms[i] = r
                centroid_ids[i] = infos[0]

        myFile.close()
        return centroid_ids

    def getCoordinatesById(self, file, centroid_ids):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        coordinates = {}
        for line in myFile:
            infos = line.split('\t')
            
            if infos[0] in centroids_ids:
                coords = {}
                for tup in infos[1].split('#'):
                    couple = tup.split(':')
                    coords.setdefault(couple[0], float(couple[1]))
                coordinates.setdefault(infos[0], coords)
                
        myFile.close()
        return coordinates

    def getDistance(self, center, doc):
        pointA, pointB = [], []
        keys = []
        s = 0.0

        key += center.keys()
        key += doc.keys()

        key = set(key)

        for k in key:
            if k in center.keys():
                pointA.append(center[k])
            else:
                pointA.append(0.0)

            if k in doc.keys():
                pointB.append(doc[k])
            else:
                pointB.append(0.0)

        for i in range(len(pointA)):
            s += pow((pointB[i] - pointA[i]), 2)

        return math.sqrt(s)

if __name__ == "__main__":
    KMeans(file)
