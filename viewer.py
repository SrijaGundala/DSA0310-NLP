import streamlit as st
import pandas as pd
import docx2txt
import io

class Viewer:
    def __init__(self, entries):
        self.entries = entries

    def read_excel_file(self, file_buffer):
        try:
            df = pd.read_excel(file_buffer)
            return df
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")

    def read_word_file(self, file_buffer):
        try:
            text = docx2txt.process(file_buffer)
            st.write(text)
        except Exception as e:
            st.error(f"Error reading Word file: {e}")

    def display_entries(self):
        st.title("RED FLAG / AUDIT EXCEPTIONS")
        st.markdown('<style>h1{text-align: center; text-decoration: underline;}</style>', unsafe_allow_html=True)
        st.subheader("View Entries")

        if not self.entries or not isinstance(self.entries, list):
            st.write("No entries available.")
        else:
            # Display column names
            col_names = ["S.no", "Description", "Category", "Incharge", "Output File", "Manual", "Date and Time"]
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            for col, col_name in zip([col1, col2, col3, col4, col5, col6, col7], col_names):
                col.write(col_name)

            # Display entries
            for i, entry in enumerate(self.entries):
                # Display each entry attribute in respective columns
                col1.write(entry.get('S.no', ''))
                col2.write(entry.get('Description', ''))
                col3.write(entry.get('Category', ''))
                col4.write(entry.get('Incharge', ''))

                # Check if the Output File exists
                output_file_buffer = entry.get('Output File')
                if output_file_buffer is not None:
                    # Add a button to read Excel file
                    if col5.button(f"Read Excel {i}"):
                        try:
                            excel_file_buffer = io.BytesIO(output_file_buffer)
                            df = self.read_excel_file(excel_file_buffer)
                            st.write(df)
                        except Exception as e:
                            st.error(f"Error reading Excel file: {e}")
                else:
                    col5.write("No output file uploaded")

                # Check if the Manual file exists
                manual_file_buffer = entry.get('Manual')
                if manual_file_buffer is not None:
                    # Add a button to read Word file
                    if col6.button(f"Read Word {i}"):
                        try:
                            word_file_buffer = io.BytesIO(manual_file_buffer)
                            self.read_word_file(word_file_buffer)
                        except Exception as e:
                            st.error(f"Error reading Word file: {e}")
                else:
                    col6.write("No manual file uploaded")

                col7.write(entry.get('Date and Time', ''))
