import csv
import io
import re

import docx
import streamlit as st


def fix_encoding(text):
    # fixes Latin-1 errors and returns UTF-8
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


st.set_page_config(page_title="Sentence Counter", page_icon="📝")
st.title("Essay Sentence Parser")
st.write(
    "Upload a Word document (.docx) to return a file containing the count of each "
    "sentence."
)

uploaded_file = st.file_uploader("Choose a .docx file", type="docx")

if uploaded_file is not None:
    doc = docx.Document(uploaded_file)
    full_text = []
    for para in doc.paragraphs:
        clean_text = fix_encoding(para.text)
        full_text.append(clean_text)

    text_content = " ".join(full_text)

    if text_content.strip():
        """performs a strip() and if text_content is true then the loop fires"""

        # splits into sentences based off of the list of values
        sentences = re.split(r"(?<=[.!?:;])\s+", text_content)
        # removes any empty strings after the split
        sentences = [s.strip() for s in sentences if s.strip()]
        st.success(f"Found **{len(sentences)}** sentences.")
        st.subheader("Word Count per Sentence")
        data = []
        for i, sentence in enumerate(sentences):
            # counting words by whitespace
            word_count = len(sentence.split())
            data.append(
                {
                    "Sentence #": i + 1,
                    "Word Count": word_count,
                    "Preview": (
                        sentence[:50] + "..." if len(sentence) > 50 else sentence
                    ),
                }
            )

        # display as interactive table
        st.dataframe(data, use_container_width=True)
        # downloadable csv
        output = io.StringIO()
        fieldnames = ["Sentence #", "Word Count", "Preview"]

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

        csv_data = output.getvalue()

        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="sentence_counts.csv",
            mime="text/csv",
        )

    else:
        st.warning("The doc looks empty.")
else:
    st.info("Awaiting file upload. Please upload a .docx file to begin.")
