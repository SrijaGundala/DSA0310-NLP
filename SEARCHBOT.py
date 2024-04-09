import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import os
import re
from PIL import Image
from fpdf import FPDF

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit configuration
st.set_page_config(
    page_title="Hyundai Motor India Limited",
    layout="wide",
)
st.title('Contracts, Policies And ISO Search BOT')
st.markdown('<style>h1{text-decoration: underline;text-align: center;}</style>', unsafe_allow_html=True)


def validate_image(text):
    """Placeholder for image validation. Currently always returns True."""
    return True


def get_context_with_keyword(text, keyword, num_lines=2):
    lines = text.split('\n')
    context_lines = []
    counter = 0
    page_number = 1

    for line in lines:
        if keyword in line.lower():
            context_lines.extend(lines[max(0, counter - num_lines):counter + num_lines + 1])
            context_lines.append(f"Page: {page_number}")
        counter += 1
    highlighted_lines = []
    for line in context_lines:
        highlighted_line = re.sub(r'(\b' + re.escape(keyword) + r'\b)',
                                  r'<span style="font-weight: bold; color: red;">\1</span>', line, flags=re.IGNORECASE)
        highlighted_lines.append(highlighted_line)

    # Add a bigger separation line after each occurrence of the keyword in the context
    separated_lines = []
    for idx, line in enumerate(highlighted_lines):
        separated_lines.append(line)
        if (idx + 1) % 4 == 0:  # Add a larger separation after every second line (i.e., after each occurrence)
            separated_lines.append("<hr style='border: 2px solid red;'>")

    return separated_lines


def extract_text_with_context(pdf_path, keywords, num_lines=2):
    images = convert_from_path(pdf_path)
    page_number = 1
    for image in images:
        text = pytesseract.image_to_string(image)
        contains_all_keywords = all(keyword.strip().lower() in text.lower() for keyword in keywords)
        if contains_all_keywords:
            context = []
            for keyword in keywords:
                context.extend(get_context_with_keyword(text, keyword, num_lines))
            context.append(f"Page: {page_number}")
            return context, text
        page_number += 1
    return None, None


def create_readable_pdf(text, output_pdf_path):
    # Encode the text as utf-8 to handle special characters
    text = text.encode('utf-8', 'replace').decode('utf-8')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)

    try:
        pdf.output(output_pdf_path)
        print(f"PDF created successfully: {output_pdf_path}")
    except Exception as e:
        print(f"Error during PDF creation: {e}")


def main():
    base_folder_path = r"C:\Users\srija\OneDrive\Desktop\abc"
    subfolders = [folder for folder in os.listdir(base_folder_path) if
                  os.path.isdir(os.path.join(base_folder_path, folder))]

    readable_folder_path = r"C:\Users\srija\OneDrive\Desktop\Readable"

    # Create subfolders if they don't exist
    for subfolder_name in ["Policies", "ISO", "Contracts"]:
        subfolder_path = os.path.join(readable_folder_path, subfolder_name)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

    query = st.text_input("Enter keywords separated by commas")
    if len(query) >= 2:
        if st.button("Search"):
            keywords = [keyword.strip().lower() for keyword in query.split(",")]

            # Create three columns layout
            col1, col2, col3 = st.columns(3)

            for subfolder in subfolders:
                subfolder_path = os.path.join(base_folder_path, subfolder)
                pdf_files = [file for file in os.listdir(subfolder_path) if file.lower().endswith(".pdf")]

                for pdf_file in pdf_files:
                    pdf_path = os.path.join(subfolder_path, pdf_file)
                    context = extract_text_with_context(pdf_path, keywords, num_lines=3)
                    if context:
                        if "contracts" in subfolder.lower():
                            with col1:
                                st.markdown("*<u><span style='font-size: large'>Contracts</span></u>*", unsafe_allow_html=True)
                                st.markdown(f"*File '{pdf_file}':*")
                                st.markdown(f"[Download Contracts](data:application/octet-stream;base64,{pdf_path.encode('utf-8').hex()})")
                                with st.expander("Show Context"):
                                    for line in context:
                                        st.markdown(line, unsafe_allow_html=True)
                        elif "policies" in subfolder.lower():
                            with col2:
                                st.markdown("*<u><span style='font-size: large'>Policies</span></u>*", unsafe_allow_html=True)
                                st.markdown(f"*File '{pdf_file}':*")
                                st.markdown(f"[Download Policies](data:application/octet-stream;base64,{pdf_path.encode('utf-8').hex()})")
                                with st.expander("Show Context"):
                                    for line in context:
                                        st.markdown(line, unsafe_allow_html=True)
                        elif "iso" in subfolder.lower():
                            with col3:
                                st.markdown("*<u><span style='font-size: large'>ISO</span></u>*", unsafe_allow_html=True)
                                st.markdown(f"*File '{pdf_file}':*")
                                st.markdown(f"[Download ISO](data:application/octet-stream;base64,{pdf_path.encode('utf-8').hex()})")
                                with st.expander("Show Context"):
                                    for line in context:
                                        st.markdown(line, unsafe_allow_html=True)


if _name_ == "_main_":
    main()