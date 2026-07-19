from app.prompting.base_prompt_builder import BasePromptBuilder
from app.prompting.prompt_templates import (
    PROMPT_TEMPLATE,
    RAG_SYSTEM_PROMPT,
)
from app.retrieval.retriever.retrieval_result import RetrievalResult


class RAGPromptBuilder(BasePromptBuilder):
    """
    Builds prompts for Retrieval-Augmented Generation.
    """

    def build(
        self,
        query: str,
        retrieval_results: list[RetrievalResult],
    ) -> str:

        context = self._build_context(
            retrieval_results
        )

        return self._build_prompt(
            query=query,
            context=context,
        )

    def _build_context(
        self,
        retrieval_results: list[RetrievalResult],
    ) -> str:
        """
        Convert retrieved chunks into a context block.
        """

        sections: list[str] = []

        for i, result in enumerate(
            retrieval_results,
            start=1,
        ):
            sections.append(
                f"[Chunk {i}]\n"
                f"{result.chunk.text.strip()}"
            )

        return "\n\n".join(sections)

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the final prompt.
        """

        return PROMPT_TEMPLATE.format(
            system_prompt=RAG_SYSTEM_PROMPT.strip(),
            context=context,
            query=query,
        )