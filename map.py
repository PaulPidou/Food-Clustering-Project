#!/usr/bin/python

import os, sys
import pygmaps
from instagram.client import InstagramAPI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Map():
    def __init__(self, locFile):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        
        try:
            myFile = open(locFile, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        browser = webdriver.Firefox()
        
        for line in myFile:
            mymap = pygmaps.maps(0, 0, 2)
            infos = line.strip().split('\t')

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
            browser.get('file://' + self.directory + url)

            body = browser.find_element_by_tag_name("body")
            body.send_keys(Keys.COMMAND + 't') # Replace by Keys.CONTROL if you are not on MAC OS X

        body.send_keys(Keys.COMMAND + 'w') # Replace by Keys.CONTROL if you are not on MAC OS X
        myFile.close()

if __name__ == '__main__':
    Map("locations.txt")
