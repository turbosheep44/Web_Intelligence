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

# remove all those whose weight is not in the top 150
# users_to_keep = []
# for user in data.keys():
#     position = 0
#     while position < len(users_to_keep) and data[users_to_keep[position]]["weight"] < data[user]["weight"]:
#         position += 1
#     users_to_keep.insert(position, user)
#     users_to_keep = users_to_keep[-100:]

# filtered_data = {user: data[user] for user in users_to_keep}
# for x in filtered_data:
#    print(x, filtered_data[x]["weight"])

# get a list of all the distinct user pairs
distinct_user_pairs = combinations(list(data.keys()), 2)
total_user_pairs = sum(1 for _ in combinations(list(data.keys()), 2))

# record a numberical id for each user
user_ids = {name: index for index,
            name in enumerate(list(data.keys()))}

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

print("\noutputting dtaa")
with open("edges.json", "w") as output:
    print(json_dumps(documents), file=output)

with open("graph.json", "w") as output:
    print(json_dumps({
        "users": [{"id": user_ids[user], "name": user, "contact": data[user]["weight"]}
                  for user in data],
        "edges":  [{"source": literal_eval(edge)[0], "target": literal_eval(
            edge)[1], "weight": len(documents[edge])} for edge in documents]
    }), file=output)
