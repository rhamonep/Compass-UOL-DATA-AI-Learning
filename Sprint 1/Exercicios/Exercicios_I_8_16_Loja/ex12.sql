/*
E12
Apresente a query para listar código, nome e data de nascimento dos dependentes do vendedor com menor valor total bruto em vendas (não sendo zero). 
As colunas presentes no resultado devem ser cddep, nmdep, dtnasc e valor_total_vendas.
Observação: Apenas vendas com status concluído.
*/

WITH TotalVendas as (

    SELECT cdvdd,
    SUM(qtd * vrunt) as qtdTotal
    
    FROM TBVENDAS
        
    WHERE status = 'Concluído'
    GROUP by cdvdd
    HAVING SUM(qtd * vrunt) > 0
),
MenorVendedor as (

    SELECT cdvdd, 
        qtdTotal
        
    FROM TotalVendas
    
    ORDER BY qtdTotal
    LIMIT 1
)
SELECT dpd.cddep,
    dpd.nmdep,
    dpd.dtnasc,
    menVddr.qtdTotal AS valor_total_vendas
    
FROM TBDEPENDENTE AS dpd
JOIN MenorVendedor AS menVddr
    ON dpd.cdvdd = menVddr.cdvdd