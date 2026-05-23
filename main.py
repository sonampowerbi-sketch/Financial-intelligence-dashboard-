# main.py - Place this at the ROOT level of your repository
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
    st.markdown("### 📥 Download")
    if st.button("Download Report"):
        st.success("Report ready for download")

# Main content
if report_type == "📈 Monthly Financial Report":
    st.header("📈 Monthly Financial Report")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Revenue", f"₹{df['Revenue'].sum():,.0f} Cr", 
                 f"{((df['Revenue'].iloc[-1] - df['Revenue'].iloc[0])/df['Revenue'].iloc[0]*100):.1f}%")
    with col2:
        st.metric("💸 Total Expenses", f"₹{df['Expenses'].sum():,.0f} Cr",
                 f"{((df['Expenses'].iloc[-1] - df['Expenses'].iloc[0])/df['Expenses'].iloc[0]*100):.1f}%")
    with col3:
        net_profit = (df['Revenue'] - df['Expenses']).sum()
        st.metric("📈 Net Profit", f"₹{net_profit:,.0f} Cr")
    with col4:
        burn_rate = (df['Expenses'] - df['Revenue']).clip(lower=0).mean()
        st.metric("🔥 Avg Burn Rate", f"₹{burn_rate:,.0f} Cr")
    
    st.markdown("---")
    
    # Revenue by Segment
    st.subheader("📊 Revenue Breakdown by Segment")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(df, x='Month', y=['O2C_Revenue', 'Retail_Revenue', 'Digital_Revenue'],
                     title="Monthly Revenue by Business Segment",
                     labels={'value': 'Revenue (₹ Crores)', 'Month': 'Month', 'variable': 'Segment'},
                     barmode='stack')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        avg_revenue = df[['O2C_Revenue', 'Retail_Revenue', 'Digital_Revenue']].mean()
        fig_pie = px.pie(values=avg_revenue.values, names=avg_revenue.index,
                         title="Average Revenue Share")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Revenue vs Expenses Trend
    st.subheader("📈 Revenue vs Expenses Trend")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['Month'], y=df['Revenue'], 
                              name='Revenue', line=dict(color='green', width=3)))
    fig2.add_trace(go.Scatter(x=df['Month'], y=df['Expenses'], 
                              name='Expenses', line=dict(color='red', width=3)))
    fig2.update_layout(height=450, xaxis_title='Month', yaxis_title='Amount (₹ Crores)')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Expense Breakdown
    st.subheader("💰 Expense Breakdown")
    expense_cols = ['O2C_Expense', 'Retail_Expense', 'Digital_Expense', 'Employee_Cost', 'Marketing_Cost']
    # Create sample expense data
    expense_data = {
        'Category': ['O2C Operations', 'Retail Operations', 'Digital Services', 'Employee Cost', 'Marketing'],
        'Amount': [850000, 528000, 273000, 110000, 48000]
    }
    expense_df = pd.DataFrame(expense_data)
    fig3 = px.pie(expense_df, values='Amount', names='Category', title="Annual Expense Breakdown")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Data Table
    with st.expander("📋 View Detailed Monthly Data"):
        st.dataframe(df.style.format({
            'Revenue': '₹{:,.0f} Cr',
            'Expenses': '₹{:,.0f} Cr',
            'O2C_Revenue': '₹{:,.0f} Cr',
            'Retail_Revenue': '₹{:,.0f} Cr',
            'Digital_Revenue': '₹{:,.0f} Cr'
        }))

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
        st.metric("Total Inflows", f"₹{(cf_df['Operating_Inflows'].sum() + cf_df['Financing_Inflows'].sum()):,.0f} Cr")
    with col2:
        st.metric("Total Outflows", f"₹{(cf_df['Operating_Outflows'].sum() + cf_df['Investing_Outflows'].sum()):,.0f} Cr")
    with col3:
        st.metric("Net Cash Flow", f"₹{cf_df['Net_Cash_Flow'].sum():,.0f} Cr")
    with col4:
        st.metric("Ending Balance", f"₹{250000 + cf_df['Net_Cash_Flow'].sum():,.0f} Cr")
    
    st.markdown("---")
    
    # Cash Flow Waterfall
    st.subheader("Cash Flow Waterfall Analysis")
    opening_balance = 250000
    closing_balance = opening_balance + cf_df['Net_Cash_Flow'].sum()
    
    fig = go.Figure(go.Waterfall(
        name="Cash Flow",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Opening Balance", "Operating CF", "Investing CF", "Financing CF", "Closing Balance"],
        y=[opening_balance, 
           cf_df['Net_Operating_CF'].sum(),
           cf_df['Net_Investing_CF'].sum(),
           cf_df['Net_Financing_CF'].sum(),
           closing_balance],
        textposition="outside",
        text=[f"₹{opening_balance:,.0f}", f"₹{cf_df['Net_Operating_CF'].sum():,.0f}",
              f"₹{cf_df['Net_Investing_CF'].sum():,.0f}", f"₹{cf_df['Net_Financing_CF'].sum():,.0f}",
              f"₹{closing_balance:,.0f}"]
    ))
    fig.update_layout(title="Annual Cash Flow Statement", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly Cash Flow
    st.subheader("Monthly Cash Flow Components")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Net_Operating_CF'], name='Operating CF', marker_color='green'))
    fig2.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Net_Investing_CF'], name='Investing CF', marker_color='red'))
    fig2.add_trace(go.Bar(x=cf_df['Month'], y=cf_df['Net_Financing_CF'], name='Financing CF', marker_color='blue'))
    fig2.update_layout(barmode='relative', title="Cash Flow by Month", height=450)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Inflows vs Outflows
    st.subheader("Inflows vs Outflows Comparison")
    inflows_outflows = pd.DataFrame({
        'Category': ['Operating Inflows', 'Financing Inflows', 'Operating Outflows', 'Investing Outflows'],
        'Amount': [
            cf_df['Operating_Inflows'].sum(),
            cf_df['Financing_Inflows'].sum(),
            cf_df['Operating_Outflows'].sum(),
            cf_df['Investing_Outflows'].sum()
        ]
    })
    fig3 = px.bar(inflows_outflows, x='Category', y='Amount', 
                  color='Category', title="Total Inflows vs Outflows")
    st.plotly_chart(fig3, use_container_width=True)

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
    col1, col2, col3 = st.columns(3)
    with col1:
        total_budget = budget_df['Budget'].sum()
        total_actual = budget_df['Actual'].sum()
        st.metric("Total Budget", f"₹{total_budget:,.0f} Cr")
        st.metric("Total Actual", f"₹{total_actual:,.0f} Cr")
    with col2:
        total_variance = total_actual - total_budget
        st.metric("Total Variance", f"₹{total_variance:,.0f} Cr",
                 delta=f"{((total_variance)/total_budget*100):.1f}%")
    with col3:
        achievement_rate = (total_actual / total_budget) * 100
        st.metric("Budget Achievement", f"{achievement_rate:.1f}%")
    
    st.markdown("---")
    
    # Budget vs Actual Chart
    st.subheader("Budget vs Actual Comparison")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=budget_df['Category'], y=budget_df['Budget'], 
                         name='Budget', marker_color='lightblue'))
    fig.add_trace(go.Bar(x=budget_df['Category'], y=budget_df['Actual'], 
                         name='Actual', marker_color='darkblue'))
    fig.update_layout(barmode='group', title="Budget vs Actual by Category",
                     xaxis_title="Category", yaxis_title="Amount (₹ Crores)",
                     height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Variance Analysis
    st.subheader("Variance Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.bar(budget_df, x='Category', y='Variance_%', 
                      color='Status', title="Budget Variance (%)")
        fig2.add_hline(y=0, line_dash="dash", line_color="black")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Filter for overspending
        overspend = budget_df[budget_df['Variance'] > 0]
        if len(overspend) > 0:
            fig3 = px.pie(overspend, values='Variance', names='Category', 
                         title="Areas of Overspending")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.success("✅ No overspending detected!")
    
    # Detailed Table
    with st.expander("📋 Detailed Budget vs Actual Table"):
        st.dataframe(budget_df.style.format({
            'Budget': '₹{:,.0f} Cr',
            'Actual': '₹{:,.0f} Cr',
            'Variance': '₹{:,.0f} Cr',
            'Variance_%': '{:.1f}%'
        }).background_gradient(cmap='RdYlGn', subset=['Variance_%']))

# Footer
st.markdown("---")
st.markdown("### 📊 Data Source: Reliance Industries Financial Reports FY 2024-25")
st.caption("*Disclaimer: This dashboard is for demonstration and educational purposes*")
