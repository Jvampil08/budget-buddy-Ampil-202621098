import streamlit as st
from datetime import date

def initialize_expense_session_state():
    """Initializes the expenses list in session state."""
    if "expenses" not in st.session_state:
        st.session_state.expenses = []

def get_available_categories():
    """Retrieves categories from session state or falls back to defaults."""
    return st.session_state.get("categories", ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Savings"])

def validate_expense_input(amount, description):
    """Validates expense amount and description input values."""
    if amount <= 0:
        st.error("Please enter a valid expense amount greater than $0.")
        return False
    if not description.strip():
        st.error("Please provide a description for this expense.")
        return False
    return True

def create_expense_dict(exp_date, category, description, amount):
    """Creates a dictionary record for a single expense entry."""
    return {
        "date": str(exp_date),
        "category": category,
        "description": description.strip(),
        "amount": float(amount)
    }

def process_expense_submission(exp_date, exp_category, exp_amount, exp_description):
    """Validates and appends a new expense to session state."""
    if validate_expense_input(exp_amount, exp_description):
        new_expense = create_expense_dict(exp_date, exp_category, exp_description, exp_amount)
        st.session_state.expenses.append(new_expense)
        st.success(f"Successfully recorded ${exp_amount:.2f} for {exp_category}!")

def render_expense_form():
    """Renders input form fields for logging a new expense."""
    st.subheader("Record New Expense")
    categories = get_available_categories()

    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("Expense Date", value=date.today())
            exp_category = st.selectbox("Category", categories)
        with col2:
            exp_amount = st.number_input("Amount ($)", min_value=0.01, step=10.0, value=0.0)
            exp_description = st.text_input("Description / Notes")

        submitted = st.form_submit_button("Add Expense")
        if submitted:
            process_expense_submission(exp_date, exp_category, exp_amount, exp_description)

def clear_all_expenses():
    """Clears all recorded expenses from session state."""
    st.session_state.expenses = []
    st.rerun()

def render_expense_history():
    """Renders the table of past expenses and clear history button."""
    st.markdown("---")
    st.subheader("Expense History")
    
    if len(st.session_state.expenses) == 0:
        st.info("No expenses recorded yet. Use the form above to log your first transaction.")
    else:
        st.write(f"Total recorded items: {len(st.session_state.expenses)}")
        st.dataframe(st.session_state.expenses, use_container_width=True)

        if st.button("Clear All Expenses"):
            clear_all_expenses()

def render_expense_page():
    """Main controller function for the Expense Tracker page."""
    st.header("Expense Tracker")
    st.write("Record and manage your day-to-day spending.")
    
    initialize_expense_session_state()
    render_expense_form()
    render_expense_history()