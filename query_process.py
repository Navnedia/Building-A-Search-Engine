import abc
import sys
from abc import ABC

from search_api import Query, SearchResults
from index import Index, DictBasedInvertedIndexWithFrequencies, ListBasedInvertedIndexWithFrequencies
from tokenizer import Tokenizer, NaiveTokenizer


class QueryParser(ABC):
    """
    Responsible for converting the input query string entered by a user into the
    structured Query representation.
    """

    @abc.abstractmethod
    def process_query(self, query_str: str, num_results: int) -> Query:
        """
        Runs the QueryParser logic.

        :param query_str: The input query string entered by the user.
        :param num_results: The max number of results requested for this search.
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


class NaiveQueryParser(QueryParser):
    """
    A QueryProcessor implementation that runs the supplied Tokenizer.
    """

    def __init__(self, tokenizer: Tokenizer):
        """
        :param tokenizer: A Tokenizer instance that will be used in parse_query.
        """
        self.tokenizer = tokenizer

    def process_query(self, query_str: str, num_results: int) -> Query:
        """
        Runs the tokenizer and wraps the output into a Query dataclass.

        :param query_str: The input query string entered by the user.
        :param num_results: The max number of results requested for this search.
        :return: Query representation with tokenized query.
        """
        return Query(terms=self.tokenizer.tokenize(query_str), num_results=num_results)


class NaiveResultFormatter(ResultFormatter):
    """
    Fake result formatter that just displays the doc_ids of the results.
    """

    def format_results_for_display(self, results: SearchResults) -> str:
        return repr(results)


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

    def run(self, query_string: str, num_results: int = 10) -> str:
        """
        Runs the query process and format results for display using the components
        specified in the constructor.

        :param query_string: The query string taken from the user.
        :param num_results: The max number of results requested for this search.
        :return: A human-readable representation of search results displayed to the user.
        """
        # Parse query and get the Query object representation.
        query: Query = self.query_parser.process_query(query_string, num_results)
        results: SearchResults = self.index.search(query)  # Search the index for the query.
        output_str: str = self.result_formatter.format_results_for_display(results)  # format results.

        return output_str


def create_naive_query_process(index_file: str) -> QueryProcess:
    """
    Loads the index into memory & initializes the QueryProcess using naive components.

    :param index_file: The filename and path to read index data from.
    :return: An instance of QueryProcess using naive components.
    """
    index = ListBasedInvertedIndexWithFrequencies(index_file)
    index.read()  # Load indexed data from the file into memory.
    # Initialize the QueryProcess using naive components:
    return QueryProcess(
        query_parser=NaiveQueryParser(NaiveTokenizer()),
        index=index,
        result_formatter=NaiveResultFormatter())


def create_query_process(index_file: str) -> QueryProcess:
    """
    Loads the index into memory & initializes the QueryProcess.

    :param index_file: The filename and path to read index data from.
    :return: An instance of QueryProcess using naive components.
    """
    index = DictBasedInvertedIndexWithFrequencies(index_file)
    index.read()  # Load indexed data from the file into memory.
    # Initialize the QueryProcess using naive components:
    return QueryProcess(
        query_parser=NaiveQueryParser(NaiveTokenizer()),
        index=index,
        result_formatter=NaiveResultFormatter())


def main(index_file: str) -> None:
    """
    Loads query process with index file and runs an interactive search query
    loop inside the console.

    :param index_file: The filename and path to read index data from.
    :return:
    """
    # Initialize the query process and load in data.
    process = create_query_process(index_file)

    # Continuously prompt user for a query and display the results:
    query = input("Please enter a query:")
    while query:
        print(process.run(query))
        query = input("Please enter a query:")


if __name__ == "__main__":
    main(index_file=sys.argv[1])
