import abc
import re
from abc import ABC
from typing import List


class Tokenizer(ABC):
    """
    A utility class interface for processing text into tokens for searching.
    This class abstracts the tokenization process to allow for different implementations
    and parameters.
    """

    @abc.abstractmethod
    def tokenize(self, data: str) -> List[str]:
        """
        Processes the raw string input by splitting it into tokens.

        :param data: The raw text string to break into separate tokens
        :return: A list strings containing the original text separated into tokens
        """
        pass


class NaiveTokenizer(Tokenizer):
    """
    A utility class for processing text into tokens for searching.

    This class implements tokenization by taking a minimal/naive approach.
    Text made lowercase and is broken up into tokens of individual words
    and punctuation separated. Punctuation is NOT removed.
    """

    def tokenize(self, data: str) -> List[str]:
        tokens = re.sub(r'(\W)', r' \1 ', data.lower())  # Split off all non-word chars.
        tokens = re.sub(r'(\w+)\s(\')\s(\w+)', r'\1\2\3', tokens)  # Fix apostrophes in the middle of words by removing spaces from previous step.
        tokens = re.sub(r'\.\s+\.\s+\.', r' ...', tokens)  # When we see three periods separated by spaces, group them into one '...' ellipsis token.
        return tokens.split()  # Split processed string into tokens.
