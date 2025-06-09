# Etapas

1. [Etapa I](./Arquivos/etapa1.sql)

2. [Etapa II](./Arquivos/etapa2.sql)

## Desafio apresentado

Dada uma base de dados de uma locadora NÃO normalizada, devemos aplicar as formas normais (3FN) e convertê-lo para o Modelo Relacional e depois do Modelo Relacional para o Modelo DImensional. Deve ser feito o modelo lógico de cada um.

## Etapa I


### Base de dados - Locacao

![tb_locacao_atributos](../Evidencias/tb_locacao_atributos.png)

Após o download da base de dados, usando o DBeaver, foi possível observar cada um dos atributos dessa tabela. 

Podemos observar que nela há muita informação duplicada e muitas dependencias indiretas, não seguindo as 3FN:

**1FN:** eliminar dados multivalorados e registros não atômicos

- Os atributos estão atômicos (um único registro), mas as colunas de "nomeCliente", "cidadeCliente", "estadoCliente" e "paisCliente", se repetem para o mesmo cliente em várias locações. Isso também acontece com as colunas referentes aos dados de carro e o mesmo para vendedor.  

**2FN**: remover dependências parciais

- Como a chave primária da tabela é "idLocacao", então para seguir a 2FN, todos os atributos devem depender unicamente dela. mas isso não acontece, atributos do cliente dependem de "idCliente", atributos de carro dependem de "idCarro", assim como atributos de vendedor e atributos de combustível.

**3FN**: remover dependências transitivas

- O atributo "estadoCliente" depende de "cidadeCliente" que depende de "idCliente".

**Solucionando:**
para seguir a 1FN, é necessário criar entidades seperadas afim de que cada entidade contenha apenas os proprios atributos sem repetição.
```
Cliente (idCliente, nome, cidade, estado, pais)
Carro (idCarro, km, classi, marca, modelo, ano, idCombustivel)
Combustivel (idCombustivel, tipo)
Vendedor (idVendedor, nome, sexo, estado)
Locacao (idLocacao, idCliente, idCarro, idVendedor, dataLocacao, horaLocacao, dataEntrega, horaEntrega, qtdDiaria, valorDiaria)
```
Fazendo isso, a 2FN e 3FN também já são respeitadas, não havendo mais dependencias parciais e nem transitivas.

Criamos então, o diagrama relacional, utilizando a ferramenta do site [Br Modelo web](https://www.brmodeloweb.com/).

![diagrama_relacional1](../Evidencias/diagrama_relacional1.png)

Pronto, agora a base de dados foi normalizada e está seguindo as 3FN. 

Utilizando esse diagrama, foi implementado em SQL a criação das novas tabelas e inserções desses dados em cada uma, conforme o arquivo da [Etapa I](./Arquivos/etapa1.sql).

### Explicações de algumas decisões na criação das tabelas

- Na tabela "Locacao" foi criado o atributo valorTotal que é o resultado de "qtdDiaria * valorDiaria" para armazenar a renda gerada naquela locação, já que parecia ser um dado muito útil para consultas. 

![not_null_locacao](../Evidencias/not_null_locacao.png)

- Os atributos de data estavam no formato DATETIME, mas so armazenavam uma data e os atributos de hora já estão em TIME. Logo o atributo foi criado como DATE (como mostrado acima). O restante dos atributos foi seguindo conforme a tabela original (tb_locacao).

![datetime_atributo](../Evidencias/datetime_atributo.png)

- Com exceção do atributo "sexo" na tabela "Vendedor" e do atributo criado "ValorTotal" na tabela "Locacao", todos os outros foram definidos como NOT NULL, já que são dados são necessários para registrar uma locação. 

![not_null_vendedor](../Evidencias/not_null_vendedor.png)

- O atributo "tipo" na tabela "Combustível" foi criado como UNIQUE para garantir um unico tipo de combustivel na tabela. O mesmo ocorre com "chassi" em carro, já que deve ser um atributo unico de cada carro (podendo também ser utilizada como chave alternativa).

![unique_combustivel](../Evidencias/unique_combustivel.png)
![unique_chassi](../Evidencias/unique_chassi.png)

### Explicações de alguns detalhes nas inserções nas tabelas:

- Para que cada carro tenha o dado correto em "km", foi necessário encontrar a quilometragem atual, já que na tabela antes do normalização, o mesmo carro aparece várias vezes com quilometragens diferentes. Para isso foi feito um WITH antes do INSERT.

![insert_carro](../Evidencias/insert_carro.png)

- As datas e horas na locação tiveram que ser formatadas. A data não se encontrava em um formato reconhecido por STRFTIME() para extrair o dia, mes, ano e dia semana na próxima etapa de modelagem dimensional. 

![data_naoformatado](../Evidencias/data_naoformatado.png)

Para resolver, antes do INSERT um WITH para formatar 

![data_cod_format](../Evidencias/data_cod_format.png)

A hora quando possuia um unico digito, também se tornava fora do padrão do STRFTIME() resultando em NULL para extrair hora. Para resolver, foi necessário adicionar um '0' no caso da hora ser menor que '10' para que haja dois digitos. No código a uma explicação de cada função utilizada para isso.

![hora_cod_format](../Evidencias/hora_cod_format.png)

### Fazendo consultas nas tabelas:

```sql
SELECT * FROM Carro
```
![consulta_carro](../Evidencias/consulta_carro.png)
```sql
SELECT * FROM Cliente
```
![consulta_cliente](../Evidencias/consulta_cliente.png)
```sql
SELECT * FROM Combustivel
```
![consulta_combustivel](../Evidencias/consulta_combustivel.png)
```sql
SELECT * FROM Locacao
```
![consulta_locacao](../Evidencias/consulta_locacao.png)
```sql
SELECT * FROM Vendedor
```
![consulta_vendedor](../Evidencias/consulta_vendedor.png)

## Etapa II

Para criar a modelagem dimensional a partir da relacional, deve-se identificar primeiro o Fato Principal. No caso dessa base de dados é a locação, já que ela contém os dados centrais das transações. 

![fato_locacao](../Evidencias/fato_locacao.png)

Em seguida, identificar as dimensões, que respondem as perguntas "Quem, O quê, Quando, Onde, Como" que serão os eixos da análise, pois o modelo dimensional é usado para análisar dados e otimizar consultas analíticas. No caso da locação:

- dimensão Cliente:  "Quem alugou o carro?", 
- dimensão Carro: "Qual carro foi alugado?", 
- dimensão Vendedor: "Quem fez a venda?",
- dimensão Data: "Em qual data o carro foi alugado?",
- dimensão Horario: "Em qual horario o carro foi alugado?",
- dimensão Combustivel: "Qual o tipo de combustivel do carro alugado?" 

Criando essas dimensões, chegamos no modelo lógico da Modelagem Relacional, com a estrutura de estrela.

![dimensoes](../Evidencias/dimensoes.png)

Utilizando esse diagrama, foi implementado em SQL a criação das VIEWS, conforme o arquivo da [Etapa II](./Arquivos/etapa2.sql).

### Explicações de algumas decisões na criação das Views

- Para criar tanto a Dim_Tempo como a Dim_Horario, foi feito um UNION para unir as datas de entrega e datas de locação

![union_dim_tempo](../Evidencias/union_dim_tempo.png)
![union_dim_horario](../Evidencias/union_dim_horario.png)

- Com a formatação da hora e data feita na etapa I, foi possível extrair individualmente os dados de dia, mes, ano, diaSemana, hora e minuto utilizando STRFTIME() como mostrado nas consultas mais abaixo.

![data_strftime](../Evidencias/data_strftime.png)
![horario_strftime](../Evidencias/horario_strftime.png)

- Foi pensado a ideia de criar idTempo e idHorario para as dimensões e adiciona-las no fato, mas seria necessário a criação de uma nova tabela. Como foi aconselhado a criação de views para esse desafio, não foi possível essa implementação. (garantiria mais performance na consulta).

### Fazendo consultas nas Views:

```sql
SELECT * FROM Dim_Tempo
```
![consulta_dim_tempo](../Evidencias/consulta_dim_tempo.png)
```sql
SELECT * FROM Dim_Horario
```
![consulta_dim_horario](../Evidencias/consulta_dim_horario.png)
```sql
SELECT * FROM Dim_Carro
```
![consulta_dim_carro](../Evidencias/consulta_dim_carro.png)
```sql
SELECT * FROM Dim_Cliente
```
![consulta_dim_cliente](../Evidencias/consulta_dim_cliente.png)
```sql
SELECT * FROM Dim_Combustivel
```
![consulta_dim_combustivel](../Evidencias/consulta_dim_combustivel.png)
```sql
SELECT * FROM Dim_Vendedor
```
![consulta_dim_vendedor](../Evidencias/consulta_dim_vendedor.png)
```sql
SELECT * FROM Fato_Locacao
```
![consulta_fato_locacao](../Evidencias/consulta_fato_locacao.png)

### Algumas análises feitas com o as Views: 

1. Qual foi receita total em cada mês?

![analise_mensal](../Evidencias/analise_mensal.png)

**Resultado:**

![consulta_analise_mensal](../Evidencias/consulta_analise_mensal.png)


2. Quais dias da semana há mais locações?

![analise_semanal](../Evidencias/analise_semanal.png)

**Resultado:**

![consulta_analise_semanal](../Evidencias/consulta_analise_semanal.png)


3. Qual hora há pico de locações por dia?

![analise_horario](../Evidencias/analise_horario.png)

**Resultado:**

![consulta_analise_horario](../Evidencias/consulta_analise_horario.png)