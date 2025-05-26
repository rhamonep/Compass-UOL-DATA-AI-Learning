------------- TABELAS -----------------

-- Tabela de Combustível
CREATE TABLE Combustivel (
    idCombustivel INTEGER PRIMARY KEY,
    tipo VARCHAR UNIQUE NOT NULL -- Tipo único de combustível
);

-- Tabela de Carros
CREATE TABLE Carro (
    idCarro INTEGER PRIMARY KEY,
    km INTEGER NOT NULL,
    chassi VARCHAR UNIQUE NOT NULL, --Pode ser chave alternativa já que identificador único
    marca VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL,
    ano INTEGER NOT NULL,
    idCombustivel INTEGER,
    FOREIGN KEY (idCombustivel) REFERENCES Combustivel(idCombustivel)
);

-- Tabela de Clientes
CREATE TABLE Cliente (
    idCliente INTEGER PRIMARY KEY,
    nome VARCHAR NOT NULL,
    cidade VARCHAR NOT NULL,
    estado VARCHAR NOT NULL,
    pais VARCHAR NOT NULL
);

-- Tabela de Vendedores
CREATE TABLE Vendedor (
    idVendedor INTEGER PRIMARY KEY,
    nome VARCHAR NOT NULL,
    sexo SMALLINT,
    estado VARCHAR NOT NULL
);

-- Tabela de Locações
CREATE TABLE Locacao (
    idLocacao INTEGER PRIMARY KEY,
    idCarro INTEGER,
    idCliente INTEGER,
    idVendedor INTEGER,
    dataLocacao DATE NOT NULL,
    horaLocacao TIME NOT NULL,
    dataEntrega DATE NOT NULL,
    horaEntrega TIME NOT NULL,
    qtdDiaria INTEGER NOT NULL,
    valorDiaria DECIMAL NOT NULL,
    valorTotal DECIMAL,
    FOREIGN KEY (idCarro) REFERENCES Carro(idCarro),
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
    FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);


------------- INSERÇÕES -----------------

-- Combustível
INSERT INTO Combustivel (idCombustivel, tipo)
SELECT DISTINCT idcombustivel, tipoCombustivel
FROM tb_locacao;

-- Carro
WITH MaiorKm as (
	SELECT 
		idCarro,
		MAX(KmCarro) as KmAtual   --Necessário encontrar a quilometragem atual do carro, logo, a maior quilometragem registrada.
	FROM tb_locacao
	GROUP BY idCarro
)
INSERT INTO Carro (idCarro, km, chassi, marca, modelo, ano, idCombustivel)
SELECT
    l.idCarro,
    km.kmAtual,
    l.classiCarro,
    l.marcaCarro,
    l.modeloCarro,
    l.anoCarro,
    l.idcombustivel
FROM tb_locacao as l
JOIN MaiorKm as km
	on l.idCarro = km.idCarro
GROUP BY l.idCarro

-- Cliente
INSERT INTO Cliente (idCliente, nome, cidade, estado, pais)
SELECT DISTINCT
    idCliente,
    nomeCliente,
    cidadeCliente,
    estadoCliente,
    paisCliente
FROM tb_locacao;

-- Vendedor
INSERT INTO Vendedor (idVendedor, nome, sexo, estado)
SELECT DISTINCT
    idVendedor,
    nomeVendedor,
    sexoVendedor,
    estadoVendedor
FROM tb_locacao;

-- Locação
WITH DataFormatada as(        --O formato atual da data não esta no formato padrão para uso do strftime(). Necessário fazer a extração e formatação.
	SELECT 
		idLocacao,
		substr(dataLocacao, 1, 4) || '-' || substr(dataLocacao, 5, 2) || '-' || substr(dataLocacao, 7, 2) as dataLocacaoFormatado, 
		substr(dataEntrega, 1, 4) || '-' || substr(dataEntrega, 5, 2) || '-' || substr(dataEntrega, 7, 2) as dataEntregaFormatado
	FROM tb_locacao   	
),
HoraFormatada as(  -- o formato atual da hora tambem não esta no formato para uso no strfime(). Se as horas tiverem apenas um digito, o comando não reconhece e retorna NULL.
	SELECT
		idLocacao,
		printf('%02d:%02d',
        	CAST(substr(horaLocacao, 1, instr(horaLocacao, ':') - 1) AS INTEGER),  -- instr retorna a posicao da primeira ocorrecao do caractere : para extrair os digitos das horas, podendo ter 2 digitos ou 1.
        																		   -- com o substr é extraido o valor equivalente a hora e convertido com CAST para um inteiro, para horas e minutos. Então, é formatado usando printf forçando o 0 no caso de 1 digito.
       		CAST(substr(horaLocacao, instr(horaLocacao, ':') + 1) AS INTEGER)) AS horaLocacaoFormatada,
    	printf('%02d:%02d',
        	CAST(substr(horaEntrega, 1, instr(horaEntrega, ':') - 1) AS INTEGER),
        	CAST(substr(horaEntrega, instr(horaEntrega, ':') + 1) AS INTEGER)) AS horaEntregaFormatada
    FROM tb_locacao
)
INSERT INTO Locacao (
    idLocacao,
    idCarro,
    idCliente,
    idVendedor,
    dataLocacao,
    horaLocacao,
    dataEntrega,
    horaEntrega,
    qtdDiaria,
    valorDiaria,
    valorTotal
)
SELECT
    l.idLocacao,
    l.idCarro,
    l.idCliente,
    l.idVendedor,
    d.dataLocacaoFormatado,
    h.horaLocacaoFormatada,
	d.dataEntregaFormatado,
    h.horaEntregaFormatada,
    l.qtdDiaria,
    l.vlrDiaria,
    l.qtdDiaria * vlrDiaria
FROM tb_locacao as l
JOIN DataFormatada as d
	on l.idLocacao = d.idLocacao
JOIN HoraFormatada as h
	on l.idLocacao = h.idLocacao;

------------- CONSULTAS -----------------

select * FROM Carro

Select * FROM Cliente

select * FROM Vendedor

SELECT * FROM Locacao

SELECT * FROM Combustivel