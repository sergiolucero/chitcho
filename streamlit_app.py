import streamlit as st
##############################################
st.set_page_config(page_title='Hable con Allende', layout='wide')
st.markdown("<h1 style='text-align: center; color: red;'>11+50: hable con Allende</h1>", unsafe_allow_html=True)

#tab1, tab2 = st.tabs(['Allende','Rettig'])
col1, col2, col3 = st.columns([1,10,1])

with col1:
    st.write(' ')
with col2:
    st.image('Allende50.jfif', width=300)
    st.write('creado como homenaje en Septiembre 2023 por Sergio Lucero')
with col3:
    st.write(' ')
st.write('version 0.1')
