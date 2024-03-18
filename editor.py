# editor.py

import streamlit as stm
from datetime import datetime

class Editor:
    def __init__(self):
        self.session_state = stm.session_state
        if "sno" not in self.session_state:
            self.session_state.sno = 1  # Initialize S.no
        if "entries" not in self.session_state:
            self.session_state.entries = []

    def main(self):
        stm.title("RED FLAG / AUDIT EXCEPTIONS")
        stm.markdown('<style>h1{text-align: center; text-decoration: underline;}</style>', unsafe_allow_html=True)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Display form for adding entries
        description = stm.text_input("Description")
        category = stm.text_input("Category")
        incharge = stm.text_input("Incharge")
        output_file = stm.file_uploader("Output File", type=["xlsx"])
        manual = stm.file_uploader("Manual", type=["docx"])

        # Add entry when "Submit" button is clicked
        if stm.button("Submit"):
            entry = {
                "S.no": self.session_state.sno,
                "Description": description,
                "Category": category,
                "Incharge": incharge,
                "Output File": output_file.name if output_file else None,
                "Manual": manual.name if manual else None,
                "Date and Time": current_datetime
            }
            self.session_state.entries.append(entry)

            self.session_state.sno += 1
