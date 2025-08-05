# Monitor de Arquivos PDF

Programa para monitorar uma pasta selecionada, convertendo arquivos .JPEG. PNG e .JPG para .PDF, e renomeando
arquivos "Summary.pdf" para "PROCURACAO CERTIFICADO.pdf"

## Requisitos

- Python 3.6 ou superior
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

1. Execute o programa (ou baixe o executavel):
```bash
python rename.py
```

2. Na interface do programa:
   - Clique em "Selecionar Pasta" para escolher a pasta que deseja monitorar 
   - Clique em "Iniciar Monitoramento" para começar a monitorar a pasta 
   - Caso queira mudar de pasta, pare o monitoramento e inicie novamente para funcionar
   - Salve os arquivos que deseja convertar para PDF na pasta selecionada
   - O programa irá automaticamente converter os arquivos para .PDF e renomear qualquer arquivo "Summary.pdf" que for adicionado à pasta para "PROCURACAO CERTIFICADO"
   - Clique em "Parar Monitoramento" para interromper o monitoramento
   - Clique em "Juntar PDFs" e selecione os arquivos PDF que deseja combinar em um único documento, e escolha o nome desse documento