import os, streamlit as st

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper, ServiceContext
from langchain.llms.openai import OpenAI

# Uncomment to specify your OpenAI API key here, or add corresponding environment variable (recommended)
os.environ['OPENAI_API_KEY']= st.secrets['OPENAI_API_KEY']

def get_response(query):
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))

    max_input_size = 8192
    num_output = 256
    max_chunk_overlap = 20
    dirpath = './docs'
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    if True: 
        documents = SimpleDirectoryReader(dirpath).load_data()
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        
        response = index.query(query)
        if response is None:
            st.error("Oops! No result found")
        else:
            st.success(response)

# Define a simple Streamlit app
st.title("Chat con Chicho")
st.image('Allende50.jfif')
query = st.text_input("Pregúntele al Doctor Allende", "")

# If the 'Submit' button is clicked
if st.button("Pregunte"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            get_response(query)
        except Exception as e:
            st.error(f"An error occurred: {e}")
