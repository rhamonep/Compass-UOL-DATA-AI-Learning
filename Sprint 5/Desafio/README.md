# Etapas
1. [[ ETAPA 1 ] - Dockerfile](./Arquivos/etapa1/Dockerfile)

2. [[ ETAPA 1 ] - Ingestão dos dados locais "Filmes e Séries" (CSV)](./Arquivos/etapa1/etapa1.py)

3. [[ ETAPA 2 ] - Função Lambda: Consulta API TMDB](./Arquivos/etapa2/etapa2.py)

4. [[ ETAPA 2 ] - Script Python - Multiplas invocações da função Lambda](./Arquivos/etapa2/etapa2.py)


# Desafio Apresentado

Este desafio marcou o início da construção do desafio final, no qual recebemos dois arquivos CSV contendo múltiplos dados sobre filmes e séries. A partir desses dados, deveríamos elaborar questões para compor uma análise analítica, que será desenvolvida ao longo das próximas sprints.

Deve-se realizar a ingestão de novos dados a partir de uma API que complemente as informações dos CSVs. Além disso, deve-se utilizar uma imagem Docker para criar um container que faça o upload desses dados para um bucket S3 dos serviços da AWS, e usar uma função Lambda para realizar as consultas na API.

Este desafio visa colocar em prática todo o conhecimento adquirido até o momento.

# Análise -  Fatores de Sucesso em Filmes de Baixo Orçamento

Após explorar os dados disponíveis e catalogados nos CSVs de filmes e séries, busquei compor uma análise que fosse de interesse para produtoras em geral. Minha ideia central foi a seguinte:

- Entre os filmes mais bem avaliados, existem tanto aqueles com alto orçamento quanto com baixo orçamento. Quais fatores podem ter contribuído para o sucesso de um filme de baixo orçamento em comparação com os de alto orçamento? Presença de atores populares? Equipe técnica renomada? Direção?

- Essa análise tem como objetivo tentar identificar algum padrão ou resultado consistente que explique o sucesso desses filmes independentemente do orçamento. O resultado poderia influenciar diretamente as produtoras a otimizar seus orçamentos ou reavaliar os recursos utilizados, de modo a aumentar as chances de sucesso.

## Etapa I - Criação do bucket, definição das análises e upload do csv

Abertura do preview do CSV para visualização dos dados para elaboração das análises.