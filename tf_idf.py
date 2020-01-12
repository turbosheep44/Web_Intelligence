from json import dumps as json_dumps
from json import load as load_json
from ast import literal_eval
from os import makedirs, path
from math import log as ln


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
    idf = ln(number_of_documents/term_in_documents)

    return tf * idf


# this method returns a list of TF.IDF values for each word in the given document
# according to the values in the term by document matrix
def document_tf_idf(term_by_document_matrix, document):
    return [{"text": word, "size": word_tf_idf(term_by_document_matrix, word, document)}
            for word in term_by_document_matrix[document]]


# generate the term by docuent matrix from the 'documents' list, where
# each document is a list of filenames
def generate_term_by_document_matrix(documents):
    # count the terms in every document
    document_terms = {}
    for document in documents:
        for filename in documents[document]:
            current_document = {}
            with open("messages/" + filename, "r") as f:
                for line in f:
                    for word in line.strip().split(" "):
                        word = word.strip()
                        current_document[word] = current_document.get(
                            word, 0)+1

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
    term_by_document_matrix = generate_term_by_document_matrix(documents)

    # create the output dir if it does not exist
    if not path.exists(output_directory):
        try:
            makedirs(path.dirname(output_directory))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # make tf_idf doc for every user pair
    for key in documents:
        # each edge output file will have the following name format idA_idB where idA < idB
        with open(f"{output_directory}/{output_file_name_function(key)}.json", "w") as output:
            t = document_tf_idf(term_by_document_matrix, key)
            # t.sort(key=lambda x: x["size"])
            print(json_dumps(t), file=output)


if __name__ == "__main__":
    print("Nodes TF.IDF")
    tf_idf("metadata.json",
           "output_json/tf_idf_nodes/",
           lambda key, value: (value["id"], set(
               value["sent"] + value["received"])),
           lambda key: key)
    print("Edges TF.IDF")
    tf_idf("output_json/edges.json",
           "output_json/tf_idf_edges/",
           lambda key, value: (frozenset(literal_eval(key)), value),
           lambda key: '_'.join(str(user_id) for user_id in sorted(key)))
