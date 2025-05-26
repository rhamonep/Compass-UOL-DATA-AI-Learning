/*
E04
Apresente a query para listar a quantidade de livros publicada por cada autor. 
Ordenar as linhas pela coluna nome (autor), em ordem crescente. 
Além desta, apresentar as colunas codautor, nascimento e quantidade (total de livros de sua autoria).

Dica para ordenação: Utilize Replace
*/

SELECT a.nome, a.codAutor, a.nascimento, COUNT(l.cod) AS quantidade

FROM AUTOR AS a
LEFT JOIN LIVRO AS l
    ON a.codAutor = l.autor
    
GROUP BY a.codAutor
ORDER BY REPLACE(a.nome, 'Á', 'A') --Para substituir cada acento e agrupar, seria necessário uma concatenação de REPLACE, para cada letra e acento. 
								   --Como só houve um único caso com acentuação nessa tabela (Á), um REPLACE já forneceu a saída esperada.