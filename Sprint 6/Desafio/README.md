# Etapas

1. [[ ETAPA 1 ] - Codigo AWS Glue (CSV)](./Arquivos/job_sprint6_local.py)

2. [[ ETAPA 2 ] - Codigo AWS (JSON)](./Arquivos/job_sprint6_tmdb.py)

# Desafio Apresentado

- Dando continuidade à construção do desafio final, nesta etapa avançamos para o processamento dos dados previamente ingeridos. Após a obtenção dos dados via arquivos CSV e complementação com dados da API TMDB, o objetivo agora é realizar o tratamento e organização dessas informações para torná-las confiáveis e prontas para análise.

- Nesta fase, trabalhamos com a camada Trusted do Data Lake, transformando os dados brutos da Raw Zone em um formato padronizado, limpo e estruturado. Para isso, utilizamos o serviço AWS Glue, com jobs em Spark, que processam os dados e os armazenam no formato Parquet, devidamente particionados por data de ingestão no S3.

- A Trusted Zone passa a ser consultável via AWS Athena, com metadados organizados no Glue Data Catalog, permitindo análises SQL eficientes sobre os dados confiáveis.

- Com isso, seguimos integrando os conhecimentos adquiridos, utilizando serviços avançados da AWS o processamento e a preparação dos dados que serão utilizados nas próximas etapas da análise.

# Desenvolvimento

## Etapa I

## Etapa II - Função Lambda

