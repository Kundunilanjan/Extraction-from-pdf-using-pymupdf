import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Text Extractor from PDF", layout="wide")
st.title("📄 Text Extractor from PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Load the PDF document
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    # Metadata and page count
    st.success(f"PDF loaded successfully with {doc.page_count} pages.")
    with st.expander("📑 PDF Metadata"):
        st.json(doc.metadata)

    # Iterate through each page
    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text()
        links = page.get_links()
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes("png")))

        st.subheader(f"📄 Page {i + 1}")

        # Show text
        with st.expander("📝 Extracted Text"):
            if text.strip():
                st.text(text)
            else:
                st.warning("No text found on this page.")

        # Show image of the page
        st.image(image, caption=f"Rendered Page {i + 1}", use_container_width=True)

        # Show links
        with st.expander("🔗 Page Links"):
            if links:
                for link in links:
                    st.json(link)
            else:
                st.caption("No links found on this page.")

else:
    st.info("Please upload a PDF file to begin.")
