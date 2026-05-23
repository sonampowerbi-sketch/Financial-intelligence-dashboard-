# app.py - Complete working version without Plotly
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Reliance Financial Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    .report-title {
        font-size: 24px;
        font-weight: bold;
        color: #1a237e;
    }
    .success-text {
        color: green;
        font-weight: bold;
    }
    .warning-text {
        color: orange;
        font-weight: bold;
    }
    .danger-text {
        color: red;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏭 Reliance Industries Limited")
st.markdown("### Financial Intelligence Dashboard - FY 2024-25")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load and prepare financial data"""
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
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/8/8f/Reliance_Industries_Logo.svg/1200px-Reliance_Industries_Logo.svg.png", width=200)
    st.markdown("---")
    
    st.header("📊 Navigation")
    report_type = st.radio(
        "Select Report",
        ["📈 Monthly Financial Report", "💰 Cash Flow Statement", "🎯 Budget vs Actual Report"],
        index=0
    )
    
    st.markdown("---")
    st.info("📅 **Financial Year:** FY 2024-25\n\n**Period:** April 2024 - March 2025")
    
    st.markdown("---")
    st.markdown("### 📥 Download Options")
    
    # Download buttons
    if st.button("📊 Download Excel Report"):
        st.success("Preparing download...")
    
    if st.button("📄 Download PDF Summary"):
        st.info("PDF generation ready")

# Function to create download link
def get_table_download_link(df, filename, sheetname):
    """Generate a download link for dataframe"""
    from openpyxl import Workbook
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheetname, index=False)
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}.xlsx">Download {filename}.xlsx</a>'
    return href

# ==================== DELIVERABLE 1: MONTHLY FINANCIAL REPORT ====================
if report_type == "📈 Monthly Financial Report":
    st.header("📈 Monthly Financial Report")
    st.markdown("*Revenue Summary, Expense Breakdown, and Burn Rate Analysis*")
    st.markdown("---")
    
    # Key Metrics Row
    st.subheader("Key Financial Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Revenue'].sum()
        revenue_growth = ((df['Revenue'].iloc[-1] - df['Revenue'].iloc[0]) / df['Revenue'].iloc[0]) * 100
        st.metric(
            label="💰 Total Revenue", 
            value=f"₹{total_revenue:,.0f} Cr",
            delta=f"{revenue_growth:.1f}%"
        )
    
    with col2:
        total_expenses = df['Expenses'].sum()
        expense_growth = ((df['Expenses'].iloc[-1] - df['Expenses'].iloc[0]) / df['Expenses'].iloc[0]) * 100
        st.metric(
            label="💸 Total Expenses", 
            value=f"₹{total_expenses:,.0f} Cr",
            delta=f"{expense_growth:.1f}%"
        )
    
    with col3:
        net_profit = df['Net_Profit'].sum()
        profit_margin = (net_profit / total_revenue) * 100
        st.metric(
            label="📈 Net Profit", 
            value=f"₹{net_profit:,.0f} Cr",
            delta=f"Margin: {profit_margin:.1f}%"
        )
    
    with col4:
        avg_burn_rate = df['Burn_Rate'].mean()
        st.metric(
            label="🔥 Avg Burn Rate", 
            value=f"₹{avg_burn_rate:,.0f} Cr/Month",
            delta="Monthly average"
        )
    
    st.markdown("---")
    
    # Revenue Breakdown by Segment
    st.subheader("📊 Revenue Breakdown by Segment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        x = np.arange(len(df['Month']))
        width = 0.25
        
        bars1 = ax.bar(x - width, df['O2C_Revenue'], width, label='O2C (Oil to Chemicals)', 
                       color='#1a237e', edgecolor='black')
        bars2 = ax.bar(x, df['Retail_Revenue'], width, label='Retail', 
                       color='#42a5f5', edgecolor='black')
        bars3 = ax.bar(x + width, df['Digital_Revenue'], width, label='Digital (Jio)', 
                       color='#90caf9', edgecolor='black')
        
        ax.set_xlabel('Month', fontsize=12, fontweight='bold')
        ax.set_ylabel('Revenue (₹ Crores)', fontsize=12, fontweight='bold')
        ax.set_title('Monthly Revenue by Business Segment', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Month'], rotation=45, ha='right')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        avg_revenue = [df['O2C_Revenue'].mean(), df['Retail_Revenue'].mean(), df['Digital_Revenue'].mean()]
        labels = ['O2C (Refining & Petrochemicals)', 'Reliance Retail', 'Jio Digital Services']
        colors = ['#1a237e', '#42a5f5', '#90caf9']
        explode = (0.05, 0.05, 0.05)
        
        wedges, texts, autotexts = ax2.pie(avg_revenue, labels=labels, colors=colors, 
                                            autopct='%1.1f%%', startangle=90, explode=explode,
                                            shadow=True, textprops={'fontsize': 9})
        ax2.set_title('Average Revenue Share by Segment', fontsize=12, fontweight='bold')
        st.pyplot(fig2)
    
    st.markdown("---")
    
    # Revenue vs Expenses Trend
    st.subheader("📈 Revenue vs Expenses Trend Analysis")
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(df['Month'], df['Revenue'], marker='o', linewidth=2.5, 
             label='Revenue', color='green', markersize=8, markeredgecolor='darkgreen')
    ax3.plot(df['Month'], df['Expenses'], marker='s', linewidth=2.5, 
             label='Expenses', color='red', markersize=8, markeredgecolor='darkred')
    
    # Fill between for profit/loss area
    ax3.fill_between(df['Month'], df['Revenue'], df['Expenses'], 
                     where=(df['Revenue'] > df['Expenses']), 
                     color='green', alpha=0.2, label='Profit Zone')
    ax3.fill_between(df['Month'], df['Revenue'], df['Expenses'], 
                     where=(df['Revenue'] < df['Expenses']), 
                     color='red', alpha=0.2, label='Loss Zone')
    
    ax3.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Amount (₹ Crores)', fontsize=12, fontweight='bold')
    ax3.set_title('Revenue vs Expenses Trend (Monthly)', fontsize=14, fontweight='bold')
    ax3.legend(loc='best', fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    st.markdown("---")
    
    # Expense Breakdown
    st.subheader("💰 Expense Breakdown Analysis")
    
    expense_data = {
        'Category': ['O2C Operations', 'Retail Operations', 'Digital Services', 
                    'Employee Cost', 'Marketing & Sales', 'Research & Development',
                    'Administrative', 'Other Expenses'],
        'Amount': [850000, 528000, 273000, 110000, 48000, 38000, 25000, 15000]
    }
    expense_df = pd.DataFrame(expense_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        colors_exp = ['#1a237e', '#283593', '#303f9f', '#3949ab', 
                      '#5c6bc0', '#7986cb', '#9fa8da', '#c5cae9']
        wedges, texts, autotexts = ax4.pie(expense_df['Amount'], 
                                            labels=expense_df['Category'],
                                            autopct='%1.1f%%', colors=colors_exp,
                                            startangle=90, textprops={'fontsize': 8})
        ax4.set_title('Annual Expense Distribution', fontsize=12, fontweight='bold')
        st.pyplot(fig4)
    
    with col2:
        st.dataframe(expense_df.style.format({'Amount': '₹{:,.0f} Cr'})
                     .highlight_max(color='lightcoral')
                     .set_properties(**{'text-align': 'left'}))
    
    st.markdown("---")
    
    # Burn Rate Analysis
    st.subheader("🔥 Burn Rate Analysis")
    
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    bars = ax5.bar(df['Month'], df['Burn_Rate'], color='orange', alpha=0.7, 
                   edgecolor='darkorange', linewidth=2)
    ax5.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Burn Rate (₹ Crores)', fontsize=12, fontweight='bold')
    ax5.set_title('Monthly Cash Burn Rate', fontsize=14, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, df['Burn_Rate'])):
        if value > 0:
            ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                    f'₹{value:,.0f}', ha='center', va='bottom', fontsize=9)
    
    st.pyplot(fig5)
    
    # Insights
    st.subheader("📊 Key Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Revenue Growth**\n\n{revenue_growth:.1f}% increase from April to March")
    with col2:
        st.success(f"**Profitability**\n\n₹{net_profit:,.0f} Cr net profit for the year")
    with col3:
        if avg_burn_rate > 0:
            st.warning(f"**Burn Rate**\n\n₹{avg_burn_rate:,.0f} Cr average monthly burn")
        else:
            st.success("**Burn Rate**\n\nNo cash burn - operating profitably")
    
    # Detailed Data Table
    with st.expander("📋 View Detailed Monthly Data Table"):
        display_df = df[['Month', 'Revenue', 'Expenses', 'Net_Profit', 'Burn_Rate']].copy()
        display_df['Margin %'] = (display_df['Net_Profit'] / display_df['Revenue']) * 100
        st.dataframe(display_df.style.format({
            'Revenue': '₹{:,.0f} Cr',
            'Expenses': '₹{:,.0f} Cr',
            'Net_Profit': '₹{:,.0f} Cr',
            'Burn_Rate': '₹{:,.0f} Cr',
            'Margin %': '{:.1f}%'
        }).background_gradient(cmap='RdYlGn', subset=['Net_Profit', 'Margin %']))
    
    # Download section
    st.markdown("---")
    st.subheader("📥 Download Report")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(get_table_download_link(display_df, "Monthly_Financial_Report", "Monthly_Report"), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown(get_table_download_link(expense_df, "Expense_Breakdown", "Expenses"), 
                   unsafe_allow_html=True)

# ==================== DELIVERABLE 2: CASH FLOW STATEMENT ====================
elif report_type == "💰 Cash Flow Statement":
    st.header("💰 Cash Flow Statement")
    st.markdown("*Inflows vs Outflows Analysis*")
    st.markdown("---")
    
    # Create cash flow data
    np.random.seed(42)
    cf_df = df.copy()
    cf_df['Operating_Inflows'] = cf_df['Revenue']
    cf_df['Operating_Outflows'] = cf_df['Expenses'] * 0.85
    cf_df['Net_Operating_CF'] = cf_df['Operating_Inflows'] - cf_df['Operating_Outflows']
    cf_df['Investing_Outflows'] = np.random.uniform(8000, 12000, len(cf_df))
    cf_df['Net_Investing_CF'] = -cf_df['Investing_Outflows']
    cf_df['Financing_Inflows'] = np.where(cf_df['Month'].str.contains('Jun|Dec'), 50000, 0)
    cf_df['Net_Financing_CF'] = cf_df['Financing_Inflows']
    cf_df['Net_Cash_Flow'] = cf_df['Net_Operating_CF'] + cf_df['Net_Investing_CF'] + cf_df['Net_Financing_CF']
    cf_df['Opening_Balance'] = 250000
    cf_df['Closing_Balance'] = cf_df['Opening_Balance'] + cf_df['Net_Cash_Flow'].cumsum()
    
    # Key Metrics
    st.subheader("Annual Cash Flow Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_inflows = cf_df['Operating_Inflows'].sum() + cf_df['Financing_Inflows'].sum()
        st.metric("💰 Total Inflows", f"₹{total_inflows:,.0f} Cr", "Operating + Financing")
    
    with col2:
        total_outflows = cf_df['Operating_Outflows'].sum() + cf_df['Investing_Outflows'].sum()
        st.metric("💸 Total Outflows", f"₹{total_outflows:,.0f} Cr", "Operating + Investing")
    
    with col3:
        net_cf = cf_df['Net_Cash_Flow'].sum()
        st.metric("📊 Net Cash Flow", f"₹{net_cf:,.0f} Cr", 
                 "Positive" if net_cf > 0 else "Negative")
    
    with col4:
        closing_balance = cf_df['Closing_Balance'].iloc[-1]
        st.metric("🏦 Closing Balance", f"₹{closing_balance:,.0f} Cr", 
                 f"From ₹{cf_df['Opening_Balance'].iloc[0]:,.0f} Cr")
    
    st.markdown("---")
    
    # Cash Flow Components
    st.subheader("Cash Flow Components by Month")
    
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(cf_df['Month']))
    width = 0.25
    
    bars1 = ax.bar(x - width, cf_df['Net_Operating_CF'], width, label='Operating CF', 
                   color='green', alpha=0.7, edgecolor='darkgreen')
    bars2 = ax.bar(x, cf_df['Net_Investing_CF'], width, label='Investing CF', 
                   color='red', alpha=0.7, edgecolor='darkred')
    bars3 = ax.bar(x + width, cf_df['Net_Financing_CF'], width, label='Financing CF', 
                   color='blue', alpha=0.7, edgecolor='darkblue')
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amount (₹ Crores)', fontsize=12, fontweight='bold')
    ax.set_title('Cash Flow Components by Month', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(cf_df['Month'], rotation=45, ha='right')
    ax.legend(loc='best', fontsize=10)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    # Net Cash Flow Trend
    st.subheader("Net Cash Flow Trend")
    
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.plot(cf_df['Month'], cf_df['Net_Cash_Flow'], marker='o', linewidth=2.5, 
             color='purple', markersize=8, markeredgecolor='darkpurple')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.fill_between(cf_df['Month'], 0, cf_df['Net_Cash_Flow'], 
                     where=(cf_df['Net_Cash_Flow'] > 0), 
                     color='green', alpha=0.3, label='Positive Cash Flow')
    ax2.fill_between(cf_df['Month'], 0, cf_df['Net_Cash_Flow'], 
                     where=(cf_df['Net_Cash_Flow'] < 0), 
                     color='red', alpha=0.3, label='Negative Cash Flow')
    ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Net Cash Flow (₹ Crores)', fontsize=12, fontweight='bold')
    ax2.set_title('Monthly Net Cash Flow Trend', fontsize=14, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    st.markdown("---")
    
    # Cumulative Cash Position
    st.subheader("Cumulative Cash Position")
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.fill_between(cf_df['Month'], 0, cf_df['Closing_Balance'], 
                     color='lightblue', alpha=0.5)
    ax3.plot(cf_df['Month'], cf_df['Closing_Balance'], marker='s', 
             linewidth=2.5, color='darkblue', markersize=6, markeredgecolor='navy')
    ax3.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Cash Balance (₹ Crores)', fontsize=12, fontweight='bold')
    ax3.set_title('Cumulative Cash Position Over Time', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    st.markdown("---")
    
    # Inflows vs Outflows
    st.subheader("Inflows vs Outflows Analysis")
    
    comparison_df = pd.DataFrame({
        'Category': ['Operating Inflows', 'Financing Inflows', 'Operating Outflows', 
                    'Investing Outflows', 'Financing Outflows'],
        'Amount': [
            cf_df['Operating_Inflows'].sum(),
            cf_df['Financing_Inflows'].sum(),
            cf_df['Operating_Outflows'].sum(),
            cf_df['Investing_Outflows'].sum(),
            cf_df['Financing_Outflows'].sum() if 'Financing_Outflows' in cf_df else 0
        ]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        colors_bar = ['green', 'lightgreen', 'red', 'darkred', 'orange']
        bars = ax4.bar(comparison_df['Category'], comparison_df['Amount'], 
                       color=colors_bar, edgecolor='black')
        ax4.set_ylabel('Amount (₹ Crores)', fontsize=11, fontweight='bold')
        ax4.set_title('Total Inflows vs Outflows', fontsize=12, fontweight='bold')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3, axis='y')
        
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}', ha='center', va='bottom', fontsize=9)
        st.pyplot(fig4)
    
    with col2:
        st.dataframe(comparison_df.style.format({'Amount': '₹{:,.0f} Cr'})
                     .bar(color='lightblue', subset=['Amount']))
    
    # Monthly Cash Flow Table
    with st.expander("📋 View Detailed Monthly Cash Flow Table"):
        display_cf = cf_df[['Month', 'Operating_Inflows', 'Operating_Outflows', 
                           'Net_Operating_CF', 'Investing_Outflows', 'Net_Investing_CF',
                           'Financing_Inflows', 'Net_Cash_Flow', 'Closing_Balance']].copy()
        st.dataframe(display_cf.style.format({
            'Operating_Inflows': '₹{:,.0f} Cr',
            'Operating_Outflows': '₹{:,.0f} Cr',
            'Net_Operating_CF': '₹{:,.0f} Cr',
            'Investing_Outflows': '₹{:,.0f} Cr',
            'Net_Investing_CF': '₹{:,.0f} Cr',
            'Financing_Inflows': '₹{:,.0f} Cr',
            'Net_Cash_Flow': '₹{:,.0f} Cr',
            'Closing_Balance': '₹{:,.0f} Cr'
        }).background_gradient(cmap='RdYlGn', subset=['Net_Cash_Flow']))
    
    # Download
    st.markdown("---")
    st.subheader("📥 Download Cash Flow Report")
    st.markdown(get_table_download_link(display_cf, "Cash_Flow_Statement", "Cash_Flow"), 
               unsafe_allow_html=True)

# ==================== DELIVERABLE 3: BUDGET VS ACTUAL ====================
else:
    st.header("🎯 Budget vs Actual Report")
    st.markdown("*Planned vs Actual Spend Analysis*")
    st.markdown("---")
    
    # Budget data
    budget_data = {
        'Category': ['O2C Revenue', 'Retail Reve
