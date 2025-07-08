# Etapas

1. [Etapa I - etl.py](./Arquivos/etapa1.ipynb)

2. [Etapa II - job.py](./Arquivos/etapa2.ipynb)


# Desafio apresentado

O desafio consiste em trabalhar com dados públicos utilizando os serviços da AWS, com foco no armazenamento e processamento de arquivos diretamente a partir do Amazon S3. O participante deve escolher um conjunto de dados único disponível no portal de dados abertos do Governo Brasileiro, realizar tres análises definidas por ele e aplicar transformações específicas com o uso de bibliotecas como pandas, polars.

A solução será dividida em duas etapas principais, desenvolvidas em Notebooks: o primeiro será responsável por enviar o arquivo ao S3, com a utilização da biblioteca boto3, enquanto o segundo realizará as análises e transformações diretamente sobre o arquivo armazenado. Durante o processo, devem ser aplicadas operações como filtragem lógica, agregações, manipulações condicionais, conversões de tipo, datas e strings. O arquivo resultante da análise deve ser salvo de volta no mesmo bucket, sem que o arquivo local seja reutilizado após o envio inicial.

## Etapa I - Criação do bucket e upload do csv



## Etapa II - manipulações, analises e upload de resultados

