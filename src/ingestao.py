"""
Script de Ingestão de PDF para RAG com LangChain e pgVector

Este script processa um arquivo PDF, cria embeddings e armazena
os vetores em um banco de dados PostgreSQL com extensão pgVector.

Uso:
    python ingestao.py <caminho_para_pdf>

Exemplo:
    python ingestao.py documentos/relatorio.pdf
"""

import sys
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da conexão com o banco
CONNECTION_STRING = "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
COLLECTION_NAME = "pdf_documents"


def verificar_arquivo_pdf(caminho_pdf: str) -> bool:
    """Verifica se o arquivo existe e é um PDF."""
    if not os.path.exists(caminho_pdf):
        print(f"❌ Erro: Arquivo não encontrado: {caminho_pdf}")
        return False

    if not caminho_pdf.lower().endswith('.pdf'):
        print(f"❌ Erro: O arquivo deve ter extensão .pdf")
        return False

    return True


def carregar_pdf(caminho_pdf: str):
    """Carrega o conteúdo do PDF."""
    print(f"📄 Carregando PDF: {caminho_pdf}")
    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()
    print(f"✅ PDF carregado: {len(documentos)} página(s) encontrada(s)")
    return documentos


def dividir_documentos(documentos):
    """Divide os documentos em chunks menores."""
    print("✂️  Dividindo documentos em chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documentos)
    print(f"✅ Documentos divididos em {len(chunks)} chunks")
    return chunks


def criar_embeddings_e_salvar(chunks):
    """Cria embeddings e salva no banco de dados pgVector."""
    print("🔄 Criando embeddings e salvando no banco de dados...")

    # Inicializar embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Limpar coleção anterior (substituir ingestão)
    try:
        # Conectar ao vector store existente e limpar
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=COLLECTION_NAME,
            connection=CONNECTION_STRING,
            use_jsonb=True,
        )

        # Deletar todos os documentos da coleção
        print("🗑️  Limpando dados anteriores...")
        vector_store.delete_collection()
        print("✅ Dados anteriores removidos")

    except Exception as e:
        print(f"ℹ️  Nenhum dado anterior encontrado (primeira ingestão)")

    # Criar novo vector store com os chunks
    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
    )

    print(f"✅ {len(chunks)} chunks salvos no banco de dados com sucesso!")
    return vector_store


def main():
    """Função principal de ingestão."""
    print("\n" + "="*60)
    print("🏗️  SISTEMA DE INGESTÃO DE PDF - RAG com LangChain")
    print("="*60 + "\n")

    # Verificar argumentos
    if len(sys.argv) != 2:
        print("❌ Uso incorreto!")
        print("📖 Uso correto: python ingestao.py <caminho_para_pdf>")
        print("📖 Exemplo: python ingestao.py documentos/relatorio.pdf")
        sys.exit(1)

    caminho_pdf = sys.argv[1]

    # Verificar se o arquivo existe
    if not verificar_arquivo_pdf(caminho_pdf):
        sys.exit(1)

    try:
        # Passo 1: Carregar PDF
        documentos = carregar_pdf(caminho_pdf)

        # Passo 2: Dividir em chunks
        chunks = dividir_documentos(documentos)

        # Passo 3: Criar embeddings e salvar
        criar_embeddings_e_salvar(chunks)

        print("\n" + "="*60)
        print("✅ INGESTÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print("➡️  Execute 'python chat.py' para fazer perguntas")
        print("="*60 + "\n")

    except Exception as e:
        print(f"\n❌ Erro durante a ingestão: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
