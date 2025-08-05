# Etapas

1. [[ ETAPA 1 ] - Codigo AWS Glue (CSV)](./Arquivos/job_sprint6_local.py)

2. [[ ETAPA 2 ] - Codigo AWS (JSON)](./Arquivos/job_sprint6_tmdb.py)

# Desafio Apresentado

- Dando continuidade à construção do desafio final, nesta etapa avançamos para o processamento dos dados previamente ingeridos. Após a obtenção dos dados via arquivos CSV e complementação com dados da API TMDB, o objetivo agora é realizar o tratamento e organização dessas informações para torná-las confiáveis e prontas para análise.

- Nesta fase, trabalhamos com a camada Trusted do Data Lake, transformando os dados brutos da Raw Zone em um formato padronizado, limpo e estruturado. Para isso, utilizamos o serviço AWS Glue, com jobs em Spark, que processam os dados e os armazenam no formato Parquet, devidamente particionados por data de ingestão no S3.

- A Trusted Zone passa a ser consultável via AWS Athena, com metadados organizados no Glue Data Catalog, permitindo análises SQL eficientes sobre os dados confiáveis.

- Com isso, seguimos integrando os conhecimentos adquiridos, utilizando serviços avançados da AWS o processamento e a preparação dos dados que serão utilizados nas próximas etapas da análise.

# Desenvolvimento

## Etapa I - Codigo AWS Glue (CSV)

#### jobs criados

![jobs criados](../Evidencias/1%20jobs%20criados.png)

#### configuracao worker job

![configuracao worker job](../Evidencias/2%20configuracao%20worker%20job%20.png)

#### configuracao number e timeout job

![configuracao number e timeout job](../Evidencias/3%20configuracao%20number%20e%20timeout%20job.png)

#### parametros de local dos dados

![parametros de local dos dados](../Evidencias/4%20parametros%20de%20local%20dos%20dados.png)

#### parametros de local para resultado

![parametros de local para resultado](../Evidencias/5%20parametros%20de%20local%20para%20resultado.png)

#### bibliotecas, argumentos, contato e caminhos

![bibliotecas, argumentos, contato e caminhos](../Evidencias/6%20bibliotecas,%20argumentos,%20contexto%20e%20caminhos.png)

#### Schema a partir do csv

![Schema a partir do csv](../Evidencias/7%20Schema%20a%20partir%20do%20csv.png)

#### filtors de genero, notaMedia, numeroVotos e rating e remocao de colunas

![filtors de genero, notaMedia, numeroVotos e rating e remocao de colunas](../Evidencias/8%20filtors%20de%20genero,%20notaMedia,%20numeroVotos%20e%20rating%20e%20remocao%20de%20colunas.png)

#### voltando para spark dataframe e convertendo para parquet

![voltando para spark dataframe e convertendo para parquet](../Evidencias/9%20voltando%20para%20spark%20dataframe%20e%20convertendo%20para%20parquet.png)

## Etapa II -  Codigo AWS (JSON)

#### repetição do cabeçalho inicial do outro job

![repetição do cabeçalho inicial do outro job](../Evidencias/10%20repetição%20do%20cabeçalho%20inicial%20do%20outro%20job.png)

#### extração do ano, mes e dia a partir da url

![extração do ano, mes e dia a partir da url](../Evidencias/11%20extração%20do%20ano,%20mes%20e%20dia%20a%20partir%20da%20url.png)

#### conversao para pandas e remocao de colunas

![conversao para pandas e remocao de colunas](../Evidencias/12%20conversao%20para%20pandas%20e%20remocao%20de%20colunas.png)

#### spark dataframe com colunas de particao e parquet particionado

![spark dataframe com colunas de particao e parquet particionado](../Evidencias/13%20spark%20dataframe%20com%20colunas%20de%20particao%20e%20parquet%20particionado.png)

## Etapa III - Resultados

#### execução dos jobs

![execução dos jobs](../Evidencias/14%20execução%20dos%20jobs.png)

#### camada trusted criada com sucesso no datalake

![camada trusted criada com sucesso](../Evidencias/15%20camada%20trusted%20criada%20com%20sucesso.png)

#### dados do csv local em parquet

![csv do local em parquet](../Evidencias/16%20csv%20do%20local%20em%20parquet.png)

#### dados dos json da api em parquet particionado

![json do tmdb em parquet particionado](../Evidencias/17%20json%20do%20tmdb%20em%20parquet%20particionado.png)

#### criação do crawler

![criação do crawler](../Evidencias/20%20criação%20do%20crawler.png)

#### duas tabelas criadas no crawler (local e tmdb)

![duas tabelas criadas no crawler (local e tmdb)](../Evidencias/21%20duas%20tabelas%20criadas%20no%20crawler%20(local%20e%20tmdb).png)

#### resultado da consulta LOCAL athena

![resultado da consulta LOCAL athena](../Evidencias/22%20resultado%20da%20consulta%20LOCAL%20athena.png)

#### resultado da consulta TMDB athena

![resultado da consulta TMDB athena](../Evidencias/23%20resultado%20da%20consulta%20TMDB%20athena.png)