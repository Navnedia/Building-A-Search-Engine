from unittest import TestCase
from counters import DictBasedTextCounter, DefaultDictBasedTextCounter, CounterBasedTextCounter

counter_imls = [DictBasedTextCounter, DefaultDictBasedTextCounter, CounterBasedTextCounter]


class TestDictBasedTextCounter(TestCase):
    def test_count_characters(self):
        for counter in counter_imls:
            with self.subTest(msg=str(counter)):
                self.assertEqual({'a': 2, 'b': 2, 'c': 1, ',': 1}, counter.count_characters('abcab,'))
