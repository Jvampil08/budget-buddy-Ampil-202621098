import streamlit as st

DEFAULT_CATEGORIES = ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Savings"]

def render_budget_page():
    st.header("Budget Planner")
    st.write("Plan your monthly income and adjust category allocations here.")
    st.selectbox("Select Category to View", DEFAULT_CATEGORIES)