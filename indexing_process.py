import abc
from abc import ABC
import dataclasses
import __future__
from typing import *


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
        pass

    @abc.abstractmethod
    def search(self, query: Query) -> SearchResults:
        pass


class Indexer(ABC):
    """
    Factory class for Index
    """

    @abc.abstractmethod
    def create_index(self) -> Index:
        pass


class DictDocumentCollection(DocumentCollection):
    """
    A DocumentCollection implementation that operates using a dictionary.
    """

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


class NaiveSearchDocumentTransformer(DocumentTransformer):
    def __init__(self, tokenizer):
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
        return NaiveTransformedDocument(doc_id=doc.doc_id, tokens=self.tokenizer.tokenize(doc.text))


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
