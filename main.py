# main.py - Working version without Plotly
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
    st.markdown("### 📊 Reports Include:")
    st.markdown("✅ Revenue Summary")
    st.markdown("✅ Expense Breakdown")
    st.markdown("✅ Burn Rate Analysis")
    st.markdown("✅ Cash Flow Statement")
    st.markdown("✅ Budget vs Actual")

# Main content
if report_type == "📈 Monthly Financial Report":
    st.header("📈 Monthly Financial Report")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_revenue = df['Revenue'].sum()
        st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f} Cr")
    with col2:
        total_expenses = df['Expenses'].sum()
        st.metric("💸 Total Expenses", f"₹{total_expenses:,.0f} Cr")
    with col3:
        net_profit = (df['Revenue'] - df['Expenses']).sum()
        st.metric("📈 Net Profit", f"₹{net_profit:,.0f} Cr")
    with col4:
        burn_rate = (df['Expenses'] - df['Revenue']).clip(lower=0).mean()
        st.metric("🔥 Avg Burn Rate", f"₹{burn_rate:,.0f} Cr")
    
    st.markdown("---")
    
    # Revenue by Segment Chart
    st.subheader("📊 Revenue Breakdown by Segment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(df['Month']))
        width = 0.25
        
        ax.bar(x - width, df['O2C_Revenue'], width, label='O2C', color='#1a237e')
        ax.bar(x, df['Retail_Revenue'], width, label='Retail', color='#42a5f5')
        ax.bar(x + width, df['Digital_Revenue'], width, label='Digital', color='#90caf9')
        ax.set_xlabel('Month', fontsize=10)
        ax.set_ylabel('Revenue (₹ Crores)', fontsize=10)
        ax.set_title('Monthly Revenue by Segment', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(df['Month'], rotation=45, ha='right', fontsize=8)
        ax.legend(loc='upper left', fontsize=9)
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        # Pie chart
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        avg_revenue = [df['O2C_Revenue'].mean(), df['Retail_Revenue'].mean(), df['Digital_Revenue'].mean()]
        labels = ['O2C (Refining)', 'Retail', 'Digital (Jio)']
        colors = ['#1a237e', '#42a5f5', '#90caf9']
        explode = (0.05, 0.05, 0.05)
        ax2.pie(avg_revenue, labels=labels, colors=colors, autopct='%1.1f%%', 
                startangle=90, explode=explode, shadow=True)
        ax2.set_title('Average Revenue Share by Segment', fontsize=12)
        st.pyplot(fig2)
    
    # Revenue vs Expenses Trend
    st.subheader("📈 Revenue vs Expenses Trend")
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(df['Month'], df['Revenue'], marker='o', linewidth=2, 
             label='Revenue', color='green', markersize=8)
    ax3.plot(df['Month'], df['Expenses'], marker='s', linewidth=2, 
             label='Expenses', color='red', markersize=8)
    ax3.fill_between(df['Month'], df['Revenue'], df['Expenses'], 
                     where=(df['Revenue'] > df['Expenses']), 
                     color='green', alpha=0.2, label='Profit Area')
    ax3.fill_between(df['Month'], df['Revenue'], df['Expenses'], 
                     where=(df['Revenue'] < df['Expenses']), 
                     color='red', alpha=0.2, label='Loss Area')
    ax3.set_xlabel('Month', fontsize=11)
    ax3.set_ylabel('Amount (₹ Crores)', fontsize=11)
    ax3.set_title('Revenue vs Expenses Trend (Monthly)', fontsize=13)
    ax3.legend(loc='best', fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    # Expense Breakdown
    st.subheader("💰 Expense Breakdown")
    
    expense_data = {
        'Category': ['O2C Operations', 'Retail Operations', 'Digital Services', 
                    'Employee Cost', 'Marketing', 'R&D'],
        'Amount': [850000, 528000, 273000, 110000, 48000, 38000]
    }
    expense_df = pd.DataFrame(expense_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        wedges, texts, autotexts = ax4.pie(expense_df['Amount'], 
                                            labels=expense_df['Category'],
                                            autopct='%1.1f%%', startangle=90)
        ax4.set_title('Annual Expense Distribution', fontsize=12)
        st.pyplot(fig4)
    
    with col2:
        st.dataframe(expense_df.style.format({'Amount': '₹{:,.0f} Cr'}))
    
    # Burn Rate Analysis
    st.subheader("🔥 Burn Rate Analysis")
    
    df['Burn_Rate'] = (df['Expenses'] - df['Revenue']).clip(lower=0)
    
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.bar(df['Month'], df['Burn_Rate'], color='orange', alpha=0.7, edgecolor='darkorange')
    ax5.set_xlabel('Month', fontsize=11)
    ax5.set_ylabel('Burn Rate (₹ Crores)', fontsize=11)
    ax5.set_title('Monthly Cash Burn Rate', fontsize=13)
    ax5.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    st.pyplot(fig5)
    
    # Data Table
    with st.expander("📋 View Detailed Monthly Data"):
        display_df = df[['Month', 'Revenue', 'Expenses', 'Burn_Rate']].copy()
        display_df['Profit/Loss'] = display_df['Revenue'] - display_df['Expenses']
        st.dataframe(display_df.style.format({
            'Revenue': '₹{:,.0f} Cr',
            'Expenses': '₹{:,.0f} Cr',
            'Burn_Rate': '₹{:,.0f} Cr',
            'Profit/Loss': '₹{:,.0f} Cr'
        }).background_gradient(cmap='RdYlGn', subset=['Profit/Loss']))

elif report_type == "💰 Cash Flow Statement":
    st.header("💰 Cash Flow Statement")
    
    # Create cash flow data
    cf_df = df.copy()
    cf_df['Operating_Inflows'] = cf_df['Revenue']
    cf_df['Operating_Outflows'] = cf_df['Expenses'] * 0.85
    cf_df['Net_Operating_CF'] = cf_df['Operating_Inflows'] - cf_df['Operating_Outflows']
    cf_df['Investing_Outflows'] = np.random.uniform(8000, 12000, len(cf_df))
    cf_df['Net_Investing_CF'] = -cf_df['Investing_Outflows']
    cf_df['Financing_Inflows'] = np.where(cf_df['Month'].str.contains('Jun|Dec'), 50000, 0)
    cf_df['Net_Financing_CF'] = cf_df['Financing_Inflows']
    cf_df['Net_Cash_Flow'] = cf_df['Net_Operating_CF'] + cf_df['Net_Investing_CF'] + cf_df['Net_Financing_CF']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_inflows = cf_df['Operating_Inflows'].sum() + cf_df['Financing_Inflows'].sum()
        st.metric("💰 Total Inflows", f"₹{total_inflows:,.0f} Cr")
    with col2:
        total_outflows = cf_df['Operating_Outflows'].sum() + cf_df['Investing_Outflows'].sum()
        st.metric("💸 Total Outflows", f"₹{total_outflows:,.0f} Cr")
    with col3:
        st.metric("📊 Net Cash Flow", f"₹{cf_df['Net_Cash_Flow'].sum():,.0f} Cr")
    with col4:
        closing_balance = 250000 + cf_df['Net_Cash_Flow'].sum()
        st.metric("🏦 Closing Balance", f"₹{closing_balance:,.0f} Cr")
    
    st.markdown("---")
    
    # Cash Flow Components
    st.subheader("Cash Flow Components Analysis")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(cf_df['Month']))
    width = 0.25
    
    ax.bar(x - width, cf_df['Net_Operating_CF'], width, label='Operating CF', 
           color='green', alpha=0.7)
    ax.bar(x, cf_df['Net_Investing_CF'], width, label='Investing CF', 
           color='red', alpha=0.7)
    ax.bar(x + width, cf_df['Net_Financing_CF'], width, label='Financing CF', 
           color='blue', alpha=0.7)
    
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Amount (₹ Crores)', fontsize=11)
    ax.set_title('Cash Flow Components by Month', fontsize=13)
    ax.set_xticks(x)
    ax.set_xticklabels(cf_df['Month'], rotation=45, ha='right')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Net Cash Flow Trend
    st.subheader("Net Cash Flow Trend")
    
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.plot(cf_df['Month'], cf_df['Net_Cash_Flow'], marker='o', linewidth=2, 
             color='purple', markersize=8)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.fill_between(cf_df['Month'], 0, cf_df['Net_Cash_Flow'], 
                     where=(cf_df['Net_Cash_Flow'] > 0), 
                     color='green', alpha=0.3, label='Positive')
    ax2.fill_between(cf_df['Month'], 0, cf_df['Net_Cash_Flow'], 
                     where=(cf_df['Net_Cash_Flow'] < 0), 
                     color='red', alpha=0.3, label='Negative')
    ax2.set_xlabel('Month', fontsize=11)
    ax2.set_ylabel('Net Cash Flow (₹ Crores)', fontsize=11)
    ax2.set_title('Monthly Net Cash Flow Trend', fontsize=13)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    # Cumulative Cash Position
    st.subheader("Cumulative Cash Position")
    
    cf_df['Cumulative_Cash'] = 250000 + cf_df['Net_Cash_Flow'].cumsum()
    
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.fill_between(cf_df['Month'], 0, cf_df['Cumulative_Cash'], 
                     color='lightblue', alpha=0.5)
    ax3.plot(cf_df['Month'], cf_df['Cumulative_Cash'], marker='s', 
             linewidth=2, color='darkblue', markersize=6)
    ax3.set_xlabel('Month', fontsize=11)
    ax3.set_ylabel('Cumulative Cash (₹ Crores)', fontsize=11)
    ax3.set_title('Cumulative Cash Position Over Time', fontsize=13)
    ax3.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)
    
    # Inflows vs Outflows
    st.subheader("Inflows vs Outflows Summary")
    
    comparison_df = pd.DataFrame({
        'Category': ['Operating Inflows', 'Financing Inflows', 'Operating Outflows', 'Investing Outflows'],
        'Amount': [
            cf_df['Operating_Inflows'].sum(),
            cf_df['Financing_Inflows'].sum(),
            cf_df['Operating_Outflows'].sum(),
            cf_df['Investing_Outflows'].sum()
        ]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        bars = ax4.bar(comparison_df['Category'], comparison_df['Amount'], 
                       color=['green', 'lightgreen', 'red', 'darkred'])
        ax4.set_ylabel('Amount (₹ Crores)', fontsize=10)
        ax4.set_title('Total Inflows vs Outflows', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}', ha='center', va='bottom', fontsize=9)
        st.pyplot(fig4)
    
    with col2:
        st.dataframe(comparison_df.style.format({'Amount': '₹{:,.0f} Cr'}))

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
    budget_df['Status'] = budget_df['Variance_%'].apply(
        lambda x: '✅ On Track' if abs(x) <= 5 else '⚠️ Review Needed'
    )
    
    # Summary Metrics
    st.subheader("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_budget = budget_df['Budget'].sum()
        total_actual = budget_df['Actual'].sum()
        st.metric("Total Budget", f"₹{total_budget:,.0f} Cr")
    with col2:
        st.metric("Total Actual", f"₹{total_actual:,.0f} Cr")
    with col3:
        total_variance = total_actual - total_budget
        delta_color = "normal" if total_variance > 0 else "inverse"
        st.metric("Total Variance", f"₹{total_variance:,.0f} Cr", 
                 delta=f"{((total_variance)/total_budget*100):.1f}%")
    with col4:
        achievement_rate = (total_actual / total_budget) * 100
        st.metric("Budget Achievement", f"{achievement_rate:.1f}%")
    
    st.markdown("---")
    
    # Budget vs Actual Chart
    st.subheader("Budget vs Actual Comparison by Category")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart
    x = np.arange(len(budget_df['Category']))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, budget_df['Budget'], width, label='Budget', 
                    color='lightblue', edgecolor='navy')
    bars2 = ax1.bar(x + width/2, budget_df['Actual'], width, label='Actual', 
                    color='darkblue', edgecolor='navy')
    ax1.set_xlabel('Category', fontsize=10)
    ax1.set_ylabel('Amount (₹ Crores)', fontsize=10)
    ax1.set_title('Budget vs Actual by Category', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(budget_df['Category'], rotation=45, ha='right', fontsize=8)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}', ha='center', va='bottom', fontsize=7)
    
    # Variance chart
    colors = ['green' if x >= 0 else 'red' for x in budget_df['Variance_%']]
    bars3 = ax2.bar(budget_df['Category'], budget_df['Variance_%'], color=colors)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.set_xlabel('Category', fontsize=10)
    ax2.set_ylabel('Variance (%)', fontsize=10)
    ax2.set_title('Budget Variance Percentage', fontsize=12)
    ax2.set_xticklabels(budget_df['Category'], rotation=45, ha='right', fontsize=8)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars3:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                fontsize=8)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Performance Analysis
    st.subheader("Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Areas of Efficiency")
        efficient = budget_df[budget_df['Variance'] < 0]
        if len(efficient) > 0:
            for _, row in efficient.iterrows():
                st.success(f"**{row['Category']}**: Saved ₹{abs(row['Variance']):,.0f} Cr ({abs(row['Variance_%']):.1f}% below budget)")
        else:
            st.info("No cost savings detected")
    
    with col2:
        st.markdown("#### ⚠️ Areas of Concern")
        concerning = budget_df[budget_df['Variance'] > 0]
        if len(concerning) > 0:
            for _, row in concerning.iterrows():
                st.warning(f"**{row['Category']}**: Overspent by ₹{row['Variance']:,.0f} Cr ({row['Variance_%']:.1f}% above budget)")
        else:
            st.success("No overspending detected!")
    
    # Detailed Table
    with st.expander("📋 Detailed Budget vs Actual Table"):
        st.dataframe(budget_df.style.format({
            'Budget': '₹{:,.0f} Cr',
            'Actual': '₹{:,.0f} Cr',
            'Variance': '₹{:,.0f} Cr',
            'Variance_%': '{:.1f}%'
        }).background_gradient(cmap='RdYlGn', subset=['Variance_%']))
    
    # Recommendations
    st.subheader("💡 Recommendations")
    
    major_variances = budget_df[abs(budget_df['Variance_%']) > 5]
    if len(major_variances) > 0:
        st.markdown("**Based on variance analysis, consider:**")
        for _, row in major_variances.iterrows():
            if row['Variance'] > 0:
                st.markdown(f"- 🔍 Review **{row['Category']}** spending (↑{row['Variance_%']:.1f}% over budget)")
            else:
                st.markdown(f"- ✅ Maintain **{row['Category']}** efficiency (↓{abs(row['Variance_%']):.1f}% under budget)")
    else:
        st.success("✅ All categories are within acceptable variance range (±5%)")

# Footer
st.markdown("---")
st.markdown("### 📊 Data Source: Reliance Industries Financial Reports FY 2024-25")
st.markdown("*Disclaimer: This dashboard is for demonstration and educational purposes*")
