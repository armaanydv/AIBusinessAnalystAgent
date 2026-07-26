"""
Prompt templates used throughout the application.
"""


class PromptTemplates:
    """
    Centralised prompt templates.
    """

    SECTION_SEPARATOR = "=" * 80

    RAG_SYSTEM_PROMPT = """
You are an expert AI Business Analyst.

Use ONLY the provided context to answer the user's question.

If the answer cannot be found in the provided context,
say that the information is not available.

Do not make up facts.

Return ONLY valid JSON.

Do not include markdown.

Do not wrap the JSON inside code fences.
"""

    PROMPT_TEMPLATE = """
{system_prompt}

{separator}
CONTEXT
{separator}

{context}

{separator}
QUESTION
{separator}

{query}

{separator}
OUTPUT FORMAT
{separator}

Return a JSON object with EXACTLY this structure:

{{
    "answer": "string",
    "supporting_evidence": [
        "string"
    ],
    "confidence": 0.0
}}
"""