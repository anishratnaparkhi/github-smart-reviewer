from langchain_core.prompts import ChatPromptTemplate
from app.chains.llm import get_chat_model
from app.chains.prompt_utils import format_documents_for_prompt
from app.schemas.review_report import CoreReviewReport

CORE_REVIEW_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert senior software engineer and architect reviewing a GitHub repository. "
            "Your goal is to provide a highly detailed, professional, and actionable review of the repository "
            "to help a student developer improve it for internship applications."
        ),
        (
            "human",
            """
            Repository context:
            {context}

            Please thoroughly review the repository context and generate a complete review report. 
            You must output a JSON object containing the following keys with high-quality markdown content for each:

            1. "summary" (Markdown content):
               Analyze the project summary. Include the following sections:
               - ## Project Purpose: Explain what this project appears to do.
               - ## Tech Stack: List detected languages, frameworks, libraries, and tools.
               - ## Main components: Explain the important files, folders, or modules.
               - ## Data flow: Explain how the project likely works from input to output.
               - ## Recruiter-friendly summary: Write a short 3-4 line explanation suitable for an internship resume or interview.

            2. "architecture" (Markdown content):
               Analyze the architecture. Include the following sections:
               - ## Architecture Style: Identify MVC, layered, client-server, monolith, microservice, library-based, script-based, etc.
               - ## Key Modules: Explain the role of important modules or folders.
               - ## Execution Flow: Explain how the application starts and how control flows.
               - ## Strengths: List architectural strengths.
               - ## Weaknesses: List architectural weaknesses.
               - ## Suggested Improvements: Practical improvements a student developer can implement.
               - ## Mermaid Diagram: Generate a simple Mermaid flowchart showing the high-level architecture.

            3. "code_quality" (Markdown content):
               Analyze code quality, style, and maintainability. Focus only on issues supported by the context. Include the following sections:
               - ## Overall Code Quality: Give a short assessment.
               - ## Issues Found: For each issue, include Severity (High/Medium/Low), File, Problem, Why it matters, and Suggested fix.
               - ## Maintainability Improvements: List practical improvements.
               - ## Positive Observations: Mention what is already good.

            4. "security" (Markdown content):
               Review possible security risks. Focus only on evidence from the context. Include the following sections:
               - ## Security Overview: Summarize the security posture.
               - ## Potential Risks: For each risk, include Severity (High/Medium/Low), File, Risk, Why it matters, and Suggested fix.
               - ## Secrets and Configuration: Mention possible hardcoded keys, debug flags, unsafe config, or exposed credentials.
               - ## Authentication and Authorization Notes: Mention auth-related risks if visible.
               - ## Safe Next Steps: List practical security improvements.

            5. "testing" (Markdown content):
               Analyze testing and reliability. Include the following sections:
               - ## Testing Overview: Explain what testing setup is visible.
               - ## Existing Tests: Mention test files, tools, or patterns found.
               - ## Missing Tests: List important missing tests.
               - ## Suggested Test Cases: Give concrete tests the developer should add.
               - ## Reliability Improvements: Mention error handling, validation, logging, and CI improvements.

            6. "readme" (Markdown content):
               Generate README improvement suggestions. Include the following sections:
               - ## README Quality: Assess the current documentation quality.
               - ## Missing Sections: List missing or weak README sections.
               - ## Improved README Outline: Generate a strong README structure.
               - ## Suggested Project Description: Write a polished project description.
               - ## Setup Instruction Improvements: Suggest clearer setup/run instructions based on the context.
            """
        )
    ]
)

def generate_consolidated_review(retriever) -> dict:
    # Set retriever parameters dynamically to fetch enough documents for a comprehensive review
    if hasattr(retriever, "search_kwargs"):
        retriever.search_kwargs["k"] = 10
        retriever.search_kwargs["fetch_k"] = 40

    documents = retriever.invoke(
        "project purpose tech stack main components architecture folder structure quality security testing readme config"
    )
    context = format_documents_for_prompt(documents)

    llm = get_chat_model()
    
    # Enable LangChain's native Pydantic structured output parsing
    structured_llm = llm.with_structured_output(CoreReviewReport)
    
    chain = CORE_REVIEW_PROMPT | structured_llm
    response_report = chain.invoke({"context": context})

    # Return standard dictionary matching the format the frontend expects
    return {
        "summary": response_report.summary,
        "architecture": response_report.architecture,
        "code_quality": response_report.code_quality,
        "security": response_report.security,
        "testing": response_report.testing,
        "readme": response_report.readme,
    }
