import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingManager:
    """Handles document embedding generation using SentenceTransformer."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.__load_model()

    def __load_model(self):
        """Load the SentenceTransformer model."""
        try:
            print(f"Loading model: {self.model_name}")

            self.model = SentenceTransformer(self.model_name)

            print(
                f"Model loaded successfully. "
                f"Embedding dimension: "
                f"{self.model.get_sentence_embedding_dimension()}"
            )

        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            raise

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""

        if self.model is None:
            raise ValueError("Model not loaded.")

        print(f"Generating embeddings for {len(texts)} texts...")

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        print(f"Generated embeddings with shape: {embeddings.shape}")

        return embeddings

    def get_embedding_dimension(self):
        """Return the embedding dimension."""

        if self.model is None:
            raise ValueError("Model not loaded.")

        return self.model.get_embedding_dimension()