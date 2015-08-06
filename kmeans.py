#!/usr/bin/python

import random, math
import sys

class KMeans():

    def __init__(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        count = 0
        for line in myFile:
            count += 1
        myFile.close()

        self.main(file, int(math.sqrt(count/2)))

    def main(self, file, k):
        print "[*] Number of K picked : " + str(k)
        first = True
        
        centroid_ids = self.getInitCentroids(file, k)
        centroids = self.getCoordinatesById(file, centroid_ids)

        count = 0

        print "[*] Start main loop."
        while True:
            count += 1
            if not first:
                centroids = newCentroids.copy()
            first = False
            print "yolo"
            keysByCluster = self.getKeysByCluster(file, centroids)
            print "[*] Got posts by closest cluster."
            newCentroids = self.getNewCentroids(file, keysByCluster)
            print "[*] Got new positions of the centroids."
            if self.isSameCluster(centroids, newCentroids):
                break

        print "[+] Final clusters found in " + str(count) + " rounds."
        print "[*] Number of final clusters : " + str(len(keysByCluster.keys()))
        self.saveClusters("clusters.txt", keysByCluster)

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

    def getKeysByCluster(self, file, centroids):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        keysByCluster = {}

        for line in myFile:
            coords, first = {}, True

            infos = line.split('\t')

            for tup in infos[1].split('#'):
                couple = tup.split(':')
                coords.setdefault(couple[0], float(couple[1]))

            for key, val in centroids.items():
                dist = self.getDistance(val, coords)
                if first:
                    minDist = dist
                    first = False
                else:
                    if dist < minDist:
                        minDist = dist
                        minCentroid = key

            keysByCluster.setdefault(minCentroid, [])
            keysByCluster[minCentroid].append(infos[0])

        myFile.close()
        return keysByCluster

    def getNewCentroids(self, file, keysByCluster):
        clusters = {}

        for key, ids in keysByCluster.items():
            try:
                myFile = open(file, 'r')
            except:
                print "[-] Fail to open the file."
                return None

            listCoords = []
            for line in myFile:
                infos = line.split('\t')
                
                if infos[0] in ids:
                    coords = {}
                    for tup in infos[1].split('#'):
                        couple = tup.split(':')
                        coords.setdefault(couple[0], float(couple[1]))
                    listCoords.append(coords)
            myFile.close()
            clusters.setdefault(key, self.getAverage(listCoords))
            
        return clusters
                
    def getCoordinatesById(self, file, ids):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        coordinates = {}
        for line in myFile:
            infos = line.split('\t')
            
            if infos[0] in ids:
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

        keys += center.keys()
        keys += doc.keys()

        keys = set(keys)

        for k in keys:
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

    def getAverage(self, listCoords):
        keys, avr = [], {}

        for coords in listCoords:
            keys += coords.keys()

        keys = set(keys)

        for k in keys:
            s = 0.0
            for coords in listCoords:
                if k in coords.keys():
                    s += coords[k]
            avr.setdefault(k, float(s / len(listCoords)))

        return avr

    def isSameCluster(self, currentCentroids, newCentroids):
        for key in currentCentroids.keys():
            if key not in newCentroids.keys():
                return False
            if len(currentCentroids[key].keys()) != len(newCentroids[key].keys()):
                return False
            shared_items = set(currentCentroids[key].items()) & set(newCentroids[key].items())
            if len(shared_items) != len(currentCentroids[key].keys()):
                return False
        return True

    def saveClusters(self, file, keysByCluster):
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False

        for key, ids in keysByCluster.items():
            post_ids = " ".join(ids)
            myFile.write(post_ids)
            myFile.write('\n')
        myFile.close()
        
if __name__ == "__main__":
    KMeans("scored_posts.txt")
