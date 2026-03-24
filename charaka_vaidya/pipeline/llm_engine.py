from groq import Groq
from charaka_vaidya.core.config import config
from charaka_vaidya.core.prompts import SYSTEM_PROMPT, MULTI_SYMPTOM_PROMPT
from charaka_vaidya.utils.logger import get_logger

logger = get_logger(__name__)

_client = None

def get_client() -> Groq:
    global _client
    if _client is None:
        import os
        key = os.getenv("GROQ_API_KEY") or config.GROQ_API_KEY
        if not key:
            raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")
        _client = Groq(api_key=key)
    return _client

def generate_response(
    user_query: str,
    context: str,
    chat_history: list = None,
    intent: str = "general",
    response_language: str = None,
    stream: bool = False,
) -> str:
    client  = get_client()
    history = chat_history or []

    # Choose prompt based on intent
    is_multi = intent == "multi_symptom"
    system_prompt = MULTI_SYMPTOM_PROMPT if is_multi else SYSTEM_PROMPT

    lang_directive = ""
    if response_language:
        lang_directive = f"\n\nIMPORTANT: Write the full response in {response_language}. Keep citations and structure in that language."

    if is_multi:
        user_message = f"""RETRIEVED CONTEXT FROM CHARAKA SAMHITA:
{context}

PATIENT'S DESCRIPTION: {user_query}

Analyze ALL symptoms mentioned above using the Multi-Symptom Diagnostic Protocol.
Classify each symptom by Vata/Pitta/Kapha and provide a unified treatment plan.{lang_directive}"""
    else:
        user_message = f"""RETRIEVED CONTEXT FROM CHARAKA SAMHITA:
{context}

USER QUERY: {user_query}
INTENT: {intent}

Respond using the 4-layer system:
Layer 1 — What does Charaka Samhita say? (cite Sthana + Adhyaya)
Layer 2 — Translate into plain, accessible language
Layer 3 — What does modern science add?
Layer 4 — Practical, actionable guidance{lang_directive}"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    max_tok = 6000 if is_multi else 4800
    logger.info(f"Groq call | model={config.LLM_MODEL} | intent={intent} | multi={is_multi}")

    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tok,
        stream=stream,
    )

    if stream:
        return response   # caller handles the stream generator
    return response.choices[0].message.content

def stream_response(user_query: str, context: str, chat_history: list = None, intent: str = "general"):
    """Yields text chunks for Streamlit st.write_stream."""
    stream = generate_response(user_query, context, chat_history, intent, stream=True)
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta

