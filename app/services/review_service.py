from app.chains.core_review_chain import generate_consolidated_review

def generate_core_review_report(retriever) -> dict:
    return generate_consolidated_review(retriever)
