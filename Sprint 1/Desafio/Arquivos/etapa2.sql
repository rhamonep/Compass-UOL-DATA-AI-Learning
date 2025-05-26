------------- DIMENSÕES -----------------

--- Dimensão Tempo ---
CREATE VIEW Dim_Tempo AS
WITH todasDatas as(
	SELECT DISTINCT
    	dataLocacao as data
	FROM Locacao
	UNION
	SELECT DISTINCT 
    	dataEntrega as data
    FROM Locacao
)	
SELECT
    data,
    strftime('%d', data) AS dia,
    strftime('%w', data) AS diaSemana,
    strftime('%m', data) AS mes,
    strftime('%Y', data) AS ano
FROM todasDatas;

-- Dimensão Hora ---
CREATE VIEW Dim_Horario AS
WITH todosHorario as(
	SELECT DISTINCT
    	horaLocacao as horario
	FROM Locacao
	UNION
	SELECT DISTINCT 
    	HoraEntrega as horario
    FROM Locacao
)	
SELECT
    horario,
    strftime('%H', horario) AS hora,
    strftime('%M', horario) AS minuto
FROM todosHorario;

-- Dimensão Cliente ---
CREATE VIEW Dim_Cliente AS
SELECT 
	idCliente, 
	nome, 
	cidade, 
	estado,
	pais
FROM Cliente;


-- Dimensão Carro ---
CREATE VIEW Dim_Carro AS
SELECT 
	idCarro, 
	chassi, 
	marca,
	modelo, 
	ano,
	idCombustivel
FROM Carro;


-- Dimensão Combustível ---
CREATE VIEW Dim_Combustivel AS
SELECT 
	idCombustivel, 
	tipo
FROM Combustivel;


-- Dimensão Vendedor ---
CREATE VIEW Dim_Vendedor AS
SELECT 
	idVendedor, 
	nome, 
	sexo, 
	estado
FROM Vendedor;

------------- FATO -----------------

-- Fato Locação ---
CREATE VIEW Fato_Locacao AS
SELECT
    idLocacao,
    idCliente,
    idCarro,
    idVendedor,
    
    dataLocacao,
    horaLocacao,
    dataEntrega,
    horaEntrega, 

    qtdDiaria,
    valorDiaria,
    valorTotal
FROM Locacao;

------------- CONSULTAS -----------------

SELECT * FROM Dim_Carro;

SELECT * FROM Dim_Cliente;

SELECT * FROM Dim_Combustivel;

SELECT * FROM Dim_Horario;

SELECT * FROM Dim_Tempo;

SELECT * FROM Dim_Vendedor;

SELECT * FROM Fato_Locacao;

------------- EXEMPLOS DE ANÁLISES COM VIEWS -----------------

-- Qual foi receita total em cada mes?

SELECT
    d.ano,
    d.mes,
    SUM(f.valorTotal) AS receitaTotal
FROM
    Fato_Locacao f
JOIN
    Dim_Tempo d ON f.dataLocacao = d.data
GROUP BY
    d.ano,
    d.mes
ORDER BY
    d.ano,
    d.mes;

-- Quais dias da semana há mais locações:

SELECT 
    dt.diaSemana,
    COUNT(l.idLocacao) AS TotalLocacoes
FROM Fato_Locacao AS l
JOIN Dim_Tempo AS dt ON l.dataLocacao = dt.data
GROUP BY dt.diaSemana
ORDER BY dt.diaSemana;

-- Quantidade de locações por hora do dia

SELECT 
    dh.hora,
    COUNT(f.idLocacao) AS total_locacoes
FROM Fato_Locacao f
JOIN Dim_Horario dh ON strftime('%H', f.horaLocacao) = dh.hora
GROUP BY dh.hora
ORDER BY total_locacoes DESC;


