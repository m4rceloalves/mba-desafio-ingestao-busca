# Guia de Uso - Ingestão e Busca Semântica com LangChain e Postgres

Sistema de ingestão de PDFs e busca semântica usando LangChain, PostgreSQL com pgVector, OpenAI e Google Gemini.
Desafio Técnico 1 - MBA em Engenharia de Software com IA (FullCycle)
Author: Marcelo Barbosa Alves

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Docker e Docker Compose** instalados
3. **Chaves de API** configuradas no arquivo `.env`:
   - `OPENAI_API_KEY` - Para OpenAI
   - `GOOGLE_API_KEY` - Para Google Gemini

## 🚀 Passos para Execução

### 1. Iniciar o Banco de Dados

Primeiro, inicie o PostgreSQL com pgVector usando Docker Compose:

```bash
docker-compose up -d
```

Aguarde alguns segundos para o banco inicializar completamente. Você pode verificar o status:

```bash
docker-compose ps
```

### 2. Instalar Dependências (se ainda não fez)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ingestão de PDF

Execute o script de ingestão passando o caminho do PDF:

```bash
python src/ingestao.py <caminho_do_pdf>
```

**Exemplo:**

```bash
python src/ingestao.py documentos/relatorio.pdf
```

**O que acontece:**
- ✅ Carrega o PDF
- ✅ Divide o conteúdo em chunks
- ✅ Cria embeddings usando OpenAI
- ✅ Salva no banco de dados PostgreSQL com pgVector
- ✅ **Remove dados anteriores** (cada ingestão substitui a anterior)

### 4. Chat Interativo

Execute o script de chat:

```bash
python src/chat.py
```

**O que acontece:**
1. Sistema pergunta qual modelo você deseja usar:
   - **Opção 1:** OpenAI (gpt-5-nano)
   - **Opção 2:** Google Gemini (gemini-2.5-flash-lite)

2. Conecta ao banco de dados

3. Abre uma interface interativa onde você pode fazer perguntas

**Exemplo de uso:**

```
➡️  PERGUNTA: Qual o faturamento da empresa?

💡 RESPOSTA: O faturamento foi de 10 milhões de reais.

➡️  PERGUNTA: Quantos funcionários temos?

💡 RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Para sair, digite: `sair`, `exit`, `quit` ou pressione `Ctrl+C`

## 🎯 Características Principais

### ✅ Sistema de Ingestão (ingestao.py)

- Aceita arquivos PDF como entrada
- Processa e divide o texto em chunks otimizados
- Cria embeddings usando OpenAI `text-embedding-3-small`
- Armazena no PostgreSQL com pgVector
- **Substitui dados anteriores** automaticamente

### ✅ Módulo de Busca (busca.py)

- Módulo com lógica de RAG (Retrieval-Augmented Generation)
- Busca semântica usando similaridade de vetores
- Respostas baseadas **exclusivamente** no conteúdo do PDF
- Responde "Não tenho informações" quando não há contexto
- Integração com OpenAI e Google Gemini

### ✅ Interface de Chat (chat.py)

- Interface CLI interativa e intuitiva
- Escolha entre **OpenAI** ou **Google Gemini**
- Loop de perguntas e respostas
- Comandos para sair: `sair`, `exit`, `quit`

## 🛠️ Estrutura do Projeto

```
📂 projeto/
├── src/
│   ├── ingestao.py          # Script de ingestão de PDFs
│   ├── busca.py             # Módulo com lógica RAG
│   └── chat.py              # Interface CLI interativa
├── docker-compose.yaml      # Configuração PostgreSQL + pgVector
├── requirements.txt         # Dependências Python
├── .env                     # Chaves de API (não commitar!)
├── README.md                # Este arquivo
└── documentos/              # Pasta para seus PDFs (opcional)
```

## 🔧 Solução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique se o caminho do PDF está correto
- Use caminhos relativos ou absolutos

### Erro: "Connection refused" ou erro de banco
- Certifique-se de que o Docker Compose está rodando:
  ```bash
  docker-compose up -d
  ```
- Aguarde alguns segundos após iniciar o Docker

### Erro: "Invalid API Key"
- Verifique se as chaves estão corretas no arquivo `.env`
- Certifique-se de que o arquivo `.env` está na raiz do projeto

### Erro ao importar bibliotecas
- Reinstale as dependências:
  ```bash
  pip install -r requirements.txt
  ```

## 💡 Dicas de Uso

1. **Use PDFs com texto selecionável** (não imagens escaneadas)
2. **PDFs menores** têm processamento mais rápido
3. **Faça perguntas específicas** para melhores resultados
4. **Cada nova ingestão substitui a anterior**

## 🔄 Reiniciar o Banco de Dados

Se precisar limpar completamente o banco:

```bash
docker-compose down -v
docker-compose up -d
```

**Atenção:** Isso apagará todos os dados. Você precisará fazer a ingestão novamente.

