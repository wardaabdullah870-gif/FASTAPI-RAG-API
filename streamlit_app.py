import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.title("📚 PDF Question Answering System")
st.write("Upload a PDF and ask questions about its content.")


# -------------------------
# PDF Upload
# -------------------------

st.header("1. Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Upload PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            f"{API_URL}/upload",
            files=files
        )

        if response.status_code == 200:

            data = response.json()

            st.success(data["message"])

            st.write(
                f"**File:** {data['filename']}"
            )

            st.write(
                f"**Pages:** {data['pages']}"
            )

            st.write(
                f"**Chunks:** {data['chunks']}"
            )

        else:
            st.error(
                f"Upload failed: {response.text}"
            )


# -------------------------
# Ask Question
# -------------------------

st.header("2. Ask a Question")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask Question"):

    if not question:
        st.warning("Please enter a question.")

    else:

        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question
            }
        )

        if response.status_code == 200:

            data = response.json()

            st.subheader("Answer")

            st.write(data["answer"])

            st.subheader("Sources")

            for source in data["sources"]:

                st.write(
                    f"📄 Page {source.get('page')} — "
                    f"{source.get('source')}"
                )

        else:

            st.error(
                f"Question failed: {response.text}"
            )