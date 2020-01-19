# Running the Program

Order of stuff:
 - `text.py` (extract metadata and separate body)
 - `stemmer.py` (clean email bodies)
 - `filter.py` (filter any unwanted users and give a numerical ID to each user)
 - `documents.py` (creates documents for each distinct user pair)
 - `graph_faxxx.py` (gets all the facts about graph and nodes)
 - `tf_idf.py` (gets all the node and edge word cloud data)
 - `pagerank.py` (calculates pagerank data for each node and saves it)
 - `alias_data.py` (adds alias data to the node data files)
 - `server.py` (serve the web dashboard)

# Files

`graph.json`: data for gabriele d3 & used by `graph_faxxx.py`

`node_data/{id}.json` : information about a particular node
`tf_idf_nodes/{id}.json` : TF.IDF data for a word cloud for this node
`tf_idf_edges/{id}_{id}.json` : TF.IDF data for a word cloud for this edge

```json
{
    "name" : "joe.borg@enron.com",
    "weight" : 7,
    "neighbour_count" : 4,
    "clustering_coefficient" : 0.333333333,
    "eccentricity" : 4,
    "average_path_distance" : 2.4575
}
```
