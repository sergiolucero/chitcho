import sys, glob, os, time

from langchain.document_loaders import Docx2txtLoader, PyPDFLoader, TextLoader

from langchain.embeddings import OpenAIEmbeddings, GPT4AllEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate

os.environ["OPENAI_API_KEY"] = "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"
yellow = "\033[0;33m";green = "\033[0;32m";white = "\033[0;39m"
##################################################
def langload(docpath = 'docs/*', tag = 'Allende'):
    print('[STARTED LOADING]')
    t0 = time.time()
    documents = []
    for ix, file in enumerate(glob.glob(docpath)):
        print(ix, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file)
        elif file.endswith('.docx') or file.endswith('.doc'):
            loader = Docx2txtLoader(file)
        elif file.endswith('.txt'):
            loader = TextLoader(file)
        # else:   print(f'CANNOT LOAD {file}')
            
        doc = loader.load()
        doc[0].metadata['tag'] = tag
        documents.extend(doc)
        
    print('LOADED:', len(documents), 'from', docpath, 'DT=', round(time.time()-t0,2))
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=10)            # 0907 increased CS from 1000
    documents = text_splitter.split_documents(documents)
    print('SPLIT:', len(documents), 'DT=', round(time.time()-t0,2))
    print('*** Creating Chroma Vectors ***')
    # embeddings = OpenAIEmbeddings()  # use max_Retries?
    embeddings = GPT4AllEmbeddings()  # use max_Retries?
    vectordb = Chroma.from_documents(documents, embedding=embeddings, persist_directory="./data")  # r for Rettig
    print('SPLIT:', len(documents), 'DT=', round(time.time()-t0,2))
    vectordb.persist()
    return vectordb
    
def chat(vectordb):
    pdf_qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb.as_retriever(search_kwargs={'k': 6}), return_source_documents=True,verbose=False)

    chat_history = []
    print(f"{yellow}---------------------------------------------------------------------------------")
    print('HOLA! Soy el DocuBot. Pregúnteme nomás.')
    print('---------------------------------------------------------------------------------')
    while True:
        query = input(f"{green}Prompt: ")
        if query in ("exit","quit","q","f"):
            print('Exiting')
            sys.exit()
        if query == '':
            continue
        result = pdf_qa({"question": query, "chat_history": chat_history})
        print(f"{white}Answer: " + result["answer"])
        chat_history.append((query, result["answer"]))