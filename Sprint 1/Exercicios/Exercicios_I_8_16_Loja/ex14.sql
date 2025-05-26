/*
E14
Apresente a query para listar o gasto médio por estado da federação. 
As colunas presentes no resultado devem ser estado e gastomedio. 
Considere apresentar a coluna gastomedio arredondada na segunda casa decimal e ordenado de forma decrescente.
Observação: Apenas vendas com status concluído.
*/

WITH GastoPorEstado AS (
    SELECT estado,
        SUM(qtd * vrunt) AS totalGasto,
        COUNT(cdven) AS numVendas
        
    FROM TBVENDAS
    
    WHERE status = 'Concluído'
    GROUP BY estado
)

SELECT estado,
    ROUND((totalGasto*1.0) / numVendas, 2) AS gastomedio -- Por conta de ser uma divisão entre dois valores inteiros, o resultado estava sendo inteiro
														 -- Por isso foi necessário multipilicar por 1.0, para o resultado ser decimal e bater com o resultado esperado.
FROM GastoPorEstado
ORDER BY gastomedio DESC