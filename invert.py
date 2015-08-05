#!/usr/bin/python

class Invert():

    def __init__(self, file):
        self.invert(file)

    def invert(self, file):
        try:
            myFile = open(file, 'r')
        except:
            print "[-] Fail to open the file."
            return False

        invertedIndex = {}
        for line in myFile:
            infos = line.split('\t')
            for tup in infos[1].split('#'):
                couple = tup.split(':')
                invertedIndex.setdefault(couple[0], [])
                invertedIndex[couple[0]].append((infos[0], couple[1]))
        myFile.close()

        normIndex = {}
        for key, val in invertedIndex.items():
            values = []
            for tup in val:
                values.append(float(tup[1]))
            normValues = self.normalizeL2(values)

            normIndex.setdefault(key, [])
            for i in range(len(val)):
                normIndex[key].append((val[i][0], normValues[i]))

        self.saveInvert("scored_post.txt", normIndex)
        return True


    def normalizeL2(self, values):
        l2norm, normValues = 0, []

        for val in values:
            l2norm += val * val

        if l2norm == 0:
            normValues = 1 * len(values)
        else:
            for val in values:
                normValues.append(float(val / l2norm))

        return normValues

    def saveInvert(self, file, index):
        try:
            myFile = open(file, 'w')
        except:
            print "[-] Fail to open the file."
            return False
        
        for key, val in index.items():
            first = True
            myFile.write(key.encode('utf-8'))
            myFile.write('\t')
            for tup in val:
                if not first:
                    myFile.write("#")
                first = False
                myFile.write(str(tup[0]))
                myFile.write(":")
                myFile.write(str(tup[1]))
            myFile.write("\n")
            
        myFile.close()
        return True
        
if __name__ == "__main__":
    Invert("tfidf.txt")
