import dataclasses
import json
from typing import List, Dict
from query_process import QueryProcess, create_expanded_query_process
from search_api import SearchResults, Query


@dataclasses.dataclass
class EvalEntry:
    query_id: int  # Query id from the queries.jsonl file.
    results_id: str  # doc_id associated with the result for query.
    eval_value: int  # Manual relevance annotation from tests.tsv.


def read_queries(queries_file: str) -> Dict[int, str]:
    """
    Read in the test queries.

    :param queries_file: The filename and path to the jsonl file with queries.
    :return: A dictionary mapping the query_id to the query string.
    """
    query_id_to_query = dict()
    with open(queries_file, 'r') as fp:
        # Add each query_id & it's associated query string to the dictionary:
        for line in fp:
            record = json.loads(line)
            query_id = int(record['_id'])
            query_text = record['metadata']['query']
            query_id_to_query[query_id] = query_text

    return query_id_to_query


def run_queries(queries_file: str, query_process: QueryProcess, num_results: int = 10) -> Dict[int, List[str]]:
    """
    Runs queries from the queries file through the search defined by query_process.

    :param queries_file: The filename and path to the jsonl file with queries.
    :param query_process: QueryProcess used to run search.
    :param num_results: Number of results requested for each query.
    :return: Dict that maps query ids to result doc_id lists.
    """
    query_id_to_query = read_queries(queries_file)  # Get the test queries from the file.
    query_id_to_result_doc_ids = dict()
    # Parse, then run each test query and store the results:
    for query_id, query_string in query_id_to_query.items():
        query: Query = query_process.query_parser.process_query(query_string, num_results)  # Parse the query string.
        results: SearchResults = query_process.index.search(query)  # Search the index for the query.
        query_id_to_result_doc_ids[query_id] = results.result_doc_ids  # store result doc_ids for the query.

    return query_id_to_result_doc_ids


def read_tests(tests_file: str) -> List[EvalEntry]:
    """
    Reads the human evaluation relevancy ratings into a list of EvalEntries.

    :param tests_file: The filename and path containing the ratings in tsv format.
    :return: A list of EvalEntries from human evaluations of query results.
    """
    result_evaluations = []
    with open(tests_file, 'r') as fp:
        fp.readline()  # Skip header line.
        # Read in all the evaluations for query result evaluations & store them in the list:
        for line in fp:
            fields = line.split()
            result_evaluations.append(
                EvalEntry(query_id=int(fields[0]), results_id=fields[1], eval_value=int(fields[2])))

    return result_evaluations


def annotate_single_result(query_id: int, doc_id: str, reference_values: List[EvalEntry]) -> EvalEntry:
    for entry in reference_values:
        if entry.query_id == query_id and entry.results_id == doc_id:
            return entry
    return EvalEntry(query_id=query_id, results_id=doc_id, eval_value=0)  # Not relevant.


def annotate_results(query_id_to_result_doc_ids: Dict[int, List[str]],
                     reference_values: List[EvalEntry]) -> List[EvalEntry]:
    """
    Annotate actual results with ratings from human evaluations.

    :param query_id_to_result_doc_ids: The output of run_run_queries().
    :param reference_values: The output of read_tests(). Gold standard outputs we want to produce.
    :return: List of EvalEntries corresponding to actual results from our search engine.
    """
    annotations = []
    for query_id, results_doc_ids in query_id_to_result_doc_ids.items():
        for doc_id in results_doc_ids:
            annotations.append(
                annotate_single_result(query_id=query_id, doc_id=doc_id, reference_values=reference_values))

    return annotations


def score_by_sum_of_eval_values(annotated_results: List[EvalEntry]) -> int:
    """
    Calculate the total score of the results compared to human evaluations.

    :param annotated_results: The annotated outputs of annotate_results().
    :return: The total results evaluation score.
    """
    return sum([entry.eval_value for entry in annotated_results])


def run_results_evaluation(index_file: str, queries_file: str, tests_file: str, alternatives_file: str, num_results: int = 100) -> int:
    """
    A function to run the whole results evaluation process in one.

    :param index_file: The filename and path to read index data from.
    :param queries_file: The filename and path to the jsonl file with queries.
    :param tests_file: The filename and path containing the ratings in tsv format.
    :param alternatives_file: The filename and path to load alternative terms.
    :param num_results: The max number of results requested for each test query. Default is 100.
    :return: The total results evaluation score.
    """
    qp: QueryProcess = create_expanded_query_process(index_file, alternatives_file)  # Create a query process.
    search_results = run_queries(queries_file, qp, num_results)  # Run the test queries through our search implementation.
    document_relevance_values = read_tests(tests_file)  # Get the human evaluated document relevancy scores for each query.
    annotated_results = annotate_results(search_results, document_relevance_values)  # Compare the human evaluations to search results.

    return score_by_sum_of_eval_values(annotated_results)  # Return the sum of result evaluation scores.
