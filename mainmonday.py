import os
import sqlite3
import pytesseract
from PIL import Image
import fitz
import cv2
import numpy as np
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def correct_skewness(image):
    """
    Corrects skewness of the image, if necessary
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def extract_text_from_image(image):
    """
    Extract text from image using pytesseract
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    return text.strip()

def check_scanned_pdf(pdf_file):
    """
    Check if PDF contains images
    """
    images = []

    pdf_doc = fitz.open(pdf_file)
    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            images.append((image, page_num + 1))  # Tuple with image and page number

    return images

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF using OCR for scanned PDFs
    """
    extracted_texts = []

    images = check_scanned_pdf(pdf_file)
    if images:
        for image, page_num in images:
            deskewed_image = correct_skewness(image)
            text = extract_text_from_image(deskewed_image)
            extracted_texts.append((page_num, text.strip()))

    if not extracted_texts:
        pdf_doc = fitz.open(pdf_file)
        extracted_texts = [(index + 1, page.get_text().strip()) for index, page in enumerate(pdf_doc)]

    return extracted_texts

def create_sqlite_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS filedetails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        category TEXT,
        pagenumber INTEGER,
        text TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_into_sqlite_table(db_name, file_name, category, texts):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert data
    for page_num, text in texts:
        cursor.execute("INSERT INTO filedetails (filename, category, pagenumber, text) VALUES (?, ?, ?, ?)",
                       (file_name, category, page_num, text))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    base_directory = r"C:\Users\srija\OneDrive\Desktop\abc"
    db_name = "filedetails.db"

    # Create SQLite table
    create_sqlite_table(db_name)

    # Iterate through subfolders and extract text from PDFs
    for subfolder in ['Contracts', 'Policies', 'ISO']:
        sub_src_folder = os.path.join(base_directory, subfolder)
        for filename in os.listdir(sub_src_folder):
            if filename.endswith('.pdf'):
                src_path = os.path.join(sub_src_folder, filename)

                # Check if file exists in SQLite database
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT filename FROM filedetails WHERE filename=?", (filename,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    print(f"File {filename} already exists in the database.")
                else:
                    # Extract text from PDF
                    texts = extract_text_from_pdf(src_path)

                    # Insert into SQLite table
                    insert_into_sqlite_table(db_name, filename, subfolder, texts)
                    print(f"Inserted text from {filename} in folder {subfolder} into SQLite table")
