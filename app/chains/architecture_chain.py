from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt

parser = StrOutputParser()

ARCHITECTURE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a software architect reviewing a GitHub Repository."
        ),
        (
            "human",
            """
            Repository context:
            {context}
            Analyze the architecture with these sections:
            ## Architecture Style
            Identify whether this looks like MVC, layered architecture, client-server, monolith, microservice, script-based, library-based, or another style.

            ## Key Modules
            Explain the role of important modules or folders.

            ## Execution Flow
            Explain how the application likely starts and how control flows through the project.

            ## Strengths
            List architectural strengths.

            ## Weaknesses
            List architectural weaknesses.

            ## Suggested Improvements
            Give practical improvements a student developer can implement.

            ## Mermaid Diagram
            Generate a simple Mermaid flowchart showing the high-level architecture.
            """,
        )
    ]
)

def generate_architecture_review(retriever) -> str:
    documents = retriever.invoke(
        "architecture folder structure routes services models controllers main app config"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()

    chain = ARCHITECTURE_PROMPT | llm | parser

    response = chain.invoke({"context": context})

    return response
