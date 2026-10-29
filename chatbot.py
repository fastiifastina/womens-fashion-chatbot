
import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

st.title("Women's Fashion Chatbot 👗")
st.write("Upload your fashion PDF and ask questions!")

api_key = os.getenv("GEMINI_API_KEY")

uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pdf_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

    if pdf_text.strip():
        st.success("PDF uploaded and read successfully!")

        question = st.text_input(
            "Ask a question about women's fashion:"
        )

        if st.button("Ask AI"):
            if not api_key:
                st.error("API key not found. Check your .env file.")
            elif not question.strip():
                st.warning("Please enter a question.")
            else:
                try:
                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=(
                            "Answer the user's question using the PDF "
                            "content below. If the answer is not in the "
                            "PDF, say so clearly.\n\n"
                            f"PDF content:\n{pdf_text[:30000]}\n\n"
                            f"Question: {question}"
                        )
                    )

                    st.subheader("Answer")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")
    else:
        st.warning("No readable text found in this PDF.")
