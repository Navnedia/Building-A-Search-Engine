from indexing_process import *
from testing_indexing_process_fakes import *
from unittest import TestCase


class TestDefaultIndexingProcess(TestCase):
    def test_run(self):
        source = FakeDocumentSource(FakeDocumentCollection.from_str_list(["d1", "d2"]))
        self.assertEqual(source.read().get_doc("0"), InputDocument(doc_id="0", text="d1"))
        indexing_process = DefaultIndexingProcess(FakeDocumentTransformer(), FakeIndexer())
        index = indexing_process.run(source)
        self.assertEqual(index.docs, [
            TransformedDocument("0", ["d1"]),
            TransformedDocument("1", ["d2"]),
        ])


