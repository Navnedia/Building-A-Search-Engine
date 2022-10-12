import hw3
from collections import Counter
from unittest import TestCase


class Test(TestCase):
    def test_compute_document_counts(self):
        self.assertEqual(
            Counter({'a': 3, 'd': 2, 'b': 2, 'c': 1, 'e': 1}),
            hw3.compute_document_counts([
                'a b c d',
                'a b d',
                'a e'
            ])
        )

    def test_compute_stopwords(self):
        # The document collection (corpus) is generated using:
        # [' '.join(['stopword1', 'stopword2'] * 2 + ['in_all_docs'] + [f'11_of_these{i}', f'11_of_those{i}'] * 11)
        #  for i in range(10)]
        # stopword1 occurres in all 10 docs, total of 20 times
        # stopword2 occurres in 9 docs, total of 18 times
        # 11_of_these{i} and 11_of_those{i} each occurres 11 time in a single document with index i.
        # in_all_docs occurres in all documents, but only occurres 10 time in the collection, so
        #   it will not make it into top 20 most common tokens.
        self.assertEqual(
            {'stopword1', 'stopword2'},
            hw3.compute_stopwords(
                [
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0 11_of_these0 11_of_those0',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1 11_of_these1 11_of_those1',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2 11_of_these2 11_of_those2',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3 11_of_these3 11_of_those3',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4 11_of_these4 11_of_those4',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5 11_of_these5 11_of_those5',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6 11_of_these6 11_of_those6',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7 11_of_these7 11_of_those7',
                    'stopword1 stopword2 stopword1 stopword2 in_all_docs 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8 11_of_these8 11_of_those8',
                    'stopword1 stopword1 in_all_docs 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9 11_of_these9 11_of_those9'
                ]
            )
        )


    def test_get_best_terms(self):
        self.assertEqual(
            [[('frequent10', 10), ('frequent9', 9), ('frequent8', 8), ('frequent7', 7),
              ('frequent6', 6), ('frequent5', 5), ('frequent4', 4), ('frequent3', 3),
              ('frequent2', 2), ('frequent1', 1)],
             [('frequent2', 2), ('frequent1', 1)]],
            hw3.get_best_terms(texts=["""
stopword1 stopword2 frequent10 frequent10 frequent10 frequent10 frequent10 frequent10 frequent10 frequent10 frequent10 frequent10
stopword1 stopword2 frequent9 frequent9 frequent9 frequent9 frequent9 frequent9 frequent9 frequent9 frequent9
stopword1 stopword2 frequent8 frequent8 frequent8 frequent8 frequent8 frequent8 frequent8 frequent8
stopword1 stopword2 frequent7 frequent7 frequent7 frequent7 frequent7 frequent7 frequent7
stopword1 stopword2 frequent6 frequent6 frequent6 frequent6 frequent6 frequent6
stopword1 stopword2 frequent5 frequent5 frequent5 frequent5 frequent5
stopword1 stopword2 frequent4 frequent4 frequent4 frequent4
stopword1 stopword2 frequent3 frequent3 frequent3
stopword1 stopword2 frequent2 frequent2
stopword1 stopword2 frequent1
stopword1 stopword2 
""", """
stopword1 stopword2 frequent2 frequent2
stopword1 stopword2 frequent1
stopword1 stopword2 
"""],
                               stopwords={'stopword1', 'stopword2'}))

    def test_create_inverted_index(self):
        self.assertEqual(
            {'a': {0}, 'b': {0, 1}, 'c': {0, 1, 2}, 'd': {1, 2}, 'e': {2}},
            hw3.create_inverted_index(['a b c', 'b c d', 'c d e']))

    def test_search_2_words(self):
        self.assertEqual(
            {1},
            hw3.search_2_words(
                'b', 'd', index={'a': {0}, 'b': {0, 1}, 'c': {0, 1, 2}, 'd': {1, 2}, 'e': {2}}))

    def test_search_query(self):
        self.assertEqual(
            {1, 3},
            hw3.search_query(
                'b d e', index={'a': {0}, 'b': {0, 1, 3}, 'c': {0, 1, 2}, 'd': {1, 2, 3}, 'e': {1, 2, 3}}))
        # Test empty:
        self.assertEqual(set(), hw3.search_query('', index={'a': {0}, 'b': {0, 1, 3}, 'c': {0, 1, 2}}))
