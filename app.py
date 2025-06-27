import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="PDF Extractor", layout="wide")
st.title("📄 PDF Extractor – Metadata, Text, Links + Unique Images")

uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"✅ PDF loaded successfully! Total Pages: {doc.page_count}")

    # Store unique images using their xref as keys
    unique_images = {}

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text()
        links = page.get_links()
        embedded_images = page.get_images(full=True)

        # Collect unique embedded images
        for img in embedded_images:
            xref = img[0]
            if xref not in unique_images:
                try:
                    base_image = doc.extract_image(xref)
                    unique_images[xref] = {
                        "page": i + 1,
                        "image": base_image["image"],
                        "ext": base_image["ext"]
                    }
                except Exception as e:
                    st.error(f"⚠️ Error extracting image on page {i + 1}: {e}")

        # ─── Per Page Content ─────────────────────────────
        st.markdown(f"---\n### 📄 Page {i + 1}")

        # 📑 Page Metadata
        with st.expander("📑 Page Metadata"):
            metadata = {
                "Page Number": i + 1,
                "Size": f"{page.rect.width} x {page.rect.height}",
                "Rotation": page.rotation,
                "Text Length": len(text),
                "Number of Links": len(links),
                "Number of Embedded Images": len(embedded_images)
            }
            st.json(metadata)

        # 📝 Text
        with st.expander("📝 Extracted Text"):
            if text.strip():
                st.text(text)
            else:
                st.warning("No text found on this page.")

        # 🔗 Links
        if links:
            with st.expander("🔗 Page Links"):
                for link in links:
                    st.json(link)
        else:
            st.caption("🔗 No links found on this page.")

    # ─── Final Section: All Unique Embedded Images ─────────────────────
    st.markdown("---")
    st.header("📸 Unique Embedded Images in PDF")

    if unique_images:
        for idx, (xref, item) in enumerate(unique_images.items(), start=1):
            image = Image.open(io.BytesIO(item["image"]))
            st.image(image, caption=f"📷 Image {idx} (first seen on Page {item['page']}, format: {item['ext']})", use_container_width=False)
    else:
        st.info("No embedded images found in the entire PDF.")
else:
    st.info("📤 Upload a PDF file to begin.")

