import streamlit as st

from kvkk.detection import find_all
from kvkk.protection import protect_text

st.set_page_config(page_title="KVKK Data Masking", layout="wide")
st.title("KVKK Personal Data Masking Tool")
st.caption("Detects and protects personal data in text. Do not enter real personal data.")

text = st.text_area("Paste your text here", height=200)

if st.button("Protect"):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        findings = find_all(text)
        protected = protect_text(text, findings)

        left, right = st.columns(2)
        with left:
            st.subheader("Original")
            st.text(text)
        with right:
            st.subheader("Protected")
            st.text(protected)

        st.info(f"{len(findings)} personal data item(s) found.")
