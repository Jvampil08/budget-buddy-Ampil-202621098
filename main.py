import streamlit as st
from dashboard_page import render_dashboard_page
from budget_page import render_budget_page
from expense_page import render_expense_page

def configure_page_settings():
    """Configures global Streamlit page layout, browser tab title, and icon."""
    st.set_page_config(
        page_title="Budget Buddy | Student Finance Tracker",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_sidebar_navigation():
    """Renders the sidebar navigation menu and project metadata."""
    st.sidebar.title("💰 Budget Buddy")
    st.sidebar.markdown("---")
    st.sidebar.write("**Student Personal Finance App**")
    
    # Navigation Radio Selector
    selected_page = st.sidebar.radio(
        "Select Page", 
        ["Dashboard", "Budget Planner", "Expense Tracker"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Project Details")
    st.sidebar.text("• Currency: Philippine Peso (₱)\n• Target: Jan/Feb 2027 Sample Data\n• Framework: Streamlit & Python")
    
    return selected_page

def route_page_selection(selected_page):
    """Routes application execution to the appropriate modular page function."""
    if selected_page == "Dashboard":
        render_dashboard_page()
    elif selected_page == "Budget Planner":
        render_budget_page()
    elif selected_page == "Expense Tracker":
        render_expense_page()

def main():
    """Main application entry point controller."""
    configure_page_settings()
    selected_page = render_sidebar_navigation()
    route_page_selection(selected_page)

if __name__ == "__main__":
    main()