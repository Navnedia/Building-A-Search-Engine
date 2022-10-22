import json
from typing import List, Set, Tuple, Dict
from collections import Counter, defaultdict

from counters import CounterBasedTextCounter, count_total_words
from tokenizer import NaiveTokenizer


def get_small_wiki_text() -> List[str]:
    """
    Load in text fields from wiki_small.json

    :return: A list of document text strings.
    """
    with open('wiki_small.json') as fp:
        return [doc['init_text'] for doc in json.load(fp) if doc['init_text']]


def dump_to_file(data, filepath: str):
    """
    Outputs data into a json file.

    :param data: The data to write to the file.
    :param filepath: The string path and name of the JSON file to write data to.
    """
    with open(filepath, 'w') as fp:
        json.dump(data, fp)


def compute_document_counts(docs: List[str]) -> Counter:
    """
    Get a count of how many documents each token appears in.

    :param docs: A list of document text strings.
    :return: A counter for number of documents each token is in.
    """
    tokenizer = NaiveTokenizer()
    document_counts = Counter()
    for doc in docs:
        # Tokenize each document into a set & add update the count totals.
        tokens = set(tokenizer.tokenize(doc))
        document_counts.update(tokens)

    return document_counts


def compute_stopwords(docs: List[str]) -> Set[str]:
    """
    Generate stop words to ignore by picking words that occur often, and in most documents. These
    words can be ignored because they won't help to narrow down the search results much.

    :param docs: A list of document text strings.
    :return: A set of stop words to ignore.
    """
    total_counts = count_total_words(docs)  # Total counts for tokens in every document.
    document_counts = compute_document_counts(docs)  # Number of documents each token appears in.
    most_common = {token for token, count in total_counts.most_common(20)}  # 20 most common tokens over all documents.
    common_across_docs = {token for token, count in document_counts.items() if count >= 9}  # Tokens that appear in at least 9 documents.

    return most_common.intersection(common_across_docs)  # Tokens in both sets are common enough to be considered irrelevant stop words.


def get_best_terms(texts: List[str], stopwords: Set[str]) -> List[List[Tuple[str, int]]]:
    """
    Calculate the most useful terms for each document. A term is useful if it is a common
    word in the document, but is not in the list of stop words.

    :param texts: A list of document text strings.
    :param stopwords: A Set of word strings to ignore.
    :return: A list of lists with tuples for the best terms and there associated count.
    """
    best_terms = []
    for text in texts:
        # Get word counts for each text.
        word_counter = CounterBasedTextCounter().count_words(text)
        for word in stopwords:  # Remove stopwords.
            del word_counter[word]
        best_terms.append(word_counter.most_common(10))  # Add the 10 most common words for this document.

    return best_terms


def create_inverted_index(docs: List[str]) -> Dict[str, Set[int]]:
    """
    Generate an inverted index for the document tokens. The inverted index will be a
    dictionary where the keys are tokens, and the value is a set of document indexes
    matching the token.

    :param docs: A list of document text strings.
    :return: The inverted index dictionary.
    """
    inverted_index = defaultdict(set)
    tokenizer = NaiveTokenizer()
    for i, text in enumerate(docs):
        tokens = tokenizer.tokenize(text)  # Tokenize each document.
        for token in tokens:
            # Add each token in the document to the inverted index. The token is the key,
            # and we add the current document index to the set of document the token appears in.
            inverted_index[token].add(i)

    return inverted_index


def search_2_words(word1: str, word2: str, index: Dict[str, Set[int]]) -> Set[int]:
    """
    Get results for document indexes that match BOTH the two query words.

    :param word1: The first query word to match.
    :param word2: The second query word to match.
    :param index: An inverted index dictionary containing the token words as the key,
        and a set of indexes matching to token as a value. See create_inverted_index.
    :return: A set of document indexes matching the query words.
    """
    return index[word1].intersection(index[word2])  # The set of document indexes that match both words.


def search_query(query: str, index: Dict[str, Set[int]]) -> Set[int]:
    """
    Get results for document indexes that match ALL the tokens in the query string.

    :param query: A string of query words to match.
    :param index: An inverted index dictionary containing the token words as the key,
        and a set of indexes matching to token as a value. See create_inverted_index.
    :return: A set of document indexes matching the tokens in the query string.
    """
    query_tokens = NaiveTokenizer().tokenize(query)
    token_matches = [index[token] for token in query_tokens]  # Get the index set for each token in the query.
    if not len(token_matches):  # If the token match sets is empty, then return an empty set.
        return set()
    return set.intersection(*token_matches)  # Take the intersection of all the query token matches.
