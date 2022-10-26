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

        :param file_path: The string path and name of the JSON file.
        """
        self.file_path = file_path

    def read(self) -> DocumentCollection:
        with open(self.file_path) as fp:  # Open raw json file and load contents.
            data = json.load(fp)
        # For every record in the file, construct an InputDocument with the raw text and
        # add it to the document collection.
        doc_collection = DictDocumentCollection()  # Create the new document collection.
        for record in data:
            doc_collection.insert(InputDocument(doc_id=record['id'], text=record['init_text']))

        return doc_collection


class TrecCovidJsonlSource(DocumentSource):
    def __init__(self, file_path: str):
        """
        A DocumentSource implementation that uses JSONL files formatted like the trec
        covid corpus.jsonl with a json record on each line of the file. This JSONL file
        is read in, and the data is used build a collection of documents.

        :param file_path: The string path and name of the JSONL file.
        """
        self.file_path = file_path

    def read(self) -> DocumentCollection:
        doc_collection = DictDocumentCollection()
        with open(self.file_path, 'r') as fp:  # Open raw jsonl file and load contents.
            # For each line of the file, parse the line as json, and add the record to the collection:
            for line in fp:
                record = json.loads(line)
                doc_collection.insert(InputDocument(doc_id=record['_id'], text=record['text']))

        return doc_collection
