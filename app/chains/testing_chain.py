from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt

parser = StrOutputParser()

TESTING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior engineer reviewing test coverage and reliability."
        ),
        (
            "human",
            """
            Code context:
            {context}
            Analyze testing and reliability.

            Return:

            ## Testing Overview
            Explain what testing setup is visible.

            ## Existing Tests
            Mention test files, tools, or patterns found.

            ## Missing Tests
            List important missing tests.

            ## Suggested Test Cases
            Give concrete tests the developer should add.

            ## Reliability Improvements
            Mention error handling, validation, logging, and CI improvements.
            """,
        ),
    ],
)

def generate_testing_review(retriever) -> str:
    documents = retriever.invoke(
        "tests pytest unittest jest vitest cypress test coverage github actions ci error handling"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()
    chain = TESTING_PROMPT | llm | parser

    response = chain.invoke({"context": context})
    return response
