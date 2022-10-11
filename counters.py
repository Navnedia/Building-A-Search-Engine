import abc
import json
from abc import ABC
from collections import defaultdict, Counter
from typing import Dict, List
from indexing_process import NaiveTokenizer


class TextCounter(ABC):
    @classmethod
    @abc.abstractmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        pass


class DictBasedTextCounter(TextCounter):
    @classmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        counts = dict()
        for char in text:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
        return counts


class DefaultDictBasedTextCounter(TextCounter):
    @classmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        counts = defaultdict(int)
        for char in text:
            counts[char] += 1
        return counts


class CounterBasedTextCounter(TextCounter):
    @classmethod
    def count_characters(cls, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(text)
        return counts

    @classmethod
    def count_words(cls, text: str) -> Dict[str, int]:
        counts = Counter()
        counts.update(NaiveTokenizer().tokenize(text))
        return counts


def get_small_wiki():
    with open('wiki_small.json') as fp:
        return json.load(fp)


def get_texts_from_data(data) -> List[str]:
    return [d['init_text'] for d in data if d['init_text']]


def count_characters_in_small_wiki(filename: str):
    with open(filename) as fp:
        records = json.load(fp)
    return CounterBasedTextCounter.count_characters(records[0]['init_text'])


def count_words_in_small_wiki(filename: str):
    with open(filename) as fp:
        records = json.load(fp)
    return CounterBasedTextCounter.count_words(records[0]['init_text'])


def count_total_words(texts_list: List[str]) -> Counter:
    counts = Counter()
    for text in texts_list:
        counts.update(CounterBasedTextCounter.count_words(text))
    return counts
