import abc
from abc import ABC
from indexing_process import Index, Query, SearchResults
import dataclasses


class QueryProcessor(ABC):
    @abc.abstractmethod
    def process_query(self, query_string: str) -> Query:
        pass


class NaiveQueryProcessor(QueryProcessor):
    """
    A QueryProcessor implementation that runs the supplied tokenizer.
    """
    def __init__(self, tokenizer):
        """
        :param tokenizer:
        """
        self.tokenizer = tokenizer

    def process_query(self, query_string: str) -> Query:
        """

        :param query_string:
        :return:
        """
        return Query(tokens=self.tokenizer.tokenize(query_string))


class ResultFormatter(ABC):
    @abc.abstractmethod
    def format_results_for_display(self, results: SearchResults) -> str:
        pass


class QueryProcess:
    def __init__(self, query_processor: QueryProcessor, index: Index, result_formatter: ResultFormatter, logger: Logger):
        self.query_processor = query_processor
        self.index = index
        self.result_formatter = result_formatter
        self.logger = logger

    def run(self, query_string: str) -> str:
        query: Query = self.query_processor.process_query(query_string)
        results: SearchResults = self.index.search(query)
        output_str: str = self.result_formatter.format_results_for_display(results)
        return output_str


def main():
    process = QueryProcess(query_processor=NaiveQueryProcessor(NaiveTokenizer()), index=IndexImplementation(), result_formatter=ResultFormatterImplementation(), logger=LoggerImplementation())
    # Get the query from the user somehow.
    print(process.run(query_string=query))