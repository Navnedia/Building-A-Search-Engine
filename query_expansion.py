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


class ThesaurusQueryExpander(QueryExpander):
    def __init__(self, term_alternatives: Dict[str, List[str]]):
        self.term_alternatives = term_alternatives

    def add_alternatives(self, term: str, alternatives: List[str]) -> None:
        # Add alternative for a term, unless alternatives list is empty.
        if isinstance(alternatives, list) and len(alternatives) > 0:
            self.term_alternatives[term] = alternatives

    def get_alternatives(self, term: str) -> List[str]:
        return self.term_alternatives.get(term, [])

    def process_query(self, query_terms: List[str]) -> Dict[str, List[str]]:
        synonyms = defaultdict(list)
        # Build a dictionary mapping the original query terms to a list of alternatives (synonyms):
        for term in query_terms:
            if term in self.term_alternatives:  # Don't include the term if we don't have alternatives for it.
                synonyms[term] = self.term_alternatives[term]

        return synonyms


class JsonlThesaurusTermAlternativesSource(TermAlternativesSource):
    def __init__(self, file_path: str):
        """
        A source reader for loading in thesaurus data in JSONL format.

        :param file_path: The filename and path to read data from.
        """
        self.file_path = file_path

    def read(self) -> QueryExpander:
        alternatives = defaultdict(list)
        # Load in alternative records from the file path:
        with open(self.file_path, 'r') as fp:
            for line in fp:
                record = json.loads(line)
                if record['syns']:  # Only record the record if the alternatives (synonyms) list isn't empty.
                    alternatives[record['term']] = record['syns']
        return ThesaurusQueryExpander(alternatives)  # Return a Query Expander with all the loaded data.
