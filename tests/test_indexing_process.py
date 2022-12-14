from testing_indexing_process_fakes import *
from unittest import TestCase


class TestDefaultIndexingProcess(TestCase):
    def test_index_default_process(self):
        source = FakeDocumentSource(FakeDocumentCollection.from_str_list(['d1', 'd2']))
        self.assertEqual(source.read().get_doc('0'), InputDocument(doc_id='0', title='', text='d1'))
        indexing_process = DefaultIndexingProcess(FakeDocumentTransformer(), NaiveIndexer(''))
        index = indexing_process.run(source)
        self.assertEqual(index.docs, [
            TransformedDocument('0', ['d1']),
            TransformedDocument('1', ['d2']),
        ])
