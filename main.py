import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("💰 Finance Analyzer Dashboard")

file = "C:/Users/My Computer/Desktop/vS codes/Finance_Analyzer/EXPENSE.xlsx"

# Load data
sheet1 = pd.read_excel(file, sheet_name="Transactions")
sheet2 = pd.read_excel(file, sheet_name="Budget")

# Clean numeric data
sheet1["Amount"] = pd.to_numeric(sheet1["Amount"], errors="coerce")
sheet2["amount"] = pd.to_numeric(sheet2["amount"], errors="coerce")

# KPIs
total_expense = sheet1["Amount"].sum()
total_budget = sheet2["amount"].sum()
savings = total_budget - total_expense
percent = (savings / total_budget) * 100

st.subheader("📊 Summary")
st.write("Total Expenditure:", total_expense)
st.write("Total Budget:", total_budget)
st.write("Savings:", savings)
st.write("Savings %:", percent)

# Category comparison
actual = sheet1.groupby("Category")["Amount"].sum()
budget = sheet2.groupby("Category")["amount"].sum()

comparison = pd.DataFrame({
    "Budget": budget,
    "Actual": actual
}).fillna(0)

comparison["Difference"] = comparison["Budget"] - comparison["Actual"]

comparison["Status"] = comparison["Difference"].apply(
    lambda x: "Under Budget" if x >= 0 else "Over Budget"
)

st.subheader("📊 Budget vs Actual")
fig1, ax1 = plt.subplots()
comparison[["Budget", "Actual"]].plot(kind="bar", ax=ax1)
st.pyplot(fig1)

# Top category
top_category = comparison["Actual"].idxmax()
st.write(" Top Spending Category:", top_category)

# Date fix
sheet1["Date"] = sheet1["Date"].astype(str) + "-2026"

# Convert properly
sheet1["Date"] = pd.to_datetime(sheet1["Date"], format="%d-%b-%Y", errors="coerce")

# Clean data
sheet1["Amount"] = pd.to_numeric(sheet1["Amount"], errors="coerce")
sheet1 = sheet1.dropna(subset=["Date", "Amount"])
sheet1 = sheet1.sort_values("Date")

# Daily trend
daily = sheet1.groupby("Date")["Amount"].sum()

st.subheader("📈 Daily Spending Trend")

fig2, ax2 = plt.subplots()
daily.plot(kind="line", marker="o", ax=ax2)

st.pyplot(fig2)

# Category-wise spending
sheet1.columns = sheet1.columns.str.strip()

sheet1["Amount"] = pd.to_numeric(sheet1["Amount"], errors="coerce")
sheet1 = sheet1.dropna(subset=["Category", "Amount"])
category_spend = sheet1.groupby("Category")["Amount"].sum()
st.subheader("📊 Expenditure by Category")

fig, ax = plt.subplots()

ax.pie(
    category_spend,
    labels=category_spend.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.axis("equal")

st.pyplot(fig)