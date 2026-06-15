from langchain_core.prompts import ChatPromptTemplate
from app.chains.llm import get_chat_model
from app.schemas.internship_report import InternshipReportSchema

INTERNSHIP_REPORT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a technical recruiter and senior software engineer preparing a student developer "
            "for software engineering internship applications. Evaluate their software project "
            "and create a highly polished, recruiter-ready report."
        ),
        (
            "human",
            """
            Core repository review report:
            {review_report}

            Generate the consolidated internship-focused preparation content. 
            You must output a JSON object containing the following keys with high-quality markdown content for each:

            1. "score" (Markdown content):
               Evaluate this project for internship readiness. Include:
               - ## Scorecard
                 Grading scorecard exactly in this format:
                 - Architecture: X/10
                 - Code Quality: X/10
                 - Security: X/10
                 - Testing: X/10
                 - Documentation: X/10
                 - Resume Impact: X/10
                 - Overall Internship Readiness: X/10
               - ## Score Explanation
                 Briefly explain the reason for each score.
               - ## Top 5 Improvements Before Applying
                 List the five highest-impact improvements needed.
               - ## Final Verdict
                 A short final verdict on recruiter readiness.

            2. "resume" (Markdown content):
               Generate resume content for this project. Include:
               - ## Concise Resume Bullet: One strong bullet under 30 words.
               - ## Technical Resume Bullet: One bullet highlighting tools, architecture, and engineering depth.
               - ## Impact-Focused Resume Bullet: One bullet emphasizing usefulness and outcome.
               - ## Skills Demonstrated: Bulleted list of technical skills demonstrated by this project.
               - ## Best Resume Project Title: Polished project title suggestion.

            3. "interview_explanations" (Markdown content):
               Generate interview-friendly explanations. Include:
               - ## 30-Second Explanation: A short elevator pitch suitable for the first answer in an interview.
               - ## 2-Minute Explanation: Deeper explanation covering problem, solution, tech stack, architecture, and result.
               - ## Architecture Explanation: Explain the architecture in simple, interview-friendly language.
               - ## Technical Challenges: List likely technical challenges faced when building this.
               - ## What I Learned: List practical learning outcomes.

            4. "interview_qa" (Markdown content):
               Generate project interview prep content. Include:
               - ## Likely Interview Questions and Answers: 8 practical Q&A pairs covering architecture, tradeoffs, bugs, testing, security, and improvements.
               - ## Deep-Dive Questions: 5 harder technical questions with concise answers.
               - ## Weaknesses and How to Explain Them: Honest weaknesses and strategic explanation methods.
               - ## Future Improvements: Meaningful, realistic enhancements.
            """
        )
    ]
)

def generate_consolidated_internship_report(review_report: str) -> dict:
    llm = get_chat_model()
    
    # Enable LangChain's native Pydantic structured output parsing
    structured_llm = llm.with_structured_output(InternshipReportSchema)
    
    chain = INTERNSHIP_REPORT_PROMPT | structured_llm
    response = chain.invoke({"review_report": review_report})
    
    # Return standard dictionary matching the format the frontend expects
    return {
        "score": response.score,
        "resume": response.resume,
        "interview_explanations": response.interview_explanations,
        "interview_qa": response.interview_qa,
    }
