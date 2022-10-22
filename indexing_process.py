from document_source import DocumentSource, WikiJsonDocumentSource
from document_transformer import DocumentTransformer, NaiveSearchDocumentTransformer
from index import Index, Indexer, NaiveIndexer
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


def create_naive_indexing_process(indexer_file: str) -> DefaultIndexingProcess:
    """
    Creates an instance of DefaultIndexingProcess by incorporating the
    naive indexing components (i.e, NaiveTokenizer, NaiveSearchDocumentTransformer, NaiveIndexer/NaiveIndex).

    :param indexer_file: The JSON file name and path for the NaiveIndex to write to, or read from.
    :return: An instance of the DefaultIndexingProcess.
    """
    doc_transformer = NaiveSearchDocumentTransformer(NaiveTokenizer())  # Construct a naive document transformer using the naive tokenizer.
    indexer = NaiveIndexer(indexer_file)  # Create a naive index/indexer using the indexer file for reading and writing indexed data.
    return DefaultIndexingProcess(doc_transformer, indexer)  # Return an indexing process using the naive components above.


def run_naive_indexing_process(input_file: str, output_file: str) -> None:
    """
    Runs the naive indexing process on the input file and writes the indexed data
    to the output file.

    :param input_file: The JSON input file name and path to read/index.
    :param output_file: The JSON output file name and path to write indexed data to.
    :return: None
    """
    naive_indexing_process = create_naive_indexing_process(output_file)  # Get an instance of the indexing process using naive components.
    wiki_source = WikiJsonDocumentSource(input_file)  # Create a document source pointing to the input json file.
    index = naive_indexing_process.run(wiki_source)  # Run indexing process to build the index for the wiki source.
    index.write()  # Write the indexed/Transformed data to the output file specified in the indexing process.
