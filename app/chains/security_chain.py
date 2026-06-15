from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt

parser = StrOutputParser()

SECURITY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a security-minded software engineer reviewing repository code."
        ),
        (
            "human",
            """
            Code context:
            {context}
            Review possible security risks. Focus only on evidence from the context.

            Return:

            ## Security Overview
            Summarize the security posture.

            ## Potential Risks
            For each risk include:
            - Severity: High / Medium / Low
            - File
            - Risk
            - Why it matters
            - Suggested fix

            ## Secrets and Configuration
            Mention possible hardcoded keys, debug flags, unsafe config, or exposed credentials if visible.

            ## Authentication and Authorization Notes
            Mention auth-related risks if visible.

            ## Safe Next Steps
            List practical security improvements.
            """,
        ),
    ],
)

def generate_security_review(retriever) -> str:
    documents = retriever.invoke(
        "api key secret password token jwt auth cors debug database url environment config security"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()
    chain = SECURITY_PROMPT | llm | parser

    response = chain.invoke({"context": context})
    return response
