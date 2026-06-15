from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt

parser = StrOutputParser()


README_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You help students improve GitHub READMEs for internship applications.",
        ),
        (
            "human",
            """Repository context:

{context}

Generate README improvement suggestions.

Return:

## README Quality
Assess the current documentation quality.

## Missing Sections
List missing or weak README sections.

## Improved README Outline
Generate a strong README structure.

## Suggested Project Description
Write a polished project description.

## Setup Instruction Improvements
Suggest clearer setup/run instructions based on the visible project context.
""",
        ),
    ]
)


def generate_readme_review(retriever) -> str:
    documents = retriever.invoke(
        "README installation setup usage features project description environment run"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()
    chain = README_PROMPT | llm | parser

    response = chain.invoke({"context": context})
    return response

