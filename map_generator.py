#!/usr/bin/python

import os, sys, argparse
import pygmaps

class Map():
    def __init__(self, locFile):
        print "[*] Map module starting"
        
        self.directory = os.path.dirname(os.path.abspath(__file__))

        for directory in ['./files', './clustermap']:
            if not os.path.exists(directory):
                os.makedirs(directory)

        self.drawMaps(locFile)

    def drawMaps(self, locFile):
        "Generate the map for each cluster"
        try:
            myFile = open(locFile, 'r')
        except:
            print "[-] Fail to open the file."
            return False
        
        for line in myFile:
            mymap = pygmaps.maps(0, 0, 2)
            infos = line.strip().split('\t')

            if len(infos) == 1:
                url = '/clustermap/clustermap_' + infos[0] +'.html'
                mymap.draw('.' + url)
                continue

            locs = infos[1].split("Location: ")
            locs.pop(0)

            for loc in locs:
                nameAndCoords = loc.split(" (Point: (")
                try:
                    coords = nameAndCoords[1]
                    coords = coords[:-3]
                except:
                    print "[-] No coordinates for this location."
                    continue

                latitude, longitude = coords.split(", ")
                mymap.addpoint(float(latitude), float(longitude), "#FC6254")

            url = '/clustermap/clustermap_' + infos[0] +'.html'
            mymap.draw('.' + url)
            
        myFile.close()
        return True

if __name__ == '__main__':
    directory, locFile = "./files/", "locations.txt"

    parser = argparse.ArgumentParser(description='Food clustering project - Map module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-lf', action="store", dest="locFile", help="Source locations file (Locations by cluster). By default: locations.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.locFile != None:
        locFile = args.locFile[0]
        
    Map(directory + locFile)
