#!/usr/bin/python

import os, os.path, sys, argparse
import operator
from selenium import webdriver
import shutil

class WebsiteGenerator():
    def __init__(self, postsFile, clusterFile, wordsFile, distFile):
        print "[*] Website generator module starting"
        
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.maps = [name for name in os.listdir('./clustermap/') if not name.startswith('.') and os.path.isfile(os.path.join('./clustermap/', name))]
        self.webDir = "/website/pages/"

        if not os.path.exists('./website/clustermap/'):
            os.makedirs('./website/clustermap/')

        for m in self.maps:
            shutil.copy('./clustermap/' + m, './website/clustermap/')

        try:
            myFile = open(clusterFile, 'r')
        except:
            print "[-] Fail to open the file."
            sys.exit(0)

        self.keyByCluster, self.cluster_ids = {}, []
        for line in myFile:
            infos = line.strip().split('\t')
            self.keyByCluster.setdefault(infos[0], infos[1].split(' '))
            self.cluster_ids.append(int(infos[0]))

        myFile.close()

        self.cluster_ids.sort()                              

        self.generateWrapper('index.html', self.keyByCluster, None, postsFile, clusterFile, wordsFile, distFile)

        for key, ids in self.keyByCluster.items():
            self.generateWrapper(key, ids, 'cluster', postsFile, clusterFile, wordsFile, distFile)

        self.generateWrapper('about.html', None, None, None, None, None, None)

        #browser = webdriver.Firefox()
        #browser.get('file://' + self.directory + self.webDir + 'index.html')

    def generateWrapper(self, key, ids, section, postsFile, clusterFile, wordsFile, distFile):
        "Generate the web pages"
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

        for i in self.cluster_ids:
            website.write('<li><a href="cluster_' + str(i) + '.html">Cluster ' + str(i) + '</a></li>')

        website.write('</ul></li><li><a href="about.html"><i class="fa fa-question"></i> About the project</a></li>')
        website.write('</ul><p class="text-muted text-center" style="margin-top: 5px">Developed by Paul Pidou</p></div></div></nav>')
        website.write('<div id="page-wrapper"><div class="container-fluid"><div class="row"><div class="col-lg-12">')

        if key == 'about.html':
            try:
                myFile = open('.' + self.webDir + 'description.html', 'r')
            except:
                print "[-] Fail to generate the about page."
                return None

            for line in myFile:
                website.write(line)

            myFile.close()

        elif key == 'index.html':
            wordByCluster = self.getMainWords(wordsFile)
            distanceClusters = self.getDistanceClusters(distFile)
            
            nbPosts = 0
            for v in ids.values():
                nbPosts += len(v)
            
            website.write('<h1 class="page-header">Summary (' + str(nbPosts) + ' Posts / ' + str(len(ids.keys())) + ' Clusters)</h1>')
            website.write('<div class="panel-body"><div class="table-responsive"><table class="table">')
            website.write('<thead><tr><th>Cluster</th><th>Number of posts</th><th>Main word</th><th>Closest cluster</th><th>Link</th></tr></thead><tbody>')
            for i in self.cluster_ids:
                dists = distanceClusters[str(i)]
                sorted_dists = sorted(dists.items(), key=operator.itemgetter(1))
                website.write('<tr><td>' + str(i) + '</td><td>' + str(len(ids[str(i)])) + '</td><td>' + wordByCluster[str(i)] + '</td><td>' + sorted_dists[0][0] + '</td><td><a href="cluster_' + str(i) + '.html"><button type="button" class="btn btn-default btn-circleg"><i class="fa fa-angle-right"></i></button></a></td></tr>')
            website.write('</tbody></table></div></div>')
            

        elif section == 'cluster':
            self.createClusterPage(postsFile, wordsFile, distFile, key, ids, website)
        
        website.write('</div></div></div></div>')
        
        for line in footer:
            website.write(line)

        footer.close()
        website.close()

    def createClusterPage(self, pf, wf, df, nbCluster, ids, website):
        "Generate a cluster web page"
        website.write('<h1 class="page-header">Cluster ' + nbCluster + '</h1>')
        website.write('<div class="panel-body"><ul class="nav nav-pills"><li class="active"><a href="#map-pills" data-toggle="tab"><i class="fa fa-globe fa-fw"></i> Map</a></li><li><a href="#picture-pills" data-toggle="tab"><i class="fa fa-camera-retro fa-fw"></i> Pictures</a></li><li><a href="#word-pills" data-toggle="tab"><i class="fa fa-list fa-fw"></i> Words</a></li><li><a href="#distance-pills" data-toggle="tab"><i class="fa fa-expand fa-fw"></i> Distances</a></li></ul>')
        website.write('<div class="tab-content" style="padding-top: 15px;"><div class="tab-pane fade in active" id="map-pills">')
        website.write('<iframe src="../clustermap/clustermap_' + nbCluster + '.html" style="border:none;height: 600px;" width=100%></iframe>')                          
        website.write('</div><div class="tab-pane fade" id="picture-pills">')

        try:
            postsFile = open(pf, 'r')
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
            wordFile = open(wf, 'r')
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

        distanceClusters = self.getDistanceClusters(df)

        dists = distanceClusters[nbCluster]
        sorted_dists = sorted(dists.items(), key=operator.itemgetter(1))

        count = 1
        for c, d in sorted_dists:
            website.write('<tr><td>' + str(count) + '</td><td>' + c + '</td><td>' + str(d) + '</td></tr>')
            count += 1

        website.write('</tbody></table></div></div>')           
                                
        website.write('</div></div></div>')
        return True

    def getMainWords(self, wf):
        "Get the most representative word for each cluster"
        try:
            wordFile = open(wf, 'r')
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

    def getDistanceClusters(self, df):
        "Get the distance between each cluster"
        try:
            distFile = open(df, 'r')
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
    directory, postsFile, clusterFile, wordsFile, distFile = "./files/", "posts.txt", "clusters.txt", "wordClusters.txt", "distanceClusters.txt"

    parser = argparse.ArgumentParser(description='Food clustering project - Website generator module', epilog="Developed by Paul Pidou.")

    parser.add_argument('-pf', action="store", dest="postsFile", help="Source posts file. By default: posts.txt", nargs=1)
    parser.add_argument('-cf', action="store", dest="clustersFile", help="Source clusters file. By default: clusters.txt", nargs=1)
    parser.add_argument('-wcf', action="store", dest="wordClustersFile", help="Source words file (Word and weight by cluster). By default: wordClusters.txt", nargs=1)
    parser.add_argument('-dcf', action="store", dest="distanceClustersFile", help="Source distances file (Distances between centroids). By default: distanceClusters.txt", nargs=1)

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
    if args.wordClustersFile != None:
        wordsFile = args.wordClustersFile[0]
    if args.distanceClustersFile != None:
        distFile = args.distanceClustersFile[0]
        
    WebsiteGenerator(directory + postsFile, directory + clusterFile, directory + wordsFile, directory + distFile)
