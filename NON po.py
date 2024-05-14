import streamlit as st
import matplotlib.pyplot as plt
from analyze_excel import process_data
import seaborn as sns
import base64
from io import BytesIO
import pandas as pd
import re
def on_upload_click():
    """
    Callback function for the upload button click event.
    """
    st.session_state.upload = True

def on_analyse_click():
    """
    Callback function for the analyse button click event.
    """
    st.session_state.analyse = True

# Initialize session state keys
if 'upload' not in st.session_state:
    st.session_state.upload = False
    st.session_state.upload_disabled = True

if 'analyse' not in st.session_state:
    st.session_state.analyse = False

st.set_page_config(layout="wide")

with st.expander("Upload Excel Files", expanded=False):
    with st.form("my_form"):
        # File Uploader
        files = st.file_uploader("Active Assets", type="xlsx", accept_multiple_files=True, key="file_uploader")
        if not files:
            st.session_state.upload_disabled = True
            st.session_state.upload = False
        else:
            st.session_state.upload_disabled = False
        # Add the submit button
        submit_button = st.form_submit_button("UPLOAD")

# Automatically trigger upload when files are selected
if files:
    on_upload_click()

if st.session_state.upload:
    # Process only the first file from the list
    grouped_data = process_data(files[0])
    t1, t2 = st.tabs(["Yearly Analysis", "Overall Analysis"])
    with t1:
        selected_year = st.selectbox('Select Year', grouped_data['year'].unique())
        filtered_data = grouped_data[grouped_data['year'] == selected_year]

        # Define card styles
        card1_style = """
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background-color: #ffffff;
                    padding: 10px;
                    border-radius: 10px;
                    font-style: bold:
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    max-width: 200px; /* Adjust the max-width as needed */
                    margin-left: 50px; /* Set left margin to auto */
                    # margin-right: auto; /* Set right margin to auto */
                """

        card2_style = """
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background-color: #ffffff;
                    padding: 10px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    max-width: 200px; /* Adjust the max-width as needed */
                    margin-left: 50px; /* Set left margin to auto */
                    # margin-right: auto; /* Set right margin to auto */
                """

        # Layout the cards

        card1, card2 = st.columns(2)
        with card1:
            Total_Amount_Alloted = filtered_data['Total_Alloted_Amount/year'].iloc[0]
            st.markdown(
                f"<h3 style='text-align: center; font-size: 25px;'>Total Amount Alloted (in Crores)</h3>",
                unsafe_allow_html=True
            )
            Total_alloted = Total_Amount_Alloted / 10000000
            st.markdown(
                f"<div style='{card1_style}'>"
                f"<h2 style='color: #007bff; text-align: center; font-size: 35px;'>₹ {Total_alloted:,.2f} Crores</h2>"
                "</div>",
                unsafe_allow_html=True
            )
            st.write("")
            st.write(
                "<h2 style='text-align: center; font-size: 25px; font-weight: bold; color: black;'>Amount Used per Year</h2>",
                unsafe_allow_html=True)
            plt.figure(figsize=(8, 5))  # Adjust figure size
            bars = sns.barplot(x=filtered_data['category'],
                               y=filtered_data['percentage_Yearly_Alloted_Amount\Category'],
                               color='darkblue', edgecolor='none', saturation=0.75,width = 0.4)  # Set bar color and remove borders

            plt.xlabel('Category', fontsize=12, fontweight='bold', color='black')  # Customize x-axis label
            plt.ylabel('Percentage of Amount Used per Year', fontsize=12, fontweight='bold',
                       color='black')  # Customize y-axis label
            plt.xticks(fontsize=10)  # Rotate x-axis labels and adjust font size
            plt.yticks(fontsize=10)  # Adjust font size of y-axis labels
            plt.tight_layout()

            # Adding value labels on top of bars
            for bar in bars.patches:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom',
                         fontsize=14)
            plt.grid(False)  # Remove gridlines

            # Adjust space between bars
            plt.subplots_adjust(wspace=0.3)

            # Show only the x and y-axis
            plt.gca().spines['top'].set_visible(False)  # Hide top spine
            plt.gca().spines['right'].set_visible(False)  # Hide right spine

            # Show plot in Streamlit
            st.pyplot(plt)

        with card2:
            Total_Transaction = filtered_data['overall_transactions/year'].iloc[0]
            st.markdown(
                f"<h3 style='text-align: center; font-size: 25px;'>Total Transactions</h3>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div style='{card2_style}'>"
                f"<h2 style='color: #28a745; text-align: center;'>{Total_Transaction:,}</h2>"
                "</div>",
                unsafe_allow_html=True
            )
            st.write("")
            st.write(
                "<h2 style='text-align: center; font-size: 25px; font-weight: bold; color: black;'>Transactions made per Year</h2>",
                unsafe_allow_html=True)
            plt.figure(figsize=(8, 5))
            bars = sns.barplot(x=filtered_data['category'], y=filtered_data['overall_transactions/category/year'],
                               color='darkblue', edgecolor='none',
                               saturation=0.75,width = 0.4)  # Adjust saturation for darker color

            plt.xlabel('Category', fontsize=12, fontweight='bold', color='black')  # Customize x-axis label
            plt.ylabel('Transactions ', fontsize=12, fontweight='bold',
                       color='black')  # Customize y-axis label
            plt.xticks(fontsize=10)  # Rotate x-axis labels and adjust font size
            plt.yticks(fontsize=10)  # Adjust font size of y-axis labels
            plt.tight_layout()

            # Remove gridlines
            plt.grid(False)

            # Adding value labels on top of bars
            for bar in bars.patches:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom',
                         fontsize=14)
            plt.gca().spines['top'].set_visible(False)  # Hide top spine
            plt.gca().spines['right'].set_visible(False)  # Hide right spine

            # Adjust space between bars
            plt.subplots_adjust(wspace=0.05)

            # Show plot in Streamlit
            st.pyplot(plt)
            st.write("")
            st.write("")
        # Create four columns for the select boxes
        # Add 'Cost Ctr' and 'G/L' to the unique categories list
        unique_categories = grouped_data['category'].unique()

        # Add 'All' option to the unique categories list
        unique_categories_with_options = ['All'] + list(unique_categories) + ['Cost Ctr', 'G/L']

        # Selectbox to choose category or other options
        selected_category = st.selectbox("Select Category or Option:", unique_categories_with_options)

        # Get all unique values in the 'Cost Ctr' column
        all_cost_ctrs = grouped_data['Cost Ctr'].unique()

        # Set selected_cost_ctr to represent all values in the 'Cost Ctr' column
        selected_cost_ctr = 'All'  # or all_cost_ctrs if you want the default to be all values

        # Filter the data based on the selected year and dropdown selections
        filtered_data = grouped_data[grouped_data['year'] == selected_year]
        df = grouped_data[grouped_data['year'] == selected_year]
        filtered_transactions = grouped_data[grouped_data['year'] == selected_year]

        if selected_category != 'All':
            if selected_category == 'Cost Ctr':
                filtered_data = filtered_data.sort_values(by='Cumulative_Alloted/Cost Ctr/Year', ascending=False)
                filtered_data.reset_index(drop=True, inplace=True)
                filtered_transactions = filtered_transactions.sort_values(by='Cumulative_transactions/Cost Ctr/Year',
                                                                          ascending=False)
                filtered_transactions.reset_index(drop=True, inplace=True)  # Reset index here
            elif selected_category == 'G/L':
                filtered_data = filtered_data.sort_values(by='Cumulative_Alloted/G/L/Year', ascending=False)
                filtered_data.reset_index(drop=True, inplace=True)
                filtered_transactions = filtered_transactions.sort_values(by='Cumulative_transactions/G/L/Year',
                                                                          ascending=False)
                filtered_transactions.reset_index(drop=True, inplace=True)  # Reset index here
            else:
                filtered_data = filtered_data[filtered_data['category'] == selected_category]
                filtered_transactions = filtered_transactions[filtered_transactions['category'] == selected_category]
                filtered_data = filtered_data.sort_values(by='percentage_of_amount/category_used/year', ascending=False)
                filtered_data.reset_index(drop=True, inplace=True)
                filtered_transactions = filtered_transactions.sort_values(by='overall_transactions/category/year',
                                                                          ascending=False)
                filtered_transactions.reset_index(drop=True, inplace=True)  # Reset index here

        col1, col2 = st.columns(2)

        with col1:
            st.write("Payment Details")
            st.write(filtered_data[['Vendor Name', 'Vendor', 'Transations/year/Vendor', 'Amount_used/Year',
                                    'percentage_of_amount/category_used/year', 'G/L', 'Cost Ctr',
                                    'Cumulative_Alloted/Cost Ctr/Year', 'Cumulative_Alloted/G/L/Year']]
                     .reset_index(drop=True))

        with col2:
            st.write("Transaction Details")
            st.write(filtered_transactions[['Vendor Name', 'Vendor', 'Transations/year/Vendor', 'Amount_used/Year',
                                            'percentage_of_amount/category_used/year', 'G/L', 'Cost Ctr',
                                            'Cumulative_Alloted/Cost Ctr/Year', 'Cumulative_Alloted/G/L/Year',
                                            'overall_transactions/category/year', 'Cumulative_transactions/G/L/Year']]
                     .reset_index(drop=True))
        excel_buffer = BytesIO()
        df = df.sort_values(by='percentage_of_amount/category_used/year', ascending=False)
        df.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)  # Reset the buffer's position to the start for reading

        # Convert Excel buffer to base64
        excel_b64 = base64.b64encode(excel_buffer.getvalue()).decode()

        # Download link for Excel file within a Markdown
        download_link = f'<a href="data:file/xls;base64,{excel_b64}" download="filtered_data.xlsx">Download Excel file</a>'
        st.markdown(download_link, unsafe_allow_html=True)