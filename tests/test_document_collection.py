from typing import Iterator

from documents import DictDocumentCollection, InputDocument
from indexing_process import *
from unittest import TestCase


class TestDictDocumentCollection(TestCase):
    def test_get_doc(self):
        test_docs = [InputDocument(doc_id='0', title='', text='d1'),
                     InputDocument(doc_id='1', title='', text='d2'),
                     InputDocument(doc_id='2', title='', text='d3')]
        dict_collection = DictDocumentCollection()
        for doc in test_docs:  # Insert and check for test documents:
            dict_collection.insert(doc)
            self.assertEqual(dict_collection.get_doc(doc.doc_id), doc)

    def test_get_batch(self):
        test_docs = [InputDocument(doc_id='0', title='', text='d1'),
                     InputDocument(doc_id='1', title='', text='d2'),
                     InputDocument(doc_id='2', title='', text='d3')]
        dict_collection = DictDocumentCollection()
        for doc in test_docs:  # Insert test documents:
            dict_collection.insert(doc)

        sub_collection = dict_collection.get_docs(['0', '2', '4'])  # Get a subset of the documents.
        self.assertIsInstance(sub_collection, DictDocumentCollection)  # Test the return type is another document collection.
        # Make sure only the correct documents are in the collection:
        self.assertEqual(sub_collection.documents, {
            '0': InputDocument(doc_id='0', title='', text='d1'),
            '2': InputDocument(doc_id='2', title='', text='d3')})

    def test_invalid(self):
        dict_collection = DictDocumentCollection()
        dict_collection.insert('fake')
        dict_collection.insert(None)
        self.assertEqual(dict_collection.documents, {})  # Make sure nothing was added above.
        self.assertIsNone(dict_collection.get_doc('invalid_id'))  # An Invalid id should return None.

    def test_iterator(self):
        dict_collection = DictDocumentCollection()
        dict_collection.insert(InputDocument(doc_id='0', title='', text='d1'))
        dict_collection.insert(InputDocument(doc_id='1', title='', text='d2'))
        dict_collection.insert(None)

        collection_iter = dict_collection.__iter__()  # Get iterator.
        # Check that the function returned an iterator.
        self.assertIsInstance(collection_iter, Iterator, 'Did not return Iterator')
        for item in collection_iter:  # Make sure the type of each item is InputDocument:
            self.assertIsInstance(item, InputDocument, 'Iterator item is not of type InputDocument')
