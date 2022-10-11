from unittest import TestCase
from indexing_process import NaiveTokenizer


class Test(TestCase):
    def test_tokenize_splits_word(self):
        self.assertEqual(NaiveTokenizer.tokenize('word1 word2'), ['word1', 'word2'])

    def test_tokenize_comma(self):
        self.assertEqual(NaiveTokenizer.tokenize('For now, we are here'), ['for', 'now', ',', 'we', 'are', 'here'])

    def test_tokenize_period(self):
        self.assertEqual(NaiveTokenizer.tokenize('For now, we are here.'), ['for', 'now', ',', 'we', 'are', 'here', '.'])

    def test_tokenize_non_word_chars(self):
        self.assertEqual(NaiveTokenizer.tokenize('10% of $10 is $1'), ['10', '%', 'of', '$', '10', 'is', '$', '1'])

    def test_tokenize__apostrophe(self):
        self.assertEqual(NaiveTokenizer.tokenize('He said \'Isn\'t O\'Brian the best?\''),
                         ['he', 'said', '\'', 'isn\'t', 'o\'brian', 'the', 'best', '?', '\''])

    def test_tokenize__ellipsis(self):
        self.assertEqual(NaiveTokenizer.tokenize('More...'), ['more', '...'])
