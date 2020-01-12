from json import load as load_json
from json import dumps as json_dumps
from ast import literal_eval
from math import inf


# using floyd warshall's algorithm to get the shortest path between all nodes
def floyd_warshall(node_count, adjacency_list):
    # create a 2d array for all path distances (all distances start at infinity)
    distance_matrix = \
        [[inf for _ in range(node_count)] for _ in range(node_count)]

    # for all the edges in the graph, set the distance matrix value to 1
    # (use 1 since edges have no cost, all that matters is the number of edges)
    for x in adjacency_list:
        for y in adjacency_list[x]:
            distance_matrix[x][y] = 1

    # distance from any node to itself is 0
    for x in range(node_count):
        distance_matrix[x][x] = 0

    # now use floyd warshall
    for k in range(node_count):
        for i in range(node_count):
            for j in range(node_count):
                if distance_matrix[i][j] > (distance_matrix[i][k] + distance_matrix[k][j]):
                    distance_matrix[i][j] = distance_matrix[i][k] + \
                        distance_matrix[k][j]

    # ensure that all nodes are connected (no paths have infinite weight)
    # and set the node_data value for eccentricity and average path distance
    for node in range(node_count):
        eccentricity = max(distance_matrix[node])
        if eccentricity == inf:
            print(f"[{node}] is not fully connected [{distance_matrix[node]}]")
            print("FAIL! GRAPH IS NOT CONNECTED!")
        node_data[node]["eccentricity"] = eccentricity
        node_data[node]["average_path_distance"] = sum(
            distance_matrix[node]) / len(distance_matrix[node])

        # extract the diameter (max eccentricity)
    diameter = max(max(distance_matrix[node]) for node in range(node_count))
    print(f"Diameter [{diameter}]")

    # extract average path length
    average_path_length = sum(
        sum(distance_matrix[node]) / (node_count-1) for node in range(node_count))/node_count
    print(f"Average path length [{average_path_length}]")

    # show paths which have maximum length
    # counter = 0
    # for x in range(node_count):
    #     for y in range(node_count):
    #         if distance_matrix[x][y] == diameter:
    #             print(f"from [{x}] to [{y}]")
    #             counter += 1
    # print(f"# of people [{counter/2}]")

    return diameter, average_path_length


def local_clustering_cofficient(node_index, adjacency_list):
    # get the neighbour node list
    neighbours = set(adjacency_list[node_index].keys())
    node_data[node_index]["neighbours"] = len(neighbours)

    # if the degree of this vertex is not > 1 then the clustering coefficient is undefined
    if not len(neighbours) > 1:
        # print(f"Local Clustering Coefficient of [{node_index}] is [-1]")
        node_data[node_index]["clustering_coefficient"] = -1
        return -1

    # calculate the number of potential edges in the node induced subgraph of the neighbours
    max_possible_neighbour_edges = (len(neighbours) * (len(neighbours) - 1))/2

    # calculate the actual number of edges between neighbours
    neighbour_edges = 0
    for neighbour in neighbours:
        for other_neighbour in neighbours:
            if other_neighbour in adjacency_list[neighbour]:
                neighbour_edges += 1
    # divide by 2 (dont count duplicates)
    neighbour_edges /= 2

    # print(f"Neighbours {neighbours}")
    # print(f"Max edges between neighbours [{max_possible_neighbour_edges}]")
    # print(f"Actual between neighbours [{neighbour_edges}]")
    # print(
    #    f"Local Clustering Coefficient of [{node_index}] is [{neighbour_edges/max_possible_neighbour_edges}]")

    node_data[node_index]["clustering_coefficient"] = neighbour_edges / \
        max_possible_neighbour_edges
    return node_data[node_index]["clustering_coefficient"]


# removes the undefined (-1) coefficients from the list
def filter_undefined_coefficients(list_of_coefficients):
    for coefficient in list_of_coefficients:
        if coefficient != -1:
            yield coefficient


# calculate the clustering coefficient for the whole graph
def global_clustering_coefficient(node_count, adjacency_list):
    # calculate the clustering coefficient for each node
    local_coefficients = [local_clustering_cofficient(
        node_index, adjacency_list) for node_index in range(node_count)]

    # sum and count the total coefficients excluding those which are undefined (-1)
    # the filter function allows for a in iterator which yields values,
    # meaning that both operations can be done in one pass or memory instead of two
    total_coefficient_value = 0
    valid_coefficient_count = 0
    for valid_coefficient in filter_undefined_coefficients(local_coefficients):
        valid_coefficient_count += 1
        total_coefficient_value += valid_coefficient

    # calculate and return global clustering coefficient
    # print(
    #     f"Total Coefficient [{total_coefficient_value}]")
    # print(
    #     f"Number of valid coefficients [{valid_coefficient_count}]")
    print(
        f"Global clustering coefficient [{total_coefficient_value / valid_coefficient_count}]")
    return total_coefficient_value / valid_coefficient_count


# creates an adjacancy list for the given graph
def construct_adjacency_list(edges):
    # make an adjacency matrix of the correct size
    # (using dictionaries for constant lookup time)
    adjacency_list = {}
    for edge in edges:
        adjacency_list[edge[0]] = adjacency_list.get(edge[0], {})
        adjacency_list[edge[0]][edge[1]] = edges[edge]
        adjacency_list[edge[1]] = adjacency_list.get(edge[1], {})
        adjacency_list[edge[1]][edge[0]] = edges[edge]

    return adjacency_list


# put relevant node data from the graph json into node_data
def get_node_data_from_graph(graph):
    for node in graph["users"]:
        node_data[node["id"]]["name"] = node["name"]
        node_data[node["id"]]["weight"] = node["contact"]


if __name__ == "__main__":
    # read the metadata json file
    with open('graph.json') as json_file:
        graph = load_json(json_file)

    # perform conversions to edges = { tuple(id, id) : weight } and get node_count
    edges = {(edge["source"],  edge["target"]): edge["weight"]
             for edge in graph["edges"]}
    node_count = len(graph["users"])

    # graph size
    graph_stats = {}
    graph_stats["node_count"] = node_count
    graph_stats["edge_count"] = len(edges)
    print(f"Nodes  [{node_count}]")
    print(f"Edges  [{len(edges)}]")

    # create node_data dictionary and initialise the container for each node
    global node_data
    node_data = {index: {} for index in range(node_count)}

    # extract useful node data from graph
    get_node_data_from_graph(graph)

    # create adjacency list and release memory which is no longer required
    adjacency_list = construct_adjacency_list(edges)
    del edges
    del graph

    # get the graph facts
    graph_stats["diameter"], graph_stats["average_path_length"] = \
        floyd_warshall(node_count, adjacency_list)
    graph_stats["global_clustering_coefficient"] = \
        global_clustering_coefficient(node_count, adjacency_list)

    # output graph stuff to file
    with open(f"graph_stats.json", "w") as outputFile:
        print(json_dumps(graph_stats), file=outputFile)

    # output the node data to files
    for node_id in node_data:
        with open(f"node_data/{node_id}.json", "w") as outputFile:
            print(json_dumps(node_data[node_id]), file=outputFile)
