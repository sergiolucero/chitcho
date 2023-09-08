import streamlit as st
##############################################
st.set_page_config(layout="wide")

#tab1, tab2 = st.tabs(['Allende','Rettig'])
col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')
with col2:
    st.title('11+50: hable con Allende')
    st.image('Allende50.jfif', width=300)
    st.write('creado como homenaje en Septiembre 2023 por Sergio Lucero')
with col3:
    st.write(' ')
st.write('version 0.1')
