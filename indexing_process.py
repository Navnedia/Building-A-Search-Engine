from document_source import DocumentSource, WikiJsonDocumentSource, TrecCovidJsonlSource
from document_transformer import DocumentTransformer, NaiveSearchDocumentTransformer
from index import Index, Indexer, NaiveIndexer, DictInvertedIndexer
from tokenizer import NaiveTokenizer


class DefaultIndexingProcess:
    """
    Simple implementation of the indexing process.

    This class runs components of the indexing process supplied to it either in the constructor
    or in the arguments to the |run| function below.
    """

    def __init__(self, document_transformer: DocumentTransformer, indexer: Indexer):
        self.document_transformer = document_transformer
        self.indexer = indexer

    def run(self, source: DocumentSource) -> Index:
        """
        Runs the Indexing Process using the supplied components.

        :param source: Source of documents to index.
        :return: An index used to search documents from the given source.
        """
        # Run the acquisition stage, or just load the results of that stage. Enable iteration over
        # all documents from the given source.
        document_collection = source.read()
        # Create an empty index. Documents will be added one at a time.
        index = self.indexer.create_index()
        for doc in document_collection:
            # Transform and index the document.
            transformed_doc = self.document_transformer.transform_document(doc)
            index.add_document(transformed_doc)

        return index


def create_naive_indexing_process(index_file: str) -> DefaultIndexingProcess:
    """
    Creates an instance of DefaultIndexingProcess by incorporating the naive indexing components
    (i.e, NaiveTokenizer, NaiveSearchDocumentTransformer, NaiveIndex).

    :param index_file: The JSON file name and path to write the index to.
    :return: An instance of the DefaultIndexingProcess.
    """
    # Construct a naive document transformer using the naive tokenizer.
    # Create a naive index/indexer using the indexer file for reading and writing indexed data.
    # Return an indexing process using the naive components above.
    return DefaultIndexingProcess(
        document_transformer=NaiveSearchDocumentTransformer(NaiveTokenizer()),
        indexer=NaiveIndexer(index_file))


def run_naive_indexing_process(input_file: str, output_file: str) -> None:
    """
    Runs the naive indexing process on the input file and writes the indexed data to the output file.

    :param input_file: The JSON input file name and path to read/index.
    :param output_file: The JSON output file name and path to write indexed data to.
    :return: None
    """
    naive_ip = create_naive_indexing_process(output_file)  # Build an indexing process using naive components.
    # Run indexing process on wiki json source collection to build the index.
    index = naive_ip.run(WikiJsonDocumentSource(input_file))
    index.write()  # Write the indexed/Transformed data to the output file.


def create_inverted_indexing_process(index_file: str) -> DefaultIndexingProcess:
    """
    Creates an instance of DefaultIndexingProcess using inverted index with TF-IDF.
    Uses DictBasedInvertedIndexWithFrequencies to build index.

    :param index_file: The JSONL file name and path to write the index to.
    :return: An instance of the DefaultIndexingProcess.
    """
    # Construct the indexing process using our dictionary inverted index with TF-IDF.
    return DefaultIndexingProcess(
        document_transformer=NaiveSearchDocumentTransformer(NaiveTokenizer()),
        indexer=DictInvertedIndexer(index_file))


def run_covid_inverted_indexing_process(input_file: str, output_file: str) -> None:
    """
    Runs the TF-IDF inverted indexing process for the Trec covid corpus. Writes index to
    output file.

    :param input_file: The JSONL input file name and path to read/index.
    :param output_file: The JSONL output file name and path to write indexed data to.
    :return: None
    """
    # Build an indexing process using TF-IDF inverted index components.
    inverted_ip = create_inverted_indexing_process(output_file)
    # Run indexing process on covid jsonl source collection to build the index.
    index = inverted_ip.run(TrecCovidJsonlSource(input_file))
    index.write()  # Write the index data to the output file.
