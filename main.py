# main.py - Complete working version
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Reliance Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("🏭 Reliance Industries Limited")
st.markdown("### Financial Intelligence Dashboard - FY 2024-25")
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
    df = pd.DataFrame(data)
    df['Net_Profit'] = df['Revenue'] - df['Expenses']
    df['Burn_Rate'] = (df['Expenses'] - df['Revenue']).clip(lower=0)
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Navigation")
    report_type = st.radio(
        "Select Report",
        ["📈 Monthly Report", "💰 Cash Flow", "🎯 Budget vs Actual"]
    )
    st.markdown("---")
    st.info("📅 FY 2024-25 (Apr 2024 - Mar 2025)")

# ==================== MONTHLY REPORT ====================
if report_type == "📈 Monthly Report":
    st.header("📈 Monthly Financial Report")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Revenue", f"₹{df['Revenue'].sum():,.0f} Cr")
    with col2:
        st.metric("Total Expenses", f"₹{df['Expenses'].sum():,.0f} Cr")
    with col3:
        st.metric("Net Profit", f"₹{df['Net_Profit'].sum():,.0f} Cr")
    with col4:
        st.metric("Avg Burn Rate", f"₹{df['Burn_Rate'].mean():,.0f} Cr")
    
    st.markdown("---")
    
    # Revenue chart
    st.subheader("Revenue by Segment")
    fig, ax = plt.subplots(figsize=(10, 5))
    x = range(len(df['Month']))
    ax.bar(x, df['O2C_Revenue'], label='O2C', color='navy')
    ax.bar(x, df['Retail_Revenue'], bottom=df['O2C_Revenue'], label='Retail', color='lightblue')
    ax.bar(x, df['Digital_Revenue'], bottom=df['O2C_Revenue']+df['Retail_Revenue'], label='Digital', color='skyblue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue (₹ Cr)')
    ax.set_title('Monthly Revenue by Segment')
    ax.set_xticks(x)
    ax.set_xticklabels(df['Month'], rotation=45)
    ax.legend()
    st.pyplot(fig)
    
    # Revenue vs Expenses
    st.subheader("Revenue vs Expenses")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(df['Month'], df['Revenue'], marker='o', label='Revenue', color='green')
    ax2.plot(df['Month'], df['Expenses'], marker='s', label='Expenses', color='red')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Amount (₹ Cr)')
    ax2.set_title('Revenue vs Expenses Trend')
    ax2.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    # Expense breakdown
    st.subheader("Expense Breakdown")
    expense_data = {
        'Category': ['O2C Ops', 'Retail Ops', 'Digital Ops', 'Employee Cost', 'Marketing'],
        'Amount': [850000, 528000, 273000, 110000, 48000]
    }
    expense_df = pd.DataFrame(expense_data)
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    ax3.pie(expense_df['Amount'], labels=expense_df['Category'], autopct='%1.1f%%')
    ax3.set_title('Annual Expense Distribution')
    st.pyplot(fig3)
    
    # Burn rate
    st.subheader("Burn Rate Analysis")
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.bar(df['Month'], df['Burn_Rate'], color='orange')
    ax4.set_xlabel('Month')
    ax4.set_ylabel('Burn Rate (₹ Cr)')
    ax4.set_title('Monthly Cash Burn Rate')
    plt.xticks(rotation=45)
    st.pyplot(fig4)
    
    # Data table
    with st.expander("View Data Table"):
        st.dataframe(df[['Month', 'Revenue', 'Expenses', 'Net_Profit', 'Burn_Rate']])

# ==================== CASH FLOW ====================
elif report_type == "💰 Cash Flow":
    st.header("💰 Cash Flow Statement")
    
    # Create cash flow data
    np.random.seed(42)
    cf_df = df.copy()
    cf_df['Operating_CF'] = df['Revenue'] - df['Expenses'] * 0.85
    cf_df['Investing_CF'] = -np.random.uniform(8000, 12000, len(df))
    cf_df['Financing_CF'] = 0
    cf_df.loc[cf_df['Month'].str.contains('Jun'), 'Financing_CF'] = 50000
    cf_df.loc[cf_df['Month'].str.contains('Dec'), 'Financing_CF'] = 50000
    cf_df['Net_CF'] = cf_df['Operating_CF'] + cf_df['Investing_CF'] + cf_df['Financing_CF']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Operating CF", f"₹{cf_df['Operating_CF'].sum():,.0f} Cr")
    with col2:
        st.metric("Investing CF", f"₹{cf_df['Investing_CF'].sum():,.0f} Cr")
    with col3:
        st.metric("Financing CF", f"₹{cf_df['Financing_CF'].sum():,.0f} Cr")
    with col4:
        st.metric("Net Cash Flow", f"₹{cf_df['Net_CF'].sum():,.0f} Cr")
    
    st.markdown("---")
    
    # Cash flow components
    st.subheader("Cash Flow Components")
    fig, ax = plt.subplots(figsize=(12, 5))
    x = range(len(cf_df['Month']))
    ax.bar(x, cf_df['Operating_CF'], label='Operating', color='green')
    ax.bar(x, cf_df['Investing_CF'], label='Investing', color='red')
    ax.bar(x, cf_df['Financing_CF'], label='Financing', color='blue')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount (₹ Cr)')
    ax.set_title('Cash Flow by Month')
    ax.set_xticks(x)
    ax.set_xticklabels(cf_df['Month'], rotation=45)
    ax.legend()
    st.pyplot(fig)
    
    # Net cash flow trend
    st.subheader("Net Cash Flow Trend")
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.plot(cf_df['Month'], cf_df['Net_CF'], marker='o', color='purple', linewidth=2)
    ax2.axhline(y=0, color='black', linestyle='--')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Net Cash Flow (₹ Cr)')
    ax2.set_title('Monthly Net Cash Flow')
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    # Cumulative position
    st.subheader("Cumulative Cash Position")
    cf_df['Cumulative'] = 250000 + cf_df['Net_CF'].cumsum()
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.fill_between(cf_df['Month'], 0, cf_df['Cumulative'], alpha=0.3, color='blue')
    ax3.plot(cf_df['Month'], cf_df['Cumulative'], marker='s', color='darkblue')
    ax3.set_xlabel('Month')
    ax3.set_ylabel('Cash Balance (₹ Cr)')
    ax3.set_title('Cumulative Cash Balance')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# ==================== BUDGET VS ACTUAL ====================
else:
    st.header("🎯 Budget vs Actual Report")
    
    # Budget data
    budget_data = {
        'Category': ['O2C Revenue', 'Retail Revenue', 'Digital Revenue', 
                    'Operating Exp', 'Employee Cost', 'Marketing', 'R&D', 'CAPEX'],
        'Budget': [1020000, 660000, 420000, 1650000, 110000, 48000, 38000, 120000],
        'Actual': [1050000, 670000, 435000, 1680000, 115000, 50000, 40000, 130000]
    }
    budget_df = pd.DataFrame(budget_data)
    budget_df['Variance'] = budget_df['Actual'] - budget_df['Budget']
    budget_df['Variance_pct'] = (budget_df['Variance'] / budget_df['Budget']) * 100
    budget_df['Status'] = budget_df['Variance_pct'].apply(
        lambda x: 'On Track' if abs(x) <= 5 else 'Review Needed'
    )
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        total_budget = budget_df['Budget'].sum()
        total_actual = budget_df['Actual'].sum()
        st.metric("Total Budget", f"₹{total_budget:,.0f} Cr")
        st.metric("Total Actual", f"₹{total_actual:,.0f} Cr")
    with col2:
        variance = total_actual - total_budget
        st.metric("Total Variance", f"₹{variance:,.0f} Cr")
    with col3:
        achievement = (total_actual / total_budget) * 100
        st.metric("Achievement", f"{achievement:.1f}%")
    
    st.markdown("---")
    
    # Budget vs Actual chart
    st.subheader("Budget vs Actual Comparison")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Bar chart
    x = range(len(budget_df['Category']))
    width = 0.35
    ax1.bar([i - width/2 for i in x], budget_df['Budget'], width, label='Budget', color='lightblue')
    ax1.bar([i + width/2 for i in x], budget_df['Actual'], width, label='Actual', color='darkblue')
    ax1.set_xlabel('Category')
    ax1.set_ylabel('Amount (₹ Cr)')
    ax1.set_title('Budget vs Actual')
    ax1.set_xticks(x)
    ax1.set_xticklabels(budget_df['Category'], rotation=45, ha='right')
    ax1.legend()
    
    # Variance chart
    colors = ['green' if x < 0 else 'red' for x in budget_df['Variance_pct']]
    ax2.bar(budget_df['Category'], budget_df['Variance_pct'], color=colors)
    ax2.axhline(y=0, color='black', linestyle='-')
    ax2.axhline(y=5, color='orange', linestyle='--')
    ax2.axhline(y=-5, color='orange', linestyle='--')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Variance (%)')
    ax2.set_title('Budget Variance')
    ax2.set_xticklabels(budget_df['Category'], rotation=45, ha='right')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Variance summary
    st.subheader("Variance Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Under Budget (Savings)**")
        under = budget_df[budget_df['Variance'] < 0]
        for _, row in under.iterrows():
            st.success(f"{row['Category']}: Saved ₹{abs(row['Variance']):,.0f} Cr")
    
    with col2:
        st.markdown("**Over Budget (Overspend)**")
        over = budget_df[budget_df['Variance'] > 0]
        for _, row in over.iterrows():
            st.warning(f"{row['Category']}: Overspent ₹{row['Variance']:,.0f} Cr")
    
    # Data table
    with st.expander("View Detailed Table"):
        st.dataframe(budget_df.style.format({
            'Budget': '₹{:,.0f} Cr',
            'Actual': '₹{:,.0f} Cr',
            'Variance': '₹{:,.0f} Cr',
            'Variance_pct': '{:.1f}%'
        }))

# Footer
st.markdown("---")
st.markdown("✅ **Deliverables:** Monthly Report | Cash Flow | Budget vs Actual")# app.py - Complete working ver
