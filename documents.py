from itertools import combinations
from json import dumps as json_dumps
from json import load as load_json
from collections import deque
from ast import literal_eval


# list intersect
# given two lists, finds the common elements in O(n) time
def intersect(listA, listB):
    setA = set(listA)
    return list(setA.intersection(listB))


# read the metadata json file
with open('metadata.json') as json_file:
    data = load_json(json_file)

# get a list of all the distinct user pairs
distinct_user_pairs = combinations(list(data.keys()), 2)
total_user_pairs = sum(1 for _ in combinations(list(data.keys()), 2))

# record a numberical id for each user
user_ids = {name: name["id"] for name in data}

# for each distinct user pair
#   one = userA.send intersect userB.received
#   two = userB.send intersect userA.received
#   document['AB'] = { one } union { two }
documents = {}
counter = 0
print(f"Total users pairs: {total_user_pairs} =>       ",  end="")

for user_pair in distinct_user_pairs:
    # counter output
    counter += 1
    print('\b\b\b\b\b\b', end="", flush=True)
    print("{:6}".format(counter), end="")

    # find common emails in sent and received and union the two
    common_emails = \
        intersect(data[user_pair[0]]["sent"], data[user_pair[1]]["received"]) + \
        intersect(data[user_pair[1]]["sent"], data[user_pair[0]]["received"])

    # if the edge actually has any weight (i.e. there exist common emails) then save it
    if len(common_emails) > 1:
        documents["(" + str(user_ids[user_pair[0]]) + ", " +
                  str(user_ids[user_pair[1]]) + ")"] = common_emails

print("\nWriting edges.json")
with open("edges.json", "w") as output:
    print(json_dumps(documents), file=output)

print("\nWriting graph.json")
with open("graph.json", "w") as output:
    print(json_dumps({
        "users": [{"id": user_ids[user], "name": user, "contact": data[user]["weight"]}
                  for user in data],
        "edges":  [{"source": literal_eval(edge)[0], "target": literal_eval(
            edge)[1], "weight": len(documents[edge])} for edge in documents]
    }), file=output)
