# 📁 Pasta de Documentos

Coloque seus arquivos PDF nesta pasta para facilitar o uso do sistema de ingestão.

## Como usar

1. Adicione seu PDF aqui (exemplo: `relatorio.pdf`)
2. Execute a ingestão:
   ```bash
   python ingest.py documentos/relatorio.pdf
   ```

## Exemplo de PDFs para teste

Você pode criar ou baixar PDFs para testar o sistema. Alguns exemplos:

- Relatórios empresariais
- Documentação técnica
- Artigos científicos
- Manuais de produtos

## Importante

- Use PDFs com **texto selecionável** (não apenas imagens)
- PDFs menores (até 50 páginas) processam mais rapidamente
- Cada nova ingestão **substitui** a anterior no banco de dados
