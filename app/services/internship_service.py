from app.chains.internship_chain import generate_consolidated_internship_report

def combine_core_report(review_report:dict) -> str:
    return f"""
# Repository Summary

{review_report["summary"]}

# Architecture Review

{review_report["architecture"]}

# Code Quality Review

{review_report["code_quality"]}

# Security Review

{review_report["security"]}

# Testing Review

{review_report["testing"]}

# README Review

{review_report["readme"]}
"""

def generate_internship_report(review_report: dict) -> dict:
    combined_report = combine_core_report(review_report)
    return generate_consolidated_internship_report(combined_report)

