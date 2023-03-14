from unittest import TestCase

from documents import TransformedDocument
from index import DictBasedInvertedIndexWithFrequencies, ListBasedInvertedIndexWithFrequencies
from query_expansion import ThesaurusQueryExpander
from search_api import Query


class TestQueryExpansion(TestCase):
    def test_process_query(self):
        # Load in alternatives.
        query_expander = ThesaurusQueryExpander(
            {'word1': ['alt1', 'alt2'], 'word2': ['alt3', 'alt4'], 'word3': ['alt5', 'alt6']})
        # Test that the expander returns the correct alternatives in the right format.
        self.assertEqual({'word1': ['alt1', 'alt2'], 'word3': ['alt5', 'alt6']},
                         query_expander.process_query(['word0', 'word1', 'word3', 'word4', 'word5']))
        # Make sure no unintended things were added to the internal data structure in the process.
        self.assertEqual({'word1': ['alt1', 'alt2'], 'word2': ['alt3', 'alt4'], 'word3': ['alt5', 'alt6']},
                         query_expander.term_alternatives)

    def test_expanded_query_index_search(self):
        #  Build a test query with alternatives:
        query = Query(
            terms=['happy', 'covid', 'rug'],
            alternatives={'covid': ['coronavirus', 'covid-19'],
                          'happy': ['joyful', 'delighted'],
                          'rug': ['carpet', 'mat'],
                          'spongy': ['sponge-like', 'squashy', 'squishy']},
            num_results=10)
        # Build some test documents:
        sample_docs = {'1': ['happy', 'other-word', 'rug', 'covid'],
                       '2': ['happy', 'other-word', 'squashy', 'mat'],
                       '3': ['tokens4', 'token5', 'token6'],
                       '4': ['other-word', 'coronavirus', 'delighted', 'mat'],
                       '5': ['cactus', 'candy', 'other-word', 'candle', 'other-word2'],
                       '6': ['tokens4', 'token5', 'token6'],
                       '7': ['sponge-like', 'squashy', 'squishy'],
                       '8': ['tokens4', 'token5', 'token6'],
                       '9': ['covid-19', 'rug', 'mat', 'happy', 'other-word']}
        # Add the test document to the index:
        dict_index = DictBasedInvertedIndexWithFrequencies('')
        for doc_id, tokens in sample_docs.items():
            dict_index.add_document(TransformedDocument(doc_id=doc_id, tokens=tokens))
        # Make sure that the index search returns only the documents that match ALL terms (or at least one of their alternatives).
        self.assertCountEqual(['1', '4', '9'], dict_index.search(query).result_doc_ids)


    def test_expanded_list_query_index_search(self):
        #  Build a test query with alternatives:
        query = Query(
            terms=['happy', 'covid', 'rug'],
            alternatives={'covid': ['coronavirus', 'covid-19'],
                          'happy': ['joyful', 'delighted'],
                          'rug': ['carpet', 'mat'],
                          'spongy': ['sponge-like', 'squashy', 'squishy']},
            num_results=10)
        # Build some test documents:
        sample_docs = {'1': ['happy', 'other-word', 'rug', 'covid'],
                       '2': ['happy', 'other-word', 'squashy', 'mat'],
                       '3': ['tokens4', 'token5', 'token6'],
                       '4': ['other-word', 'coronavirus', 'delighted', 'mat'],
                       '5': ['cactus', 'candy', 'other-word', 'candle', 'other-word2'],
                       '6': ['tokens4', 'token5', 'token6'],
                       '7': ['sponge-like', 'squashy', 'squishy'],
                       '8': ['tokens4', 'token5', 'token6'],
                       '9': ['covid-19', 'rug', 'mat', 'happy', 'other-word']}
        # Add the test document to the index:
        dict_index = ListBasedInvertedIndexWithFrequencies('')
        for doc_id, tokens in sample_docs.items():
            dict_index.add_document(TransformedDocument(doc_id=doc_id, tokens=tokens))
        # Make sure that the index search returns only the documents that match ALL terms (or at least one of their alternatives).
        self.assertCountEqual(['1', '4', '9'], dict_index.search2(query).result_doc_ids)