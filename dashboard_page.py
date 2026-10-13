import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def get_available_months():
    #Returns a list of available months for selection
    return ["January 2027", "February 2027", "March 2027", "April 2027"]

def render_month_selector():
    #Renders the month selector dropdown on the dashboard and stores selection in session state
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
    #Calculates total actual expenses and breakdown by category for the selected month
    expenses = st.session_state.get("expenses", [])
    actual_by_category = {}
    total_actual = 0.0
    
    for exp in expenses:
        exp_month = exp.get("month", "")
        if exp_month == target_month:
            cat = exp.get("category", "Miscellaneous")
            amt = float(exp.get("amount", 0.0))
            actual_by_category[cat] = actual_by_category.get(cat, 0.0) + amt
            total_actual += amt
            
    return total_actual, actual_by_category

def get_planned_budget_for_month(target_month):
    #Retrieves planned budget allocations and total income for the selected month
    raw_budget = st.session_state.get("raw_budget_data", [])
    planned_allocations = {}
    total_planned = 0.0
    monthly_income = 0.0
    
    month_records = [r for r in raw_budget if r["month"] == target_month]
    
    if month_records:
        monthly_income = month_records[0]["income"]
        for r in month_records:
            cat = r["category"]
            amt = r["planned_amount"]
            planned_allocations[cat] = amt
            total_planned += amt
    else:
        monthly_income = st.session_state.get("monthly_income", 15000.0)
        planned_allocations = st.session_state.get("budget_allocations", {})
        total_planned = sum(planned_allocations.values())
        
    return monthly_income, total_planned, planned_allocations

def render_financial_summary_cards(monthly_income, total_planned, total_actual, money_remaining):
    #Renders top-level summary metrics cards in Philippine Pesos
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"₱{monthly_income:,.2f}")
    col2.metric("Planned Expenses", f"₱{total_planned:,.2f}")
    col3.metric("Actual Expenses", f"₱{total_actual:,.2f}")
    col4.metric(
        "Money Remaining", 
        f"₱{money_remaining:,.2f}", 
        delta_color="inverse" if money_remaining < 0 else "normal"
    )

def render_budget_pie_chart(planned_allocations):
    #Renders a Matplotlib pie chart showing planned budget distribution
    st.subheader("Planned Budget Distribution")
    
    if not planned_allocations or sum(planned_allocations.values()) == 0:
        st.info("No planned budget allocations available to chart.")
        return

    fig, ax = plt.subplots(figsize=(5, 5))
    categories = list(planned_allocations.keys())
    amounts = list(planned_allocations.values())
    
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    ax.axis('equal')
    st.pyplot(fig)

def render_planned_vs_actual_chart(categories, planned_vals, actual_vals):
    #Renders a Matplotlib bar chart comparing planned vs actual spending by category
    st.subheader("Planned vs. Actual Spending")
    
    if not categories:
        st.info("No data available for comparison chart.")
        return

    fig, ax = plt.subplots(figsize=(7, 5))
    x = range(len(categories))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], planned_vals, width, label='Planned', color='skyblue')
    ax.bar([i + width/2 for i in x], actual_vals, width, label='Actual', color='salmon')
    
    ax.set_ylabel('Amount (₱)')
    ax.set_title('Planned vs. Actual Spending by Category')
    ax.set_xticks(list(x))
    ax.set_xticklabels(categories, rotation=30, ha='right')
    ax.legend()
    
    plt.tight_layout()
    st.pyplot(fig)

def render_budget_breakdown_table(categories, planned_allocations, actual_by_category):
    #Renders a detailed breakdown table comparing planned, actual, and remaining amounts per category
    st.markdown("---")
    st.subheader("Category Budget Breakdown")
    
    breakdown_data = []
    for cat in categories:
        planned = planned_allocations.get(cat, 0.0)
        actual = actual_by_category.get(cat, 0.0)
        remaining = planned - actual
        status = "✅ On Track" if remaining >= 0 else "⚠️ Over Budget"
        
        breakdown_data.append({
            "Category": cat,
            "Planned (₱)": f"₱{planned:,.2f}",
            "Actual (₱)": f"₱{actual:,.2f}",
            "Remaining / Over (₱)": f"₱{remaining:,.2f}",
            "Status": status
        })
        
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True)

def render_dashboard_page():
    #Main controller function for the fully completed Dashboard page
    st.header("Financial Dashboard")
    st.write("Overview of your monthly financial health, visual analytics, and category breakdowns.")
    
    #1. Select Month
    selected_month = render_month_selector()
    st.markdown("---")
    
    #2. Gather Data for Selected Month
    monthly_income, total_planned, planned_allocations = get_planned_budget_for_month(selected_month)
    total_actual, actual_by_category = calculate_actual_expenses_for_month(selected_month)
    money_remaining = monthly_income - total_actual
    
    #3. Render Summary Metric Cards
    render_financial_summary_cards(monthly_income, total_planned, total_actual, money_remaining)
    st.markdown("---")
    
    #4. Render Visualizations (Matplotlib Charts side by side)
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        render_budget_pie_chart(planned_allocations)
        
    with col_chart2:
        all_categories = sorted(list(set(list(planned_allocations.keys()) + list(actual_by_category.keys()))))
        planned_vals = [planned_allocations.get(c, 0.0) for c in all_categories]
        actual_vals = [actual_by_category.get(c, 0.0) for c in all_categories]
        render_planned_vs_actual_chart(all_categories, planned_vals, actual_vals)
        
    #5. Render Detailed Breakdown Table
    all_categories = sorted(list(set(list(planned_allocations.keys()) + list(actual_by_category.keys()))))
    render_budget_breakdown_table(all_categories, planned_allocations, actual_by_category)