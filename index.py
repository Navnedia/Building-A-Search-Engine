import abc
import json
import math
from abc import ABC
from collections import defaultdict, Counter
from dataclasses import asdict
from typing import List

from documents import TransformedDocument
from search_api import Query, SearchResults


class Index(ABC):
    """
    Index that is the final output of the Indexing Process and the main source for Query Process.
    """

    @abc.abstractmethod
    def add_document(self, doc: TransformedDocument) -> None:
        """
        Add a new transformed document to be saved in the index.

        :param doc: A TransformedDocument to add to the index
        :return: None
        """
        pass

    @abc.abstractmethod
    def search(self, query: Query) -> SearchResults:
        """
        Takes a Query dataclass and finds matching SearchResults by searching through
        the indexed documents.

        :param query: The structured Query representation with terms as tokens.
        :return: A structured representation of search results containing the doc_ids.
        """
        pass

    @abc.abstractmethod
    def read(self):
        """Read in data from the file_path specified in the index class constructor."""
        pass

    @abc.abstractmethod
    def write(self):
        """Write out data to the file_path specified in the index class constructor."""
        pass


class Indexer(ABC):
    """Factory class for Index"""

    @abc.abstractmethod
    def create_index(self) -> Index:
        """
        Creates a new Index class with the appropriate factory parameters

        :return: An instance of an Index class created with the supplied parameters.
        """
        pass


class NaiveIndex(Index):
    def __init__(self, file_path: str):
        """
        Index that is the final output of the Indexing Process and the main source for Query Process.

        A Naive implementation of Index.

        :param file_path: The string path and name of the JSON file to read and write the index to.
        """
        self.docs: List[TransformedDocument] = []
        self.file_path = file_path

    def add_document(self, doc: TransformedDocument) -> None:
        self.docs.append(doc)

    def search(self, query: Query) -> SearchResults:
        query_terms = set(query.terms)  # Convert query terms to a set, so we can use set operations like subset.
        # Check for the query terms in each indexed document; record the doc_id if yes:
        # Return results with the SearchResults dataclass.
        return SearchResults(
            result_doc_ids=[document.doc_id for document in self.docs if query_terms.issubset(document.tokens)])

    def read(self):
        with open(self.file_path, 'r') as fp:  # Open the index file and read in data:
            index_records = json.load(fp)
        # For each document in the records, load a TransformedDocument into the list.
        self.docs = [TransformedDocument(doc_id=document['doc_id'], tokens=document['tokens'])
                     for document in index_records]

    def write(self):
        # Create a new list converting the TransformedDocuments to dictionaries.
        dict_docs = [asdict(document) for document in self.docs]
        with open(self.file_path, 'w') as fp:  # Open the index file and write out data:
            json.dump(dict_docs, fp)


class NaiveIndexer(Indexer):
    def __init__(self, file_path: str):
        """
        A Factory class for NaiveIndex

        :param file_path: The string path and name of the JSON file for indexes to read and write to.
        """
        self.file_path = file_path

    def create_index(self) -> Index:
        return NaiveIndex(self.file_path)


def term_frequency(term_count: int, document_length: int) -> float:
    """
    Calculate the frequency of a term in the document, that is the number of times
    it occurs, relative to the length of the document.

    :param term_count: The number of times the term occurs in the document.
    :param document_length: The length or number of tokens in the document.
    :return: The term frequency.
    """
    return term_count / document_length


def inverse_document_frequency(term_document_count: int, number_of_documents: int) -> float:
    """
    Calculate the inverse document frequency for a given term.

    :param term_document_count: The number of documents a term occurs in.
    :param number_of_documents: The total number of documents.
    :return: The inverse document frequency.
    """
    return math.log(number_of_documents / term_document_count)


class ListBasedInvertedIndexWithFrequencies(Index):
    def __init__(self, file_path: str):
        """
        Index that is the final output of the Indexing Process and the main source for Query Process.

        A list based implementation of invert Index including ordering results by TF-IDF.

        :param file_path: The string path and name of the JSONL file to read and write the index to.
        """
        self.file_path = file_path
        self.num_documents = 0  # Number of documents in the index.
        # Inverted index dict mapping a term to a list of pairs (doc_id, term_frequency).
        # Ex: {'word1': [('f8dhg68', 0.013), ('ukj7sy6', 0.02), ('we34rh0', 0.01)], 'word2':  [('mk2gr52', 0.003)]}
        self.term_to_doc_id_and_frequencies = defaultdict(list)
        self.doc_counts = Counter()  # The number of documents each term occurs in.

    def add_document(self, doc: TransformedDocument) -> None:
        self.num_documents += 1  # Update number of documents in index.
        term_counts = Counter(doc.tokens)  # Number of term occurrences for this document.
        for term, count in term_counts.items():  # For each unique term in the document:
            self.doc_counts[term] += 1
            # Add this doc_id and term frequency to the current terms inverted index entry.
            self.term_to_doc_id_and_frequencies[term].append(
                (doc.doc_id, term_frequency(count, len(doc.tokens))))

    def search(self, query: Query) -> SearchResults:
        match_scores = defaultdict(float)  # Total TF-IDF scores for each document matching the terms.
        match_counts = defaultdict(int)  # Number of query terms each document matched for.
        for term in query.terms:
            # If a term is not found anywhere in the index, then we return empty results,
            # because each query term must be present in the matches.
            if term not in self.term_to_doc_id_and_frequencies:
                # If we want to ignore terms with no matches, we can do continue here to move to the next term.
                return SearchResults([])
            # Calculate the inverse document frequency for the given term.
            idf = inverse_document_frequency(self.doc_counts[term], self.num_documents)
            for doc_id, tf in self.term_to_doc_id_and_frequencies[term]:
                # For each document matching the term, increment documents match number, and update
                # the term frequency–inverse document frequency (TF-IDF) score of the document.
                match_counts[doc_id] += 1
                match_scores[doc_id] += tf * idf

        # Remove any documents that don't match all the query words.
        match_scores = {doc_id: score for doc_id, score in match_scores.items()
                        if match_counts[doc_id] == len(query.terms)}
        # Return SearchResults ordered by the TF-IDF total query score.
        return SearchResults(sorted(match_scores.keys(), key=match_scores.get))

    def read(self):
        with open(self.file_path, 'r') as fp:
            # Read the first line metadata and store the count of documents in the index.
            self.num_documents = json.loads(fp.readline())['number_of_documents']
            # Initialize empty index & count variables:
            self.term_to_doc_id_and_frequencies = defaultdict(list)
            self.doc_counts = Counter()

            for line in fp:  # For each line, load the record into memory.
                record = json.loads(line)
                term = record['term']
                self.doc_counts[term] = record['documents_count']  # Store the documents count for the term.
                # Load the term inverted index record with the matching doc_id's, and frequency in the document:
                # Convert to a list of pairs.
                self.term_to_doc_id_and_frequencies[term] = [
                    (index_record['doc_id'], index_record['tf']) for index_record in record['index']]

    def write(self):
        with open(self.file_path, 'w') as fp:
            # Write a special record to the first line that stores the number of documents in the index.
            metadata = {'number_of_documents': self.num_documents}
            fp.write(json.dumps(metadata) + '\n')

            # For each unique term across all documents, create a json record with the term,
            # the number of documents it occurs in, and the inverted index with matching doc_ids
            # and the term frequency in the document. Finally, write this json record to a
            # new line in the file.
            for term, doc_count in self.doc_counts.items():
                record = {
                    'term': term,
                    'documents_count': doc_count,
                    'index': [{'doc_id': doc_id, 'tf': tf}
                              for doc_id, tf in self.term_to_doc_id_and_frequencies[term]]
                }
                fp.write(json.dumps(record) + '\n')
