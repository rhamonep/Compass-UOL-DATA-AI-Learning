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

---

### ![1](../Evidencias/Captura%20de%20tela%202025-07-21%20204145.png)
- Importação das bibliotecas que serão utilizadas ao longo do script. Destaque para:
  - `os`: utilizada principalmente para leitura de variáveis de ambiente definidas no arquivo `.env`.
  - `pandas`: responsável pela manipulação dos arquivos CSV, transformando-os em DataFrames.
  - `boto3`: biblioteca da AWS usada para fazer as chamadas e interações com o S3 (upload, verificação de arquivos, criação de bucket, etc).

---

### ![2](../Evidencias/Captura%20de%20tela%202025-07-21%20204150.png)
- Aqui foram definidos os parâmetros principais que serão usados no restante da execução:
  - Nome do bucket que será acessado/criado.
  - Caminho base dentro do projeto e onde estão localizados os arquivos CSV.
  - Tamanho do lote (batch) que define como os dados filtrados serão particionados.
  - Nomes dos arquivos que serão gerados e enviados ao S3.
  - A categoria (ex: “filmes” ou “séries”), que servirá como pasta principal dentro da estrutura do bucket, organizada por ano, mês e dia — conforme especificação.

---

### ![3](../Evidencias/Captura%20de%20tela%202025-07-21%20204154.png)
- Criação do cliente S3 a partir da sessão configurada via boto3. Essa sessão é quem vai permitir que a aplicação consiga interagir com o S3 e realizar as operações necessárias (upload, verificação de existência, etc).

---

### ![4](../Evidencias/Captura%20de%20tela%202025-07-21%20204157.png)
- Verificação da existência do bucket com o nome que foi previamente definido.
- Caso o bucket ainda não exista, ele é criado automaticamente com as permissões padrão.

---

### ![5](../Evidencias/Captura%20de%20tela%202025-07-21%20204202.png)
- Nesse ponto, extraímos a data atual para montar o caminho onde os arquivos serão armazenados no S3 (seguindo a estrutura: ano/mês/dia).
- Antes de fazer o upload, o código verifica se já existe um arquivo com aquele mesmo nome e caminho. Se ainda não estiver presente no bucket, o upload é feito.

---

### ![6](../Evidencias/Captura%20de%20tela%202025-07-21%20204209.png)
- Aqui foi definida a lógica de filtragem dos dados do CSV original:
  - O foco foi selecionar filmes ou séries que se encaixassem nos gêneros "romance" ou "drama".
  - Para restringir ainda mais os dados e buscar amostras mais relevantes, decidi trabalhar apenas com os títulos mais populares. A seleção foi feita considerando dois critérios combinados: número de votos e nota média.
  - A ideia foi considerar títulos que estivessem no “top 5%” dos mais votados — assim, garantimos uma amostra significativa tanto em quantidade quanto em qualidade (evitando títulos com nota alta, mas poucos votos).
  - Esse recorte inicial ainda passará por uma filtragem adicional depois, cruzando os dados com a API do TMDB para validar e refinar os resultados.

---

### ![7](../Evidencias/Captura%20de%20tela%202025-07-21%20204214.png)
### ![8](../Evidencias/Captura%20de%20tela%202025-07-21%20204219.png)
- Execução da função principal que coordena as etapas do processo.

---

### ![9](../Evidencias/Captura%20de%20tela%202025-07-21%20204234.png)
- Criação da imagem Docker que será usada para rodar o pipeline em ambiente isolado.

---

### ![10](../Evidencias/Captura%20de%20tela%202025-07-21%20204428.png)
- Resultado da execução do build da imagem. Aqui conseguimos validar que o ambiente foi montado corretamente.

---

### ![11](../Evidencias/Captura%20de%20tela%202025-07-21%20204537.png)
- Exibição da estrutura de diretórios local no projeto até esse ponto da execução.

---

### ![12](../Evidencias/Captura%20de%20tela%202025-07-21%20204602.png)
- Execução do container Docker.
- Verificação de que o volume foi montado corretamente, permitindo o acesso ao diretório `/data` dentro do container e leitura correta dos arquivos.

---

### ![13](../Evidencias/Captura%20de%20tela%202025-07-21%20204827.png)
- Estrutura de diretórios após a execução do script dentro do container.
- Mostra os arquivos gerados a partir da filtragem e divisão em lotes.

---

### ![14](../Evidencias/Captura%20de%20tela%202025-07-21%20204846.png)
- Logs que confirmam a criação de cada um dos arquivos com os IDs filtrados.

---

### ![15](../Evidencias/Captura%20de%20tela%202025-07-21%20204853.png)
- Confirmação via log do sucesso no upload de cada CSV com os IDs filtrados para o bucket no S3.

---

### ![16](../Evidencias/Captura%20de%20tela%202025-07-21%20204903.png)
- Visualização da estrutura no bucket após o upload — validação de que os diretórios (por categoria/data) foram criados corretamente.

---

### ![18](../Evidencias/Captura%20de%20tela%202025-07-21%20204921.png)
- Confirmação do sucesso no upload do arquivo `movies.csv`.

---

### ![19](../Evidencias/Captura%20de%20tela%202025-07-21%20204935.png)
- Confirmação do sucesso no upload do arquivo `series.csv`.

---

### ![17](../Evidencias/Captura%20de%20tela%202025-07-21%20204911.png)
- Confirmação de que os arquivos com os IDs filtrados (em batches) também foram enviados com sucesso para o S3.

---

## Etapa II - Função Lambda

---

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


### Script que vai fazer a invocação da função lambda para cada um dos arquivos contidos no caminho prefixado: 
---
![42](../Evidencias/Captura%20de%20tela%202025-07-21%20221059.png)
![41](../Evidencias/Captura%20de%20tela%202025-07-21%20221054.png)
![43](../Evidencias/Captura%20de%20tela%202025-07-21%20221122.png)
![44](../Evidencias/Captura%20de%20tela%202025-07-21%20221126.png)
![46](../Evidencias/Captura%20de%20tela%202025-07-21%20224448.png)
![45](../Evidencias/Captura%20de%20tela%202025-07-21%20221937.png)
![25](../Evidencias/Captura%20de%20tela%202025-07-21%20205233.png)
