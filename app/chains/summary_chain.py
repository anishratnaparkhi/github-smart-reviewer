from langchain_core.prompts import ChatPromptTemplate

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

SUMMARY_PROMPT = ChatPromptTemplate.from_messages(
[
    (
        "system",
        "You are a senior software engineer. Review the provided repository context and explain the project clearly.",
    ),
    (
        "human",
        """
        Repository context:
        {context}
        Generate a repository summary with these sections:

        ## Project Purpose
        Explain what this project appears to do.
        ## Tech Stack
        List detected languages, frameworks, libraries, and tools.
        ## Main components
        Explain the important files, folders or modules.
        ## Data flow
        Explain how the project likely works from input to output.
        ## Recruiter-friendly summary
        Write a short 3-4 line explanation suitable for an internship resume or interview.
        """,
        ),
    ]
)

def generate_repository_summary(retriever) -> str:
    documents = retriever.invoke("project purpose tech stack main files architecture README entrypoint")
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()
    chain = SUMMARY_PROMPT | llm | parser

    response = chain.invoke({"context": context})
    return response