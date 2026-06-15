from pydantic import BaseModel, Field

class CoreReviewReport(BaseModel):
    summary: str = Field(
        description="Markdown report analyzing project purpose, tech stack, main components, data flow, and recruiter-friendly summary."
    )
    architecture: str = Field(
        description="Markdown report analyzing architecture style, key modules, execution flow, strengths, weaknesses, suggested improvements, and a Mermaid diagram flowchart."
    )
    code_quality: str = Field(
        description="Markdown report analyzing code quality, style, best practices, modularization, and suggestions."
    )
    security: str = Field(
        description="Markdown report analyzing security, vulnerabilities, data protection, and suggestions."
    )
    testing: str = Field(
        description="Markdown report analyzing testing framework, test coverage, missing tests, and suggestions."
    )
    readme: str = Field(
        description="Markdown report analyzing README completeness, structure, and suggestions."
    )
