import streamlit as st
import pandas as pd

st.title('Daily Coffee Consumption')

chart_data=pd.DataFrame(np.random.randn(20,3),columns=["a","b","c"])

employees=['Øyvind','Rodrigo','Valentina','Fede','Iggy']

with st.sidebar:
  st.header("Input Coffee Consumption")
  name=st.selectbox('Name',employees)
  
