import abc
from abc import ABC
import dataclasses
from dataclasses import asdict
import __future__
from typing import *
import json
import re


@dataclasses.dataclass
class InputDocument:
    """
    Common raw document representation as produced by Text Acquisition stage.

    This representation is stored in the DocumentCollection.
    """
    doc_id: str
    text: str


@dataclasses.dataclass
class TransformedDocument:
    """
    Document representation after the Text Transformation stage.

    This representation is the input to the Indexing stage.
    """
    doc_id: str
    tokens: List[str]


class DocumentCollection(ABC):
    """
    Collection of InputDocuments.

    Abstracts Document Data Store.
    Produced and updated by the indexing process.
    Used by Query Process for User Interactions.
    """

    @abc.abstractmethod
    def insert(self, doc: InputDocument) -> None:
        """
        Add a document into the document collection.

        :param doc: An InputDocument to add to the collection
        :return: None
        """
        pass

    @abc.abstractmethod
    def get_doc(self, doc_id: str) -> InputDocument:
        """
        Get a document by document ID.

        :param doc_id: ID of the document to return
        :return: An InputDocument for the given doc_id
        """
        pass

    @abc.abstractmethod
    def get_docs(self, doc_ids: Iterable[str]) -> 'DocumentCollection':
        """
        Batch get.

        :param doc_ids: IDs of the documents to retrieve
        :return: A collection of documents with the given IDs.
        """
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[InputDocument]:
        """
        :return: Iterator over all documents in the collection
        """
        pass


class DocumentSource(ABC):
    """
    Text Acquisition component of the Indexing Process.

    This can be a feed or a crawled source, though the current interface reads all documents
    at the same time (i.e..
    """

    @abc.abstractmethod
    def read(self) -> DocumentCollection:
        """
        Get documents from this source.

        :return: The DocumentCollection of all documents from this source.
        """
        pass


class Tokenizer(ABC):
    """
    A utility class interface for processing text into tokens for searching.
    This class abstracts the tokenization process to allow for different implementations
    and parameters.
    """

    @staticmethod
    @abc.abstractmethod
    def tokenize(data: str) -> List[str]:
        """
        Processes the raw string input by splitting it into tokens.

        :param data: The raw text string to break into separate tokens
        :return: A list strings containing the original text separated into tokens
        """
        pass


class DocumentTransformer(ABC):
    """
    Text Transformation component of the Index Process.

    Text normalization and tokenization is expected to be part of this component.
    """

    @abc.abstractmethod
    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        pass


@dataclasses.dataclass
class Query:
    tokens: List[str]


@dataclasses.dataclass
class SearchResults:
    doc_ids: List[str]


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


class DictDocumentCollection(DocumentCollection):
    """A DocumentCollection implementation that operates using a dictionary."""

    def __init__(self):
        self.documents = {}

    def insert(self, doc: InputDocument) -> None:
        # If the input is an instance of InputDocument, then add it to the dictionary with the id as the key.
        if isinstance(doc, InputDocument):
            self.documents[doc.doc_id] = doc

    def get_doc(self, doc_id: str) -> InputDocument | None:
        return self.documents.get(doc_id)  # Return the InputDocument, or None if not found.

    def get_docs(self, doc_ids: Iterable[str]) -> 'DocumentCollection':
        doc_collection = DictDocumentCollection()  # Create a new document collection.
        for requested_id in doc_ids:  # For each of the requested ID's, add the document to the collection:
            doc_collection.insert(self.documents.get(requested_id))

        return doc_collection

    def __iter__(self) -> Iterator[InputDocument]:
        return iter(self.documents.values())


class WikiJsonDocumentSource(DocumentSource):
    def __init__(self, file_path: str):
        """
        A DocumentSource implementation that uses JSON files to read in the data and build
        a collection of documents.

        :param file_path: The string path and name of the JSON file
        """
        self.file_path = file_path

    def read(self) -> DocumentCollection:
        with open(self.file_path) as fp:  # Open raw json file and load contents.
            records = json.load(fp)
        # For every record in the file, construct an InputDocument with the raw text and
        # add it to the document collection.
        doc_collection = DictDocumentCollection()  # Create the new document collection.
        for record in records:
            doc_collection.insert(InputDocument(record['id'], record['init_text']))

        return doc_collection


class NaiveTokenizer(Tokenizer):
    """
    A utility class for processing text into tokens for searching.

    This class implements tokenization by taking a minimal/naive approach.
    Text made lowercase and is broken up into tokens of individual words
    and punctuation separated. Punctuation is NOT removed.
    """

    @staticmethod
    def tokenize(data: str) -> List[str]:
        tokens = re.sub(r'(\W)', r' \1 ', data.lower())  # Split off all non-word chars.
        tokens = re.sub(r'(\w+)\s(\')\s(\w+)', r'\1\2\3', tokens)  # Fix apostrophes in the middle of words by removing spaces from previous step.
        tokens = re.sub(r'\.\s+\.\s+\.', r' ...', tokens)  # When we see three periods separated by spaces, group them into one '...' ellipsis token.
        return tokens.split()  # Split processed string into tokens.


class NaiveSearchDocumentTransformer(DocumentTransformer):
    def __init__(self, tokenizer: Tokenizer):
        """
        A DocumentTransformer implementation that runs the supplied tokenizer.

        :param tokenizer: A tokenizer instance that will be used in document transformation.
        """
        self.tokenizer = tokenizer

    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        """
        Creates TransformedDocument from the given InputDocument by tokenizing its text.
        Uses the tokenizer instance supplied in the constructor.

        :param doc: The InputDocument to be transformed.
        :return: The transformed document
        """
        return TransformedDocument(doc_id=doc.doc_id, tokens=self.tokenizer.tokenize(doc.text))


class NaiveIndex(Index):
    def __init__(self, file_path: str):
        """
        Index that is the final output of the Indexing Process and the main source for Query Process.

        A Naive implementation of index.

        :param file_path: The string path and name of the JSON file to read and write the index to.
        """
        self.docs = []
        self.file_path = file_path

    def add_document(self, doc: TransformedDocument) -> None:
        self.docs.append(doc)

    def search(self, query: Query) -> SearchResults:
        pass

    def read(self):
        with open(self.file_path, 'r') as fp:  # Open the index file and read in data:
            index_records = json.load(fp)
        # For each document in the records, construct a TransformedDocument obj and add it to the list:
        for document in index_records:
            self.docs.append(TransformedDocument(doc_id=document['doc_id'], tokens=document['tokens']))

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


class DefaultIndexingProcess:
    """
    Simple implementation of the indexing process.

    This class runs components of the indexing process supplied to it either in the constructor
    or in the arguments to the |run| function below.
    """

    def __init__(self, document_transformer: DocumentTransformer, indexer: Indexer):
        self.document_transformer = document_transformer
        self.indexer = indexer

    def run(self, source: DocumentSource) -> Index:
        """
        Runs the Indexing Process using the supplied components.

        :param source: Source of documents to index.
        :return: An index used to search documents from the given source.
        """
        # Run the acquisition stage, or just load the results of that stage. Enable iteration over
        # all documents from the given source.
        document_collection = source.read()
        # Create an empty index. Documents will be added one at a time.
        index = self.indexer.create_index()
        for doc in document_collection:
            # Transform and index the document.
            transformed_doc = self.document_transformer.transform_document(doc)
            index.add_document(transformed_doc)

        return index
