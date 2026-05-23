# main.py - COMPLETELY FIXED VERSION
import streamlit as st
import pandas as pd
import numpy as np

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
    df['Margin'] = (df['Net_Profit'] / df['Revenue']) * 100
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("## 📊 Navigation")
    report_type = st.radio(
        "Select Report",
        ["📈 Monthly Financial Report", "💰 Cash Flow Statement", "🎯 Budget vs Actual Report"],
        index=0
    )
    st.markdown("---")
    st.info("📅 **Financial Year:** FY 2024-25\n\n**Period:** April 2024 - March 2025")

# ==================== DELIVERABLE 1: MONTHLY FINANCIAL REPORT ====================
if report_type == "📈 Monthly Financial Report":
    st.header("📈 Monthly Financial Report")
    st.markdown("*Revenue Summary, Expense Breakdown, and Burn Rate Analysis*")
    st.markdown("---")
    
    # Key Metrics Row
    st.subheader("📊 Key Financial Metrics")
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
        st.metric(
            label="💸 Total Expenses", 
            value=f"₹{total_expenses:,.0f} Cr"
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
            value=f"₹{avg_burn_rate:,.0f} Cr/Month"
        )
    
    st.markdown("---")
    
    # Revenue Breakdown by Segment
    st.subheader("📊 Revenue Breakdown by Segment")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        revenue_by_segment = df[['Month', 'O2C_Revenue', 'Retail_Revenue', 'Digital_Revenue']].set_index('Month')
        st.bar_chart(revenue_by_segment, height=400)
        st.caption("Monthly Revenue by Business Segment (₹ Crores)")
    
    with col2:
        avg_revenue_data = {
            'Segment': ['O2C', 'Retail', 'Digital'],
            'Avg Revenue': [
                f"₹{df['O2C_Revenue'].mean():,.0f} Cr",
                f"₹{df['Retail_Revenue'].mean():,.0f} Cr",
                f"₹{df['Digital_Revenue'].mean():,.0f} Cr"
            ]
        }
        avg_df = pd.DataFrame(avg_revenue_data)
        st.dataframe(avg_df, use_container_width=True)
    
    st.markdown("---")
    
    # Revenue vs Expenses Trend
    st.subheader("📈 Revenue vs Expenses Trend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Revenue Trend")
        revenue_trend = df[['Month', 'Revenue']].set_index('Month')
        st.line_chart(revenue_trend, height=300)
    
    with col2:
        st.subheader("Expenses Trend")
        expense_trend = df[['Month', 'Expenses']].set_index('Month')
        st.line_chart(expense_trend, height=300)
    
    st.subheader("Revenue vs Expenses Comparison")
    comparison = df[['Month', 'Revenue', 'Expenses']].set_index('Month')
    st.area_chart(comparison, height=350)
    
    st.markdown("---")
    
    # Expense Breakdown
    st.subheader("💰 Expense Breakdown")
    
    expense_data = {
        'Category': ['O2C Operations', 'Retail Operations', 'Digital Services', 
                    'Employee Cost', 'Marketing & Sales', 'R&D', 'Other'],
        'Amount (₹ Cr)': [850000, 528000, 273000, 110000, 48000, 38000, 25000]
    }
    expense_df = pd.DataFrame(expense_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.bar_chart(expense_df.set_index('Category'), height=350)
    
    with col2:
        st.dataframe(expense_df, use_container_width=True)
    
    st.markdown("---")
    
    # Burn Rate Analysis
    st.subheader("🔥 Burn Rate Analysis")
    
    burn_df = df[['Month', 'Burn_Rate']].set_index('Month')
    st.bar_chart(burn_df, height=350)
    
    # Insights
    st.subheader("📊 Key Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Revenue Growth**\n\n{revenue_growth:.1f}% increase")
    
    with col2:
        profitable_months = len(df[df['Net_Profit'] > 0])
        st.success(f"**Profitability**\n\n{profitable_months}/12 months profitable")
    
    with col3:
        if avg_burn_rate > 0:
            st.warning(f"**Burn Rate**\n\n₹{avg_burn_rate:,.0f} Cr avg monthly")
        else:
            st.success("**Burn Rate**\n\nOperating profitably")
    
    # Detailed Data Table
    with st.expander("📋 View Detailed Monthly Data Table"):
        display_df = df[['Month', 'Revenue', 'Expenses', 'Net_Profit', 'Burn_Rate']].copy()
        st.dataframe(display_df)

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
    cf_df['Financing_Inflows'] = 0
    cf_df.loc[cf_df['Month'].str.contains('Jun'), 'Financing_Inflows'] = 50000
    cf_df.loc[cf_df['Month'].str.contains('Dec'), 'Financing_Inflows'] = 50000
    cf_df['Net_Financing_CF'] = cf_df['Financing_Inflows']
    cf_df['Net_Cash_Flow'] = cf_df['Net_Operating_CF'] + cf_df['Net_Investing_CF'] + cf_df['Net_Financing_CF']
    
    # Key Metrics
    st.subheader("Annual Cash Flow Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_inflows = cf_df['Operating_Inflows'].sum() + cf_df['Financing_Inflows'].sum()
        st.metric("💰 Total Inflows", f"₹{total_inflows:,.0f} Cr")
    
    with col2:
        total_outflows = cf_df['Operating_Outflows'].sum() + cf_df['Investing_Outflows'].sum()
        st.metric("💸 Total Outflows", f"₹{total_outflows:,.0f} Cr")
    
    with col3:
        net_cf = cf_df['Net_Cash_Flow'].sum()
        st.metric("📊 Net Cash Flow", f"₹{net_cf:,.0f} Cr")
    
    with col4:
        closing_balance = 250000 + net_cf
        st.metric("🏦 Closing Balance", f"₹{closing_balance:,.0f} Cr")
    
    st.markdown("---")
    
    # Cash Flow Components
    st.subheader("Cash Flow Components by Month")
    
    cf_components = cf_df[['Month', 'Net_Operating_CF', 'Net_Investing_CF', 'Net_Financing_CF']].set_index('Month')
    st.bar_chart(cf_components, height=400)
    st.caption("Note: Positive values = inflows, Negative values = outflows")
    
    st.markdown("---")
    
    # Net Cash Flow Trend
    st.subheader("Net Cash Flow Trend")
    net_cf_trend = cf_df[['Month', 'Net_Cash_Flow']].set_index('Month')
    st.area_chart(net_cf_trend, height=350)
    
    st.markdown("---")
    
    # Cumulative Cash Position
    st.subheader("Cumulative Cash Position")
    cf_df['Cumulative_Cash'] = 250000 + cf_df['Net_Cash_Flow'].cumsum()
    cumulative = cf_df[['Month', 'Cumulative_Cash']].set_index('Month')
    st.line_chart(cumulative, height=350)
    
    st.markdown("---")
    
    # Inflows vs Outflows Summary
    st.subheader("Inflows vs Outflows Summary")
    
    inflows_outflows = pd.DataFrame({
        'Category': ['Operating Inflows', 'Financing Inflows', 'Operating Outflows', 'Investing Outflows'],
        'Amount (₹ Cr)': [
            cf_df['Operating_Inflows'].sum(),
            cf_df['Financing_Inflows'].sum(),
            cf_df['Operating_Outflows'].sum(),
            cf_df['Investing_Outflows'].sum()
        ]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(inflows_outflows.set_index('Category'), height=350)
    with col2:
        st.dataframe(inflows_outflows, use_container_width=True)
    
    # Monthly Cash Flow Table
    with st.expander("📋 View Detailed Monthly Cash Flow Table"):
        display_cf = cf_df[['Month', 'Net_Operating_CF', 'Net_Investing_CF', 
                           'Net_Financing_CF', 'Net_Cash_Flow', 'Cumulative_Cash']].copy()
        st.dataframe(display_cf)

# ==================== DELIVERABLE 3: BUDGET VS ACTUAL ====================
else:
    st.header("🎯 Budget vs Actual Report")
    st.markdown("*Planned vs Actual Spend Analysis*")
    st.markdown("---")
    
    # Budget data
    budget_data = {
        'Category': ['O2C Revenue', 'Retail Revenue', 'Digital Revenue', 
                    'Operating Expenses', 'Employee Cost', 'Marketing', 
                    'R&D', 'CAPEX'],
        'Budget': [1020000, 660000, 420000, 1650000, 110000, 48000, 38000, 120000],
        'Actual': [1050000, 670000, 435000, 1680000, 115000, 50000, 40000, 130000]
    }
    budget_df = pd.DataFrame(budget_data)
    budget_df['Variance'] = budget_df['Actual'] - budget_df['Budget']
    budget_df['Variance_Pct'] = (budget_df['Variance'] / budget_df['Budget']) * 100
    
    # Add status column
    def get_status(pct):
        if abs(pct) <= 5:
            return "✅ On Track"
        elif pct > 0:
            return "⚠️ Over Budget"
        else:
            return "📉 Under Budget"
    
    budget_df['Status'] = budget_df['Variance_Pct'].apply(get_status)
    
    # Summary Metrics
    st.subheader("Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    
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
    
    with col4:
        revenue_cats = ['O2C Revenue', 'Retail Revenue', 'Digital Revenue']
        revenue_actual = budget_df[budget_df['Category'].isin(revenue_cats)]['Actual'].sum()
        revenue_budget = budget_df[budget_df['Category'].isin(revenue_cats)]['Budget'].sum()
        revenue_achievement = (revenue_actual / revenue_budget) * 100
        st.metric("Revenue Achievement", f"{revenue_achievement:.1f}%")
    
    st.markdown("---")
    
    # Budget vs Actual Comparison
    st.subheader("Budget vs Actual Comparison")
    
    comparison_df = budget_df.set_index('Category')[['Budget', 'Actual']]
    st.bar_chart(comparison_df, height=450)
    
    st.markdown("---")
    
    # Variance Analysis
    st.subheader("Variance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Under Budget (Savings)")
        under_budget = budget_df[budget_df['Variance'] < 0]
        if len(under_budget) > 0:
            for _, row in under_budget.iterrows():
                st.success(f"**{row['Category']}**: Saved ₹{abs(row['Variance']):,.0f} Cr")
        else:
            st.info("No categories under budget")
    
    with col2:
        st.markdown("#### ⚠️ Over Budget (Overspending)")
        over_budget = budget_df[budget_df['Variance'] > 0]
        if len(over_budget) > 0:
            for _, row in over_budget.iterrows():
                st.warning(f"**{row['Category']}**: Overspent ₹{row['Variance']:,.0f} Cr")
        else:
            st.success("No overspending detected")
    
    st.markdown("---")
    
    # Revenue Performance
    st.subheader("Revenue Performance")
    revenue_cats = ['O2C Revenue', 'Retail Revenue', 'Digital Revenue']
    revenue_df = budget_df[budget_df['Category'].isin(revenue_cats)]
    revenue_compare = revenue_df.set_index('Category')[['Budget', 'Actual']]
    st.bar_chart(revenue_compare, height=350)
    
    st.markdown("---")
    
    # Expense Performance
    st.subheader("Expense Performance")
    expense_cats = ['Operating Expenses', 'Employee Cost', 'Marketing', 'R&D', 'CAPEX']
    expense_df = budget_df[budget_df['Category'].isin(expense_cats)]
    expense_compare = expense_df.set_index('Category')[['Budget', 'Actual']]
    st.bar_chart(expense_compare, height=350)
    
    st.markdown("---")
    
    # Variance Table
    st.subheader("Variance Analysis Table")
    variance_table = budget_df[['Category', 'Budget', 'Actual', 'Variance', 'Variance_Pct', 'Status']].copy()
    
    # Format the dataframe for display
    variance_table_display = variance_table.copy()
    variance_table_display['Budget'] = variance_table_display['Budget'].apply(lambda x: f"₹{x:,.0f} Cr")
    variance_table_display['Actual'] = variance_table_display['Actual'].apply(lambda x: f"₹{x:,.0f} Cr")
    variance_table_display['Variance'] = variance_table_display['Variance'].apply(lambda x: f"₹{x:,.0f} Cr")
    variance_table_display['Variance_Pct'] = variance_table_display['Variance_Pct'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(variance_table_display, use_container_width=True)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Based on variance analysis:**")
        major_variances = budget_df[abs(budget_df['Variance_Pct']) > 5]
        if len(major_variances) > 0:
            for _, row in major_variances.iterrows():
                if row['Variance'] > 0:
                    st.markdown(f"- 🔍 Review **{row['Category']}**")
                else:
                    st.markdown(f"- ✅ Maintain **{row['Category']}**")
        else:
            st.success("All categories within acceptable range")
    
    with col2:
        st.markdown("**Key Actions:**")
        st.markdown("""
        - 📊 Monthly budget reviews
        - 🎯 Control marketing spend
        - 📈 Optimize revenue streams
        - 💰 Reduce operating costs
        """)

# Footer
st.markdown("---")
st.markdown("### ✅ All Three Deliverables Completed:")
col1, col2, col3 = st.columns(3)
with col1:
    st.success("📈 Monthly Financial Report")
with col2:
    st.success("💰 Cash Flow Statement")
with col3:
    st.success("🎯 Budget vs Actual Report")
st.markdown("---")
st.caption("📊 Reliance Industries Financial Intelligence Dashboard - FY 2024-25")
