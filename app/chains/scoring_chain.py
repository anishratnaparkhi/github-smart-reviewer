from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model

parser = StrOutputParser()


SCORING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You evaluate student software projects for internship readiness. Be fair, specific, and practical.",
        ),
        (
            "human",
            """Core repository review report:

                {review_report}

                Score this project for internship readiness.

                Return exactly these sections:

                ## Scorecard
                Use this format:
                - Architecture: X/10
                - Code Quality: X/10
                - Security: X/10
                - Testing: X/10
                - Documentation: X/10
                - Resume Impact: X/10
                - Overall Internship Readiness: X/10

                ## Score Explanation
                Explain the reason for each score briefly.

                ## Top 5 Improvements Before Applying
                List the five highest-impact improvements.

                ## Final Verdict
                Give a short verdict on whether this project is ready to show recruiters.
                """,
        ),
    ],
)


def generate_project_score(review_report: str) -> str:
    llm = get_chat_model()
    chain = SCORING_PROMPT | llm | parser
    response = chain.invoke({"review_report": review_report})
    return response