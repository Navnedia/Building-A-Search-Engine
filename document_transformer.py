import abc
from abc import ABC

from documents import InputDocument, TransformedDocument
from tokenizer import Tokenizer


class DocumentTransformer(ABC):
    """
    Text Transformation component of the Index Process.

    Text normalization and tokenization is expected to be part of this component.
    """

    @abc.abstractmethod
    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        pass


class NaiveSearchDocumentTransformer(DocumentTransformer):
    def __init__(self, tokenizer: Tokenizer):
        """
        A DocumentTransformer implementation that runs the supplied tokenizer.

        :param tokenizer: A tokenizer instance that will be used in document transformation.
        """
        self.tokenizer = tokenizer

    def transform_document(self, doc: InputDocument) -> TransformedDocument:
        """
        Creates TransformedDocument from the given InputDocument by tokenizing its text.
        Uses the tokenizer instance supplied in the constructor.

        :param doc: The InputDocument to be transformed.
        :return: The transformed document.
        """
        return TransformedDocument(doc_id=doc.doc_id, tokens=self.tokenizer.tokenize(doc.text))
