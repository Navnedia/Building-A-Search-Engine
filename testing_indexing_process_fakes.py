from indexing_process import *


class FakeDocumentCollection(DocumentCollection):
    def __init__(self, docs: List[InputDocument]):
        self.docs = docs

    @classmethod
    def from_str_list(cls, docs: List[str]):
        return cls([InputDocument(doc_id=str(i), text=doc) for i, doc in enumerate(docs)])

    def insert(self, doc: InputDocument) -> None:
        self.docs.append(doc)

    def get_doc(self, doc_id):
        return next((d for d in self.docs if d.doc_id == doc_id), None)

    def get_docs(self, doc_ids: Iterable[str]):
        return FakeDocumentCollection([d for d in self.docs if d.doc_id in doc_ids])

    def __iter__(self):
        return self.docs.__iter__()


class FakeDocumentSource(DocumentSource):
    def __init__(self, doc_collection: DocumentCollection):
        self.doc_collection = doc_collection

    def read(self):
        return self.doc_collection


class FakeDocumentTransformer(DocumentTransformer):
    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        return TransformedDocument(doc.doc_id, doc.text.split())


class FakeIndex(Index):
    def __init__(self):
        self.docs = []

    def add_document(self, doc: TransformedDocument) -> None:
        self.docs.append(doc)


class FakeIndexer(Indexer):
    def create_index(self) -> Index:
        return FakeIndex()
