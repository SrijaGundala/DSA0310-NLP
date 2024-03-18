import streamlit as stm
from datetime import datetime

class Editor:
    @staticmethod
    def main():
        # Initialize SessionState to store and update S.no
        session_state = stm.session_state
        if not hasattr(session_state, "descriptions"):
            session_state.descriptions = []
        if not hasattr(session_state, "categories"):
            session_state.categories = []
        if not hasattr(session_state, "incharges"):
            session_state.incharges = []
        if not hasattr(session_state, "output_files"):
            session_state.output_files = []
        if not hasattr(session_state, "manuals"):
            session_state.manuals = []
        if not hasattr(session_state, "times"):
            session_state.times = []

        stm.title("RED FLAG / AUDIT EXCEPTIONS")
        stm.markdown('<style>h1{color: black; text-align: center;}</style>', unsafe_allow_html=True)

        # Display form for adding entries
        description = stm.text_input("Description")
        category = stm.text_input("Category")
        incharge = stm.text_input("Incharge")
        output_file = stm.file_uploader("Output File", type=["xlsx"])
        manual = stm.file_uploader("Manual", type=["docx"])

        # Add entry when "Submit" button is clicked
        if stm.button("Submit"):
            session_state.descriptions.append(description)
            session_state.categories.append(category)
            session_state.incharges.append(incharge)
            session_state.output_files.append(output_file)
            session_state.manuals.append(manual)
            session_state.times.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # Add current time

        # Divide the page into 7 columns
        col1, col2, col3, col4, col5, col6, col7, col8 = stm.columns(8)

        # Display attributes in respective columns
        col1.write("S.no:")
        for i in range(len(session_state.descriptions)):
            col1.write(i + 1)  # Display serial number starting from 1

        col2.write("Descriptions")
        for desc in session_state.descriptions:
            col2.write(desc)

        col3.write("Categories")
        for cat in session_state.categories:
            col3.write(cat)

        col4.write("Incharges")
        for inchrge in session_state.incharges:
            col4.write(inchrge)

        col5.write("Output Files")
        for output_file in session_state.output_files:
            if output_file is not None:
                col5.write(output_file.name)  # Display file name
            else:
                col5.write("None")

        col6.write("Manuals:")
        for manual in session_state.manuals:
            if manual is not None:
                col6.write(manual.name)  # Display file name
            else:
                col6.write("None")

        col7.write("Date and Time:")
        for time in session_state.times:
            col7.write(time)

# Run the Editor app
Editor.main()
