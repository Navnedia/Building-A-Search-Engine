import abc
import dataclasses
from abc import ABC
from typing import List, Iterable, Iterator, Dict


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
        Add another document into this document collection.

        :param doc: An InputDocument to add to the collection.
        :return: None
        """
        pass

    @abc.abstractmethod
    def get_doc(self, doc_id: str) -> InputDocument:
        """
        Get a document by document ID.

        :param doc_id: ID of the document to return.
        :return: An InputDocument for the given doc_id.
        """
        pass

    @abc.abstractmethod
    def get_docs(self, doc_ids: Iterable[str]) -> 'DocumentCollection':
        """
        Batch get.

        :param doc_ids: IDs of the documents to retrieve.
        :return: A collection of documents with the given IDs.
        """
        pass

    @abc.abstractmethod
    def __iter__(self) -> Iterator[InputDocument]:
        """
        :return: Iterator over all documents in the collection.
        """
        pass


class DictDocumentCollection(DocumentCollection):
    """
    In memory DocumentCollection implementation that uses a dict of doc_ids and corresponding InputDocuments.
    """

    def __init__(self, docs_dict: Dict[str, InputDocument] = None):
        """
        Create a new DictDocumentCollection. Leave argument blank to create an empty instance,
        or supply an argument to include data right away.

        :param docs_dict: A dictionary with doc_ids as keys, and InputDocuments for values.
        """
        if not docs_dict:
            docs_dict = dict()
        self.documents = docs_dict

    @staticmethod
    def create_empty() -> 'DictDocumentCollection':
        """
        :return: An empty instance of DictDocumentCollection
        """
        return DictDocumentCollection(dict())

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
