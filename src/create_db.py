from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def carregar_documentos():
    """Carrega os documentos do diretório 'documentos'"""
    try:
        diretorio_arquivos = os.path.join(BASE_DIR, "documentos")
        carregador = PyPDFDirectoryLoader(diretorio_arquivos)
        documentos = carregador.load()
        print(f"Documentos carregados: {len(documentos)}")
        return documentos
    except Exception as e:
        
        print(f"Erro ao carregar documentos: {e}")
        return None

def dividir_documentos(documentos):
    """Divide os documentos em pedacos"""
    try:
        separador = RecursiveCharacterTextSplitter(
            chunk_size=2000, #numero de caracteres por pedaco
            chunk_overlap=500, #numero de caracteres de sobreposicao entre os pedacos
            length_function=len, #funcao para calcular o tamanho do pedaco
            add_start_index=True, #adicionar o indice inicial do pedaco
        )
        
        chunks = separador.split_documents(documentos)
        print(f"Documentos divididos em: {len(chunks)} pedacos")
        return chunks
    except Exception as e:
        print(f"Erro ao dividir documentos: {e}")
        return None

        
def vetorizar_documentos(chunks):
    """Vetoriza os documentos"""
    try:
        db = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(),
            persist_directory=os.path.join(BASE_DIR, "faqs_db")
            
        )
        print("Base de dados criada com sucesso!")
    except Exception as e:
        print(f"Erro ao vetorizar documentos: {e}")
        return None
    


def criar_base_dados():
    # Carregar documentos
    #dividir em pedacos
    #criar embedding
    try:
        documentos = carregar_documentos()
        chunks = dividir_documentos(documentos)
        vetorizar_documentos(chunks)
        print("Processo completo sem erros.")
    except Exception as e:
        print(f"Erro ao criar base de dados: {e}")

if __name__ == "__main__":
    criar_base_dados()