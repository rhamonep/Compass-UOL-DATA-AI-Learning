/*
E05
Apresente a query para listar o nome dos autores que publicaram livros através de editoras NÃO situadas na região sul do Brasil. 
Ordene o resultado pela coluna nome, em ordem crescente. 
Não podem haver nomes repetidos em seu retorno.
*/

SELECT DISTINCT a.nome

FROM AUTOR AS a
JOIN LIVRO AS l
    ON a.codAutor = l.autor
JOIN EDITORA AS ed
    ON ed.codEditora = l.editora
JOIN ENDERECO AS end
    ON ed.endereco = end.codEndereco
    
WHERE end.estado NOT IN ('PARANÁ', 'SANTA CATARINA', 'RIO GRANDE DO SUL')
GROUP BY a.nome
ORDER BY a.nome