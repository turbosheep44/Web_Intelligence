from stemming.porter2 import stem
import re
import os
from os import listdir
from os.path import isfile, join

stopList = {}
with open("stopwords.txt" , "r") as stopListLines:
    for line in stopListLines:
        stopList[line.strip()] = 0

def removeStopwordsAndStem(rootDir,file):
    output = ""
    with open(rootDir+file , "r+") as fileRead:
        for line in fileRead:
            words = line.split()
            for word in words:
                if(word not in stopList and '@' not in word and '*' not in word and '\'' not in word and '/' not in word):
                    ts = re.sub("[^ A-Za-z]", "", word)
                    if(len(ts) > 0 ):
                        output += str(stem(ts)) + " "
                
        fileOut = open ('anotherStemmer2/'+file, 'w+')
        fileOut.write(output)
        fileOut.close()

 
lines = os.listdir("all_Test/")
counter = 0
for line in lines:
    h = line.replace("/", "").replace("\n", "")
    removeStopwordsAndStem("all_Test/",h)
    print("File No + " + str(counter))
    counter += 1

        
 