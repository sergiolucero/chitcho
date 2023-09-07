import streamlit as st
from awslib import s3_contents
from textlib import droplines
from linelib import simple_recorder 
##############################################
st.set_page_config(layout="wide")

tab1, tab2 = st.tabs(['Grabación','Revisión'])
with tab1:
    st.title('👨‍⚕️CETRAM QuantMed LLM Doctor🤖')
    for dropline in droplines:
        st.write(dropline)
    simple_recorder()
with tab2:
    st.header('Contents of cetram-felix/AUDIO')
    contents = s3_contents()  
    st.table(contents)
