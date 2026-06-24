import os
from typing import Final

import requests
import streamlit as st

from converter_service import convert_bytes_to_markdown

DEFAULT_BACKEND_URL: Final[str] = "http://127.0.0.1:8000"


def main() -> None:
    st.set_page_config(page_title="MarkItDown Converter", page_icon="MD", layout="wide")
    st.title("Markdown Converter")
    st.caption(
        "Upload a file, convert it to Markdown, and optionally route the request through the backend API."
    )

    with st.sidebar:
        st.subheader("Runtime")
        backend_url = st.text_input(
            "Backend URL",
            value=os.getenv("MARKITDOWN_BACKEND_URL", DEFAULT_BACKEND_URL),
        ).rstrip("/")
        use_backend = st.checkbox("Use backend when available", value=True)
        use_plugins = st.checkbox("Enable plugins", value=False)

    uploaded_file = st.file_uploader(
        "Upload a file",
        type=["pdf", "docx", "pptx", "txt", "md", "html", "csv", "json", "xml", "xlsx", "xls"],
    )

    if uploaded_file is not None:
        left_column, right_column = st.columns([1, 1])

        with left_column:
            st.write("**Selected file**")
            st.write(uploaded_file.name)
            st.write(f"{uploaded_file.size} bytes")

        convert_clicked = st.button("Convert to Markdown", type="primary")

        if convert_clicked:
            file_bytes = uploaded_file.getvalue()
            markdown_text = None
            source = "local"

            if use_backend:
                try:
                    response = requests.post(
                        f"{backend_url}/convert",
                        files={
                            "file": (
                                uploaded_file.name,
                                file_bytes,
                                uploaded_file.type or "application/octet-stream",
                            )
                        },
                        data={"use_plugins": str(use_plugins).lower()},

                        timeout=60,
                    )
                    response.raise_for_status()
                    payload = response.json()
                    markdown_text = payload.get("markdown", "")
                    source = f"backend ({backend_url})"
                except Exception as exc:
                    st.warning(f"Backend unavailable, using local conversion instead: {exc}")

            if markdown_text is None:
                markdown_text = convert_bytes_to_markdown(
                    file_bytes,
                    uploaded_file.name,
                    use_plugins=use_plugins,
                )

            with right_column:
                st.success(f"Conversion complete using {source}.")
                st.download_button(
                    "Download Markdown",
                    data=markdown_text,
                    file_name=f"{uploaded_file.name}.md",
                    mime="text/markdown",
                )
                st.text_area(
                    "Markdown output",
                    markdown_text,
                    height=500,
                )
    else:
        st.info("Choose a document to convert.")


if __name__ == "__main__":
    main()

