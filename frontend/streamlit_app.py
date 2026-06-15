import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


from pathlib import Path

import streamlit as st

from app.chains.llm import LLMConfigError
from app.indexing.embedding import EmbeddingConfigError
from app.loaders.file_loader import scan_repository
from app.loaders.github_loader import GitHubLoaderError, clone_github_repo
from app.services.indexing_service import prepare_documents_and_chunks
from app.services.internship_service import generate_internship_report
from app.services.report_export_service import (
    build_markdown_report,
    create_report_filename,
)
from app.services.retriever_service import (
    prepare_vector_store_and_retriever,
    retrieve_relevant_chunks,
)
from app.services.review_service import generate_core_review_report
from app.utils.cleanup import cleanup_expired_sessions, cleanup_repo_directory


st.set_page_config(
    page_title="Smart GitHub Project Reviewer",
    page_icon="",
    layout="wide",
)


def reset_analysis() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def has_processing_results() -> bool:
    required_keys = {
        "repo_info",
        "scan_result",
        "indexing_summary",
        "retriever",
        "vector_store_path",
    }
    return required_keys.issubset(st.session_state.keys())


def has_core_review() -> bool:
    return "review_report" in st.session_state


def has_internship_report() -> bool:
    return "internship_report" in st.session_state


def has_complete_report() -> bool:
    required_keys = {
        "repo_info",
        "scan_result",
        "indexing_summary",
        "review_report",
        "internship_report",
    }
    return required_keys.issubset(st.session_state.keys())


st.title("Smart GitHub Project Reviewer")

st.write(
    "Enter a public GitHub repository URL to analyze its architecture, "
    "code quality, documentation, and internship readiness."
)

col_input, col_btn, col_reset = st.columns([6, 2, 2])
with col_input:
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="Paste public GitHub repository URL here...",
        label_visibility="collapsed"
    )
with col_btn:
    analyze_clicked = st.button("Analyze Repository", use_container_width=True)
with col_reset:
    if st.button("Reset Analysis", use_container_width=True):
        reset_analysis()

if analyze_clicked:
    if not repo_url.strip():
        st.error("Please enter a GitHub repository URL.")
    else:
        try:
            cleanup_expired_sessions(max_age_hours=24)
        except Exception:
            pass  # Do not block the run if clean up fails
            
        repo_info = None
        try:
            with st.spinner("Cloning repository..."):
                repo_info = clone_github_repo(repo_url)

            st.success("Repository cloned successfully.")

            with st.spinner("Scanning repository files..."):
                scan_result = scan_repository(Path(repo_info["local_path"]))

            st.success("Repository files scanned successfully.")

            with st.spinner("Creating LangChain documents and chunks..."):
                indexing_result = prepare_documents_and_chunks(scan_result)

            st.success("Documents and chunks created successfully.")

            if not indexing_result["chunks"]:
                st.warning("No chunks were created from the selected files.")
            else:
                with st.spinner("Creating embeddings and FAISS vector store..."):
                    retrieval_result = prepare_vector_store_and_retriever(
                        chunks=indexing_result["chunks"],
                        session_id=repo_info["session_id"],
                    )

                st.success("Vector store and retriever created successfully.")

                st.session_state["repo_info"] = repo_info
                st.session_state["scan_result"] = scan_result
                st.session_state["indexing_summary"] = {
                    "document_count": indexing_result["document_count"],
                    "chunk_count": indexing_result["chunk_count"],
                }
                st.session_state["retriever"] = retrieval_result["retriever"]
                st.session_state["vector_store_path"] = str(
                    retrieval_result["vector_store_path"]
                )

                if "review_report" in st.session_state:
                    del st.session_state["review_report"]

                if "internship_report" in st.session_state:
                    del st.session_state["internship_report"]

        except GitHubLoaderError as error:
            st.error(str(error))
        except EmbeddingConfigError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Analysis failed: {error}")
        finally:
            if repo_info and "session_id" in repo_info:
                try:
                    cleanup_repo_directory(repo_info["session_id"])
                except Exception:
                    pass


if has_processing_results():
    repo_info = st.session_state["repo_info"]
    scan_result = st.session_state["scan_result"]
    indexing_summary = st.session_state["indexing_summary"]

    st.divider()
    st.header("Repository Processing Summary")

    col_meta1, col_meta2 = st.columns(2)
    with col_meta1:
        st.markdown(f"**Repository Name:** `{repo_info['repo_name']}`")
        st.markdown(f"**Normalized URL:** [Link]({repo_info['repo_url']})")
    with col_meta2:
        st.markdown(f"**Session ID:** `{repo_info['session_id']}`")
        st.markdown(f"**Vector Store Path:** `{st.session_state['vector_store_path']}`")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Files Scanned", scan_result["total_files_scanned"])
    col2.metric("Selected Files", scan_result["selected_file_count"])
    col3.metric("Documents", indexing_summary["document_count"])
    col4.metric("Chunks", indexing_summary["chunk_count"])

    detected_languages = ", ".join(scan_result["languages"])
    st.caption(
        "Languages detected: "
        + (detected_languages if detected_languages else "None")
    )

    with st.expander("Selected Files"):
        st.dataframe(scan_result["selected_files"], use_container_width=True)

    with st.expander("Skipped Files"):
        st.dataframe(scan_result["skipped_files"], use_container_width=True)

    st.subheader("Retriever Test")

    col_q, col_q_btn = st.columns([7, 3])
    with col_q:
        retrieval_query = st.text_input(
            "Test retrieval query",
            value="What does this project do?",
            label_visibility="collapsed"
        )
    with col_q_btn:
        run_retrieval = st.button("Run Retrieval Test", use_container_width=True)

    if run_retrieval:
        try:
            retrieved_chunks = retrieve_relevant_chunks(
                st.session_state["retriever"],
                retrieval_query,
            )

            st.write(f"Retrieved chunks: {len(retrieved_chunks)}")

            for index, chunk in enumerate(retrieved_chunks, start=1):
                file_path = chunk.metadata.get("file_path", "Unknown file")

                with st.expander(f"Retrieved Chunk {index}: {file_path}"):
                    st.write("Language:", chunk.metadata.get("language"))
                    st.write("Chunk size:", chunk.metadata.get("chunk_size"))
                    st.code(chunk.page_content[:1500])

        except Exception as error:
            st.error(f"Retrieval test failed: {error}")

    st.divider()
    st.header("Core Repository Review")

    if st.button("Generate Core Review Report"):
        try:
            with st.spinner("Generating AI review report..."):
                review_report = generate_core_review_report(
                    st.session_state["retriever"]
                )

            st.session_state["review_report"] = review_report

            if "internship_report" in st.session_state:
                del st.session_state["internship_report"]

            st.success("Core review report generated successfully.")

        except LLMConfigError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Review generation failed: {error}")


if has_core_review():
    review_report = st.session_state["review_report"]

    overview_tab, architecture_tab, quality_tab, security_tab, testing_tab, readme_tab = st.tabs(
        [
            "Overview",
            "Architecture",
            "Code Quality",
            "Security",
            "Testing",
            "README",
        ]
    )

    with overview_tab:
        st.markdown(review_report["summary"])

    with architecture_tab:
        st.markdown(review_report["architecture"])

    with quality_tab:
        st.markdown(review_report["code_quality"])

    with security_tab:
        st.markdown(review_report["security"])

    with testing_tab:
        st.markdown(review_report["testing"])

    with readme_tab:
        st.markdown(review_report["readme"])

    st.divider()
    st.header("Internship Readiness")

    if st.button("Generate Internship-Focused Report"):
        try:
            with st.spinner(
                "Generating resume bullets, interview prep, and project score..."
            ):
                internship_report = generate_internship_report(
                    st.session_state["review_report"]
                )

            st.session_state["internship_report"] = internship_report
            st.success("Internship-focused report generated successfully.")

        except LLMConfigError as error:
            st.error(str(error))
        except Exception as error:
            st.error(f"Internship report generation failed: {error}")


if has_internship_report():
    internship_report = st.session_state["internship_report"]

    score_tab, resume_tab, explanation_tab, qa_tab = st.tabs(
        [
            "Project Score",
            "Resume",
            "Interview Explanation",
            "Interview Q&A",
        ]
    )

    with score_tab:
        st.markdown(internship_report["score"])

    with resume_tab:
        st.markdown(internship_report["resume"])

    with explanation_tab:
        st.markdown(internship_report["interview_explanations"])

    with qa_tab:
        st.markdown(internship_report["interview_qa"])


if has_complete_report():
    st.divider()
    st.header("Export Report")

    markdown_report = build_markdown_report(
        repo_info=st.session_state["repo_info"],
        scan_result=st.session_state["scan_result"],
        indexing_result=st.session_state["indexing_summary"],
        review_report=st.session_state["review_report"],
        internship_report=st.session_state["internship_report"],
    )

    file_name = create_report_filename(
        st.session_state["repo_info"].get("repo_name", "github-review-report")
    )

    st.download_button(
        label="Download Complete Markdown Report",
        data=markdown_report,
        file_name=file_name,
        mime="text/markdown",
    )