/*
E07
Apresente a query para listar o nome dos autores com nenhuma publicação. 
Apresentá-los em ordem crescente.
*/

SELECT a.nome

FROM AUTOR AS a
LEFT JOIN LIVRO AS l
    ON a.codAutor = l.autor
    
WHERE l.cod is NULL
GROUP BY a.codAutor



