import abc
import json
from abc import ABC
from typing import List, Dict
from collections import defaultdict


class QueryExpander(ABC):
    """
    An abstract class for generating/expanding the query with related alternative terms.
    """

    @abc.abstractmethod
    def add_alternatives(self, term: str, alternatives: List[str]) -> None:
        """
        Add a term with alternatives to the internal reference for future queries.

        :param term: The term you want to add.
        :param alternatives: A list of alternatives for the given term.
        """
        pass

    @abc.abstractmethod
    def get_alternatives(self, term: str) -> List[str]:
        """
        Get the alternative terms for the specified term.

        :param term: The specific term you want to look up.
        :return: A list of alternative terms.
        """
        pass

    @abc.abstractmethod
    def process_query(self, terms: List[str]) -> Dict[str, List[str]]:
        """
        Process terms to generate a set of alternative terms for each when alternative exist.

        :param terms: A list of term tokens to generate alternative terms from.
        :return: A dictionary mapping the original term to a list of alternative terms.
        """
        pass


class TermAlternativesSource(ABC):
    """
    An abstract source reader for loading in alternative terms to use in query expansion.
    """

    @abc.abstractmethod
    def read(self) -> QueryExpander:
        """
        Load alternative terms from this source.

        :return: A instance of QueryExpander with all the data loaded in.
        """
        pass
