import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from main import processar_pergunta, buscar_contexto
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, "faqs_db")
db = Chroma(
    persist_directory=PATH, 
    embedding_function=OpenAIEmbeddings()
)

pergunta = "Quais países vocês atendem?"
print(f"Pergunta: {pergunta}")

resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)
print("\n--- Resultados e Scores da Busca ---")
for i, (doc, score) in enumerate(resultados):
    print(f"[{score:.4f}] {doc.page_content[:150].strip()}...")

resposta, contexto = processar_pergunta(pergunta)

print(f"\n--- Resposta Gerada ---")
print(resposta)
