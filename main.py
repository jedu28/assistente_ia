import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv


# Carrega as variáveis de ambiente
load_dotenv()

PATH = "faqs_db"

def carregar_prompt():
    """Carrega o template de prompt a partir de um arquivo de texto."""
    caminho_prompt = os.path.join("faqs_db", "metadatos", "info.txt")
    try:
        with open(caminho_prompt, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        print(f"Erro ao carregar prompt: {e}")
        return ""

PROMPT_TEMPLATE = carregar_prompt()

def carregar_banco_dados():
    """Carrega e retorna a instância do Chroma DB."""
    if not os.path.exists(PATH):
        raise FileNotFoundError(f"A base de dados '{PATH}' não foi encontrada.")
        
    return Chroma(
        persist_directory=PATH, 
        embedding_function=OpenAIEmbeddings()
    )

def buscar_contexto(db, pergunta, k=3):
    """Busca os documentos mais relevantes na base de dados.
    Caso nao encontre documentos relevantes, retorna uma mensagem informando que nao foi possivel encontrar informacoes sobre a pergunta.
    """
    resultados_busca = db.similarity_search_with_relevance_scores(pergunta, k=k)
    contexto = "\n\n".join([doc.page_content for doc, score in resultados_busca])
    for doc, score in resultados_busca:
        if score > 0.7:
            contexto += "Fonte: " + doc.metadata["source"] + "\n"
    if contexto == "":
        return "Nao encontrei informacoes sobre a sua pergunta."
    return contexto

def gerar_resposta(pergunta, contexto):
    """Gera a resposta usando o LLM com base na pergunta e no contexto."""
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["documento", "pergunta"]
    )
    prompt_formatado = prompt.format(documento=contexto, pergunta=pergunta)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    resposta = llm.invoke(prompt_formatado)
    return resposta.content

def processar_pergunta(pergunta):
    """Função principal que integra todo o fluxo: busca + geração."""
    db = carregar_banco_dados()
    contexto = buscar_contexto(db, pergunta)
    resposta = gerar_resposta(pergunta, contexto)
    return resposta, contexto

if __name__ == "__main__":
    # Teste em console
    try:
        pergunta_usuario = input("Digite sua pergunta: ")
        resposta_gerada, contexto_usado = processar_pergunta(pergunta_usuario)
        
        print("\n--- CONTEXTO USADO ---")
        print(contexto_usado)
        
        print("\n--- RESPOSTA ---")
        print(resposta_gerada)
    except Exception as e:
        print(f"Erro: {e}")
