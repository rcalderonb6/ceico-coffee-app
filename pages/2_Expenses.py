import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np

# EXPENSES_DATA_FILE=

# Load expenses data from file if it exists, otherwise create it
# try:
#     coffee_df = pd.DataFrame(np.load(COFFEE_DATA_FILE, allow_pickle=True),columns=COLUMNS)
    
# except FileNotFoundError:
#     coffee_df = pd.DataFrame(
#         [
#             {"Date": str(date).strip('00:00:00'), "Name": member, "Cups": 0, "Total Cups/Kg":0,"Coffee Bag Number":0, "Full Date": date ,}
#             for member in members
#             for date in date_range
#         ]
#     )



if "expenses" not in st.session_state:
    st.session_state["expenses"] = []  # Initialize empty list for expenses
    
st.title("💰 Expense Splitter")

st.session_state["users"]=st.session_state["coffee_data"]["Name"].unique()

# Sidebar to manage expenses
st.sidebar.header("Add Expenses 💰")
expense_user = st.sidebar.selectbox("Who paid?", st.session_state["users"])
expense_amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
expense_description = st.sidebar.text_input("Description")
if st.sidebar.button("Add Expense"):
    if expense_user and expense_amount > 0:
        st.session_state["expenses"].append(
            {"user": expense_user, "amount": expense_amount, "description": expense_description}
        )
        st.sidebar.success(f"Added expense: {expense_description} - ${expense_amount} by {expense_user}")
    else:
        st.sidebar.warning("Please select a user and enter a valid amount.")

# Sidebar to manage users
st.sidebar.header("Manage Users")
new_user = st.sidebar.text_input("Add a user")

if st.sidebar.button("Add User"):
    if new_user and new_user not in st.session_state["users"]:
        st.session_state["users"].append(new_user)
        st.sidebar.success(f"Added user: {new_user}")
    elif new_user in st.session_state["users"]:
        st.sidebar.warning(f"User '{new_user}' already exists.")
    else:
        st.sidebar.warning("Please enter a valid name.")

# Display expenses
st.header("Expenses")
if st.session_state["expenses"]:
    expenses_df = pd.DataFrame(st.session_state["expenses"])
    st.dataframe(expenses_df,width=800,height=100)
else:
    st.write("No expenses added yet.")

# Calculate totals and balances
if len(st.session_state["users"]) > 0 and len (st.session_state["expenses"])>0:
    # Total expenses and per-person share
    total_expenses = sum(e["amount"] for e in st.session_state["expenses"])
    per_person_share = total_expenses / len(st.session_state["users"])

    # Balances
    balances = {user: -per_person_share for user in st.session_state["users"]}
    for expense in st.session_state["expenses"]:
        balances[expense["user"]] += expense["amount"]

    st.header("Balances")
    balance_df = pd.DataFrame(balances.items(), columns=["User", "Balance"])
    st.dataframe(balance_df,width=800,height=200)

    # Simplify debts
    st.header("Who Owes Whom")
    creditors = [(user, balance) for user, balance in balances.items() if balance > 0]
    debtors = [(user, -balance) for user, balance in balances.items() if balance < 0]

    transactions = []
    for debtor, debt in debtors:
        for creditor, credit in creditors:
            if debt == 0:
                break
            amount = min(debt, credit)
            transactions.append({"From": debtor, "To": creditor, "Amount": amount})
            debt -= amount
            credit -= amount
            creditors = [(c, cr) for c, cr in creditors if cr > 0]

    if transactions:
        transactions_df = pd.DataFrame(transactions)
        st.dataframe(transactions_df,width=800,height=200)
    else:
        st.write("No debts to settle; everyone is even!")

    # Visualize balances with bar chart
    st.header("Balance Overview")
    
    # st.write(balance_df['Balance'].size)
    # colors=["#ffaa00"]*balance_df['Balance'].size
    
    # colors[balance_df['Balance']<=0]="#ffaa00"
    st.bar_chart(balance_df,x='User',y='Balance')#,color=colors)
    # positive_balances = {user: balance for user, balance in balances.items() if balance > 0}
    # negative_balances = {user: balance for user, balance in balances.items() if balance < 0}
    
    # fig, ax = plt.subplots(figsize=(10, 5))
    # fig.patch.set_facecolor("black")  # Set figure background color
    # ax.set_facecolor("black") 
    # # Positive balances
    # ax.bar(
    #     positive_balances.keys(),
    #     positive_balances.values(),
    #     color="green",
    #     label="Positive Balances",
    # )

    # # Negative balances
    # ax.bar(
    #     negative_balances.keys(),
    #     negative_balances.values(),
    #     color="red",
    #     label="Negative Balances",
    #     edgecolor="white"
    # )

    # ax.axhline(0, color="white", linewidth=0.8)
    # ax.set_title("Balance Overview",color='white')
    # ax.set_xlabel("Users",color='white')
    # ax.set_ylabel("Balance",color='white')
    # ax.legend(facecolor="black", edgecolor="white")  # Legend with black background

    # st.pyplot(fig)
