from stemming.porter2 import stem
import re
import os
from os import listdir
import sys
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
                
        fileOut = open (outputFolder + '/'+file, 'w+')
        fileOut.write(output)
        fileOut.close()
 
global inputFolder
global outputFolder
        
if __name__ == "__main__":
    fullCmdArguments = sys.argv
    argumentList = fullCmdArguments[1:]
    inputFolder = argumentList[0]
    outputFolder = argumentList[1]

    print( argumentList)

    if(len(argumentList) == 2):
        lines = os.listdir(inputFolder+'/')
        counter = 0
        for line in lines:
            h = line.replace("/", "").replace("\n", "")
            removeStopwordsAndStem(inputFolder+'/',h)
            print("File No + " + str(counter))
            counter += 1
    else:
        print("NOt working")
