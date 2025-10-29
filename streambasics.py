
import streamlit as st
st.title("Basic Ttitle")
st.header("header part")
st.text("this part contains basic text")
st.markdown("**bold text**and *italic text*")

#radiobutton
option=st.radio('select a option:',['m','e'])
st.write("select option is",option)

#dropdown
city=st.selectbox("slelect city",['deh','mun'])
st.write(f"you choose {city}")

name=st.text_input("enter your name")
st.write("hello",name)

 