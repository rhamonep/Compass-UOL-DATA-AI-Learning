# Resumo da Sprint

- Nesta sprint, estudei cursos da AWS focados em análise de dados na nuvem. Aprendi a usar o AWS Glue para organizar e preparar dados, facilitando a análise sem precisar gerenciar servidores. Também acompanhei tutoriais que mostram como aplicar essas ferramentas na prática.

- Com isso, entendi melhor como funciona o processo de trabalho com dados na AWS e como usar as ferramentas para tornar esse processo mais simples e eficiente.



## AWS Skill Builder - Fundamentals of Analytics on AWS – Part 2 (Portuguese)

- Neste curso, aprofundei o conhecimento sobre como analisar dados usando os serviços da AWS. Aprendi a organizar e proteger os dados, além de entender melhor como diferentes serviços funcionam juntos para processar grandes volumes de informação. Também vi como escolher o formato certo para armazenar dados e garantir que o acesso seja seguro e eficiente.



## AWS Skill Builder - AWS Glue Getting Started (Português)

- Aqui, aprendi a usar o AWS Glue para preparar dados para análise. Vi como criar processos para copiar, transformar e limpar dados automaticamente, sem precisar configurar servidores. Também entendi como o Glue ajuda a manter os dados organizados para que outras ferramentas da AWS possam acessar com facilidade.



## AWS - Playlist Tutoriais Técnicos - Analytics (YouTube)

- Nesta série de vídeos, acompanhei exemplos práticos de como usar as ferramentas de análise da AWS. Os tutoriais mostraram passo a passo como configurar serviços, conectar dados e criar consultas para extrair informações. Isso ajudou a entender na prática o funcionamento dos serviços estudados nos cursos.

# Desafio

- [Arquivos](./Desafio/Arquivos/)
- [README.MD](./Desafio/README.md)


# Exercícios

## Exercicio - Parte 1 - Geração e massa de dados

- Nesta atividade, desenvolvemos scripts em Python para gerar dados que serão utilizados em etapas futuras com Apache Spark. Inicialmente, na Etapa 1, criamos uma lista com 250 números inteiros aleatórios e aplicamos o método reverse para inverter sua ordem. Em seguida, na Etapa 2, declaramos uma lista com nomes de 20 animais, ordenamos em ordem crescente e salvamos cada item em um arquivo de texto, um por linha. Por fim, na Etapa 3, geramos um grande volume de nomes de pessoas utilizando a biblioteca names. Definimos 39.080 nomes únicos e geramos 10 milhões de nomes aleatórios com base nessa amostra, armazenando tudo em um arquivo nomes_aleatorios.txt, com um nome por linha.

- [Codigo - etapa 1 - 250 numeros](./Exercicios/Arquivos/Exercios/Ex%20I%20-%20etapa1.py)
- [Codigo - etapa 2 - 20 animais](./Exercicios/Arquivos/Exercios/Ex%20I%20-%20etapa2.py)
- [Codigo - etapa 3 - 10_000_000 nomes txt](./Exercicios/Arquivos/Exercios/Ex%20I%20-%20etapa3.py)

## Exercicio - Parte 2 - Apache Spark

- Nesta atividade, utilizamos o arquivo nomes_aleatorios.txt para explorar funcionalidades do Apache Spark voltadas à manipulação de DataFrames. Inicialmente, configuramos o ambiente e criamos uma SparkSession para carregar os dados com spark.read.csv, armazenando em df_nomes.

- Em seguida, ajustamos o schema do DataFrame, renomeando a coluna para Nomes e exibindo as primeiras linhas. Adicionamos novas colunas com dados gerados aleatoriamente, como Escolaridade, com três níveis (Fundamental, Médio, Superior), Pais, com nomes de 13 países da América do Sul, e AnoNascimento, com valores entre 1945 e 2010. Para essas operações, priorizamos funções nativas do Spark, evitando loops explícitos.

- Utilizamos métodos como select e filter para consultar dados, como identificar pessoas nascidas neste século ou da geração Millennials (1980–1994). Repetimos essas operações utilizando Spark SQL, registrando o DataFrame como tabela temporária.

- Por fim, com Spark SQL, agrupamos os dados por país e geração, filtrando por faixas de ano para obter a quantidade de pessoas por geração em cada país. O resultado foi exibido em ordem crescente de país, geração e quantidade.

- [Codigo - Apache Spark](./Exercicios/Arquivos/Exercios/Ex%20II%20-%20apache-spark.ipynb)


## Lab AWS Glue

- Neste laboratório, construímos um processo de ETL usando o serviço AWS Glue. Iniciamos com o upload do arquivo nomes.csv para um bucket no S3.

- Criamos uma role IAM chamada AWSGlueServiceRole-Lab4, com permissões amplas (S3, Glue, Lake Formation, CloudWatch). A role foi configurada como padrão no serviço AWS Glue, garantindo acesso aos recursos necessários.

- No AWS Lake Formation, criamos um banco de dados chamado glue-lab, onde os metadados das tabelas geradas pelo crawler foram armazenados.

- Criamos um job Glue via Script Editor, com engine Spark, linguagem Python 3 e 2 workers. O script utilizou o glueContext.spark_session para processar os dados. Parâmetros como S3_INPUT_PATH e S3_TARGET_PATH foram definidos para flexibilizar o código.

- O job leu o arquivo CSV, converteu os nomes para maiúsculo, imprimiu schema, contagem total e agrupada por ano/sexo. Também identificou o nome mais frequente por gênero e escreveu o resultado em formato JSON no S3, particionado por sexo e ano.

- Em seguida, criamos um crawler chamado FrequenciaRegistroNomesCrawler apontando para esse diretório. O crawler populou automaticamente a tabela frequencia_registro_nomes_eua no banco glue-lab.

- Por fim, validamos os dados no AWS Athena, consultando a tabela com SQL diretamente pelo Glue Catalog.

- [Codigo Job - AWS Glue ](./Exercicios/Arquivos/Lab/job_aws_glue_lab_4.py)
[jobs criados](./Evidencias/1%20jobs%20criados.png)

# Evidencias 

## Exercicio - Parte 1 - Geração e massa de dados


#### etapa 1
![etapa 1](./Exercicios/Evidencias/Parte%20I%20-%20Geração%20de%20Dados/etapa1.png)

#### etapa 2
![etapa 2](./Exercicios/Evidencias/Parte%20I%20-%20Geração%20de%20Dados/etapa2.png)

#### etapa 2 - txt
![etapa 2 - txt](./Exercicios/Evidencias/Parte%20I%20-%20Geração%20de%20Dados/etapa2%20-%20txt.png)

#### etapa 3
![etapa 3](./Exercicios/Evidencias/Parte%20I%20-%20Geração%20de%20Dados/etapa3.png)

#### etapa 3 - txt
![etapa 3 - txt](./Exercicios/Evidencias/Parte%20I%20-%20Geração%20de%20Dados/etapa3%20-%20txt.png)

---

## Exercicio - Parte 2 - Apache Spark

### etapa 1  
![1 etapa1](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/1%20etapa1.png)

### etapa 2  
![2 etapa2](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/2%20etapa2.png)

### etapa 3  
![3 etapa3](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/3%20etapa3.png)

### etapa 4  
![4 etapa4](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/4%20etapa4.png)

### etapa 5  
![5 etapa5](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/5%20etapa5.png)

### etapa 6  
![6 etapa6](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/6%20etapa6.png)

### etapa 7  
![7 etapa7](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/7%20etapa7.png)

### etapa 8  
![8 etapa8](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/8%20etapa8.png)

### etapa 9  
![9 etapa9](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/9%20etapa9.png)

### etapa 10  
![10 etapa10](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/10%20etapa10.png)

### etapa 10 - Consulta
![11 etapa10 show part 1](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/11%20etapa10%20show%20part%201.png)

![12 etapa10 show part 2](./Exercicios/Evidencias/Parte%20II%20-%20Apache%20Spark/12%20etapa10%20show%20part%202.png)

---

## Lab AWS Glue

### nomes csv - s3  
![1 nomes csv - s3](./Exercicios/Evidencias/Lab%20AWS%20Glue/1%20nomes%20csv%20-%20s3.png)

### role - lab4  
![2 role - lab4](./Exercicios/Evidencias/Lab%20AWS%20Glue/2%20role%20-%20lab4.png)

### role - permitions  
![3 role - permitions](./Exercicios/Evidencias/Lab%20AWS%20Glue/3%20role%20-%20permitions.png)

### aws glue - role select  
![4 aws glue - role select](./Exercicios/Evidencias/Lab%20AWS%20Glue/4%20aws%20glue%20-%20role%20select.png)

### access to bucket s3  
![5 access to bucket s3](./Exercicios/Evidencias/Lab%20AWS%20Glue/5%20access%20to%20bucket%20s3.png)

### update glue service role  
![6 update glue service role](./Exercicios/Evidencias/Lab%20AWS%20Glue/6%20update%20glue%20service%20role.png)

### database glue lab  
![7 database glue lab](./Exercicios/Evidencias/Lab%20AWS%20Glue/7%20database%20glue%20lab.png)

### job spark fresk  
![8 job spark fresk](./Exercicios/Evidencias/Lab%20AWS%20Glue/8%20job%20spark%20fresk.png)

### job config 1  
![9 job config 1](./Exercicios/Evidencias/Lab%20AWS%20Glue/9%20job%20config%201.png)

### job config 2  
![10 job config 2](./Exercicios/Evidencias/Lab%20AWS%20Glue/10%20job%20config%202.png)

### job config 3  
![11 job config 3](./Exercicios/Evidencias/Lab%20AWS%20Glue/11%20job%20config%203.png)

### job parameters input  
![12 job parameters input](./Exercicios/Evidencias/Lab%20AWS%20Glue/12%20job%20parameters%20input.png)

### job parameters output  
![13 job parameters output](./Exercicios/Evidencias/Lab%20AWS%20Glue/13%20job%20parameters%20output.png)

### scriptjob 1  
![14 scriptjob 1](./Exercicios/Evidencias/Lab%20AWS%20Glue/14%20script%20job%201.png)

### script job 2  
![15 script job 2](./Exercicios/Evidencias/Lab%20AWS%20Glue/15%20script%20job%202.png)

### script job 3  
![16 script job 3](./Exercicios/Evidencias/Lab%20AWS%20Glue/16%20script%20job%203.png)

### script job 4  
![17 scriptjob 4](./Exercicios/Evidencias/Lab%20AWS%20Glue/17%20script%20job%204.png)

### job run result  
![18 job run result](./Exercicios/Evidencias/Lab%20AWS%20Glue/18%20job%20run%20result.png)

### job run log  
![19 job run log](./Exercicios/Evidencias/Lab%20AWS%20Glue/19%20job%20run%20log.png)

### job log schema  
![20 job log schema](./Exercicios/Evidencias/Lab%20AWS%20Glue/20%20job%20log%20schema.png)

### job log lines count and names count  
![21 job log lines count and names count](./Exercicios/Evidencias/Lab%20AWS%20Glue/21%20job%20log%20lines%20count%20and%20names%20count%20.png)

### job log top1 names and year, top10 names per year  
![22 job log top1 names and year, top10 names per year](./Exercicios/Evidencias/Lab%20AWS%20Glue/22%20job%20log%20top1%20names%20and%20year,%20top10%20names%20per%20year.png)

### crawler  
![23 crawler](./Exercicios/Evidencias/Lab%20AWS%20Glue/23%20crawler.png)

### target db  
![24 target db](./Exercicios/Evidencias/Lab%20AWS%20Glue/24%20target%20db.png)

### crawler starting  
![25 crawler starting](./Exercicios/Evidencias/Lab%20AWS%20Glue/25%20crawler%20starting.png)

### crawler sucess  
![26 crawler sucess](./Exercicios/Evidencias/Lab%20AWS%20Glue/26%20crawler%20sucess.png)

### table created  
![27 table created](./Exercicios/Evidencias/Lab%20AWS%20Glue/27%20table%20created.png)

### athena data  
![28 athena data](./Exercicios/Evidencias/Lab%20AWS%20Glue/28%20athena%20data.png)

### athena query  
![29 athena query](./Exercicios/Evidencias/Lab%20AWS%20Glue/29%20athena%20query.png)

### athena query result  
![30 athena query result](./Exercicios/Evidencias/Lab%20AWS%20Glue/30%20athena%20query%20result.png)

# Certificados

### AWS - Fundamentals of Analytics on AWS - Part 2 (Português)
![AWS - Fundamentals of Analytics on AWS - Part 2 (Português)](./Certificados/AWS%20-%20Fundamentals%20of%20Analytics%20on%20AWS%20-%20Part%202%20(Português).png)

---

### AWS - Glue Getting Started (Portugues)
![AWS - Glue Getting Started (Portugues)](./Certificados/AWS%20-%20Glue%20Getting%20Started%20(Portugues).png)

---
