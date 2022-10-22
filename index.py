import abc
import json
from abc import ABC
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

        A Naive implementation of index.

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
