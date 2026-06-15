from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt

parser = StrOutputParser()

QUALITY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict but helpful code reviewer."
        ),
        (
            "human",
            """
            Code context:
            {context}
            Review the code quality. Focus only on issues supported by the provided context.

            Return:

            ## Overall Code Quality
            Give a short assessment.

            ## Issues Found
            For each issue include:
            - Severity: High / Medium / Low
            - File
            - Problem
            - Why it matters
            - Suggested fix

            ## Maintainability Improvements
            List practical improvements.

            ## Positive Observations
            Mention what is already good.
            """,
        ),
    ],
)

def generate_code_quality_review(retriever) -> str:
    documents = retriever.invoke(
        "error handling duplicate code large functions validation logging configuration code quality"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()

    chain = QUALITY_PROMPT | llm | parser
    response = chain.invoke({"context":context})
    return response
