# main.py - Simplified version without Plotly
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Reliance Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("🏭 Reliance Industries - Financial Intelligence Dashboard")
st.markdown("---")

# Load data
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
        ["📈 Monthly Financial Report", "💰 Cash Flow Statement", "🎯 Budget vs Actual Report"]
    )
    
    st.markdown("---")
    st.info("📅 Financial Year: FY 2024-25")

# Main content
if report_type == "📈 Monthly Financial Report":
    st.header("📈 Monthly Financial Report")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Revenue", f"₹{df['Revenue'].sum():,.0f} Cr")
    with col2:
        st.metric("💸 Total Expenses", f"₹{df['Expenses'].sum():,.0f} Cr")
    with col3:
        net_profit = (df['Revenue'] - df['Expenses']).sum()
        st.metric("📈 Net Profit", f"₹{net_profit:,.0f} Cr")
    with col4:
        burn_rate = (df['Expenses'] - df['Revenue']).clip(lower=0).mean()
        st.metric("🔥 Avg Burn Rate", f"₹{burn_rate:,.0f} Cr")
    
    st.markdown("---")
    
    # Revenue by Segment - Using matplotlib
    st.subheader("📊 Revenue Breakdown by Segment")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Bar chart
    x = np.arange(len(df['Month']))
    width = 0.25
    
    ax1.bar(x - width, df['O2C_Revenue'], width, label='O2C', color='navy')
    ax1.bar(x, df['Retail_Revenue'], width, label='Retail', color='lightblue')
    ax1.bar(x + width, df['Digital_Revenue'], width, label='Digital', color='skyblue')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Revenue (₹ Crores)')
    ax1.set_title('Monthly Revenue by Segment')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df['Month'], rotation=45)
    ax1.legend()
    
    # Pie chart
    avg_revenue = [df['O2C_Revenue'].mean(), df['Retail_Revenue'].mean(), df['Digital_Revenue'].mean()]
    labels = ['O2C', 'Retail', 'Digital']
    colors = ['navy', 'lightblue', 'skyblue']
    ax2.pie(avg_revenue, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Average Revenue Share')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Revenue vs Expenses Trend
    st.subheader("📈 Revenue vs Expenses Trend")
    
    fig2, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df['Month'], df['Revenue'], marker='o', linewidth=2, label='Revenue', color='green')
    ax.plot(df['Month'], df['Expenses'], marker='s', linewidth=2, label='Expenses', color='red')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount (₹ Crores)')
    ax.set_title('Revenue vs Expenses Trend')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    # Data Table
    with st.expander("📋 View Detailed Monthly Data"):
        st.dataframe(df)

elif report_type == "💰 Cash Flow Statement":
    st.header("💰 Cash Flow Statement")
    
    # Create cash flow data
    cf_df = df.copy()
    cf_df['Operating_CF'] = cf_df['Revenue'] - cf_df['Expenses'] * 0.8
    cf_df['Investing_CF'] = -np.random.uniform(8000, 12000, len(cf_df))
    cf_df['Financing_CF'] = np.where(cf_df['Month'].str.contains('Jun|Dec'), 50000, 0)
    cf_df['Net_CF'] = cf_df['Operating_CF'] + cf_df['Investing_CF'] + cf_df['Financing_CF']
    
    # Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Operating CF", f"₹{cf_df['Operating_CF'].sum():,.0f} Cr")
        st.metric("Total Investing CF", f"₹{cf_df['Investing_CF'].sum():,.0f} Cr")
    with col2:
        st.metric("Total Financing CF", f"₹{cf_df['Financing_CF'].sum():,.0f} Cr")
        st.metric("Net Cash Flow", f"₹{cf_df['Net_CF'].sum():,.0f} Cr")
    
    st.markdown("---")
    
    # Cash flow chart
    st.subheader("Cash Flow Components")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    x = np.arange(len(cf_df['Month']))
    ax.bar(x, cf_df['Operating_CF'], label='Operating CF', color='green', alpha=0.7)
    ax.bar(x, cf_df['Investing_CF'], label='Investing CF', color='red', alpha=0.7)
    ax.bar(x, cf_df['Financing_CF'], label='Financing CF', color='blue', alpha=0.7)
    
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount (₹ Crores)')
    ax.set_title('Cash Flow by Month')
    ax.set_xticks(x)
    ax.set_xticklabels(cf_df['Month'], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Summary table
    st.subheader("Monthly Cash Flow Summary")
    summary_df = cf_df[['Month', 'Operating_CF', 'Investing_CF', 'Financing_CF', 'Net_CF']].round(0)
    st.dataframe(summary_df)

else:  # Budget vs Actual Report
    st.header("🎯 Budget vs Actual Report")
    
    # Budget data
    budget_data = {
        'Category': ['O2C Revenue', 'Retail Revenue', 'Digital Revenue', 
                    'Operating Expenses', 'Employee Cost', 'Marketing', 'R&D', 'CAPEX'],
        'Budget': [1020000, 660000, 420000, 1650000, 110000, 48000, 38000, 120000],
        'Actual': [1050000, 670000, 435000, 1680000, 115000, 50000, 40000, 130000]
    }
    budget_df = pd.DataFrame(budget_data)
    budget_df['Variance'] = budget_df['Actual'] - budget_df['Budget']
    budget_df['Variance_%'] = (budget_df['Variance'] / budget_df['Budget']) * 100
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_budget = budget_df['Budget'].sum()
        total_actual = budget_df['Actual'].sum()
        st.metric("Total Budget", f"₹{total_budget:,.0f} Cr")
        st.metric("Total Actual", f"₹{total_actual:,.0f} Cr")
    with col2:
        total_variance = total_actual - total_budget
        st.metric("Total Variance", f"₹{total_variance:,.0f} Cr")
    with col3:
        achievement_rate = (total_actual / total_budget) * 100
        st.metric("Budget Achievement", f"{achievement_rate:.1f}%")
    
    st.markdown("---")
    
    # Budget vs Actual Chart
    st.subheader("Budget vs Actual Comparison")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar chart
    x = np.arange(len(budget_df['Category']))
    width = 0.35
    
    ax1.bar(x - width/2, budget_df['Budget'], width, label='Budget', color='lightblue')
    ax1.bar(x + width/2, budget_df['Actual'], width, label='Actual', color='darkblue')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Amount (₹ Crores)')
    ax1.set_title('Budget vs Actual by Category')
    ax1.set_xticks(x)
    ax1.set_xticklabels(budget_df['Category'], rotation=45, ha='right')
    ax1.legend()
    
    # Variance chart
    colors = ['red' if x < 0 else 'green' for x in budget_df['Variance_%']]
    ax2.bar(budget_df['Category'], budget_df['Variance_%'], color=colors)
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Variance (%)')
    ax2.set_title('Budget Variance Percentage')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_xticklabels(budget_df['Category'], rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Detailed Table
    st.subheader("Detailed Analysis")
    st.dataframe(budget_df.style.format({
        'Budget': '₹{:,.0f} Cr',
        'Actual': '₹{:,.0f} Cr',
        'Variance': '₹{:,.0f} Cr',
        'Variance_%': '{:.1f}%'
    }))

st.markdown("---")
st.caption("📊 Reliance Industries Financial Intelligence Dashboard - FY 2024-25")
