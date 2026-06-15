from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model

parser = StrOutputParser()


INTERVIEW_EXPLANATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You help students explain their software projects clearly in technical interviews.",
        ),
        (
            "human",
            """Core repository review report:

                {review_report}

                Generate interview explanations.

                Return exactly these sections:

                ## 30-Second Explanation
                A short explanation suitable for the first answer in an interview.

                ## 2-Minute Explanation
                A deeper explanation covering problem, solution, tech stack, architecture, and result.

                ## Architecture Explanation
                Explain the architecture in interview-friendly language.

                ## Technical Challenges
                List likely technical challenges faced while building this project.

                ## What I Learned
                List practical learning outcomes a student can confidently discuss.
                """,
        ),
    ]
)


def generate_interview_explanations(review_report: str) -> str:
    llm = get_chat_model()
    chain = INTERVIEW_EXPLANATION_PROMPT | llm | parser
    response = chain.invoke({"review_report": review_report})
    return response