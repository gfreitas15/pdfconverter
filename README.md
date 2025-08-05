# Monitor de Arquivos PDF

Este programa monitora uma pasta e renomeia automaticamente arquivos PDF chamados "Summary.pdf" para "Procuracao Certificado.pdf".

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

1. Execute o programa:
```bash
python rename.py
```

2. Na interface do programa:
   - Clique em "Selecionar Pasta" para escolher a pasta que deseja monitorar
   - Clique em "Iniciar Monitoramento" para começar a monitorar a pasta
   - O programa irá automaticamente renomear qualquer arquivo "Summary.pdf" que for adicionado à pasta para "PROCURACAO CERTIFICADO"
   - Clique em "Parar Monitoramento" para interromper o monitoramento