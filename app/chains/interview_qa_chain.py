from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model

parser = StrOutputParser()


INTERVIEW_QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical interviewer preparing project-specific interview questions and strong student answers.",
        ),
        (
            "human",
            """Core repository review report:

                {review_report}

                Generate project interview preparation content.

                Return exactly these sections:

                ## Likely Interview Questions and Answers
                Generate 8 practical Q&A pairs. Cover architecture, implementation, tradeoffs, bugs, testing, security, and improvements.

                ## Deep-Dive Questions
                Generate 5 harder technical questions with concise answers.

                ## Weaknesses and How to Explain Them
                List possible project weaknesses and how the student should honestly explain them.

                ## Future Improvements
                List improvements that sound realistic and technically meaningful.
                """,
        ),
    ]
)


def generate_interview_qa(review_report: str) -> str:
    llm = get_chat_model()
    chain = INTERVIEW_QA_PROMPT | llm | parser
    response = chain.invoke({"review_report": review_report})
    return response