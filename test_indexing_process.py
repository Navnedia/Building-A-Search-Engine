from indexing_process import *
from testing_indexing_process_fakes import *
from unittest import TestCase


# Should I put these other tests in a separate file?
class TestDefaultIndexingProcess(TestCase):
    def test_index_default_process(self):
        source = FakeDocumentSource(FakeDocumentCollection.from_str_list(['d1', 'd2']))
        self.assertEqual(source.read().get_doc('0'), InputDocument(doc_id='0', text='d1'))
        indexing_process = DefaultIndexingProcess(FakeDocumentTransformer(), NaiveIndexer())
        index = indexing_process.run(source)
        self.assertEqual(index.docs, [
            TransformedDocument('0', ['d1']),
            TransformedDocument('1', ['d2']),
        ])


class TestDictDocumentCollection(TestCase):
    def test_dict_doc_collection(self):
        fake_collection = FakeDocumentCollection.from_str_list(['d1', 'd2'])
        dict_collection = DictDocumentCollection()
        dict_collection.insert(InputDocument('0', 'd1'))
        dict_collection.insert(InputDocument('1', 'd2'))
        self.assertEqual(dict_collection.get_doc('0'), fake_collection.get_doc('0'))
        self.assertEqual(dict_collection.get_doc('1'), fake_collection.get_doc('1'))

    def test_insert_none(self):
        dist_collection = DictDocumentCollection()
        dist_collection.insert(None)
        self.assertEqual(dist_collection.documents, {})

    def test_get_doc_none(self):
        self.assertIsNone(DictDocumentCollection().get_doc('invalid_id'))

    def test_get_docs(self):
        fake_collection = FakeDocumentCollection.from_str_list(['d1', 'd2', 'd3'])
        dict_collection = DictDocumentCollection()
        dict_collection.insert(InputDocument('0', 'd1'))
        dict_collection.insert(InputDocument('1', 'd2'))
        dict_collection.insert(InputDocument('2', 'd3'))
        sub_collection = dict_collection.get_docs(['0', '2', '4'])
        self.assertIsInstance(sub_collection, DictDocumentCollection)
        self.assertEqual(sub_collection.get_doc('0'), fake_collection.get_doc('0'))
        self.assertEqual(sub_collection.get_doc('1'), None)
        self.assertEqual(sub_collection.get_doc('2'), fake_collection.get_doc('2'))
        self.assertEqual(sub_collection.get_doc('4'), None)

    def test_iterator(self):
        dict_collection = DictDocumentCollection()
        dict_collection.insert(InputDocument('0', 'd1'))
        dict_collection.insert(InputDocument('1', 'd2'))
        dict_collection.insert(None)
        collection_iter = dict_collection.__iter__()
        self.assertIsInstance(collection_iter, Iterator, 'Did not return Iterator')
        for item in collection_iter:
            self.assertIsInstance(item, InputDocument, 'Iterator item is not of type InputDocument')

