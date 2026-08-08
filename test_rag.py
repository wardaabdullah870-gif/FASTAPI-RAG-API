from app.loader import DocumentLoader
from app.chunker import TextChunker
from app.embedder import EmbeddingManager
from app.vector_store import VectorStore

from app.loader import DocumentLoader
from app.chunker import TextChunker

loader = DocumentLoader()
documents = loader.load_all_documents()

chunker = TextChunker()
chunks = chunker.split_documents(documents)

print(f"Loaded {len(documents)} documents")
print(f"Created {len(chunks)} chunks")