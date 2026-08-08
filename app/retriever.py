from typing import List, Dict, Any


class RAGRetriever:
    """Handles query-based retrieval from the vector store"""

    def __init__(self, vector_store: VectorStore, embedding_manager: EmbeddingManager):
        """
        Initialize the retriever.

        Args:
            vector_store: Vector store containing document embeddings.
            embedding_manager: Manager for generating query embeddings.
        """
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Retrieve the most relevant documents for a query.

        Args:
            query: User's question.
            n_results: Number of documents to retrieve.

        Returns:
            ChromaDB query results.
        """

        print(f"Searching for: {query}")

        # Generate embedding for the query
        query_embedding = self.embedding_manager.generate_embeddings([query])

        # Search ChromaDB
        results = self.vector_store.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results
        )

        print(f"Retrieved {len(results['documents'][0])} documents")

        return results

    def display_results(self, results: Dict[str, Any]):
        """
        Display retrieved documents in a readable format.
        """

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i, (doc, meta, distance) in enumerate(
            zip(documents, metadatas, distances), start=1
        ):
            print("=" * 80)
            print(f"Result {i}")
            print(f"Similarity Distance: {distance:.4f}")
            print(f"Metadata: {meta}")
            print("-" * 80)
            print(doc)
            print()
        retriever = RAGRetriever(

 )

vector_store=vectorstore,
embedding_manager=embedding_manager


query = "What is machine learning?"

results = retriever.retrieve(
    query=query,
    n_results=3
)