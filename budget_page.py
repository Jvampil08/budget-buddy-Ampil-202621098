import streamlit as st
import csv
import os

DEFAULT_CATEGORIES = ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Savings", "Miscellaneous"]

def load_budget_data_from_csv():
    """Loads all budget entries from budget_data.csv."""
    budget_records = []
    csv_filename = "budget_data.csv"
    
    if os.path.exists(csv_filename):
        try:
            with open(csv_filename, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        income_val = float(row.get("income", 0.0))
                        planned_val = float(row.get("planned_amount", 0.0))
                    except ValueError:
                        income_val = 0.0
                        planned_val = 0.0
                        
                    entry = {
                        "month": row.get("month", "January 2027"),
                        "income_source": row.get("income_source", "Allowance"),
                        "income": income_val,
                        "category": row.get("category", "Miscellaneous"),
                        "planned_amount": planned_val
                    }
                    budget_records.append(entry)
        except Exception as e:
            st.error(f"Error loading budget CSV: {e}")
            
    return budget_records

def initialize_budget_session_state():
    """Initializes budget session state with data parsed from CSV."""
    if "raw_budget_data" not in st.session_state:
        st.session_state.raw_budget_data = load_budget_data_from_csv()
    
    if "selected_budget_month" not in st.session_state:
        st.session_state.selected_budget_month = "January 2027"
        
    if "monthly_income" not in st.session_state:
        st.session_state.monthly_income = 15000.0
        
    if "income_source" not in st.session_state:
        st.session_state.income_source = "Allowance"
        
    if "budget_allocations" not in st.session_state:
        # Load default allocations for January 2027 from csv data
        update_state_for_selected_month("January 2027")

def update_state_for_selected_month(target_month):
    """Filters CSV records for the selected month and populates session state."""
    st.session_state.selected_budget_month = target_month
    allocations = {}
    
    found_records = [r for r in st.session_state.raw_budget_data if r["month"] == target_month]
    
    if found_records:
        st.session_state.income_source = found_records[0]["income_source"]
        st.session_state.monthly_income = found_records[0]["income"]
        for r in found_records:
            allocations[r["category"]] = r["planned_amount"]
    else:
        # Fallback if month doesn't exist in CSV yet
        for cat in DEFAULT_CATEGORIES:
            allocations[cat] = 0.0
            
    st.session_state.budget_allocations = allocations
    st.session_state.categories = list(allocations.keys())

def render_income_section():
    """Renders month selection, income source, and expected income inputs in Pesos."""
    st.subheader("1. Monthly Income Setup")
    
    available_months = ["January 2027", "February 2027", "March 2027", "April 2027"]
    current_month = st.session_state.get("selected_budget_month", "January 2027")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox(
            "Select Month", 
            available_months,
            index=available_months.index(current_month) if current_month in available_months else 0
        )
        if selected_month != st.session_state.selected_budget_month:
            update_state_for_selected_month(selected_month)
            st.rerun()
            
    with col2:
        st.text_input("Income Source", value=st.session_state.income_source, key="income_source")
    
    st.session_state.monthly_income = st.number_input(
        "Expected Monthly Income (₱)", 
        min_value=0.0, 
        value=float(st.session_state.monthly_income), 
        step=500.0
    )

def add_new_category(new_cat_name):
    """Adds a new category bucket to the current month's budget."""
    cleaned_name = new_cat_name.strip()
    if cleaned_name and cleaned_name not in st.session_state.categories:
        st.session_state.categories.append(cleaned_name)
        st.session_state.budget_allocations[cleaned_name] = 0.0
        st.success(f"Added category: {cleaned_name}")
        st.rerun()
    elif cleaned_name in st.session_state.categories:
        st.warning("Category already exists.")

def render_category_adder():
    """Renders the form input to add custom budget categories."""
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
    """Renders an input box and remove button for a single category bucket in Pesos."""
    col_a, col_b, col_c = st.columns([3, 2, 1])
    with col_a:
        st.text(cat)
    with col_b:
        current_val = st.session_state.budget_allocations.get(cat, 0.0)
        allocated = st.number_input(
            f"Amount for {cat}", 
            min_value=0.0, 
            value=float(current_val), 
            step=100.0, 
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
    """Renders all category allocation fields and calculates total planned expenses."""
    st.subheader("2. Budget Buckets & Allocations")
    render_category_adder()
    st.write("Allocate planned amounts for each category:")
    
    total_planned = 0.0
    for cat in list(st.session_state.categories):
        allocated = render_single_allocation_row(cat)
        total_planned += allocated
    return total_planned

def render_budget_summary(total_planned):
    """Displays total income, planned expenses, and unallocated balance metrics in Pesos."""
    st.markdown("---")
    st.subheader("Budget Summary")
    unallocated = st.session_state.monthly_income - total_planned
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    col_sum1.metric("Total Income", f"₱{st.session_state.monthly_income:,.2f}")
    col_sum2.metric("Total Planned Expenses", f"₱{total_planned:,.2f}")
    col_sum3.metric("Unallocated Income", f"₱{unallocated:,.2f}", delta_color="inverse" if unallocated < 0 else "normal")

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