import streamlit as st
import pandas as pd

st.title('Daily Coffee Consumption')

chart_data=pd.DataFrame(np.random.randn(20,3),columns=["a","b","c"])

employees=['Øyvind','Rodrigo','Valentina','Fede','Iggy']

coffees_per_kg=0

with st.sidebar:
  st.header("Add a coffee!☕")
  name=st.selectbox('Name',employees)
  last_coffee=st.selectbox('What is the last coffee?',['yes','no'])
  
  if last_coffee:
    price_per_cup=compute_price_per_cup(number_of_cups,price_kg)
    coffees_per_kg
