import re
import string
from os import listdir
from os.path import isfile, join
import json
import os
import re
import json
import sys


finveremails = {}
allemails = []
with open("finver.json") as fileName:
    finveremails = json.load(fileName)

with open("testingsave.json") as fileName:
    allemails = json.load(fileName)

print(len(set(finveremails.keys())))

setall = set(allemails)
print([duplicate for index, duplicate in enumerate(allemails) if duplicate in allemails[index+1:] ])