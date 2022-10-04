from indexing_process import *
from testing_indexing_process_fakes import *
from unittest import TestCase


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

    def test_get_batch(self):
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
