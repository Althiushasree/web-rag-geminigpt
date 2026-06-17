import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"


def build_prompt(query: str, context_chunks: list[str]) -> str:
    """Construct a RAG prompt from the user query and retrieved context."""
    if context_chunks:
        context_block = "\n\n".join(
            f"[Source {i + 1}]\n{chunk}" for i, chunk in enumerate(context_chunks)
        )
        prompt = (
            "You are a helpful assistant. Use the following retrieved web context to answer "
            "the user's question accurately and concisely. If the context does not contain "
            "enough information, say so and answer from your own knowledge.\n\n"
            f"--- Retrieved Context ---\n{context_block}\n\n"
            f"--- User Question ---\n{query}\n\n"
            "Answer:"
        )
    else:
        prompt = (
            "You are a helpful assistant. No web context was retrieved. "
            f"Answer the following question from your own knowledge:\n\n{query}"
        )

    return prompt


def generate_answer(query: str, context_chunks: list[str]) -> str:
    """
    Send the query and retrieved context to Gemini and return the generated answer.
    """
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Add it to your .env file or environment variables."
        )

    model = genai.GenerativeModel(MODEL_NAME)
    prompt = build_prompt(query, context_chunks)

    response = model.generate_content(prompt)
    return response.text.strip()
