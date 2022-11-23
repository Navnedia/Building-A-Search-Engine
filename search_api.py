import dataclasses
from typing import List, Dict


@dataclasses.dataclass
class Query:
    terms: List[str]  # A list of search terms as tokens.
    alternatives: Dict[str, List[str]]  # Map terms to a list of alternative or related terms.
    num_results: int  # The max number of results to return.


@dataclasses.dataclass
class SearchResults:
    result_doc_ids: List[str]
