# Etapas

1. [Etapa I - etl.py](./Arquivos/etl/etl.py)

2. [Etapa II - job.py](./Arquivos/job/job.py)

3. [Etapa III - docker-compose.yml](./Arquivos/docker-compose.yml)

# Desafio apresentado

O desafio consiste em realizar a limpeza e análise de dados a partir do arquivo `concert_tours_by_women.csv`, que contém informações sobre turnês musicais. O arquivo possui dados provenientes de webscraping, podendo apresentar erros, dados incompletos ou desorganizados.

O objetivo é criar um script `etl.py` que limpe esses dados, gere um novo arquivo estruturado (`csv_limpo.csv`) e, a partir dele, outro script `job.py` que vai responda as perguntas apresentadas em um arquivo de texto `respostas.txt` e gere gráficos `Q4.png` e `Q5.png`. 

Toda a solução precisa rodar dentro de containers Docker, que vão se comunicar entre si através de um `docker-compose`. Além disso, os dados processados devem ser salvos em uma pasta local, que funciona como um volume compartilhado entre os containers.

## Etapa I - etl.py

![e1-imports](../Evidencias/e1-imports.png)

![e1-badlines](../Evidencias/e1-badlines.png)

![e1-leitura](../Evidencias/e1-leitura.png)

![e1-regex-ref](../Evidencias/e1-regex-ref.png)

![e1-regex-ref-result](../Evidencias/e1-regex-ref-result.png)

![e1-regex-title](../Evidencias/e1-regex-title.png)

![e1-split-year](../Evidencias/e1-split-year.png)

![e1-format-types](../Evidencias/e1-format-types.png)

![e1-format-types-result](../Evidencias/e1-format-types-result.png)

![e1-rename-fix-column](../Evidencias/e1-rename-fix-column.png)

![e1-result-expected](../Evidencias/e1-result-expected.png)

![e1-rename-fix-column-result](../Evidencias/e1-rename-fix-column-result.png)

## Etapa II - job.py

![e2-imports](../Evidencias/e2-imports.png)

![e2-leitura](../Evidencias/e2-leitura.png)

![e2-funcao-escrita](../Evidencias/e2-funcao-escrita.png)

![e2-criacao-txt](../Evidencias/e2-criacao-txt.png)

![e2-criacao-txt-result](../Evidencias/e2-criacao-txt-result.png)

![e2-q1](../Evidencias/e2-q1.png)

![e2-q1-result](../Evidencias/e2-q1-result.png)

![e2-q2](../Evidencias/e2-q2.png)

![e2-q2-result](../Evidencias/e2-q2-result.png)

![e2-q3](../Evidencias/e2-q3.png)

![e2-q3-result](../Evidencias/e2-q3-result.png)

![e2-q4](../Evidencias/e2-q4.png)

![e2-q4-grafico](../Evidencias/e2-q4-grafico.png)

![e2-q4-grafico-result](../Evidencias/e2-q4-grafico-result.png)

![e2-q5](../Evidencias/e2-q5.png)

![e2-q5-grafico](../Evidencias/e2-q5-grafico.png)

![e2-q5-grafico-result](../Evidencias/e2-q5-grafico-result.png)

## Etapa III - docker-compose.yml

![e3-estrutura](../Evidencias/e3-estrutura.png)

![e3-dockerfile-etl](../Evidencias/e3-dockerfile-etl.png)

![e3-dockerfile-job](../Evidencias/e3-dockerfile-job.png)

![/e3-env](../Evidencias/e3-env.png)

![e3-docker-compose](../Evidencias/e3-docker-compose.png)

![e3-resultado-build](../Evidencias/e3-resultado-build.png)

![e3-resultado-up](../Evidencias/e3-resultado-up.png)

![e3-resultado-volume](../Evidencias/e3-resultado-volume.png)