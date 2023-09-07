import glob, os
import time
import streamlit as st
from textlib import text_and_soap
from timelib import chile_time
###############################
def audiosave(fn, audio_bytes):    
    fw = open(fn, 'wb')
    fw.write(audio_bytes)
    fw.close()

def process(audio_bytes): #, fecha, paciente):
    t0 = chile_time()
    fn = f'AUDIO/{t0}.wav'
    audiosave(fn, audio_bytes)
    return text_and_soap(fn) #, fecha, paciente)
