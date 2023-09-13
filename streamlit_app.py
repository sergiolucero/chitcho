import os, streamlit as st
import boto3
import time, datetime
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain.llms.openai import OpenAI   # could be llama_index.llms  but maybe some other version
#######################################
os.environ['OPENAI_API_KEY']= st.secrets['OPENAI_API_KEY']
max_input_size = 8192;     num_output = 256;     max_chunk_overlap = 20;    dirpath = './docs'
#######################################
now = datetime.datetime.now
@st.cache_resource(show_spinner=False)
def get_index(idx_file = 'index2.pkl'):
    
    if os.path.exists(idx_file):
        index = GPTSimpleVectorIndex.load_from_disk(idx_file)
    else:
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.3, model_name="gpt-3.5-turbo-0613"))  # was text-davinci-003
        prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
        documents = SimpleDirectoryReader(dirpath).load_data()
        prompt = "Contesta como Salvador Allende, el autor de los discursos"
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, 
                                                       prompt_helper=prompt_helper) #, system_prompt=prompt)
        
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(idx_file)
    return index

def enviar_comentario(name, comment):
    timestamp = int(time.time())   # idealmente: now()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('chicho-cetram')
    table.put_item(Item={'username': name, 'timestamp': timestamp,
                         'comments': comment})

def comentarios():   # send to dynamodb
    st.write('Comentario')
    with st.form(key='comment_form'):
      name = st.text_input('Nombre')
      comment = st.text_area('Comentario')
      submit_button = st.form_submit_button(label='Enviar')
      if submit_button:
          st.write(f'Nombre: {name}')
          st.write(f'Comentario: {comment}')
          enviar_comentario(name, comment, timestamp)
          st.write('Gracias!')


def get_response(query):
    t0 = time.time()
    index = get_index()    
    response = index.query(query)
    if response is None:
        st.error("Oops! No result found")
    else:
        dt = round(time.time()-t0,2)
        tdt = f'[DT: {dt} secs]'
        st.success(str(response))
        comentarios()
##################################################################
st.title("Chat con el Chicho")
col1, col2 = st.columns(2)
with col1:
    st.image('Allende50.jfif', width=300)
with col2:
    query = st.text_input("Pregúntele al Doctor Allende", "¿cuál es la importancia del cobre?")
    if st.button("Pregunte"):
        if not query.strip():
            st.error(f"Escriba una pregunta.")
        else:
            try:
                get_response(query)
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
            
st.write('''creado en septiembre 2023 por Sergio Lucero. Fuentes: Textos de Salvador Allende (1971) de la Biblioteca Clodomiro Almeyda + ALLENDE
            a 50 años de su elección, discursos fundamentales (de la Biblioteca del Congreso).''')
