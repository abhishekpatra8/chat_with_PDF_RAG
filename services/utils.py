from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from models import model
import base64, uuid, os, datetime

filepath = "./uploads/"; embed_db_folder = "./db/"
load_dotenv()


def convert_bytes_to_pdf(filename, bs64):
    fileid = str(uuid.uuid4()).replace("-", "")
    bytes = base64.b64decode(bs64, validate=True)
    try:
        f = open(f'{filepath}{filename.replace(" ", "_")}', 'wb')
        f.write(bytes)
        f.close()
        return fileid
    except Exception as e:
        print(e)


def create_embeddings(filename, bs64):
    try:
        embedding_id = convert_bytes_to_pdf(filename, bs64)

        embediding_path = embed_db_folder + f"chroma_embeddings/{embedding_id}_embeddings"

        loader = PyPDFLoader(filepath + filename)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        docs = text_splitter.split_documents(loader.load())

        embedding = OllamaEmbeddings(model=os.getenv("MODEL"))

        Chroma.from_documents(persist_directory=embediding_path, documents=docs, embedding=embedding)

        os.remove(filepath + filename)

        return embedding_id
    except Exception as e:
        print(e)
        return False


def ask_question(data):
    embediding_path = embed_db_folder + f"chroma_embeddings/{data['embedding_id']}_embeddings"
    
    embeddings = OllamaEmbeddings(model=os.getenv("MODEL"))

    vectorstore = Chroma(persist_directory=embediding_path, embedding_function=embeddings)

    llm = OllamaLLM(model=os.getenv("MODEL"))

    setup = RunnableParallel(context=vectorstore.as_retriever(), question=RunnablePassthrough())

    template = """You are acting as a Request For Proposal(RFP) Writer. You have to answer based on the given question and available context. 
                And be very specific while answering the question. Be very precise to one line answer, and no other detailed information. \n \
                If you can't answer the question, just say, I don't know. \n 
                Context: {context} \n\n
                Question: {question}"""
    
    prompt = ChatPromptTemplate.from_template(template)

    chain = setup | prompt | llm | StrOutputParser()

    return chain.invoke(data['prompt'])