import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        _client = Groq(api_key=api_key)
    return _client


# ------------------------------------------------------------
# Groq supported models (as of 2026)
# ------------------------------------------------------------
# Primary:   openai/gpt-oss-120b   (fast + smart, recommended)
# Fallback:  openai/gpt-oss-20b    (lighter, faster)
# Fallback:  llama-3.1-8b-instant  (very fast, small)
PRIMARY_MODEL = "openai/gpt-oss-120b"
FALLBACK_MODEL = "llama-3.1-8b-instant"


def _chat(messages, temperature=0.7, max_tokens=800):
    """Try primary model, fall back to secondary on failure."""
    client = get_client()
    try:
        response = client.chat.completions.create(
            model=PRIMARY_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        # If primary fails, try fallback
        try:
            response = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception:
            raise e


def ask_llm(prompt: str, pdf_text: str = None, db_context: str = None) -> str:
    """Send a query to Groq LLM with optional PDF and DB context."""
    system_parts = [
        "You are Jarvis, an intelligent banking assistant for IntelliBank.",
        "You help users with: transactions, fraud alerts, account balances, and PDF document analysis.",
        "Be concise, professional, and helpful. Use emojis where appropriate.",
        "If the user asks in Roman Urdu, respond in Roman Urdu. Otherwise respond in English.",
        "Keep answers short (under 200 words) unless the user asks for detail."
    ]

    if pdf_text:
        pdf_snippet = pdf_text[:25000]
        system_parts.append(
            f"\n\nA PDF document has been uploaded. Here is its content:\n"
            f"---PDF START---\n{pdf_snippet}\n---PDF END---\n"
            f"Answer questions based on this document when relevant."
        )

    if db_context:
        system_parts.append(f"\n\nCurrent bank data:\n{db_context}")

    system_prompt = "\n".join(system_parts)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        return _chat(messages, temperature=0.7, max_tokens=800)
    except Exception as e:
        return f"⚠️ AI service error: {str(e)}"


def summarize_pdf(pdf_text: str) -> str:
    """Generate a smart summary of the PDF using Groq."""
    if not pdf_text:
        return "No PDF document is currently loaded."

    pdf_snippet = pdf_text[:25000]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a financial document analyst. "
                "Summarize the given bank statement/document concisely. "
                "Include: account numbers, key amounts, dates, transaction patterns, "
                "and any suspicious activity. Use bullet points and emojis."
            )
        },
        {
            "role": "user",
            "content": f"Summarize this document:\n\n{pdf_snippet}"
        }
    ]

    try:
        return _chat(messages, temperature=0.5, max_tokens=700)
    except Exception as e:
        return f"⚠️ Could not summarize PDF: {str(e)}"