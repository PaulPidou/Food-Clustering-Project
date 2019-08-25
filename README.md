# Food-Clustering-Project

## General principle
The general principle of the food clustering project is to retrieve the Instagram posts related to food over a certain period of time and cluster them. The clustering is performed thanks to the tags put by the user.

## Ressources used
- Instagram API
- Wikipedia API for Python
- TextBlob Python library
- NLTK - Natural Language Toolkit
- pygmaps - Python wrapper for Google Maps
- SB Admin - Boostrap theme

## Modules

Each module can be used separately

### Instagram Bot module
This module retrieves and saves the Instagram posts related to food.

```
usage: instagram_bot.py [-h] -ci CLIENT_ID -cs CLIENT_SECRET [-pf POSTSFILE] [-d DURATION] [--version]

Food clustering project - Instagram Bot module

optional arguments:
  -h, --help         show this help message and exit
  -ci CLIENT_ID      Instagram Client ID [Required]
  -cs CLIENT_SECRET  Instagram Client Secret [Required]
  -pf POSTSFILE      File to save the instagram posts. By default: posts.txt
  -d DURATION        Duration of the posts retrieving. By default: 60 mins
  --version          show program's version number and exit
```
        
### Preprocess module

```
usage: preprocess.py [-h] [-pf POSTSFILE] [-ppf PREPROCESSFILE] [--version]

Food clustering project - Preprocess module

optional arguments:
  -h, --help           show this help message and exit
  -pf POSTSFILE        Source posts file. By default: posts.txt
  -ppf PREPROCESSFILE  File to save the preprocess posts. By default:
                       preproceed_posts.txt
  --version            show program's version number and exit
````

### TF-IDF module

```
usage: tfidf.py [-h] [-ppf PREPROCESSFILE] [-tf TFIDFFILE] [--version]

Food clustering project - TF-IDF module

optional arguments:
  -h, --help           show this help message and exit
  -ppf PREPROCESSFILE  Source preproceed posts. By default:
                       preproceed_posts.txt
  -tf TFIDFFILE        File to save the TF-IDF scores. By default: tfidf.txt
  --version            show program's version number and exit
````

### Invert index module
```
usage: invert.py [-h] [-tf TFIDFFILE] [-spf SCOREDPOSTSFILE] [--version]

Food clustering project - Invert index module

optional arguments:
  -h, --help            show this help message and exit
  -tf TFIDFFILE         Source TFIDF file. By default: tfidf.txt
  -spf SCOREDPOSTSFILE  File to save the scored posts. By default:
                        scored_posts.txt
  --version             show program's version number and exit
````

### K-Means module
```
usage: kmeans.py [-h] [-spf SCOREDPOSTSFILE] [-cf CLUSTERSFILE]
                 [-wcf WORDCLUSTERSFILE] [-dcf DISTANCECLUSTERSFILE]
                 [--version]
Food clustering project - K-Means module
optional arguments:
  -h, --help            show this help message and exit
  -spf SCOREDPOSTSFILE  Source posts file. By default: scored_posts.txt
  -cf CLUSTERSFILE      File to save the instagram ids by cluster. By default:
                        clusters.txt
  -wcf WORDCLUSTERSFILE
                        File to save the words and weigth by cluster. By
                        default: wordClusters.txt
  -dcf DISTANCECLUSTERSFILE
                        File to save the distances between the centroids. By
                        default: distanceClusters.txt
  --version             show program's version number and exit
````
  
### Location module
```
usage: location.py [-h] [-pf POSTSFILE] [-cf CLUSTERSFILE] [-lf LOCFILE] [--version]

Food clustering project - Location module

optional arguments:
  -h, --help        show this help message and exit
  -pf POSTSFILE     Source posts file. By default: posts.txt
  -cf CLUSTERSFILE  Source clusters file. By default: clusters.txt
  -lf LOCFILE       File to save the locations by cluster. By default:
                    locations.txt
  --version         show program's version number and exit
````

### Map module
```
usage: map_generator.py [-h] [-lf LOCFILE] [--version]

Food clustering project - Map module

optional arguments:
  -h, --help   show this help message and exit
  -lf LOCFILE  Source locations file (Locations by cluster). By default:
               locations.txt
  --version    show program's version number and exit
````
 
### Website Generator module
This module generates the website that presents the results (Need SB Admin theme -  https://github.com/IronSummitMedia/startbootstrap-sb-admin and FancyBox - http://fancybox.net/ to work correctly).

```
usage: website_generator.py [-h] [-pf POSTSFILE] [-cf CLUSTERSFILE]
                            [-wcf WORDCLUSTERSFILE]
                            [-dcf DISTANCECLUSTERSFILE] [--version]

Food clustering project - Website generator module

optional arguments:
  -h, --help            show this help message and exit
  -pf POSTSFILE         Source posts file. By default: posts.txt
  -cf CLUSTERSFILE      Source clusters file. By default: clusters.txt
  -wcf WORDCLUSTERSFILE
                        Source words file (Word and weight by cluster). By
                        default: wordClusters.txt
  -dcf DISTANCECLUSTERSFILE
                        Source distances file (Distances between centroids).
                        By default: distanceClusters.txt
  --version             show program's version number and exit
```
## Main application
The main application puts all the modules together and allows the user to launch the whole process with only one command line.

```
usage: application.py [-h] -ci CLIENT_ID -cs CLIENT_SECRET [-pf POSTSFILE]
                      [-d DURATION] [-ppf PREPROCESSFILE] [-tf TFIDFFILE]
                      [-spf SCOREDPOSTSFILE] [-cf CLUSTERSFILE]
                      [-wcf WORDCLUSTERSFILE] [-dcf DISTANCECLUSTERSFILE]
                      [-lf LOCFILE] [--version]

Food clustering project - Main application

optional arguments:
  -h, --help            show this help message and exit
  -ci CLIENT_ID         Instagram Client ID [Required]
  -cs CLIENT_SECRET     Instagram Client Secret [Required]
  -pf POSTSFILE         File to save the instagram posts. By default:
                        posts.txt
  -d DURATION           Duration of the posts retrieving. By default: 60 mins
  -ppf PREPROCESSFILE   File to save the preprocess posts. By default:
                        preproceed_posts.txt
  -tf TFIDFFILE         File to save the TF-IDF scores. By default: tfidf.txt
  -spf SCOREDPOSTSFILE  File to save the scored posts. By default:
                        scored_posts.txt
  -cf CLUSTERSFILE      File to save the instagram ids by cluster. By default:
                        clusters.txt
  -wcf WORDCLUSTERSFILE
                        File to save the words and weigth by cluster. By
                        default: wordClusters.txt
  -dcf DISTANCECLUSTERSFILE
                        File to save the distances between the centroids. By
                        default: distanceClusters.txt
  -lf LOCFILE           File to save the locations by cluster. By default:
                        locations.txt
  --version             show program's version number and exit

Developed by Paul Pidou.
```
