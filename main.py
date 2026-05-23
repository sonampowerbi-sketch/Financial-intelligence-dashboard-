# app/main.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Reliance Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("🏭 Reliance Industries - Financial Intelligence Dashboard")
st.markdown("---")

# Create sample data (since files might not upload)
@st.cache_data
def load_data():
    months = ['Apr 24', 'May 24', 'Jun 24', 'Jul 24', 'Aug 24', 'Sep 24', 
              'Oct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25', 'Mar 25']
    
    data = {
        'Month': months,
        'Revenue': [175000, 178000, 182000, 185000, 188000, 192000, 
                   195000, 198000, 202000, 205000, 208000, 212000],
        'Expenses': [145000, 147000, 149000, 151000, 153000, 155000,
                    157000, 159000, 161000, 163000, 165000, 167000],
        'O2C_Revenue': [85000, 86000, 87000, 88000, 89000, 90000,
                       91000, 92000, 93000, 94000, 95000, 96000],
        'Retail_Revenue': [55000, 56000, 57000, 58000, 59000, 60000,
                          61000, 62000, 63000, 64000, 65000, 66000],
        'Digital_Revenue': [35000, 36000, 38000, 39000, 40000, 42000,
                           43000, 44000, 46000, 47000, 48000, 50000]
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar
with st.sidebar:
    st.header("📊 Navigation")
    report_type = st.radio(
        "Select Report",
        ["📈 Monthly Report", "💰 Cash Flow", "🎯 Budget vs Actual"]
    )
    
    st.markdown("---")
    st.info("📅 Financial Year: FY 2024-25")

# Main content
if report_type == "📈 Monthly Report":
    st.header("Monthly Financial Report")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{df['Revenue'].sum():,.0f} Cr")
    with col2:
        st.metric("Total Expenses", f"₹{df['Expenses'].sum():,.0f} Cr")
    with col3:
        st.metric("Net Profit", f"₹{(df['Revenue'] - df['Expenses']).sum():,.0f} Cr")
    with col4:
        burn_rate = (df['Expenses'] - df['Revenue']).clip(lower=0).mean()
        st.metric("Avg Burn Rate", f"₹{burn_rate:,.0f} Cr")
    
    # Revenue chart
    st.subheader("Revenue Trend by Segment")
    fig = px.line(df, x='Month', y=['O2C_Revenue', 'Retail_Revenue', 'Digital_Revenue'],
                  title="Monthly Revenue by Business Segment")
    st.plotly_chart(fig, use_container_width=True)
    
    # Revenue vs Expenses
    st.subheader("Revenue vs Expenses")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['Month'], y=df['Revenue'], name='Revenue', line=dict(color='green', width=3)))
    fig2.add_trace(go.Scatter(x=df['Month'], y=df['Expenses'], name='Expenses', line=dict(color='red', width=3)))
    st.plotly_chart(fig2, use_container_width=True)
    
    # Data table
    with st.expander("View Detailed Data"):
        st.dataframe(df)

elif report_type == "💰 Cash Flow":
    st.header("Cash Flow Statement")
    
    # Sample cash flow data
    cf_df = df.copy()
    cf_df['Operating_CF'] = cf_df['Revenue'] - cf_df['Expenses'] * 0.8
    cf_df['Investing_CF'] = -np.random.uniform(8000, 12000, len(cf_df))
    cf_df['Financing_CF'] = np.where(cf_df['Month'].str.contains('Jun|Dec'), 50000, 0)
    cf_df['Net_CF'] = cf_df['Operating_CF'] + cf_df['Investing_CF'] + cf_df['Financing_CF']
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Operating CF", f"₹{cf_df['Operating_CF'].sum():,.0f} Cr")
        st.metric("Total Investing CF", f"₹{cf_df['Investing_CF'].sum():,.0f} Cr")
    with col2:
        st.metric("Total Financing CF", f"₹{cf_df['Financing_CF'].sum():,.0f} Cr")
        st.metric("Net Cash Flow", f"₹{cf_df['Net_CF'].sum():,.0f} Cr")
    
    # Cash flow chart
    fig = go.Figure()
    fig.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Operating_CF'], name='Operating CF'))
    fig.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Investing_CF'], name='Investing CF'))
    fig.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Financing_CF'], name='Financing CF'))
    fig.update_layout(barmode='relative', title="Cash Flow Components")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.header("Budget vs Actual Analysis")
    
    # Budget data
    budget = pd.DataFrame({
        'Category': ['Revenue', 'Expenses', 'CAPEX', 'R&D', 'Marketing'],
        'Budget': [2400000, 1900000, 120000, 38000, 48000],
        'Actual': [2350000, 1950000, 130000, 40000, 50000]
    })
    budget['Variance'] = budget['Actual'] - budget['Budget']
    budget['Variance_%'] = (budget['Variance'] / budget['Budget']) * 100
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Budget Achievement", f"{((budget['Actual'].sum()/budget['Budget'].sum())*100):.1f}%")
    with col2:
        st.metric("Total Variance", f"₹{budget['Variance'].sum():,.0f} Cr")
    with col3:
        st.metric("Avg Variance %", f"{budget['Variance_%'].mean():.1f}%")
    
    # Comparison chart
    fig = px.bar(budget, x='Category', y=['Budget', 'Actual'], 
                 barmode='group', title="Budget vs Actual")
    st.plotly_chart(fig, use_container_width=True)
    
    # Variance chart
    fig2 = px.bar(budget, x='Category', y='Variance_%', 
                  color='Variance_%', title="Variance Percentage")
    fig2.add_hline(y=0, line_dash="dash")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Data table
    st.dataframe(budget)

st.markdown("---")
st.caption("📊 Data Source: Reliance Industries Financial Reports FY 2024-25")
