# Etapas

1. [[ ETAPA 1 ] - Ingestão dos dados locais "Filmes e Séries" (CSV)](./Arquivos/etapa1/etapa1.py)

2. [[ ETAPA 1 ] - Dockerfile](./Arquivos/etapa1/Dockerfile)

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

# Desenvolvimento

## Etapa I 


![1](../Evidencias/Captura%20de%20tela%202025-07-21%20204145.png)
- Importação das bibliotecas utilizadas. Principais:
    - OS: (leitura do .env) 
    - pandas: manipulação do csv em dataframes
    - boto3: utilização das funções de manipulação da aws
---



![2](../Evidencias/Captura%20de%20tela%202025-07-21%20204150.png)
- Nome do bucket a ser acessado, o caminho definido da especificação, e local da pastas de dados que contem os csv's. 
- Definição do tamanho do batch que será usado para particionar o resultado dos ID's filtrados
- nome dos arquivos para serem subidos no s3 e a categoria que vai funcionar como o diretório para aquela categoria (separado por pastas de ano, mes e dia)

![3](../Evidencias/Captura%20de%20tela%202025-07-21%20204154.png)
---
- Criação do cliente que é a conexão com as chamadas no s3 atraves de uma sessão.


![4](../Evidencias/Captura%20de%20tela%202025-07-21%20204157.png)
- Verificar se o bucket existe com o nome especificado e cria se não existir.
---

![5](../Evidencias/Captura%20de%20tela%202025-07-21%20204202.png)
- extrai a data de hoje para definir o caminho que nada mais é que a key no bucket do s3. Isso fez parte da espeficicação.
- verifica se já há um csv com esse nome, e se não houver, faz o upload.
---
![6](../Evidencias/Captura%20de%20tela%202025-07-21%20204209.png)

- Nessa parte é onde defini como será a filtragem dos dados do csv. Aqui que defini a quantidade de amostragem que usaria para realizar nossa analise. Alem de filtrar por genero de romance/drama, decidi trabalhar com aqueles no topo de popularidade baseado na quantidade de votos e nota média de cada um em relação a nota media e numero de votos medio do todo. Dessa forma, é considerado não apenas a qualidade da nota mas também em relação a prporção da quantidade de votos. 

- Decidi trabalhar com o "top 5%" dos dados de filmes mais votados. Uma boa margem para avaliar os melhores filmes, já que ainda vamos ter que filtrar e eliminar os casos em que foi muito descrepante o calculo realizado com o csv e da consulta na API do TMDB.
---
![7](../Evidencias/Captura%20de%20tela%202025-07-21%20204214.png)
![8](../Evidencias/Captura%20de%20tela%202025-07-21%20204219.png)
- Chamada das funcões na main
---
![9](../Evidencias/Captura%20de%20tela%202025-07-21%20204234.png)
- Criação da imagem Docker
---
![10](../Evidencias/Captura%20de%20tela%202025-07-21%20204428.png)
- Execução e resultado do build da imagem docker
---
![11](../Evidencias/Captura%20de%20tela%202025-07-21%20204537.png)
- Exibição de como estava a estrutura de pastas até esse momento.
---
![12](../Evidencias/Captura%20de%20tela%202025-07-21%20204602.png)
- Chamada do container e mostrando que o volume foi montado corretamente, acessando o diretorio /data e exibindo o conteudo corretamente
---
![13](../Evidencias/Captura%20de%20tela%202025-07-21%20204827.png)
- Resultado do diretorio apos a execução do container com o script da etapa1.
---
![14](../Evidencias/Captura%20de%20tela%202025-07-21%20204846.png)
- Logs de confirmação da criação de cada uma das partes da lista de Id's filtrado.
---
![15](../Evidencias/Captura%20de%20tela%202025-07-21%20204853.png)
- Logs de confirmação no upload de cada um dos csv's no bucket do s3 
---
![16](../Evidencias/Captura%20de%20tela%202025-07-21%20204903.png)
- Resultado esperado no bucket, com os diretorios esperados presentes
---
![18](../Evidencias/Captura%20de%20tela%202025-07-21%20204921.png)
- sucesso no upload de "movies.csv"
---
![19](../Evidencias/Captura%20de%20tela%202025-07-21%20204935.png)
- sucesso no upload de "series.csv"
---
![17](../Evidencias/Captura%20de%20tela%202025-07-21%20204911.png)
- sucesso no upload dos csvs com os id filtrados
---

# Etapa 2

![28](../Evidencias/Captura%20de%20tela%202025-07-21%20220906.png)
![29](../Evidencias/Captura%20de%20tela%202025-07-21%20220911.png)
![30](../Evidencias/Captura%20de%20tela%202025-07-21%20220915.png)
![31](../Evidencias/Captura%20de%20tela%202025-07-21%20220918.png)
![32](../Evidencias/Captura%20de%20tela%202025-07-21%20220923.png)
![33](../Evidencias/Captura%20de%20tela%202025-07-21%20220932.png)
![34](../Evidencias/Captura%20de%20tela%202025-07-21%20220940.png)
![36](../Evidencias/Captura%20de%20tela%202025-07-21%20220958.png)
![37](../Evidencias/Captura%20de%20tela%202025-07-21%20221009.png)
![38](../Evidencias/Captura%20de%20tela%202025-07-21%20221014.png)
![20](../Evidencias/Captura%20de%20tela%202025-07-21%20205048.png)
![22](../Evidencias/Captura%20de%20tela%202025-07-21%20205126.png)
![27](../Evidencias/Captura%20de%20tela%202025-07-21%20205303.png)
![26](../Evidencias/Captura%20de%20tela%202025-07-21%20205257.png)
![23](../Evidencias/Captura%20de%20tela%202025-07-21%20205140.png)
![24](../Evidencias/Captura%20de%20tela%202025-07-21%20205150.png)
![21](../Evidencias/Captura%20de%20tela%202025-07-21%20205108.png)



![39](../Evidencias/Captura%20de%20tela%202025-07-21%20221019.png)
![40](../Evidencias/Captura%20de%20tela%202025-07-21%20221047.png)
![41](../Evidencias/Captura%20de%20tela%202025-07-21%20221054.png)
![42](../Evidencias/Captura%20de%20tela%202025-07-21%20221059.png)
![43](../Evidencias/Captura%20de%20tela%202025-07-21%20221122.png)
![44](../Evidencias/Captura%20de%20tela%202025-07-21%20221126.png)
![46](../Evidencias/Captura%20de%20tela%202025-07-21%20224448.png)
![45](../Evidencias/Captura%20de%20tela%202025-07-21%20221937.png)
![25](../Evidencias/Captura%20de%20tela%202025-07-21%20205233.png)
