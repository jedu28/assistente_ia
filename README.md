# 📚 Assistente Virtual IA - RAG com Streamlit

Este é um projeto de um **Assistente Virtual Inteligente** desenvolvido em Python que utiliza a arquitetura **RAG (Retrieval-Augmented Generation)** para responder a perguntas com base em uma base de conhecimento em PDF (neste caso, documentos da EcoStream).

O sistema conta com uma interface de chat interativa feita em [Streamlit](https://streamlit.io/) e utiliza o [LangChain](https://www.langchain.com/) em conjunto com o banco de dados vetorial [ChromaDB](https://www.trychroma.com/) e a API da [OpenAI](https://openai.com/).

---

## 🛠 Tecnologias Utilizadas

- **[Python 3.9+](https://www.python.org/)**
- **[Streamlit](https://streamlit.io/)**: Interface gráfica amigável para chat.
- **[LangChain](https://python.langchain.com/)**: Orquestração do fluxo do LLM, prompts e recuperação de dados.
- **[ChromaDB](https://www.trychroma.com/)**: Banco de dados vetorial local persistente.
- **[OpenAI API](https://platform.openai.com/)**:
  - `text-embedding-3-small` / `text-embedding-ada-002` para vetorização dos documentos.
  - `gpt-4o-mini` para geração de texto conversacional.
- **PyPDF**: Leitura e extração de dados de arquivos PDF.

---

## 📂 Estrutura do Projeto

```text
├── .env                 # (Não versionado) Sua chave da API da OpenAI
├── .gitignore           # Ignora arquivos desnecessários e chaves da API
├── app.py               # Interface Gráfica Streamlit do Chatbot
├── create_db.py         # Script para ler PDFs, gerar chunks e criar a base vetorial
├── main.py              # Lógica principal de recuperação de contexto (RAG) e chamadas ao LLM
├── requirements.txt     # Dependências do projeto
├── documentos/          # Pasta onde ficam os PDFs de origem (Ex: FAQ EcoStream)
└── faqs_db/             # Pasta gerada pelo ChromaDB com os vetores de dados
    └── metadatos/
        └── info.txt     # Arquivo de configuração de template do Prompt
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/jedu28/assistente_ia.git
cd assistente_ia
```

### 2. Configurar o Ambiente Virtual
É altamente recomendado utilizar um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Mac/Linux
# No Windows: venv\Scripts\activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API da OpenAI:
```env
OPENAI_API_KEY="sk-SuaChaveAqui"
```

### 5. (Opcional) Recriar a Base de Conhecimento
Caso você adicione novos PDFs na pasta `documentos/`, será necessário recriar o banco de dados vetorial. Antes disso, apague a pasta `faqs_db` (lembre-se de fazer backup do `info.txt`):
```bash
python create_db.py
```

### 6. Rodar a Aplicação
Inicie o servidor local do Streamlit:
```bash
streamlit run app.py
```
O aplicativo abrirá automaticamente no seu navegador em `http://localhost:8501`.

---

## ☁️ Como Fazer Deploy no Streamlit Cloud

1. Faça login em [share.streamlit.io](https://share.streamlit.io/).
2. Clique em **"New app"** e conecte seu repositório GitHub (`jedu28/assistente_ia`).
3. O caminho para o "Main file path" deve ser `app.py`.
4. Clique em **"Advanced Settings"** e na aba "Secrets", cole sua variável de ambiente:
   ```toml
   OPENAI_API_KEY="sk-SuaChaveAqui"
   ```
5. Clique em **Deploy**. A nuvem lerá automaticamente o arquivo `requirements.txt` e colocará sua aplicação no ar!

---

## 📝 Personalização do Prompt

O comportamento do bot (personalidade, restrições e orientações gerais) pode ser modificado facilmente editando o arquivo de texto em `faqs_db/metadatos/info.txt`. Nenhuma alteração no código Python é necessária para mudar como ele interpreta o contexto e responde!
