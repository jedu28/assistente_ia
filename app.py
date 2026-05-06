import streamlit as st
from main import carregar_banco_dados, buscar_contexto, gerar_resposta

# Configuração da página do Streamlit
st.set_page_config(page_title="Assistente Virtual da ecostream", page_icon="📚")
st.title("📚 Assistente Virtual da ecostream")
st.write("Faça sua pergunta sobre nossa empresa e responderei com base na nossa base de conhecimento!")

# Carrega o banco de dados e mantém no cache do Streamlit para não recarregar a cada interação
@st.cache_resource
def get_db():
    try:
        return carregar_banco_dados()
    except FileNotFoundError as e:
        st.warning(str(e) + " Certifique-se de rodar 'create_db.py' primeiro.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar o banco de dados: {e}")
        return None

db = get_db()

if db:
    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens antigas
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do usuário
    if pergunta_usuario := st.chat_input("Digite sua pergunta:"):
        # Adiciona a mensagem do usuário ao histórico e exibe na tela
        st.session_state.messages.append({"role": "user", "content": pergunta_usuario})
        with st.chat_message("user"):
            st.markdown(pergunta_usuario)

        # Processamento e resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Buscando informações e gerando resposta..."):
                try:
                    # 1. Busca contexto utilizando a função modularizada
                    contexto = buscar_contexto(db, pergunta_usuario)
                    
                    # 2. Gera a resposta utilizando a função modularizada
                    resposta = gerar_resposta(pergunta_usuario, contexto)
                    
                    st.markdown(resposta)
                    
                    # Opcional: mostrar o contexto usado para gerar a resposta
                    with st.expander("Ver contexto recuperado (Fontes)"):
                        if contexto.strip():
                            st.info(contexto)
                        else:
                            st.warning("Nenhum contexto relevante encontrado para a pergunta.")
                            
                    # Salva no histórico
                    st.session_state.messages.append({"role": "assistant", "content": resposta})
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao processar sua pergunta: {e}")
