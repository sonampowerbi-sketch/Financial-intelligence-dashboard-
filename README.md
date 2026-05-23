# Reliance Industries - Financial Intelligence Dashboard 📊

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📊 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://reliance-financial-intelligence.streamlit.app)

## 📋 Overview

This repository contains a complete **Financial Intelligence System** for Reliance Industries, providing:
- ✅ Monthly Financial Reports (Revenue, Expenses, Burn Rate)
- ✅ Cash Flow Statements (Inflows vs Outflows)
- ✅ Budget vs Actual Analysis

## 🚀 Features

### 1. Monthly Financial Report
- Revenue summary by segment (O2C, Retail, Digital)
- Expense breakdown with category analysis
- Burn rate calculation and trend analysis
- Interactive charts and graphs

### 2. Cash Flow Statement
- Operating, Investing, and Financing activities
- Inflows vs Outflows visualization
- Opening and closing balance tracking
- Waterfall chart analysis

### 3. Budget vs Actual
- Planned vs actual spend comparison
- Variance analysis with % calculations
- Performance status indicators
- Executive summary dashboard

## 🛠️ Installation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/reliance-financial-intelligence.git
cd reliance-financial-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app/main.py
