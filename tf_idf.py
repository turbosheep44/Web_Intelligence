from json import dumps as json_dumps
from json import load as load_json
from ast import literal_eval
from os import makedirs, path
from math import log
from sys import argv as cmd_args


# given the term by document matrix and a document to search ('searchDoc'),
# this method calculates the TF.IDF value for 'word'
def word_tf_idf(term_by_document_matrix, word, searchDoc):
    # Term frequency (default 0)
    tf = term_by_document_matrix[searchDoc].get(word, 0)

    # inverse document frequency
    number_of_documents = len(term_by_document_matrix.keys())
    # count how many documents the word appears in
    term_in_documents = sum(
        1 for doc in term_by_document_matrix if word in term_by_document_matrix[doc])
    idf = log(number_of_documents/term_in_documents)

    return tf * idf


# this method returns a list of TF.IDF values for each word in the given document
# according to the values in the term by document matrix
def document_tf_idf(term_by_document_matrix, document):
    tf_idf_dict = [{"text": word, "size": word_tf_idf(term_by_document_matrix, word, document)}
                   for word in term_by_document_matrix[document]]

    # filter the top values
    number_of_terms_to_keep = -1 * min(50, int(log(len(tf_idf_dict), 1.2)))

    tf_idf_dict = [
        # construct a new list from the sorted list
        {"text": t[0], "size": t[1]}
        for t in
        # sort the original list by size
        sorted(((word["text"], word["size"]) for word in tf_idf_dict),
               key=lambda x: x[1])
        # keep only the top n% of terms
        [number_of_terms_to_keep:]
    ]

    # normalise the values
    largest_word_size = max(
        tf_idf_dict, key=lambda word: word["size"])["size"]
    largest_word_size /= 100  # values will be in range (0, 100]
    for word in tf_idf_dict:
        word["size"] = word["size"]/largest_word_size

    return tf_idf_dict


# generate the term by docuent matrix from the 'documents' list, where
# each document is a list of filenames
def generate_term_by_document_matrix(documents):
    # count the terms in every document
    document_terms = {}
    for document in documents:
        current_document = {}
        for filename in documents[document]:
            with open(f"{cmd_args[3]}/" + filename, "r") as f:
                for line in f:
                    for word in line.strip().split(" "):
                        word = word.strip()
                        current_document[word] = \
                            current_document.get(word, 0)+1
        document_terms[document] = current_document
        # print("{:2}".format(filename) + " : " + str(current_document))
    return document_terms


def tf_idf(input_file, output_directory, conversion_function, output_file_name_function):
    # read the input file which contains information about
    # which files should be part of each document
    with open(input_file) as json_file:
        input_data = load_json(json_file)

    # perform conversion to documents and release memory holding input file
    documents = {}
    for node in input_data:
        key, value = conversion_function(node, input_data[node])
        documents[key] = value
    del input_data

    # generate term by document matrix
    print("Generate term by document matrix...")
    term_by_document_matrix = generate_term_by_document_matrix(documents)

    # create the output dir if it does not exist
    if not path.exists(output_directory):
        try:
            makedirs(path.dirname(output_directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # make tf_idf doc for every user pair
    counter = 0
    print(f"Total {len(documents.keys())} =>      ", end="")
    for key in documents:
        counter += 1
        print(f"\b\b\b\b\b", end="", flush=True)
        print(f"{counter:5}", end="")
        # each edge output file will have the following name format idA_idB where idA < idB
        with open(f"{output_directory}/{output_file_name_function(key)}.json", "w") as output:
            print(json_dumps(document_tf_idf(term_by_document_matrix, key)),
                  file=output)
    print("")


if __name__ == "__main__":
    print("Nodes TF.IDF")
    tf_idf(f"{cmd_args[1]}",
           f"{cmd_args[2]}/tf_idf_nodes/",
           lambda key, value: (value["id"],
                               set(value["sent"] + value["received"])),
           lambda key: key)
    print("Edges TF.IDF")
    tf_idf(f"{cmd_args[2]}/edges.json",
           f"{cmd_args[2]}/tf_idf_edges/",
           lambda key, value: (frozenset(literal_eval(key)), value),
           lambda key: '_'.join(str(user_id) for user_id in sorted(key)))
