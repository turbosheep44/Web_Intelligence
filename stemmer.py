from stemming.porter2 import stem
import re
stopList = {}
with open("stopwords.txt" , "r") as stopListLines:
    for line in stopListLines:
        stopList[line.strip()] = 0

print(stopList)
def removeStopwordsAndStem(file):
    output = ""
    with open(file , "r+") as fileRead:
        for line in fileRead:
            words = line.split()
            for word in words:
                if(word not in stopList):
                    ts = re.sub("[^ A-Za-z]", "", word)
                    if(len(ts) > 0 ):
                        output += str(stem(ts)) + " "
        fileRead.seek(0)
        fileRead.write(output)
        fileRead.truncate()
 
with open("email_paths.txt", "r") as allLines:
    counter = 0
    for line in allLines:
        
        h = line.replace("/", "").replace("\n", "") + "H"
        removeStopwordsAndStem("messages/"+h)
        print("File No + " + str(counter))
        counter += 1
        
 