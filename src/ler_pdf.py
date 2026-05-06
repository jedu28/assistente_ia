import os
from langchain_community.document_loaders import PyPDFLoader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
caminho = os.path.join(BASE_DIR, "documentos", "FAQ_Completo_5_Paginas_EcoStream.pdf")
loader = PyPDFLoader(caminho)
docs = loader.load()
for i, doc in enumerate(docs):
    print(f"\n--- Pagina {i+1} ---")
    print(doc.page_content[:300])
