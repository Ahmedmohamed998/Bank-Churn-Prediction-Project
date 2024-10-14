import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st

st.set_page_config(page_title="Churn Modelling Dashboard", layout="wide")
st.title("Churn Modelling Dashboard")
st.markdown("")
st.markdown("")
@st.cache_data
def df_get_from_csv():
    df = pd.read_csv(r"E:\road masr\project\Bank churn.csv")
    return df

df = df_get_from_csv()
df.drop(['Unnamed: 0'],axis=1,inplace=True)
df['Exited'] = [1 if i > 0.5 else 0 for i in df['Exited']]
df.drop_duplicates(inplace=True)
df['joining_year'] = 2024 - df['Tenure']

# Streamlit app
# Side bar
st.sidebar.header("Please filter here:")
gender = st.sidebar.multiselect("Select Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
year = st.sidebar.multiselect("Select Year", options=df['joining_year'].unique(), default=df['joining_year'].unique())
exited = st.sidebar.multiselect("Select if customer exited or not", options=df['Exited'].unique(), default=df['Exited'].unique())
df = df.query('Gender == @gender & joining_year == @year & Exited == @exited')

# Calculate total number of customers and total balance
total_customers = df.shape[0]
total_balance = df['Balance'].sum()

# Display total number of customers and total balance at the top of the app
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### Total Number of Customers: {total_customers}")
with col2:
    st.markdown(f"### Total Balance: ${total_balance:,.2f}")
st.markdown("")
st.markdown("")
# Create a layout with three columns
col1, col2, col3 = st.columns([2, 2, 2])

# Gender Distribution Pie Chart
with col1:
    st.subheader("Gender Distribution")
    fig = px.pie(df, names='Gender', title="Gender Distribution", color_discrete_sequence=['blue', 'pink'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- Approximately 58% of the customers are male.""")

# Age Distribution Histogram
with col2:
    st.subheader("Age Distribution")
    fig = px.histogram(df, x='Age', title="Age Distribution", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='blue', width=2)))
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- The average age of customers is around 36.23 years.""")

# Churned Customers by Age Group
with col3:
    st.subheader("Churned Customers by Age Group")
    age_bins = [18, 30, 40, 50, 54]
    age_labels = ['18-30', '31-40', '41-50', '51-53']
    df['AgeGroup'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)
    churn_count = df[df['Exited'] == 1].groupby('AgeGroup')['Exited'].count().reset_index()
    fig = px.bar(churn_count, x='AgeGroup', y='Exited', title='Number of Churned Customers by Age Group', labels={'Exited': 'Number of Churned Customers', 'AgeGroup': 'Age Group'}, height=450, color_discrete_sequence=['red'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- Most customers who churned are between the ages of 41 and 50.""")

# Geography Distribution Bar Chart
with col1:
    st.subheader("Geography Distribution")
    geo_counts = df['Geography'].value_counts().reset_index()
    geo_counts.columns = ['Geography', 'Count']
    fig = px.bar(geo_counts, y='Geography', x='Count', title="Geography Distribution", color='Geography', color_discrete_sequence=['lightblue', 'blue', 'purple'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- The majority of our customers are from France.""")

# Credit Card Ownership Bar Chart
with col2:
    st.subheader("Credit Card Ownership Distribution")
    credit = df['HasCrCard'].value_counts().reset_index()
    credit.columns = ['Status', 'Count']
    fig = px.bar(credit, y='Count', x='Status', title='Has Credit Card Distribution', color_discrete_sequence=['red', 'lightred'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- A significant proportion (around 76.7%) of customers have a credit card (HasCrCard).""")

# Credit Score Distribution Histogram
with col3:
    st.subheader("Credit Score Distribution")
    fig = px.histogram(df, x='CreditScore', title="Credit Score Distribution", color_discrete_sequence=['blue'])
    fig.update_traces(marker=dict(line=dict(color='blue', width=2)))
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- The average credit score is approximately 656.12 - The minimum credit score is 526, and the maximum is 792.""")

# Exited Customers Bar Chart
with col1:
    st.subheader("Exited Customers Distribution")
    Exited = df['Exited'].value_counts().reset_index()
    Exited.columns = ['Status', 'Count']
    fig = px.bar(Exited, y='Count', x='Status', title='Exited Customers Distribution', color_discrete_sequence=['blue'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- About 11.2% of customers have exited the bank (Exited = 1). - The majority (about 88.7%) have not exited the bank (Exited = 0).""")

# Joining Year Line Chart
with col2:
    st.subheader("Joining Year Distribution")
    df['joining_year'] = 2024 - df['Tenure']
    year = df['joining_year'].value_counts().reset_index()
    year.columns = ['Joining Year', 'Count']
    year = year.sort_values(by='Joining Year')
    fig = px.line(year, x='Joining Year', y='Count', title="Joining Year Distribution", color_discrete_sequence=['red'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- The year 2022 saw the highest number of customers, totaling 15.368k. - Conversely, 2024 had the lowest number of customers, with only 3884. - On average, we attract around 13.800k customers each year.""")

# Active Member Distribution Pie Chart
with col3:
    st.subheader("Active Member Distribution")
    fig = px.pie(df, names='IsActiveMember', title="Active Member Distribution", color_discrete_sequence=['red', 'black'])
    st.plotly_chart(fig)
    with st.expander("Insights"):
        st.write("""- Approximately 50.6% of customers are active members (IsActiveMember).""")

# Churned Customers by Country
st.markdown("### Churned Customers by Country")
df_churned = df[df['Exited'] == 1].groupby('Geography').size().reset_index(name='num_churned')
fig = px.bar(
    df_churned,
    x='Geography', 
    y='num_churned', 
    color='num_churned', 
    color_continuous_scale='Reds',  
    labels={'num_churned': 'Number of Churned Customers', 'Geography': 'Country'},
    title='Number of Churned Customers by Country'
)
fig.update_layout(
    xaxis_title='Country',
    yaxis_title='Number of Churned Customers',
    xaxis_tickangle=-45,
    width=1500
)
st.plotly_chart(fig)
with st.expander("Insights"):
     st.write("""- It is natural that the largest value is from fance because the largest number of customers are there.
- However, in the case of Spain and Germany, Spain has more customers than Germany, but fewer churned customers.
- So the number of churned customers varies significantly across countries. Certain countries have a higher concentration of churned customers, which may indicate areas where targeted retention strategies could be beneficial.""")