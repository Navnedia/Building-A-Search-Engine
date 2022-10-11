

def indexing_process(filename: str) -> indexing_process.Index:
    with open(filename) as fp:
        data = json.load(fp)
    Input_docments = [InputDocument(doc['doc_id'], doc['init_text']) for doc in data]
    ...

    return index

# def search(query: str, index: Index):
#     query_words = set(tokenize(query))
#     documents: List[set[str]] = ...


def search(query: str, documents: List[Set[str]]):
    query_words = set(tokenize(query))
    match_count_dict = dict()
    for word in query_words:
        for i, doc in enumerate(documents):
            if word in doc:
                if i in match_count_dict:
                    match_count_dict[i] += 1
                else:
                    match_count_dict[i] = 1
    matching_ids = [i for i, count in match_count_dict.items() if count == len(query_words)]
