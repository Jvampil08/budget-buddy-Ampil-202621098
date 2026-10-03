import streamlit as st
from dashboard_page import render_dashboard_page
from budget_page import render_budget_page
from expense_page import render_expense_page

def main():
    st.set_page_config(page_title="Budget Buddy", page_icon="💰", layout="wide")
    st.title("💰 Budget Buddy")
    st.caption("Know where your money goes")

    # Multi-page sidebar navigation
    page = st.sidebar.radio("Navigation", ["Dashboard", "Budget Planner", "Expense Tracker"])

    if page == "Dashboard":
        render_dashboard_page()
    elif page == "Budget Planner":
        render_budget_page()
    elif page == "Expense Tracker":
        render_expense_page()

if __name__ == "__main__":
    main()