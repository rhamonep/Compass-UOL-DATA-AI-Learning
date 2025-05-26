/*
E10
A comissão de um vendedor é definida a partir de um percentual sobre o total de vendas (quantidade * valor unitário) por ele realizado. 
O percentual de comissão de cada vendedor está armazenado na coluna perccomissao, tabela tbvendedor. 
Com base em tais informações, calcule a comissão de todos os vendedores, considerando todas as vendas armazenadas na base de dados com status concluído.
As colunas presentes no resultado devem ser vendedor, valor_total_vendas e comissao. O valor de comissão deve ser apresentado em ordem decrescente arredondado na segunda casa decimal.
*/

WITH TotalVendas AS (
    SELECT cdvdd,
    SUM(qtd * vrunt) AS qtdTotal
    
    FROM TBVENDAS
        
    WHERE status = 'Concluído'
    GROUP BY cdvdd
)

SELECT vddr.nmvdd AS vendedor,
    ttvnda.qtdTotal AS valor_total_vendas,
    ROUND(ttvnda.qtdTotal * vddr.perccomissao / 100, 2) AS comissao
    
FROM TBVENDEDOR AS vddr
JOIN TotalVendas AS ttvnda
    ON vddr.cdvdd = ttvnda.cdvdd
    
ORDER BY comissao DESC