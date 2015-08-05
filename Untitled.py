
try:
    myFile = open("preproceed_posts.txt", 'r')
    copy = open("copy.txt", 'w')
except:
    print "Fail"

ids = []
for line in myFile:
    infos = line.split('\t')

    if infos[0] not in ids:
        ids.append(infos[0])
        copy.write(line)
    else:
        print infos[0]

myFile.close()
copy.close()
