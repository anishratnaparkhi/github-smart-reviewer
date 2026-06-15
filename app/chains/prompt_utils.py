def format_documents_for_prompt(documents) -> str:
    formatted_chunks = []

    for index,document in enumerate(documents, start=1):
        file_path = document.metadata.get("file_path", "Unknown file")
        language = document.metadata.get("language", "Unknown language")
        content = document.page_content

        formatted_chunks.append(
            f"""CHUNK {index}
            File: {file_path}
            Language: {language}
            {content}
            """
        )

    return "\n\n---\n\n".join(formatted_chunks)
