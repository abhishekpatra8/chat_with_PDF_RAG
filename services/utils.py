from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_postgres import PGVector
# from db.database import db_connect
from dotenv import load_dotenv
import base64, uuid, os

filepath = "./uploads/"
load_dotenv()

# if "OPENAI_API_KEY" not in os.environ:
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


class PDF_OPERATIONS:
    def __init__(self, data):
        self.data = data


    def convert_bytes_to_pdf(self):
        random_filename = str(uuid.uuid4()).replace("-", "")
        bytes = base64.b64decode(self.data, validate=True)
        try:
            f = open(f'{filepath}{random_filename}.pdf', 'wb')
            f.write(bytes)
            f.close()
            return f'{random_filename}.pdf'
        except Exception as e:
            print(e)


    def create_embeddings(self):
        try:
            # filename = self.convert_bytes_to_pdf()
            filename = filepath + "8fb4e702ff894577aca681555f33ff56.pdf"

            loader = PyPDFLoader(filename)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
            docs = text_splitter.split_documents(loader.load())

            embeddings = HuggingFaceEmbeddings()

            PGVector.from_documents(embedding=embeddings, documents=docs, collection_name=os.getenv("COLLECTION_NAME"), connection=os.getenv("CONNECTION_STRING"), use_jsonb=True)

            return True
        except Exception as e:
            print(e)
            return False


    def ask_question(self):
        embeddings = HuggingFaceEmbeddings()

        db = PGVector(embeddings=embeddings, collection_name=os.getenv("COLLECTION_NAME"), connection=os.getenv("CONNECTION_STRING"), use_jsonb=True)
        print(db)

        similarity = " ".join(i.page_content for i in db.similarity_search(self.data, k=3))

        embed_ques = embeddings.embed_query(self.data)

        llm = OllamaLLM(model=os.getenv("MODEL"))

        setup = RunnableParallel(context=db.as_retriever(), question=RunnablePassthrough())

        template = """You are acting as a Request For Proposal(RFP) Writer. You have to answer based on the given question and available context. \
                    If you can't answer the question, just say, I don't know.
                    Context: {context}
                    Question: {question}"""
        
        prompt = ChatPromptTemplate.from_template(template)

        chain = setup | prompt | llm | StrOutputParser()

        # result = chain.invoke({"context": similarity, "question": self.data})
        result = chain.invoke(self.data)
        print(result)