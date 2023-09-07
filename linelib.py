import os
import streamlit as st
from textlib import chunk_summary, diagnostico
from audiorecorder import audiorecorder
from recorder import process
##############################
def fileread(fecha):
    pfn = f'previo-{fecha}.txt'
    if os.path.exists(pfn):
        lines = open(pfn, encoding='utf-8').read()
        lines = lines.split('-'*80)
        #lines = [line.split(chr(10)) for line in lines]
    return lines
    
def linetabs(fecha):
    lines = fileread(fecha)
    tabs = {}
    #for line in lines:
    line = lines[0]
    paciente = line.split(chr(10))[0][:5]  # drops patient_id
    tab = linetab(line, fecha, paciente) 
    tabs[paciente] = tab
    
    return tabs
    
def linetab(lines, fecha, paciente):   
    #html = open(filename).read()
    slines = lines.lstrip().split(chr(10))
    head = slines[0]  # dos líneas: (hora+ID, nombre paciente)
    head_split = head.split()
    #st.write('HEAD:', head_split[0][:5])
    #st.write('PAT:', ' '.join(head_split[1:]))
    #head[0] = head[0][:5]
    #st.write('HEAD:', head_split[0][:5])
    nombre_paciente = ' '.join(head_split[1:])
    
    body = slines[1:]
    #st.info(head)  # 
    #for bodline in body:
    #    st.write(bodline)
    
    audio = audiorecorder("Presione para grabar", 
                          "Grabando... presione para terminar",
                         key = head)
    
    if len(audio) > 0:
        st.audio(audio.tobytes())
        with st.spinner('procesando...'):
            text, soap, dts = process(audio.tobytes(), fecha, nombre_paciente)
            col1, col2 = st.columns(2)
        
            #with col1:
            if True:
                st.header(f'TRANSCRIPCION AUDIO:')   # [dt={dts[0]} secs]
                st.info(text)  # was write
                #diagnostico(text)
                        
            #with col2:
            if True:
                #st.write('add thumbs up/dn buttons to regenerate/accept!')
                st.header(f'resumen SOAP:') # [dt={dts[1]} secs]
                st.write(soap)
                st.write('-'*80)
                chunk_summary(text)

def video_recorder():
    pass
    # FUTURE: https://blog.streamlit.io/how-to-build-the-streamlit-webrtc-component/   

def simple_recorder():   
    
    audio = audiorecorder("Presione para grabar", 
                          "Grabando... presione para terminar")
    
    if len(audio) > 0:
        st.audio(audio.tobytes())
        with st.spinner('procesando...'):
            text, soap, dts = process(audio.tobytes())
            col1, col2 = st.columns(2)
        
            st.header(f'TRANSCRIPCION AUDIO:')   # [dt={dts[0]} secs]
            st.info(text)  # was write

            st.header(f'resumen SOAP:') # [dt={dts[1]} secs]
            st.write(soap)
            st.write('-'*80)
            chunk_summary(text)
