import os
import sqlite3
import pandas as pd
import streamlit as st
import re
import base64

# Base directory where your files are located
base_directory = r"C:\Users\srija\OneDrive\Desktop\abc"

def highlight_keyword(text, keyword):
    """
    Highlight the keyword in the text using HTML styling
    """
    return re.sub(r'(' + keyword + ')', r'<mark style="background-color: red;">\1</mark>', text, flags=re.IGNORECASE)


def get_download_link(filename):
    """
    Generate a download link for the given filename
    """
    return f"[Download {filename}](./pdfs/{filename})"


def download_file(file_path, file_name):
    with open(file_path, "rb") as file:
        file_content = file.read()
        b64 = base64.b64encode(file_content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'
        return href


def search_data(db_name, keyword, category):
    conn = sqlite3.connect(db_name)

    # Prepare SQL query
    query = f"SELECT * FROM filedetails WHERE text LIKE ? AND category = ?"

    # Fetch data with keyword and category
    df = pd.read_sql_query(query, conn, params=('%' + keyword + '%', category))

    conn.close()

    # Highlight keyword in text column
    df['text'] = df['text'].apply(highlight_keyword, keyword=keyword)

    # Add download link column
    df['Download'] = df['filename'].apply(lambda x: download_file(os.path.join(base_directory, category, x), x))

    return df


if __name__ == "__main__":
    db_name = "filedetails.db"
    st.set_page_config(
        page_title="Hyundai Motor India Limited",
        layout="wide",
    )
    st.title('Contracts, Policies, and ISO Search BOT')
    st.markdown('<style>h1{text-decoration: underline;text-align: center;}</style>', unsafe_allow_html=True)
    st.markdown('<style>body{background-color: #f4f4f4;}</style>', unsafe_allow_html=True)
    # Search keyword input
    keyword = st.text_input("Enter keyword to search:", "")

    # Category selection
    category = st.selectbox(
        "Select Category:",
        ("Contracts", "ISO", "Policies")
    )

    if st.button("Search"):
        # Fetch data based on keyword and category
        df = search_data(db_name, keyword, category)

        # Display results in Streamlit custom table
        if df.empty:
            st.write(f"No results found for keyword '{keyword}' in the '{category}' category.")
        else:
            st.write(df.drop(columns=['filename']).to_html(escape=False, index=False), unsafe_allow_html=True)
