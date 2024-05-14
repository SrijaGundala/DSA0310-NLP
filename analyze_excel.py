import pandas as pd
import streamlit as st
@st.cache_resource(show_spinner=False)
# Function to concatenate and aggregate data
def process_data(files):
    data = pd.read_excel(files)
    df1 = pd.read_excel(
        r"C:\Users\srija\OneDrive\Desktop\nonPO\costctr.xlsx",
        header=1)
    df2 = pd.read_excel(
        r"C:\Users\srija\OneDrive\Desktop\nonPO\GLNAME.xlsx",
        header=1)
    df = data.copy()
    dfcost = df1.copy()
    dfGL = df2.copy()
    dfcost = dfcost.rename(columns={'Short text': 'CostctrName'})
    dfcost = dfcost[['Cost Ctr', 'CostctrName']]
    dfGL = dfGL.rename(columns={'Long Text': 'G/L Name'})
    dfGL = dfGL.rename(columns={'G/L Acct': 'G/L'})
    mapping = dict(zip(dfGL['G/L'], dfGL['G/L Name']))
    df['G/L Name'] = df['G/L'].map(mapping)
    mapping = dict(zip(dfcost['Cost Ctr'], dfcost['CostctrName']))
    df['CostctrName'] = df['Cost Ctr'].map(mapping)
    filtered_df = df
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df.index += 1
    filtered_df['Pstng Date'] = pd.to_datetime(filtered_df['Pstng Date'], errors='coerce')
    filtered_df['year'] = filtered_df['Pstng Date'].dt.year
    df = filtered_df.copy()
    df['Cummulative_transactions'] = len(df)
    df['Cummulative_transactions/category'] = df.groupby('category')['category'].transform('count')
    df['overall_transactions/year'] = df.groupby('year')['year'].transform('count')
    df['overall_transactions/category/year'] = df.groupby(['category', 'year'])['category'].transform('count')
    df['cumulative_Transations/Vendor'] = df.groupby('Vendor')['Vendor'].transform('count')
    df['Transations/year/Vendor'] = df.groupby(['year', 'Vendor'])['Vendor'].transform('count')
    df['Cumulative_percentransations_made'] = (df['cumulative_Transations/Vendor'] / df[
        'Cummulative_transactions']) * 100
    df['Cumulative_percentransations_made/category'] = (df['cumulative_Transations/Vendor'] / df[
        'Cummulative_transactions/category']) * 100
    df['percentransations_made/category/year'] = (df['Transations/year/Vendor'] / df[
        'overall_transactions/category/year']) * 100
    df['percentransations_made/year'] = (df['Transations/year/Vendor'] / df['overall_transactions/year']) * 100
    df['cumulative_Alloted_Amount'] = df['Amount'].sum()
    df['cumulative_Alloted_Amount\Category'] = df.groupby('category')['Amount'].transform('sum')
    yearly_total = df.groupby('year')['Amount'].sum().reset_index()
    yearly_total.rename(columns={'Amount': 'Total_Alloted_Amount/year'}, inplace=True)
    df = pd.merge(df, yearly_total, on='year', how='left')
    df['Yearly_Alloted_Amount\Category'] = df.groupby(['category', 'year'])['Amount'].transform('sum')
    df['Cumulative_Amount_used'] = df.groupby(['Vendor', 'category'])['Amount'].transform('sum')
    df['Amount_used/Year'] = df.groupby(['Vendor', 'year', 'category'])['Amount'].transform('sum')
    df['Cumulative_percentageamount_used'] = (df['Cumulative_Amount_used'] / df['cumulative_Alloted_Amount']) * 100
    df['total_percentage_of_amount/category_used'] = (df['Cumulative_Amount_used'] / df[
        'cumulative_Alloted_Amount\Category']) * 100
    df['percentage_amount_used_per_year'] = (df['Amount_used/Year'] / df['Total_Alloted_Amount/year']) * 100
    df['percentage_of_amount/category_used/year'] = (df['Amount_used/Year'] / df[
        'Yearly_Alloted_Amount\Category']) * 100
    df['percentage_Yearly_Alloted_Amount\Category'] = (df['Yearly_Alloted_Amount\Category'] / df[
        'Total_Alloted_Amount/year']) * 100
    df['Cumulative_transactions/Cost Ctr'] = df.groupby(['Cost Ctr'])['Cost Ctr'].transform('count')
    df['Cumulative_transactions/Cost Ctr/Year'] = df.groupby(['Cost Ctr','year'])['Cost Ctr'].transform('count')
    df['Cumulative_Alloted/Cost Ctr'] = df.groupby(['Cost Ctr'])['Amount'].transform('sum')
    df['Cumulative_Alloted/Cost Ctr/Year'] = df.groupby(['Cost Ctr','year'])['Amount'].transform('sum')
    df['Percentage_Cumulative_Alloted/Cost Ctr'] = (df['Cumulative_Alloted/Cost Ctr'] / df['cumulative_Alloted_Amount']) * 100
    df['Percentage_Cumulative_Alloted/Cost Ctr/Year'] = (df['Cumulative_Alloted/Cost Ctr/Year'] / df['Total_Alloted_Amount/year']) * 100
    df['Cumulative_transactions/G/L'] = df.groupby(['G/L'])['G/L'].transform('count')
    df['Cumulative_transactions/G/L/Year'] = df.groupby(['G/L', 'year'])['G/L'].transform('count')
    df['Cumulative_Alloted/G/L'] = df.groupby(['G/L'])['Amount'].transform('sum')
    df['Cumulative_Alloted/G/L/Year'] = df.groupby(['G/L', 'year'])['Amount'].transform('sum')
    df['Percentage_Cumulative_Alloted/G/L'] = (df['Cumulative_Alloted/G/L'] / df[
        'cumulative_Alloted_Amount']) * 100
    df['Percentage_Cumulative_Alloted/G/L/Year'] = (df['Cumulative_Alloted/G/L/Year'] / df[
        'Total_Alloted_Amount/year']) * 100
    df = df.drop_duplicates(subset=['Vendor', 'year'], keep='first')
    df = df.sort_values(by='percentage_of_amount/category_used/year', ascending=False)
    df.reset_index(drop=True, inplace=True)
    df['Vendor'] = df['Vendor'].astype(str)
    df.reset_index(drop=True, inplace=True)
    return df
