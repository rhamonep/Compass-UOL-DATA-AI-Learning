/*
E03
 Apresente a query para listar as 5 editoras com mais livros na biblioteca. 
 O resultado deve conter apenas as colunas quantidade, nome, estado e cidade. 
 Ordenar as linhas pela coluna que representa a quantidade de livros em ordem decrescente.
*/

SELECT COUNT(l.cod) AS quantidade, ed.nome, end.estado, end.cidade

FROM LIVRO AS l
JOIN EDITORA AS ed
    ON l.editora = ed.codEditora
JOIN ENDERECO AS end
    ON ed.endereco = end.codEndereco
    
GROUP BY ed.nome, end.estado, end.cidade
ORDER BY quantidade DESC
LIMIT 5