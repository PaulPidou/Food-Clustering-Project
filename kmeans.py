#!/usr/bin/python

import random, math
import operator
import argparse, sys, os

class KMeans():
    def __init__(self, scoredPostsFile, clustersFile, wordClustersFile, distFile):
        print "[*] K-Means module starting"
        
        if not os.path.exists('./files'):
            os.makedirs('./files')
            
        try:
            myFile = open(scoredPostsFile, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        count = 0
        for line in myFile:
            count += 1
        myFile.close()

        self.main(scoredPostsFile, clustersFile, int(math.sqrt(count/2)))
        self.wordByCluster(scoredPostsFile, clustersFile, wordClustersFile)
        self.saveDistanceBetweenCluster(wordClustersFile, distFile)

    def main(self, scoredPostsFile, clustersFile, k):
        "Apply the main process of the K-Means algorithm"
        print "[*] Number of K picked : " + str(k)
        first = True
        
        centroid_ids = self.getInitCentroids(scoredPostsFile, k)
        centroids = self.getCoordinatesById(scoredPostsFile, centroid_ids)

        count = 0

        print "[*] Start main loop."
        while True:
            count += 1
            if not first:
                centroids = newCentroids.copy()
            first = False
            keysByCluster = self.getKeysByCluster(scoredPostsFile, centroids)
            print "[*] Got posts by closest cluster."
            newCentroids = self.getNewCentroids(scoredPostsFile, keysByCluster)
            print "[*] Got new positions of the centroids."
            if self.isSameCluster(centroids, newCentroids):
                break

        print "[+] Final clusters found in " + str(count) + " rounds."
        print "[*] Number of final clusters : " + str(len(keysByCluster.keys()))
        self.saveClusters(clustersFile, keysByCluster)

    def getInitCentroids(self, file, k):
        "Get the K initial random centroids"
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        randoms = [0.0] * k
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

    def getCoordinatesById(self, file, ids):
        "Get the coordinates of the given list of centroids"
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return None

        coordinates, count = {}, 0
        for line in myFile:
            infos = line.split('\t')
            
            if infos[0] in ids:
                coords = {}
                for tup in infos[1].split('#'):
                    couple = tup.split(':')
                    coords.setdefault(couple[0], float(couple[1]))
                coordinates.setdefault(count, coords)
                count += 1

        myFile.close()
        return coordinates

    def getKeysByCluster(self, file, centroids):
        "Get the posts classify by cluster"
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
                    minCentroid = key
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
        "Get the new position of the centroids"
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

    def getDistance(self, center, doc):
        "Get the distance between a post and a centroid"
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
        "Get the average of the list of coordinates"
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
        "Check if two list of centroids are identical"
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
        "Save the final clusters found"
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False

        for key, ids in keysByCluster.items():
            post_ids = " ".join(ids)
            myFile.write(str(key))
            myFile.write('\t')
            myFile.write(post_ids)
            myFile.write('\n')
        myFile.close()
        return True

    def wordByCluster(self, scoredPostsFile, clustersFile, saveFile):
        "Save the coordinates of the final centroids"
        try:
            myFile = open(clustersFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        keysByCluster = {}
        for line in myFile:
            infos = line.strip().split('\t')
            ids = infos[1].split(" ")
            keysByCluster.setdefault(infos[0], ids)
        myFile.close()

        clusters = self.getNewCentroids(scoredPostsFile, keysByCluster)

        try:
            myFile = open(saveFile, 'w')
        except:
            print "[-] Fail to open the file."
            return False
        
        for key, coords in clusters.items():
            sorted_coords = sorted(coords.items(), key=operator.itemgetter(1), reverse=True)
            first = True
            myFile.write(str(key))
            myFile.write('\t')
            for word, value in sorted_coords:
                if not first:
                    myFile.write(" ")
                first = False
                myFile.write(word + ":" + str(value))
            myFile.write('\n')
        myFile.close()
        return True

    def saveDistanceBetweenCluster(self, wordClusterFile, distanceCluster):
        "Save the distances between the final centroids"
        try:
            wordFile = open(wordClusterFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        wordsByCluster = {}
        for line in wordFile:
            infos = line.strip().split('\t')

            coords = {}
            for c in infos[1].split(' '):
                tup = c.split(':')
                coords.setdefault(tup[0], float(tup[1]))

            wordsByCluster.setdefault(infos[0], coords)

        wordFile.close()

        try:
            wordFile = open(wordClusterFile, 'r')
            distanceFile = open(distanceCluster, 'w')
        except:
            print "[-] Fail to open the file."
            return False

        for line in wordFile:
            for k, v in wordsByCluster.items():
                infos = line.strip().split('\t')

                if infos[0] != k:
                    coords = {}
                    for c in infos[1].split(' '):
                        tup = c.split(':')
                        coords.setdefault(tup[0], float(tup[1]))

                    distance = self.getDistance(v, coords)
                    distanceFile.write(k + '\t' + infos[0] + '\t' + str(distance) + '\n')

        wordFile.close()
        distanceFile.close()
        return True
           

if __name__ == "__main__":
    directory, scoredPostsFile, clustersFile, wordClustersFile, distFile = "./files/", "scored_posts.txt", "clusters.txt", "wordClusters.txt", "distanceClusters.txt"

    parser = argparse.ArgumentParser(description='Food clustering project - K-Means module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-spf', action="store", dest="scoredPostsFile", help="Source posts file. By default: scored_posts.txt", nargs=1) 
    parser.add_argument('-cf', action="store", dest="clustersFile", help="File to save the instagram ids by cluster. By default: clusters.txt", nargs=1)
    parser.add_argument('-wcf', action="store", dest="wordClustersFile", help="File to save the words and weigth by cluster. By default: wordClusters.txt", nargs=1)
    parser.add_argument('-dcf', action="store", dest="distanceClustersFile", help="File to save the distances between the centroids. By default: distanceClusters.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.scoredPostsFile != None:
        scoredPostsFile = args.scoredPostsFile[0]
    if args.clustersFile != None:
        clustersFile = args.clustersFile[0]
    if args.wordClustersFile != None:
        wordClustersFile = args.wordClustersFile[0]
    if args.distanceClustersFile != None:
        distFile = args.distanceClustersFile[0]
        
    KMeans(directory + scoredPostsFile, directory + clustersFile, directory + wordClustersFile, directory + distFile)
    
