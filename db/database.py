from dotenv import load_dotenv
import psycopg2, os

load_dotenv()

def db_connect():
    # conn = psycopg2.connect(host=os.getenv("POSTGRE_HOST"), user=os.getenv("POSTGRE_USER"), password=os.getenv("POSTGRE_PASS"), dbname=os.getenv("POSTGRE_DB"))
    # return conn
    pass