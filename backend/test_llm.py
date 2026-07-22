from app.llm.llm_request import LLMRequest
from app.providers.llm_provider import get_llm


def main():
    llm = get_llm()

    response = llm.generate(
        LLMRequest(
            prompt="Say hello in one sentence."
        )
    )

    print(response.content)
    print(response.input_tokens)
    print(response.output_tokens)
    print(response.total_tokens)


if __name__ == "__main__":
    main()
