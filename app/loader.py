from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader
)


class DocumentLoader:
    """Loads text and PDF documents."""

    def __init__(self):
        self.text_path = "app/data/documents/text_files"
        self.pdf_path = "app/data/documents/pdf_files"

    def load_text_documents(self):
        loader = DirectoryLoader(
            self.text_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        return loader.load()

    def load_pdf_documents(self):
        loader = DirectoryLoader(
            self.pdf_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        return loader.load()

    def load_single_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        return loader.load()

    def load_all_documents(self):
        text_docs = self.load_text_documents()
        pdf_docs = self.load_pdf_documents()

        return text_docs + pdf_docs