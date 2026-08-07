from app.prompting.base_prompt_builder import BasePromptBuilder
from app.prompting.prompt_templates import PromptTemplates
from app.retrieval.reranker.rerank_result import (
    RerankResult,
)


class RAGPromptBuilder(BasePromptBuilder):
    """
    Builds prompts for Retrieval-Augmented Generation.
    """

    def build(
        self,
        query: str,
        retrieval_results: list[RerankResult],
    ) -> str:
        context = self._build_context(retrieval_results)

        return self._build_prompt(
            query=query,
            context=context,
        )

    def _build_context(
        self,
        retrieval_results: list[RerankResult]
    ) -> str:
        """
        Convert retrieved chunks into a formatted context block.
        """

        if not retrieval_results:
            return (
                "No relevant information was retrieved "
                "from the knowledge base."
            )

        context_parts: list[str] = []

        for index, result in enumerate(retrieval_results, start=1):

            chunk = result.chunk

            lines = [
                f"[Chunk {index}]",
            ]

            page_number = getattr(chunk.metadata, "page_number", None)
            section = getattr(chunk.metadata, "section", None)
            similarity = getattr(result, "score", None)

            if page_number is not None:
                lines.append(f"Page: {page_number}")

            if section:
                lines.append(f"Section: {section}")

            if similarity is not None:
                lines.append(f"Similarity: {similarity:.4f}")

            lines.append("")
            lines.append(chunk.text.strip())

            context_parts.append("\n".join(lines))

        return "\n\n".join(context_parts)

    def _build_prompt(
        self,
        query: str,
        context: str,
    ) -> str:
        """
        Build the final prompt.
        """

        return PromptTemplates.PROMPT_TEMPLATE.format(
            system_prompt=PromptTemplates.RAG_SYSTEM_PROMPT.strip(),
            separator=PromptTemplates.SECTION_SEPARATOR,
            context=context,
            query=query,
        )