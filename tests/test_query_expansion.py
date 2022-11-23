from unittest import TestCase

from documents import TransformedDocument
from index import DictBasedInvertedIndexWithFrequencies
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
