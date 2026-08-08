import os
from groq import Groq


class RAGPipeline:
    """Handles retrieval and question answering."""

    def __init__(self, vector_store, embedding_manager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def answer_question(self, question: str, top_k: int = 3):
        """Answer a question using retrieved documents."""

        # 1. Retrieve relevant documents
        retrieved_docs = self.vector_store.retrieve(
            query=question,
            embedding_manager=self.embedding_manager,
            top_k=top_k
        )

        # 2. Create context
        context = "\n\n".join(
            doc["content"]
            for doc in retrieved_docs
        )

        # 3. Create prompt
        prompt = f"""
You are a helpful AI assistant that answers questions
using the provided document context.

Answer the user's question based only on the context.

If the answer is not found in the context, say:
"I could not find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

        # 4. Send prompt to Groq
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        # 5. Get answer
        answer = response.choices[0].message.content

        # 6. Prepare unique sources
        sources = []
        seen = set()

        for doc in retrieved_docs:
            metadata = doc["metadata"]

            source = metadata.get("source", "")

            # Use human-readable PDF page number
            page = metadata.get("page_label")

            # Fallback if page_label doesn't exist
            if page is None:
                page = metadata.get("page")

            # Unique combination of file + page
            key = (source, page)

            if key not in seen:
                seen.add(key)

                sources.append({
                    "page": page,
                    "source": source
                })

        return {
            "answer": answer,
            "sources": sources
        }
    