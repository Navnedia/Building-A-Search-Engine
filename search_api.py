import dataclasses
from typing import List


@dataclasses.dataclass
class Query:
    terms: List[str]
    num_results: int


@dataclasses.dataclass
class SearchResults:
    result_doc_ids: List[str]
