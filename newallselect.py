import os
import sqlite3
import pandas as pd
import streamlit as st
import re
import base64

# Base directory where your files are located
base_directory = r"C:\Users\srija\OneDrive\Desktop\abc"

def highlight_keywords(text, keyword_colors):
    """
    Highlight the keywords in the text using HTML styling with different colors
    """
    for keyword, color in keyword_colors:
        text = re.sub(r'(' + re.escape(keyword) + ')', r'<mark style="background-color: {};">\1</mark>'.format(color), text, flags=re.IGNORECASE)
    return text

def get_download_link(filename):
    """
    Generate a download link for the given filename
    """
    return f"[Download {filename}](./pdfs/{filename})"

def download_file(file_path, file_name):
    full_path = os.path.join(base_directory, file_path)
    with open(full_path, "rb") as file:
        file_content = file.read()
        b64 = base64.b64encode(file_content).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_name}">Download {file_name}</a>'
        return href

def search_data(db_name, keywords, category):
    conn = sqlite3.connect(db_name)

    # Prepare SQL query
    if category:
        query = f"SELECT * FROM filedetails WHERE category = ?"
        params = (category,)
    else:
        query = "SELECT * FROM filedetails WHERE category IN ('Contracts', 'ISO', 'Policies')"
        params = ()

    # Fetch data with category
    df = pd.read_sql_query(query, conn, params=params)

    conn.close()

    # Split keywords by comma and assign colors
    keyword_list = [keyword.strip() for keyword in keywords.split(",")]
    colors = ['#ff0000', '#00ff00', '#0000ff']  # Example colors: red, green, blue
    keyword_colors = list(zip(keyword_list, colors))

    # Filter DataFrame based on keywords
    filtered_df = df[df['text'].apply(lambda x: all(keyword.lower() in x.lower() for keyword in keyword_list))]

    # Highlight keywords in text column
    filtered_df['text'] = filtered_df['text'].apply(lambda x: highlight_keywords(x, keyword_colors))

    # Add download link column
    filtered_df['Download'] = filtered_df.apply(lambda row: download_file(os.path.join(row['category'], row['filename']), row['filename']), axis=1)

    # Drop duplicates based on 'filename', 'text', 'pagenumber', and 'category'
    filtered_df = filtered_df.drop_duplicates(subset=['filename', 'text', 'pagenumber', 'category'])

    return filtered_df

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
    keyword = st.text_input("Enter keywords separated by commas to search:", "")

    # Category selection
    category = st.selectbox(
        "Select Category:",
        ("", "Contracts", "ISO", "Policies")
    )

    if st.button("Search"):
        # Fetch data based on keywords and category
        df = search_data(db_name, keyword, category if category else None)

        # Display results in Streamlit custom table
        if df.empty:
            st.write(f"No results found for keywords '{keyword}' in the selected category.")
        else:
            st.write(df.drop(columns=['filename']).to_html(escape=False, index=False), unsafe_allow_html=True)
