import streamlit as st
from pdf2image import convert_from_path
import pytesseract
import os
from PIL import Image
import re
import base64
from fpdf import FPDF

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configure Streamlit page
st.set_page_config(
    page_title="Hyundai Motor India Limited",
    layout="wide",
)
st.title('Contracts, Policies, and ISO Search BOT')
st.markdown('<style>h1{text-decoration: underline;text-align: center;}</style>', unsafe_allow_html=True)
st.markdown('<style>body{background-color: #f4f4f4;}</style>', unsafe_allow_html=True)

# CSS for centering the button
st.markdown("""
    <style>
        .centered_button {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

def get_context_with_keyword(text, keyword, num_lines=2):
    lines = text.split('\n')
    context_lines = []
    counter = 0
    page_number = 1

    for line in lines:
        if keyword in line.lower():
            context_lines.extend(lines[max(0, counter - num_lines):counter + num_lines + 1])
            context_lines.append(f"Page: {page_number}")  # Add page number
            context_lines.append("-----")  # Add a separator line after each occurrence
        counter += 1
        if '-----' in line:
            page_number += 1

    highlighted_lines = []
    for line in context_lines:
        highlighted_line = re.sub(r'(\b' + re.escape(keyword) + r'\b)',
                                  r'<span style="font-weight: bold; color: red;">\1</span>', line, flags=re.IGNORECASE)
        highlighted_lines.append(highlighted_line)

    return highlighted_lines

def extract_text_with_context(pdf_path, keywords, num_lines=2):
    images = convert_from_path(pdf_path)
    page_number = 1
    extracted_text = ""
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text += text + "\n"
        contains_all_keywords = all(keyword.strip().lower() in text.lower() for keyword in keywords)
        if contains_all_keywords:
            context = []
            for keyword in keywords:
                context.extend(get_context_with_keyword(text, keyword, num_lines))
            context.append(f"Page: {page_number}")
            return context, extracted_text
        page_number += 1

def download_file(file_path, file_name):
    with open(file_path, "rb") as file:
        file_content = file.read()
        b64 = base64.b64encode(file_content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'
        return href

def save_text_as_txt(text, output_path):
    with open(output_path, "w") as txt_file:
        txt_file.write(text)

def main():
    base_folder_path = r"C:\Users\srija\OneDrive\Desktop\abc"
    subfolders = [folder for folder in os.listdir(base_folder_path) if
                  os.path.isdir(os.path.join(base_folder_path, folder))]

    query = st.text_input("Enter keywords separated by commas", max_chars=50, key="search_input")

    if len(query) >= 2:
        with st.markdown('<div class="centered_button">', unsafe_allow_html=True):
            if st.button("Search"):
                keywords = [keyword.strip().lower() for keyword in query.split(",")]

                col1, col2, col3 = st.columns(3)

                for subfolder in subfolders:
                    subfolder_path = os.path.join(base_folder_path, subfolder)
                    pdf_files = [file for file in os.listdir(subfolder_path) if file.lower().endswith(".pdf")]

                    for pdf_file in pdf_files:
                        pdf_path = os.path.join(subfolder_path, pdf_file)
                        context, extracted_text = extract_text_with_context(pdf_path, keywords,
                                                                            num_lines=3)
                        if context:
                            if "contracts" in subfolder.lower():
                                with col1:
                                    st.markdown("**<u><span style='font-size: large'>Contracts</span></u>**",
                                                unsafe_allow_html=True)
                                    st.markdown(f"**File '{pdf_file}':**")
                                    download_link = download_file(pdf_path, pdf_file)
                                    st.markdown(download_link, unsafe_allow_html=True)
                                    with st.expander("Show Context"):
                                        for line in context:
                                            st.markdown(line, unsafe_allow_html=True)
                                    txt_file_path = f"{pdf_file.replace('.pdf', '_readable.txt')}"
                                    save_text_as_txt(extracted_text, txt_file_path)
                                    st.markdown(download_file(txt_file_path, txt_file_path.split('/')[-1]),
                                                unsafe_allow_html=True)
                            elif "policies" in subfolder.lower():
                                with col2:
                                    st.markdown("**<u><span style='font-size: large'>Policies</span></u>**",
                                                unsafe_allow_html=True)
                                    st.markdown(f"**File '{pdf_file}':**")
                                    download_link = download_file(pdf_path, pdf_file)
                                    st.markdown(download_link, unsafe_allow_html=True)
                                    with st.expander("Show Context"):
                                        for line in context:
                                            st.markdown(line, unsafe_allow_html=True)
                                    txt_file_path = f"{pdf_file.replace('.pdf', '_readable.txt')}"
                                    save_text_as_txt(extracted_text, txt_file_path)
                                    st.markdown(download_file(txt_file_path, txt_file_path.split('/')[-1]),
                                                unsafe_allow_html=True)
                            elif "iso" in subfolder.lower():
                                with col3:
                                    st.markdown("**<u><span style='font-size: large'>ISO</span></u>**",
                                                unsafe_allow_html=True)
                                    st.markdown(f"**File '{pdf_file}':**")
                                    download_link = download_file(pdf_path, pdf_file)
                                    st.markdown(download_link, unsafe_allow_html=True)
                                    with st.expander("Show Context"):
                                        for line in context:
                                            st.markdown(line, unsafe_allow_html=True)
                                    txt_file_path = f"{pdf_file.replace('.pdf', '_readable.txt')}"
                                    save_text_as_txt(extracted_text, txt_file_path)
                                    st.markdown(download_file(txt_file_path, txt_file_path.split('/')[-1]),
                                                unsafe_allow_html=True)

if __name__ == "__main__":
    main()
