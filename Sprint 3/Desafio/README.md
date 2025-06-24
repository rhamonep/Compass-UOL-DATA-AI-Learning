# Etapas

1. [Etapa I - etl.py](./Arquivos/etl/etl.py)

2. [Etapa II - job.py](./Arquivos/job/job.py)

3. [Etapa III - docker-compose.yml](./Arquivos/docker-compose.yml)

# Desafio apresentado

O desafio consiste em realizar a limpeza e análise de dados a partir do arquivo `concert_tours_by_women.csv`, que contém informações sobre turnês musicais. O arquivo possui dados provenientes de webscraping, podendo apresentar erros, dados incompletos ou desorganizados.

O objetivo é criar um script `etl.py` que limpe esses dados, gere um novo arquivo estruturado (`csv_limpo.csv`) e, a partir dele, outro script `job.py` que vai responda as perguntas apresentadas em um arquivo de texto `respostas.txt` e gere gráficos `Q4.png` e `Q5.png`. 

Toda a solução precisa rodar dentro de containers Docker, que vão se comunicar entre si através de um `docker-compose`. Além disso, os dados processados devem ser salvos em uma pasta local, que funciona como um volume compartilhado entre os containers.

## Etapa I - etl.py

![alt text](../Evidencias/image-0.png)

![alt text](../Evidencias/image.png)

![alt text](../Evidencias/image-1.png)

![alt text](../Evidencias/image-2.png)

![alt text](../Evidencias/image-3.png)

![alt text](../Evidencias/image-4.png)

![alt text](../Evidencias/image-5.png)

![alt text](../Evidencias/image-6.png)

![alt text](../Evidencias/image-7.png)

![alt text](../Evidencias/image-10.png)

![alt text](../Evidencias/image-8.png)

![alt text](../Evidencias/image-9.png)

## Etapa II - job.py

![alt text](../Evidencias/image-11.png)

![alt text](../Evidencias/image-12.png)

![alt text](../Evidencias/image-13.png)

![alt text](../Evidencias/image-15.png)

![alt text](../Evidencias/image-14.png)

![alt text](../Evidencias/image-16.png)

![alt text](../Evidencias/image-17.png)

![alt text](../Evidencias/image-18.png)

![alt text](../Evidencias/image-19.png)

![alt text](../Evidencias/image-20.png)

![alt text](../Evidencias/image-21.png)

![alt text](../Evidencias/image-37.png)

![alt text](../Evidencias/image-23.png)

![alt text](../Evidencias/image-24.png)

![alt text](../Evidencias/image-25.png)

![alt text](../Evidencias/image-26.png)

## Etapa III - docker-compose.yml

![alt text](../Evidencias/image-36.png)

![alt text](../Evidencias/image-27.png)

![alt text](../Evidencias/image-28.png)

![alt text](../Evidencias/image-29.png)

![alt text](../Evidencias/image-30.png)

![alt text](../Evidencias/image-32.png)

![alt text](../Evidencias/image-33.png)

![alt text](../Evidencias/image-34.png)