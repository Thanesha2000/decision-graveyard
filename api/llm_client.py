import os
from groq import Groq


def _get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    return Groq(api_key=api_key)


def reason_about_relevance(historical_context: str, current_context: str, question: str) -> str:
    """
    Asks an LLM: given what was true historically and what's true now,
    does the historical objection/reasoning still apply?
    """
    client = _get_client()
    prompt = f"""You are analyzing whether a past organizational decision's reasoning still applies today.

HISTORICAL CONTEXT (from the decision graveyard):
{historical_context}

CURRENT CONTEXT (stated by the user):
{current_context}

QUESTION: {question}

Reason step by step: what was the original objection/concern, does the current context
change or resolve it, and what is your verdict? End with a clear one-line verdict:
either "STILL APPLIES" or "NO LONGER APPLIES" or "PARTIALLY APPLIES", followed by
a brief explanation.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
