"""
Módulo de Busca Semântica com RAG usando LangChain e pgVector

Este módulo fornece as funções principais para busca semântica
e recuperação de informações usando RAG (Retrieval-Augmented Generation).

As funções deste módulo são utilizadas por chat.py para a interface interativa.
"""

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco
CONNECTION_STRING = "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
COLLECTION_NAME = "pdf_documents"


def inicializar_vector_store():
    """Inicializa a conexão com o vector store."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

    return vector_store


def criar_chain_rag(vector_store, llm):
    """Cria a chain de RAG para responder perguntas."""

    # Criar retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # Template do prompt
    template = """Você é um assistente que responde perguntas baseado EXCLUSIVAMENTE no contexto fornecido abaixo.

REGRAS IMPORTANTES:
1. Responda APENAS com informações presentes no contexto
2. Se a informação NÃO estiver no contexto, responda EXATAMENTE: "Não tenho informações necessárias para responder sua pergunta."
3. Seja direto e objetivo
4. Não invente, não deduza, não especule

CONTEXTO:
{context}

PERGUNTA: {question}

RESPOSTA:"""

    prompt = ChatPromptTemplate.from_template(template)

    # Função para formatar documentos
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Criar chain usando LCEL
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain


def processar_pergunta(chain, pergunta: str) -> str:
    """
    Processa uma pergunta e retorna a resposta.

    Args:
        chain: A chain RAG configurada
        pergunta: A pergunta do usuário

    Returns:
        str: A resposta gerada pelo sistema RAG
    """
    resposta = chain.invoke(pergunta)
    return resposta


def inicializar_sistema_rag(llm):
    """
    Inicializa todo o sistema RAG: vector store + chain.

    Args:
        llm: O modelo de linguagem (ChatOpenAI ou ChatGoogleGenerativeAI)

    Returns:
        A chain RAG configurada e pronta para uso
    """
    # Inicializar vector store
    vector_store = inicializar_vector_store()

    # Criar e retornar chain RAG
    chain = criar_chain_rag(vector_store, llm)

    return chain
