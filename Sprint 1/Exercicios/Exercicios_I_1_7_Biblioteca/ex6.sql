/*
E06
Apresente a query para listar o autor com maior número de livros publicados. 
O resultado deve conter apenas as colunas codautor, nome, quantidade_publicacoes.
*/

SELECT a.codAutor, a.nome, COUNT(l.cod) AS quantidade_publicacoes

FROM AUTOR AS a
JOIN LIVRO AS l
    ON a.codAutor = l.autor
    
GROUP BY a.codAutor
ORDER BY quantidade_publicacoes DESC
LIMIT 1