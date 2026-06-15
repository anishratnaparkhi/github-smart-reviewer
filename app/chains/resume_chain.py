from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.chains.llm import get_chat_model

parser = StrOutputParser()

RESUME_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You help students convert technical projects into strong internship resume bullets."
        ),
        (
            "human",
            """
            Core repository review report:

            {review_report}

            Generate resume content for this project.

            Return exactly these sections:

            ## Concise Resume Bullet
            One strong bullet under 30 words.

            ## Technical Resume Bullet
            One bullet highlighting tools, architecture, and engineering depth.

            ## Impact-Focused Resume Bullet
            One bullet emphasizing real-world usefulness and outcome.

            ## Skills Demonstrated
            List technical skills demonstrated by this project.

            ## Best Resume Project Title
            Suggest a polished project title.
            """,
        ),
    ],
)

def generate_resume_content(review_report: str) -> str:
    llm = get_chat_model()
    chain = RESUME_PROMPT | llm | parser
    response = chain.invoke({"review_report": review_report})
    return response
