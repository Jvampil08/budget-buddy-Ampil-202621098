import streamlit as st

def get_available_months():
    """Returns a list of available months for selection."""
    return ["January 2027", "February 2027", "March 2027", "April 2027"]

def render_month_selector():
    """Renders the month selector dropdown on the dashboard and stores selection in session state."""
    if "dashboard_month" not in st.session_state:
        st.session_state.dashboard_month = "January 2027"
        
    available_months = get_available_months()
    selected_month = st.selectbox(
        "Select Month to View Dashboard", 
        available_months,
        index=available_months.index(st.session_state.dashboard_month) if st.session_state.dashboard_month in available_months else 0,
        key="dash_month_select"
    )
    st.session_state.dashboard_month = selected_month
    return selected_month

def calculate_actual_expenses_for_month(target_month):
    """Calculates total actual expenses for the selected month."""
    expenses = st.session_state.get("expenses", [])
    total_actual = 0.0
    
    for exp in expenses:
        # Match by month string
        exp_month = exp.get("month", "")
        if exp_month == target_month:
            total_actual += float(exp.get("amount", 0.0))
            
    return total_actual

def get_planned_budget_for_month(target_month):
    """Retrieves planned budget totals and income for the selected month."""
    raw_budget = st.session_state.get("raw_budget_data", [])
    total_planned = 0.0
    monthly_income = 0.0
    
    month_records = [r for r in raw_budget if r["month"] == target_month]
    
    if month_records:
        monthly_income = month_records[0]["income"]
        for r in month_records:
            total_planned += r["planned_amount"]
    else:
        # Fallback if no CSV record exists for this month yet
        monthly_income = st.session_state.get("monthly_income", 15000.0)
        planned_allocations = st.session_state.get("budget_allocations", {})
        total_planned = sum(planned_allocations.values())
        
    return monthly_income, total_planned

def render_financial_summary_cards(monthly_income, total_planned, total_actual, money_remaining):
    """Renders top-level summary metrics cards in Philippine Pesos."""
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"₱{monthly_income:,.2f}")
    col2.metric("Planned Expenses", f"₱{total_planned:,.2f}")
    col3.metric("Actual Expenses", f"₱{total_actual:,.2f}")
    col4.metric(
        "Money Remaining", 
        f"₱{money_remaining:,.2f}", 
        delta_color="inverse" if money_remaining < 0 else "normal"
    )

def render_dashboard_page():
    """Main controller function for the Dashboard page (Part 1)."""
    st.header("Financial Dashboard")
    st.write("Overview of your monthly financial health and metrics.")
    
    # 1. Select Month
    selected_month = render_month_selector()
    st.markdown("---")
    
    # 2. Gather Data for Selected Month
    monthly_income, total_planned = get_planned_budget_for_month(selected_month)
    total_actual = calculate_actual_expenses_for_month(selected_month)
    money_remaining = monthly_income - total_actual
    
    # 3. Render Summary Metric Cards
    render_financial_summary_cards(monthly_income, total_planned, total_actual, money_remaining)
    
    st.markdown("---")
    st.info("Matplotlib visual charts and category breakdown tables will be added soon!")