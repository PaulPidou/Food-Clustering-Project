#!/usr/bin/python

import argparse, sys

class Location():
    def __init__(self, postsFile, clustersFile, locationFile):
        try:
            myFile = open(clustersFile, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        clusters = {}
        for line in myFile:
            infos = line.strip().split('\t')
            clusters.setdefault(infos[0], infos[1].split(" "))
        myFile.close()

        try:
            myFile = open(postsFile, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        locations = {}
        for line in myFile:
            infos = line.split('\t')

            for key, ids in clusters.items():
                locations.setdefault(key, [])
                if infos[0] in ids:
                    if infos[3] != 'None':                       
                        locations[key].append(infos[3])
        myFile.close()

        self.saveLocations(locationFile, locations)


    def saveLocations(self, file, locations):
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False

        for key, loc in locations.items():
            loc_str = " ".join(loc)
            myFile.write(str(key))
            myFile.write('\t')
            myFile.write(loc_str)
            myFile.write('\n')
        myFile.close()
        return True

if __name__ == "__main__":
    postsFile, clustersFile, locFile = "posts.txt", "clusters.txt", "locations.txt"

    parser = argparse.ArgumentParser(description='Final project - Location module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-pf', action="store", dest="postsFile", help="Source posts file. By default: posts.txt", nargs=1) 
    parser.add_argument('-cf', action="store", dest="clustersFile", help="Source clusters file. By default: clusters.txt", nargs=1)
    parser.add_argument('-lf', action="store", dest="locFile", help="File to save the locations by cluster. By default: locations.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.postsFile != None:
        postsFile = args.postsFile[0]
    if args.clustersFile != None:
        clustersFile = args.clustersFile[0]
    if args.locFile != None:
        locFile = args.locFile[0]
        
    Location(postsFile, clustersFile, locFile)
