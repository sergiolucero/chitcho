import os, streamlit as st
import time
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from llama_index.llms import OpenAI   # was langchain.llms.openai

# Uncomment to specify your OpenAI API key here, or add corresponding environment variable (recommended)
os.environ['OPENAI_API_KEY']= st.secrets['OPENAI_API_KEY']

@st.cache_resource(show_spinner=False)
def get_index():
    if os.path.exists(idx_file):
        index = GPTSimpleVectorIndex.load_from_disk(idx_file)
    else:
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo-0613"))  # was text-davinci-003
        prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
        documents = SimpleDirectoryReader(dirpath).load_data()
        prompt = "Contesta como Salvador Allende, el autor de los discursos"
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, 
                                                       prompt_helper=prompt_helper,
                                                       system_prompt=prompt)
        
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        index.save_to_disk(idx_file)
    return index
    
def get_response(query):

    max_input_size = 8192;     num_output = 256
    max_chunk_overlap = 20;    dirpath = './docs'; idx_file = 'index.pkl'
    t0 = time.time()
    index = get_index()    
    response = index.query(query)
    if response is None:
        st.error("Oops! No result found")
    else:
        dt = round(time.time()-t0,2)
        tdt = f'[DT: {dt} secs]'
        st.success(str(response) + tdt)
##################################################################
st.title("Chat con Chicho")
st.image('Allende50.jfif', width=300)
query = st.text_input("Pregúntele al Doctor Allende", "")

if st.button("Pregunte"):
    if not query.strip():
        st.error(f"Escriba una pregunta.")
    else:
        try:
            get_response(query)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
            
st.write('creado en septiembre 2023 por Sergio Lucero')
