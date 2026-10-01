import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import requests

from frontend.formatter import format_docx, format_pdf
from frontend.sanitizer import sanitize_text

API_URL = "http://127.0.0.1:8000/generate"


st.set_page_config(
    page_title="LegalEase",
    layout="centered"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")


doc_type = st.text_input(
    "📄 Document Type",
    "Non-Disclosure Agreement"
)

parties = st.text_area(
    "👥 Parties",
    "Alice (Client), Bob (Consultant)"
)

terms = st.text_area(
    "📜 Terms (use ; for separation)",
    "Confidentiality;No sharing of data;Valid for 1 year"
)

date = st.text_input(
    "📅 Effective Date",
    "Jan 1, 2025"
)


if st.button("🚀 Generate Document"):

    with st.spinner("Generating..."):

        try:
            response = requests.post(
                API_URL,
                json={
                    "document_type": doc_type,
                    "parties": parties,
                    "terms": terms,
                    "date": date
                },
                timeout=120
            )

            if response.status_code == 200:

                text = sanitize_text(
                    response.json()["document"]
                )

                st.session_state["doc"] = text

            else:

                st.error(
                    f"❌ Failed to generate document. "
                    f"Status: {response.status_code}"
                )

                st.code(response.text)

        except requests.exceptions.RequestException as error:

            st.error(
                f"❌ Could not connect to LegalEase API:\n{error}"
            )


if "doc" in st.session_state:

    st.success("✅ Document Generated!")

    edited_text = st.text_area(
        "✏️ Edit Document",
        st.session_state["doc"],
        height=300
    )

    st.download_button(
        "📥 Download TXT",
        edited_text,
        file_name="document.txt"
    )


    if st.button("📄 Generate DOCX"):

        path = format_docx(edited_text)

        with open(path, "rb") as f:

            st.download_button(
                "⬇️ Download DOCX",
                f,
                file_name="document.docx"
            )


    if st.button("📄 Generate PDF"):

        path = format_pdf(edited_text)

        with open(path, "rb") as f:

            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name="document.pdf"
            )