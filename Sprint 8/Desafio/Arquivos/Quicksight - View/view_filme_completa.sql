-- View para unir fato_filme com todas as bridges (gênero, keyword, país)
-- Divide orcamento, receita e votos pela quantidade de repetições para evitar agregações incorretas

CREATE OR REPLACE VIEW view_filme_completa AS
WITH combinacoes_filme AS (
    -- Calcula o número total de combinações para cada filme
    -- (quantidade de gêneros × quantidade de keywords × quantidade de países)
    SELECT 
        f.id_filme,
        f.ano,
        f.mes,
        COUNT(DISTINCT bg.id_genero) AS qtd_generos,
        COUNT(DISTINCT bk.id_keyword) AS qtd_keywords, 
        COUNT(DISTINCT bp.id_pais_producao) AS qtd_paises,
        (COUNT(DISTINCT bg.id_genero) * 
         COUNT(DISTINCT bk.id_keyword) * 
         COUNT(DISTINCT bp.id_pais_producao)) AS fator_divisao
    FROM fato_filme f
    LEFT JOIN bridge_filme_genero bg 
        ON f.id_filme = bg.id_filme 
        AND f.ano = bg.ano 
        AND f.mes = bg.mes
    LEFT JOIN bridge_filme_keyword bk 
        ON f.id_filme = bk.id_filme 
        AND f.ano = bk.ano 
        AND f.mes = bk.mes
    LEFT JOIN bridge_filme_pais bp 
        ON f.id_filme = bp.id_filme 
        AND f.ano = bp.ano 
        AND f.mes = bp.mes
    GROUP BY f.id_filme, f.ano, f.mes
)

SELECT 
    -- Chaves primárias
    f.id_filme,
    f.id_tempo,
    bg.id_genero,
    bk.id_keyword,
    bp.id_pais_producao,
    
    -- Campos de particionamento
    f.ano,
    f.mes,
    
    -- Dimensões
    df.id_imdb,
    df.titulo_principal,
    dg.genero,
    dk.keyword,
    dp.pais_producao,
    dt.data_lancamento,
    dt.nome_mes,
    dt.trimestre,
    dt.decada,
    
    -- Métricas ajustadas (divididas pelo fator de repetição)
    CASE 
        WHEN cf.fator_divisao > 0 THEN f.receita / cf.fator_divisao
        ELSE f.receita
    END AS receita,
    
    CASE 
        WHEN cf.fator_divisao > 0 THEN f.orcamento / cf.fator_divisao
        ELSE f.orcamento
    END AS orcamento,
    
    CASE 
        WHEN cf.fator_divisao > 0 THEN CAST(f.numero_votos AS DOUBLE) / cf.fator_divisao
        ELSE CAST(f.numero_votos AS DOUBLE)
    END AS numero_votos,
    
    -- ROI - Return on Investment
    CASE 
        WHEN cf.fator_divisao > 0 AND f.orcamento > 0 AND f.receita > 0
        THEN ROUND(((f.receita / cf.fator_divisao) - (f.orcamento / cf.fator_divisao)) / (f.orcamento / cf.fator_divisao), 4)
        ELSE NULL 
    END AS roi,
    
    -- Fator de divisão aplicado (para verificação)
    cf.fator_divisao,
    
    -- Quantidades por filme
    cf.qtd_generos,
    cf.qtd_keywords,
    cf.qtd_paises,
    
    -- Métricas que não precisam de ajuste (são médias ou percentuais)
    f.nota_media,
    f.popularidade_tmdb,
    f.duracao_minutos

FROM fato_filme f

-- Joins com as dimensões
INNER JOIN dim_filme df ON f.id_filme = df.id_filme
INNER JOIN dim_tempo dt ON f.id_tempo = dt.id_tempo

-- Joins com as bridges (INNER JOIN para garantir que só filmes com todas as informações apareçam)
INNER JOIN bridge_filme_genero bg 
    ON f.id_filme = bg.id_filme 
    AND f.ano = bg.ano 
    AND f.mes = bg.mes

INNER JOIN bridge_filme_keyword bk 
    ON f.id_filme = bk.id_filme 
    AND f.ano = bk.ano 
    AND f.mes = bk.mes

INNER JOIN bridge_filme_pais bp 
    ON f.id_filme = bp.id_filme 
    AND f.ano = bp.ano 
    AND f.mes = bp.mes

-- Joins com as dimensões das bridges
INNER JOIN dim_genero dg ON bg.id_genero = dg.id_genero
INNER JOIN dim_keyword dk ON bk.id_keyword = dk.id_keyword
INNER JOIN dim_pais_producao dp ON bp.id_pais_producao = dp.id_pais_producao

-- Join com os fatores de divisão calculados
INNER JOIN combinacoes_filme cf 
    ON f.id_filme = cf.id_filme 
    AND f.ano = cf.ano 
    AND f.mes = cf.mes;
