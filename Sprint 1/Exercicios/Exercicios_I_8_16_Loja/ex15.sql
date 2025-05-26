/*
E15
Apresente a query para listar os códigos das vendas identificadas como deletadas. Apresente o resultado em ordem crescente.
*/

SELECT cdven

FROM TBVENDAS

WHERE deletado is '1'
ORDER BY cdven