"""
Script de Chat Interativo para Sistema RAG

Este script fornece a interface CLI interativa para fazer perguntas
ao sistema RAG, delegando a lógica de busca semântica para search.py.

Uso:
    python chat.py
"""

import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from search import inicializar_sistema_rag, processar_pergunta

# Carregar variáveis de ambiente
load_dotenv()


def escolher_modelo():
    """Permite ao usuário escolher entre OpenAI e Gemini."""
    print("\n" + "="*60)
    print("🤖 ESCOLHA O MODELO DE IA")
    print("="*60)
    print("1. OpenAI (gpt-5-nano)")
    print("2. Google Gemini (gemini-2.5-flash-lite)")
    print("="*60)

    while True:
        escolha = input("\n➡️  Digite 1 ou 2: ").strip()

        if escolha == "1":
            print("✅ Modelo selecionado: OpenAI gpt-5-nano")
            return ChatOpenAI(
                model="gpt-5-nano",
                temperature=0
            )
        elif escolha == "2":
            print("✅ Modelo selecionado: Google Gemini")
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-flash-lite",
                temperature=0
            )
        else:
            print("❌ Opção inválida! Digite 1 ou 2.")


def exibir_cabecalho():
    """Exibe o cabeçalho do sistema de chat."""
    print("\n" + "="*60)
    print("🔍 SISTEMA DE BUSCA SEMÂNTICA - RAG com LangChain")
    print("="*60)
    print("ℹ️  Digite sua pergunta ou 'sair' para encerrar")
    print("="*60 + "\n")


def loop_interativo(chain):
    """Loop principal de interação com o usuário."""
    exibir_cabecalho()

    while True:
        try:
            pergunta = input("\n➡️  PERGUNTA: ").strip()

            if not pergunta:
                print("⚠️  Por favor, digite uma pergunta válida.")
                continue

            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n" + "="*60)
                print("👋 Encerrando o sistema. Até logo!")
                print("="*60 + "\n")
                break

            # Delegar processamento para search.py
            print(f"\n💭 PERGUNTA: {pergunta}")
            print("-"*60)

            try:
                resposta = processar_pergunta(chain, pergunta)
                print(f"💡 RESPOSTA: {resposta}")
                print("-"*60)

            except Exception as e:
                print(f"❌ Erro ao processar pergunta: {str(e)}")
                print("-"*60)

        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("👋 Sistema interrompido. Até logo!")
            print("="*60 + "\n")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")


def main():
    """Função principal do sistema de chat."""
    try:
        # Escolher modelo
        llm = escolher_modelo()

        # Inicializar sistema RAG (delegar para search.py)
        print("\n🔄 Inicializando sistema RAG...")
        chain = inicializar_sistema_rag(llm)
        print("✅ Sistema RAG configurado!")

        # Iniciar loop interativo
        loop_interativo(chain)

    except Exception as e:
        print(f"\n❌ Erro ao inicializar o sistema: {str(e)}")
        print("ℹ️  Certifique-se de que:")
        print("   1. O Docker Compose está rodando (docker-compose up -d)")
        print("   2. Você executou a ingestão de um PDF (python ingest.py <pdf>)")
        print("   3. As chaves de API estão configuradas no arquivo .env")
        sys.exit(1)


if __name__ == "__main__":
    main()
