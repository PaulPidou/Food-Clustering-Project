#!/usr/bin/python

import os, os.path, sys
import operator
from selenium import webdriver

class GenerateWebsite():
    def __init__(self):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.maps = [name for name in os.listdir('./clustermap/') if not name.startswith('.') and os.path.isfile(os.path.join('./clustermap/', name))]
        self.webDir = "/website/pages/"

        try:
            myFile = open('clusters.txt', 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        keyByCluster = {}
        for line in myFile:
            infos = line.strip().split('\t')
            keyByCluster.setdefault(infos[0], infos[1].split(' '))

        myFile.close()

        self.generateWrapper('index.html', keyByCluster, None)

        for key, ids in keyByCluster.items():
            self.generateWrapper(key, ids, 'cluster')

        #browser = webdriver.Firefox()
        #browser.get('file://' + self.directory + self.webDir + 'index.html')

    def generateWrapper(self, key, ids, section):
        try:
            if section != None:
                website = open('.' + self.webDir + section + '_' + key + '.html', 'w')
            else:
                website = open('.' + self.webDir + key, 'w')
            header = open('.' + self.webDir + 'header.html', 'r')
            footer = open('.' + self.webDir + 'footer.html', 'r')
        except:
            print "[-] Fail to generate the website."
            return None

        for line in header:
            website.write(line)

        header.close()

        for clusterMap in self.maps:
            number = clusterMap[11:-5]
            website.write('<li><a href="cluster_' + number + '.html">Cluster ' + number + '</a></li>')

        website.write('</ul></li></ul></div></div></nav>')
        website.write('<div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12">')

        if section == None:
            wordByCluster = self.getMainWords()
            distanceClusters = self.getDistanceClusters()
            website.write('<h1 class="page-header">Summary</h1>')
            website.write('<div class="panel-body"><div class="table-responsive"><table class="table">')
            website.write('<thead><tr><th>Cluster</th><th>Number of members</th><th>Main word</th><th>Closest cluster</th><th>Link</th></tr></thead><tbody>')
            for i in range(len(ids.keys())):
                dists = distanceClusters[str(i)]
                sorted_dists = sorted(dists.items(), key=operator.itemgetter(1))
                website.write('<tr><td>' + str(i) + '</td><td>' + str(len(ids[str(i)])) + '</td><td>' + wordByCluster[str(i)] + '</td><td>' + sorted_dists[0][0] + '</td><td><a href="cluster_' + str(i) + '.html"><button type="button" class="btn btn-default btn-circleg"><i class="fa fa-angle-right"></i></button></a></td></tr>')
            website.write('</tbody></table></div></div>')
            

        elif section == 'cluster':
            self.createClusterPage(key, ids, website)
        
        website.write('</div></div></div></div>')
        
        for line in footer:
            website.write(line)

        footer.close()
        website.close()

    def createClusterPage(self, nbCluster, ids, website):
        website.write('<h1 class="page-header">Cluster ' + nbCluster + '</h1>')
        website.write('<div class="panel-body"><ul class="nav nav-pills"><li class="active"><a href="#map-pills" data-toggle="tab"><i class="fa fa-globe fa-fw"></i> Map</a></li><li><a href="#picture-pills" data-toggle="tab"><i class="fa fa-camera-retro fa-fw"></i> Pictures</a></li><li><a href="#word-pills" data-toggle="tab"><i class="fa fa-list fa-fw"></i> Words</a></li><li><a href="#distance-pills" data-toggle="tab"><i class="fa fa-expand fa-fw"></i> Distances</a></li></ul>')
        website.write('<div class="tab-content" style="padding-top: 15px;"><div class="tab-pane fade in active" id="map-pills">')
        website.write('<iframe src="../../clustermap/clustermap_' + nbCluster + '.html" style="border:none;height: 600px;" width=100%></iframe>')                          
        website.write('</div><div class="tab-pane fade" id="picture-pills">')

        try:
            postsFile = open('posts.txt', 'r')
        except:
            print "[-] Fail to open the file."
            return False

        for line in postsFile:
            infos = line.strip().split('\t')

            if infos[0] in ids:
                tags = infos[1].split('#')
                tags_str = " #".join(tags)
                website.write('<a class="fancybox" rel="group" href="' + infos[5] + '" title="#' + tags_str + " " + infos[2] + " " + infos[4] + '"><img src="' + infos[5] + '" alt="" height="150" width="150">')

        postsFile.close()

        website.write('</div><div class="tab-pane fade" id="word-pills">')

        try:
            wordFile = open('wordClusters.txt', 'r')
        except:
            print "[-] Fail to open the file."
            return False

        website.write('<div class="panel-body"><div class="table-responsive"><table class="table">')
        website.write('<thead><tr><th>#</th><th>Word</th><th>Weight</th></tr></thead><tbody>')
                                    
        for line in wordFile:
            infos = line.strip().split('\t')

            if infos[0] == nbCluster:
                coords = infos[1].split(' ')
                count = 1
                for coord in coords:
                    tup = coord.split(':')
                    website.write('<tr><td>' + str(count) + '</td><td>' + tup[0] + '</td><td>' + tup[1] + '</td></tr>')
                    count += 1

        website.write('</tbody></table></div></div>')           
        wordFile.close()

        website.write('</div><div class="tab-pane fade" id="distance-pills">')
        website.write('<div class="panel-body"><div class="table-responsive"><table class="table">')
        website.write('<thead><tr><th>#</th><th>Cluster</th><th>Distance</th></tr></thead><tbody>')

        distanceClusters = self.getDistanceClusters()

        dists = distanceClusters[nbCluster]
        sorted_dists = sorted(dists.items(), key=operator.itemgetter(1))

        count = 1
        for c, d in sorted_dists:
            website.write('<tr><td>' + str(count) + '</td><td>' + c + '</td><td>' + str(d) + '</td></tr>')
            count += 1

        website.write('</tbody></table></div></div>')           
                                
        website.write('</div></div></div>')
        return True

    def getMainWords(self):
        try:
            wordFile = open('wordClusters.txt', 'r')
        except:
            print "[-] Fail to open the file."
            return None

        wordByCluster = {}
        for line in wordFile:
            infos = line.split('\t')
            words = infos[1].split(':')

            wordByCluster.setdefault(infos[0], words[0])

        wordFile.close()
        return wordByCluster

    def getDistanceClusters(self):
        try:
            distFile = open('distanceClusters.txt', 'r')
        except:
            print "[-] Fail to open the file."
            return None

        distClust = {}
        for line in distFile:
            infos = line.strip().split('\t')

            distClust.setdefault(infos[0], {})
            distClust[infos[0]].setdefault(infos[1], float(infos[2]))

        distFile.close()
        return distClust
            
if __name__ == '__main__':
    GenerateWebsite()
