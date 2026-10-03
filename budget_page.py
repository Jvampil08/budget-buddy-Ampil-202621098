import streamlit as st

DEFAULT_CATEGORIES = ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Savings"]

def initialize_budget_session_state():
    """Initializes session state variables for budget tracking."""
    if "categories" not in st.session_state:
        st.session_state.categories = DEFAULT_CATEGORIES.copy()
    if "budget_allocations" not in st.session_state:
        st.session_state.budget_allocations = {cat: 0.0 for cat in st.session_state.categories}
    if "monthly_income" not in st.session_state:
        st.session_state.monthly_income = 0.0

def render_income_section():
    """Renders month selection, income source, and expected income input."""
    st.subheader("1. Monthly Income Setup")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Select Month", 
            ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            key="selected_month"
        )
    with col2:
        st.text_input("Income Source", value="Salary", key="income_source")
    
    st.session_state.monthly_income = st.number_input(
        "Expected Monthly Income ($)", 
        min_value=0.0, 
        value=st.session_state.monthly_income, 
        step=100.0
    )

def add_new_category(new_cat_name):
    """Adds a new category to the list and dictionary if it doesn't already exist."""
    cleaned_name = new_cat_name.strip()
    if cleaned_name and cleaned_name not in st.session_state.categories:
        st.session_state.categories.append(cleaned_name)
        st.session_state.budget_allocations[cleaned_name] = 0.0
        st.success(f"Added category: {cleaned_name}")
        st.rerun()
    elif cleaned_name in st.session_state.categories:
        st.warning("Category already exists.")

def render_category_adder():
    """Renders the text input and button for adding custom budget categories."""
    new_cat = st.text_input("Add New Category", key="new_category_input")
    if st.button("Add Category"):
        add_new_category(new_cat)

def remove_category(category_name):
    """Removes a category and its budget allocation."""
    if len(st.session_state.categories) > 1:
        st.session_state.categories.remove(category_name)
        del st.session_state.budget_allocations[category_name]
        st.rerun()

def render_single_allocation_row(cat):
    """Renders input and remove button for a single category bucket."""
    col_a, col_b, col_c = st.columns([3, 2, 1])
    with col_a:
        st.text(cat)
    with col_b:
        current_val = st.session_state.budget_allocations.get(cat, 0.0)
        allocated = st.number_input(
            f"Amount for {cat}", 
            min_value=0.0, 
            value=current_val, 
            step=50.0, 
            key=f"budget_{cat}", 
            label_visibility="collapsed"
        )
        st.session_state.budget_allocations[cat] = allocated
    with col_c:
        if len(st.session_state.categories) > 1:
            if st.button("Remove", key=f"del_{cat}"):
                remove_category(cat)
    return allocated

def render_category_allocations():
    """Renders the category list and computes total planned expenses."""
    st.subheader("2. Budget Buckets & Allocations")
    render_category_adder()
    st.write("Allocate planned amounts for each category:")
    
    total_planned = 0.0
    for cat in list(st.session_state.categories):
        allocated = render_single_allocation_row(cat)
        total_planned += allocated
    return total_planned

def render_budget_summary(total_planned):
    """Displays total income, planned expenses, and unallocated balance metrics."""
    st.markdown("---")
    st.subheader("Budget Summary")
    unallocated = st.session_state.monthly_income - total_planned
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    col_sum1.metric("Total Income", f"${st.session_state.monthly_income:,.2f}")
    col_sum2.metric("Total Planned Expenses", f"${total_planned:,.2f}")
    col_sum3.metric("Unallocated Income", f"${unallocated:,.2f}", delta_color="inverse" if unallocated < 0 else "normal")

    if total_planned > st.session_state.monthly_income:
        st.error("⚠️ Warning: Your planned expenses exceed your expected monthly income!")

def render_budget_page():
    """Main controller function for the Budget Planner page."""
    st.header("Budget Planner")
    st.write("Set up your monthly income and customize your spending categories.")
    
    initialize_budget_session_state()
    render_income_section()
    total_planned = render_category_allocations()
    render_budget_summary(total_planned)