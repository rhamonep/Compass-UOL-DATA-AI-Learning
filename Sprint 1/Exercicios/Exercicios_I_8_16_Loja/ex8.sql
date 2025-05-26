/*
E08
Apresente a query para listar o código e o nome do vendedor com maior número de vendas (contagem), e que estas vendas estejam com o status concluída.  
As colunas presentes no resultado devem ser, portanto, cdvdd e nmvdd.
*/

SELECT vddr.cdvdd, vddr.nmvdd

FROM TBVENDEDOR AS vddr 
JOIN TBVENDAS AS vnda
    ON vddr.cdvdd = vnda.cdvdd
WHERE vnda.status = 'Concluído'
GROUP BY vddr.cdvdd
ORDER BY COUNT(vnda.cdven) DESC
LIMIT 1