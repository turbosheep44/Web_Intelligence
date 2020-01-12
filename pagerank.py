
from json import load as load_json
from json import dumps as json_dumps


def print_m(m):
    print("\n".join([str(["{:.2f}".format(e)
                          for e in m[i]]) for i in range(size)]))


# read metadata
with open("metadata.json", "r") as input_file:
    data = load_json(input_file)

# construct the matrix of links
size = len(data.keys())

# create the matrix of the correct size
reference_matrix = [[0 for x in range(size)]
                    for y in range(size)]

# construct boolen adjacency matrix
for person in data:
    for other_person in data:
        # does 'person' reference 'other_person'?
        # i.e. did 'person' send an email to 'other_person'
        person_sent_set = set(data[person]["sent"])
        if sum(1 for received in data[other_person]["received"]
               if received in person_sent_set):
            # if there was a reference then set this value to 1
            reference_matrix[data[other_person]["id"]][data[person]["id"]] = 1

# enforce that each column sums to 1 (distribute importance among outgoing links)
for column in range(size):
    column_total = sum(1 for index in range(size)
                       if reference_matrix[index][column])

    if column_total == 0 or (column_total == 1 and reference_matrix[column][column]):
        print(
            f"Redistribute self-referencing column [{column}] -> count: [{column_total}]")
        for index in range(size):
            reference_matrix[index][column] = 1/size
    else:
        for index in range(size):
            if reference_matrix[index][column]:
                reference_matrix[index][column] = 1/column_total


# print_m(reference_matrix)
# exit()

# create the rank matrix
rank = [1/size for _ in range(size)]

# pagerank time
for iteration_count in range(2500):
    # reset rank column vector
    new_rank = list(range(size))

    # for i in range(size):
    #     print(f" : [{rank[i]:.4f}]")

    # update rank for every node
    for n in range(size):
        new_rank[n] = sum(reference_matrix[n][i] * rank[i]
                          for i in range(size))

    # calculate the total change in rank
    rank_delta = sum(abs(rank[i]-new_rank[i]) for i in range(size))

    # set the new rank
    rank = new_rank

    if rank_delta < 0.000000001:
        print(f"Finished after [{iteration_count}] iterations")
        break
    # print(f"\n--------------{rank_delta}---------------\n")

print(f"Biggest rank [{max(rank)}] at [{rank.index(max(rank))}]")
print(f"Total pagerank [{sum(rank)}]")

# output pagerank data
rank_dict = {index: value for index, value in enumerate(rank)}
with open("output_json/pagerank.json", "w") as pagerank_output_file:
    print(json_dumps(rank_dict), file=pagerank_output_file)

# for each person, output to their node_data file their pagerank score
rank.sort(reverse=True)
for person_id in rank_dict:
    with open(f"output_json/node_data/{person_id}.json", "r") as person_data_file:
        person_data = load_json(person_data_file)
    # add one because indices are zero-based
    person_data["page_rank"] = rank.index(rank_dict[person_id]) + 1

    # rewrite the file
    with open(f"output_json/node_data/{person_id}.json", "w") as person_data_file:
        print(json_dumps(person_data), file=person_data_file)
