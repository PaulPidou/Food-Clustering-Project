#!/usr/bin/python

import argparse, sys

from instagram_bot import *
from preprocess import *
from tfidf import *
from invert import *
from kmeans import *
from location import *
from map_generator import *
from website_generator import *

class Application():
    def __init__(self, directory, postsFile, duration, preproceed_postsFile, tfidfFile, scoredPostsFile, clustersFile, wordsFile, distFile, locFile):
        self.main(directory, postsFile, duration, preproceed_postsFile, tfidfFile, scoredPostsFile, clustersFile, wordsFile, distFile, locFile)

    def main(self, directory, postsFile, duration, preproceed_postsFile, tfidfFile, scoredPostsFile, clustersFile, wordsFile, distFile, locFile):
        InstaFood(args.client_id[0], args.client_secret[0], directory + postsFile, duration)
        PreProcess(directory + postsFile, directory + preproceed_postsFile)
        TFIDF(directory + preproceed_postsFile, directory + tfidfFile)
        Invert(directory + tfidfFile, directory + scoredPostsFile)
        KMeans(directory + scoredPostsFile, directory + clustersFile, directory + wordsFile, directory + distFile)
        Location(directory + postsFile, directory + clustersFile, directory + locFile)
        Map(directory + locFile)
        WebsiteGenerator(directory + postsFile, directory + clustersFile, directory + wordsFile, directory + distFile)

if __name__ == "__main__":
    directory, postsFile, preproceed_postsFile, tfidfFile, scoredPostsFile, clustersFile, wordsFile, distFile, locFile = "./files/", "posts.txt", "preproceed_posts.txt", "tfidf.txt",  "scored_posts.txt", "clusters.txt", "wordClusters.txt", "distanceClusters.txt", "locations.txt"
    duration = 60
    
    parser = argparse.ArgumentParser(description='Food clustering project - Main application', epilog="Developed by Paul Pidou.")

    parser.add_argument('-ci', action="store", dest="client_id", help="Instagram Client ID [Required]", nargs=1, required=True)
    parser.add_argument('-cs', action="store", dest="client_secret", help="Instagram Client Secret [Required]", nargs=1, required=True)
    parser.add_argument('-pf', action="store", dest="postsFile", help="File to save the instagram posts. By default: posts.txt", nargs=1)
    parser.add_argument('-d', action="store", dest="duration", help="Duration of the posts retrieving. By default: 60 mins", nargs=1)
    parser.add_argument('-ppf', action="store", dest="preprocessFile", help="File to save the preprocess posts. By default: preproceed_posts.txt", nargs=1)
    parser.add_argument('-tf', action="store", dest="tfidfFile", help="File to save the TF-IDF scores. By default: tfidf.txt", nargs=1)
    parser.add_argument('-spf', action="store", dest="scoredPostsFile", help="File to save the scored posts. By default: scored_posts.txt", nargs=1)
    parser.add_argument('-cf', action="store", dest="clustersFile", help="File to save the instagram ids by cluster. By default: clusters.txt", nargs=1)
    parser.add_argument('-wcf', action="store", dest="wordClustersFile", help="File to save the words and weigth by cluster. By default: wordClusters.txt", nargs=1)
    parser.add_argument('-dcf', action="store", dest="distanceClustersFile", help="File to save the distances between the centroids. By default: distanceClusters.txt", nargs=1)
    parser.add_argument('-lf', action="store", dest="locFile", help="File to save the locations by cluster. By default: locations.txt", nargs=1)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args, unknown = parser.parse_known_args()

    if unknown:
        print '[-] Unknown argument(s) : ' + str(unknown).strip('[]')
        print '[*] Exciting ...'
        sys.exit(0)

    if args.postsFile != None:
        postsFile = args.postsFile[0]
    if args.duration != None:
        duration = args.duration[0]
    if args.preprocessFile != None:
        preproceed_postsFile = args.preprocessFile[0]
    if args.tfidfFile != None:
        tfidfFile = args.tfidfFile[0]
    if args.scoredPostsFile != None:
        scoredPostsFile = args.scoredPostsFile[0]
    if args.clustersFile != None:
        clustersFile = args.clustersFile[0]
    if args.wordClustersFile != None:
        wordsFile = args.wordClustersFile[0]
    if args.distanceClustersFile != None:
        distFile = args.distanceClustersFile[0]
    if args.locFile != None:
        locFile = args.locFile[0]

    Application(directory, postsFile, duration, preproceed_postsFile, tfidfFile, scoredPostsFile, clustersFile, wordsFile, distFile, locFile)
