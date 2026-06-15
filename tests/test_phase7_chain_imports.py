def test_phase7_chain_imports():
    from app.chains.resume_chain import generate_resume_content
    from app.chains.interview_explanation_chain import generate_interview_explanations
    from app.chains.interview_qa_chain import generate_interview_qa
    from app.chains.scoring_chain import generate_project_score

    assert callable(generate_resume_content)
    assert callable(generate_interview_explanations)
    assert callable(generate_interview_qa)
    assert callable(generate_project_score)