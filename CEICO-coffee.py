# st.title('Daily Coffee Consumption')

# chart_data=pd.DataFrame(np.random.randn(20,3),columns=["a","b","c"])

# members=['Øyvind','Rodrigo','Valentina','Fede','Iggy']

# number_of_cups, price_kg=10,2.

# def compute_price_per_cup(n_cups,price_kg):
#   return price_kg/n_cups

# with st.sidebar:
#   st.header("Add a coffee!☕")
#   name=st.selectbox('Name',members)
#   last_coffee=st.selectbox('What is the last coffee?',['yes','no'])
  
#   if last_coffee:
#     price_per_cup=compute_price_per_cup(number_of_cups,price_kg)
#     coffees_per_kg

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# ---- Page Setup ----
# about_page = st.Page(page='pages/About')

# coffees_per_kg=0
# number_of_cups, price_kg=10,2.

# Define file paths for persistent storage
COFFEE_DATA_FILE = '.data/.coffee_data.npy'
MEMBERS_FILE = '.data/.members.csv'
COLUMNS=["Date", "Name", "Cups", "Total Cups/Kg", "Coffee Bag Number", "Full Date"]
#,"Balance"]

# Predefine the date range
start_date = datetime(2024, 11, 26)
end_date = datetime(2025, 2, 1)
date_range = pd.date_range(start=start_date, end=end_date,freq='24h')

# Load members
try:
    members = pd.read_csv(MEMBERS_FILE)['Name'].to_list()
    random_members=np.random.choice(members, size=5, replace=False),
    
except FileNotFoundError:
    st.error(f"File {MEMBERS_FILE} not found. Please ensure it exists.")
    st.stop()
except KeyError:
    st.error("The members.csv file must have a column named 'Name'. Please update the file and try again.")
    st.stop()

# Load coffee data from file if it exists, otherwise create it
try:
    coffee_df = pd.DataFrame(np.load(COFFEE_DATA_FILE, allow_pickle=True),columns=COLUMNS)
    
except FileNotFoundError:
    coffee_df = pd.DataFrame(
        [
            {"Date": str(date).strip('00:00:00'), "Name": member, "Cups": 0, "Total Cups/Kg":0,"Coffee Bag Number":0, "Full Date": date ,}
            for member in members
            for date in date_range
        ]
    )

# Initialize session state for persistent tracking
if "coffee_data" not in st.session_state:
    st.session_state["coffee_data"] = coffee_df

# Title
st.title("☕ CEICO Coffee App")

# Sidebar: Input cups for a single person
st.sidebar.header("☕ Enter your coffee consumption")

selected_person = st.sidebar.selectbox(
    "Who are you recording consumption for?",
    st.session_state["coffee_data"]["Name"].unique(),
)
cups = st.sidebar.number_input("Enter cups of coffee:", min_value=0, step=1)
entry_date = st.sidebar.date_input('Enter the date for the entry', min_value=start_date, max_value=end_date)
# st.write(str(entry_date).strip("00:00:00"))
last_coffee=st.sidebar.selectbox('Did you open a new coffee bag?',['No','Yes'])
  
#   if last_coffee:
#     price_per_cup=compute_price_per_cup(number_of_cups,price_kg)
#     coffees_per_kg

# Save data to the file
def store_data():
    st.session_state["coffee_data"].to_numpy().dump(COFFEE_DATA_FILE)

# Update today's entry when the button is clicked
if st.sidebar.button("Log Entry"):
    st.session_state["coffee_data"].loc[
        (st.session_state["coffee_data"]["Name"] == selected_person)
        & (st.session_state["coffee_data"]["Full Date"] == pd.Timestamp(entry_date)),
        "Cups",
    ] = cups
    store_data()
    st.sidebar.success(f"Entry for {entry_date} logged successfully!")

# Display current data for the selected person
st.subheader(f"Coffee Consumption Data for {selected_person}")
person_data = st.session_state["coffee_data"][
    st.session_state["coffee_data"]["Name"] == selected_person
]

# st.dataframe(person_data.sort_values(by="Date"))
editable_df= st.data_editor(coffee_df,width=800,height=200)

st.subheader("Metrics")
col1,col2,col3=st.columns(3)

with col1:
    st.metric(label="Average Cups per Day",value=1)

with col2:
    st.metric(label="Average $/Cup",value=1)

with col3:
    st.metric(label="Average $/Month",value=1)

# Consumption trends: Multi-select for users
st.subheader("Consumption Trends")
st.write("Here are some consumption trends for 5 randomly selected users")
selected_people = st.multiselect(
    "Select the people you want to include in the plot:",
    st.session_state["coffee_data"]["Name"].unique(),
    # default=np.random.choice(st.session_state["coffee_data"]["Name"].unique(), size=5, replace=False),
    default=st.session_state["coffee_data"]["Name"].unique()[:5],
    # default=person_data.unique(),
)

# Plot consumption trends for selected people
if selected_people:
    # Filter data for selected people and up to today's date
    filtered_data = st.session_state["coffee_data"][
        (st.session_state["coffee_data"]["Name"].isin(selected_people))
        & (st.session_state["coffee_data"]["Full Date"] <= pd.Timestamp(entry_date))
    ]

    if not filtered_data.empty:
        # Pivot the data for plotting (each person's consumption as a separate column)
        pivot_data = filtered_data.pivot(index="Full Date", columns="Name", values="Cups")
        # st.bar_chart(data=None, *, x=None, y=None, x_label=None, y_label=None, color=None, horizontal=False, stack=None, width=None, height=None, use_container_width=True)
        st.line_chart(
            pivot_data,
            use_container_width=True,
            height=400,
        )
