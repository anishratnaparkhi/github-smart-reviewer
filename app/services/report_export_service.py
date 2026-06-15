from datetime import datetime

def build_markdown_report(repo_info: dict, scan_result: dict, indexing_result: dict, review_report: dict, internship_report: dict) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
# Smart GitHub Project Reviewer Report

## Report Metadata

- Generated at: {generated_at}
- Repository: {repo_info.get("repo_name", "Unknown")}
- Repository URL: {repo_info.get("repo_url", "Unknown")}
- Session ID: {repo_info.get("session_id", "Unknown")}

## Repository Processing Summary

- Total files scanned: {scan_result.get("total_files_scanned", 0)}
- Selected files: {scan_result.get("selected_file_count", 0)}
- Skipped files: {scan_result.get("skipped_file_count", 0)}
- Detected languages: {", ".join(scan_result.get("languages", [])) or "None"}
- LangChain documents: {indexing_result.get("document_count", 0)}
- Text chunks: {indexing_result.get("chunk_count", 0)}

# Core Repository Review

## Repository Summary

{review_report.get("summary", "")}

## Architecture Review

{review_report.get("architecture", "")}

## Code Quality Review

{review_report.get("code_quality", "")}

## Security Review

{review_report.get("security", "")}

## Testing Review

{review_report.get("testing", "")}

## README Improvement Suggestions

{review_report.get("readme", "")}

# Internship Readiness Report

## Project Score

{internship_report.get("score", "")}

## Resume Content

{internship_report.get("resume", "")}

## Interview Explanations

{internship_report.get("interview_explanations", "")}

## Interview Q&A

{internship_report.get("interview_qa", "")}    
"""

def create_report_filename(repo_name: str) -> str:
    safe_name = "".join(
        character if character.isalnum() or character in ("-", "_") else "-"
        for character in repo_name
    ).strip("-")

    if not safe_name:
        safe_name = "github-review-report"
    
    return f"{safe_name}-review-report.md"