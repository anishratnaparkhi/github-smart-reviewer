from pydantic import BaseModel, Field

class InternshipReportSchema(BaseModel):
    score: str = Field(
        description="Markdown content with an internship-readiness scorecard (graded out of 10 for Architecture, Code Quality, Security, Testing, Documentation, Resume Impact, and Overall), a brief explanation of each score, top 5 improvements before applying, and a final verdict."
    )
    resume: str = Field(
        description="Markdown content containing: Concise Resume Bullet (under 30 words), Technical Resume Bullet, Impact-Focused Resume Bullet, Skills Demonstrated list, and a Best Resume Project Title suggestion."
    )
    interview_explanations: str = Field(
        description="Markdown content containing: 30-Second Pitch/Explanation, 2-Minute Deep Explanation, Architecture Explanation in interview-friendly language, Technical Challenges list, and What I Learned list."
    )
    interview_qa: str = Field(
        description="Markdown content containing: 8 Likely Interview Questions & Answers, 5 Deep-Dive Questions, Project Weaknesses and How to Explain Them, and Future Improvements."
    )
