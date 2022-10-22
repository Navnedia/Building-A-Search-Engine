import abc
from abc import ABC

from search_api import Query, SearchResults
from index import Index, NaiveIndex
from tokenizer import Tokenizer, NaiveTokenizer


class QueryParser(ABC):
    """
    Responsible for converting the input query string entered by a user into the
    structured Query representation.
    """

    @abc.abstractmethod
    def process_query(self, query_str: str) -> Query:
        """
        Runs the QueryParser logic.

        :param query_str: The input query string entered by the user.
        :return: Structured Query representation to be used by search.
        """
        pass


class ResultFormatter(ABC):
    """
    Abstract class responsible for presenting each result to the users.
    """

    @abc.abstractmethod
    def format_results_for_display(self, results: SearchResults) -> str:
        """
        Takes SearchResults dataclass and outputs a string to be displayed to users.

        :param results: Structured representation of search results containing the doc_ids.
        :return: A human-readable string containing all the search results as they should be
            displayed to users.
        """
        pass


class QueryProcess:
    """
    Class responsible for running the whole query process.
    """

    def __init__(self, query_parser: QueryParser, index: Index, result_formatter: ResultFormatter):
        """
        Constructor taking all the necessary components to process queries.

        :param query_parser: Specific implementation instance of a QueryParser.
        :param index: Specific implementation instance of an Index with all the data necessary
            to run a search.
        :param result_formatter: Specific implementation instance of a ResultFormatter.
        """
        self.query_parser = query_parser
        self.index = index
        self.result_formatter = result_formatter

    def run(self, query_string: str) -> str:
        """
        Runs the query process and format results for display using the components
        specified in the constructor.

        :param query_string: The query string taken from the user.
        :return: A human-readable representation of search results displayed to the user.
        """
        query: Query = self.query_parser.process_query(query_string)  # Process the query into tokens.
        results: SearchResults = self.index.search(query)  # Search the index for the query.
        output_str: str = self.result_formatter.format_results_for_display(results)  # format results.

        return output_str


def main():
    process = QueryProcess(query_processor=NaiveQueryProcessor(NaiveTokenizer()), index=IndexImplementation(), result_formatter=ResultFormatterImplementation(), logger=LoggerImplementation())
    # Get the query from the user somehow.
    print(process.run(query_string=query))