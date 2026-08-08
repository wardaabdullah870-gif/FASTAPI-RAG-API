import os
import chromadb


class VectorStore:
    """Manages document embeddings in a ChromaDB vector store."""

    def __init__(
        self,
        collection_name: str = "pdf_documents",
        persist_directory: str = "app/data/vector_store"
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        self.client = None
        self.collection = None

        self._initialize_store()

    def _initialize_store(self):
        """Initialize ChromaDB."""

        os.makedirs(self.persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "description": "PDF document embeddings for RAG"
            }
        )

        print(
            f"Vector store initialized. "
            f"Collection: {self.collection_name}"
        )

        print(
            f"Existing documents in collection: "
            f"{self.collection.count()}"
        )

    def add_documents(self, documents, embeddings):
        """Add documents and their embeddings to ChromaDB."""

        start_id = self.collection.count()

        ids = [
            str(i)
            for i in range(
                start_id,
                start_id + len(documents)
            )
        ]

        texts = [
            doc.page_content
            for doc in documents
        ]

        metadatas = [
            doc.metadata
            for doc in documents
        ]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        print(
            f"Added {len(documents)} documents "
            f"to vector store."
        )

    def retrieve(
        self,
        query,
        embedding_manager,
        top_k=3
    ):
        """Retrieve unique relevant document pages."""

        # Generate query embedding
        query_embedding = embedding_manager.generate_embeddings(
            [query]
        )[0]

        # Get more chunks than needed.
        # This allows us to find different pages
        # even when several top chunks come from
        # the same page.
        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k * 3
        )

        retrieved_docs = []
        seen_pages = set()

        for doc, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):

            source = metadata.get("source", "")

            # Prefer the human-readable PDF page number
            page = metadata.get("page_label")

            # Fallback to zero-based page number
            if page is None:
                page = metadata.get("page")

            # Unique combination:
            # PDF file + page
            page_key = (source, page)

            # Skip duplicate pages
            if page_key in seen_pages:
                continue

            seen_pages.add(page_key)

            retrieved_docs.append({
                "content": doc,
                "metadata": metadata,
                "distance": distance
            })

            # Stop after finding top_k unique pages
            if len(retrieved_docs) >= top_k:
                break

        return retrieved_docs
