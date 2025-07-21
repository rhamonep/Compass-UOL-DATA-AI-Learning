# Resumo

- Nesta sprint, aprofundamos o uso do Apache Spark com PySpark para processamento distribuído e eficiente de grandes volumes de dados, explorando suas capacidades para transformar e analisar dados de forma rápida e escalável.

- Também exploramos os principais serviços da AWS para construção de arquiteturas serverless de análise de dados, com foco em ingestão, armazenamento, catalogação, consulta e visualização, utilizando ferramentas como Amazon S3, AWS Glue, Athena e QuickSight.

- O objetivo foi integrar o poder do processamento em Spark com a flexibilidade e escalabilidade da AWS, garantindo pipelines analíticos eficientes, seguros e otimizados para diferentes tipos de análise.

---

## Formação Spark com PySpark: o Curso Completo

- Curso focado no Apache Spark, uma ferramenta robusta para processamento distribuído em larga escala.

- Principais conceitos abordados:  
  - Estrutura do Spark (RDDs, DataFrames, SparkSQL).  
  - Uso do PySpark para manipulação e transformação de dados.  
  - Integração com arquivos CSV, JSON, Parquet e bancos de dados.  
  - Execução local e em clusters simulados.

- Realização de exercícios práticos envolvendo DataFrames, funções de agregação, joins, filtros e transformações utilizando a API do PySpark.

---

## AWS Skill Builder – Fundamentals of Analytics on AWS (Portuguese)

- Compreensão dos tipos de análise de dados — descritiva, diagnóstica, preditiva e prescritiva — e sua aplicação para gerar valor nos negócios.

- Diferença entre data lakes, data warehouses e data marts, ilustrada com exemplos práticos.

- Visão completa do ciclo analítico na AWS, da ingestão à visualização, passando por armazenamento, catálogo, processamento e consulta.

- Serviços AWS para cada etapa do ciclo:  
  - Amazon Kinesis e AWS Glue para ingestão;  
  - Amazon S3 e Redshift para armazenamento;  
  - AWS Glue Data Catalog para organização dos metadados;  
  - Athena, EMR e Redshift Spectrum para consultas;  
  - QuickSight para visualização.

- Importância dos 5 Vs do Big Data (volume, velocidade, variedade, veracidade e valor) no tratamento de dados.

- Uso de formatos otimizados (Parquet, ORC) e particionamento para melhorar a performance das consultas.

- Governança de dados com IAM, Lake Formation e monitoramento via CloudWatch para garantir segurança e conformidade.

- Introdução prática a Machine Learning na AWS, com casos de uso, níveis de serviço e integração com pipelines analíticos.

- Processos ETL e ELT, com orientações sobre quando aplicar cada abordagem para eficiência.

- Testes de conhecimento aplicados para fixação dos conceitos e preparação para certificações.

---

## AWS Skill Builder – Serverless Analytics (Portuguese)

- Fundamentos da arquitetura serverless para análise de dados na AWS.

- Serviços principais envolvidos: AWS Lambda, Amazon Kinesis e Amazon S3, que permitem processamento e análise sem gerenciamento de servidores.

- Benefícios do modelo serverless: escalabilidade, flexibilidade e redução de custos operacionais.

- Integração dos serviços para construção de pipelines analíticos modernos e eficientes.

---

## AWS Skill Builder – Introduction to Amazon Athena (Portuguese)

- Apresentação do Amazon Athena para execução de consultas SQL diretamente no Amazon S3, sem necessidade de infraestrutura dedicada.

- Facilidade de análise de grandes volumes de dados de forma rápida e simples.

- Uso de formatos otimizados e integração com AWS Glue Data Catalog para melhor desempenho e organização dos dados.

- Exemplos práticos de consultas ad-hoc e análises exploratórias.
 

# Desafio

- [Arquivos](./Desafio/Arquivos/)
- [README.MD](./Desafio/README.md)

---

# Exercícios

## Apache Spark - Contador de Palavras

- Nesse exericio desenvolvemos um job de processamento de dados com o Apache Spark, utilizando um container Docker com a imagem jupyter/all-spark-notebook. Realizamos o pull da imagem e, caso necessário, utilizamos o Google Colab como alternativa. Em seguida, criamos e iniciamos um container com a imagem, expondo a porta 8888 para acessar o Jupyter Lab via navegador. Usamos o terminal do container para executar o pyspark com as flags interativas, habilitando o Spark Shell. Por fim, com comandos no Shell do Spark, processamos o conteúdo do arquivo README.md do repositório GitHub, contando as ocorrências de cada palavra presente no texto.

## Exercicios TMDB

- Criamos uma conta no portal do TMDB e geramos uma chave de API para acessar os dados públicos da plataforma. Com a chave em mãos, testamos a comunicação com a API usando Python e a biblioteca requests. Construímos uma URL de requisição para obter os filmes mais bem avaliados, especificando o idioma como português. Em seguida, extraímos e estruturamos os dados relevantes — como título, data de lançamento, sinopse e avaliação média — em um DataFrame com a biblioteca pandas, exibindo os resultados no notebook para validação.
---

# Evidências

### Apache Spark - Contador de Palavras

[Lista de comandos para execução do contador](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/comandos_spark.txt)

![pull_jupyter](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/1_pull_jupyter.png)

![jupyter_lab](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/2_jupyter_lab.png)

![url_acesso](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/3_url_acesso.png)

![browser](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/4_browser.png)

![docker_spark](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/5_docker_spark.png)

![wget_readme](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/6_wget_readme.png)

![pyspark](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/7_pyspark.png)

![spark_codigo](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/8_pyspark_codigo.png)

![resultado_1](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/9_resultado_1.png)

![resultado_2](./Exercicios/Apache%20Spark%20-%20Contador%20de%20Palavras/10_resultado_2.png)

### Exercicios TMDB

[Codigo .py](./Exercicios/Exercicios%20TMDB/Exercicio_TMDB.py)

```python
import requests
import pandas as pd
from IPython.display import display

api_key = "SUA CHAVE"

url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR"

response = requests.get(url)
data = response.json()

filmes = []

for movie in data['results']:
    df = {
        'Titulo': movie['title'],
        'Data de lançamento': movie['release_date'],
        'Visão geral': movie['overview'],
        'Votos': movie['vote_count'],
        'Média de votos': movie['vote_average']
    }
    filmes.append(df)

df = pd.DataFrame(filmes)
display(df)
```


![resultado_2](./Exercicios/Exercicios%20TMDB/1_codigo_resultado.png)


---

# Certificados

---

### AWS - Fundamentals of Analytics on AWS - Part 1 (Português)
![ Fundamentals of Analytics on AWS](./Certificados/AWS%20-%20Fundamentals%20of%20Analytics%20on%20AWS%20-%20Part%201%20(Português).png)

---

### AWS - Introduction to Amazon Athena (Português)
![Introduction to Amazon Athena](./Certificados/AWS%20-%20Introduction%20to%20Amazon%20Athena%20(Português).png)

---

### AWS - Serveless Analytics (Português)
![Serveless Analytics](./Certificados/AWS%20-%20Serveless%20Analytics%20(Português).png)

---

