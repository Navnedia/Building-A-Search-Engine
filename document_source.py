import abc
import json
from abc import ABC

from documents import InputDocument, DocumentCollection, DictDocumentCollection


class DocumentSource(ABC):
    """
    Text Acquisition component of the Indexing Process.

    This can be a feed or a crawled source, though the current interface reads all documents
    at the same time.
    """

    @abc.abstractmethod
    def read(self) -> DocumentCollection:
        """
        Get documents from this source.

        :return: The DocumentCollection of all documents from this source.
        """
        pass


class WikiJsonDocumentSource(DocumentSource):
    def __init__(self, file_path: str):
        """
        A DocumentSource implementation that uses JSON files formatted like wiki_small.json
        to read in the data and build a collection of documents.

        :param file_path: The string path and name of the JSON file
        """
        self.file_path = file_path

    def read(self) -> DocumentCollection:
        with open(self.file_path) as fp:  # Open raw json file and load contents.
            data = json.load(fp)
        # For every record in the file, construct an InputDocument with the raw text and
        # add it to the document collection.
        doc_collection = DictDocumentCollection()  # Create the new document collection.
        for record in data:
            doc_collection.insert(InputDocument(record['id'], record['init_text']))

        return doc_collection