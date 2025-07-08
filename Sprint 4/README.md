# Resumo

- Nesta semana, os estudos foram focados em três cursos da AWS Skill Builder, com o objetivo de entender melhor tanto a parte de negócios quanto a parte prática do uso da nuvem AWS.

- Os conteúdos mostraram como apresentar as soluções da AWS de forma clara para diferentes tipos de clientes, como destacar os benefícios financeiros de migrar para a nuvem, e ainda proporcionaram uma experiência prática e interativa sobre os principais serviços da AWS.

- Além disso, foi possível perceber como é importante ter uma visão completa, não só técnica, mas também estratégica, para atuar com soluções em nuvem, seja vendendo, planejando ou executando.

## AWS Partner: Sales Accreditation (Business)

- Esse curso foi voltado para a atuação na área comercial e precisa entender como posicionar a AWS como solução para os clientes.

- Foi possível aprender como mapear o momento atual de cada cliente (se estão iniciando ou já têm algum uso da nuvem), como apresentar as vantagens da AWS com base nas necessidades reais e como conduzir conversas mais estratégicas, focadas em valor de negócio e não apenas em tecnologia.

- Também foi reforçada a importância de alinhar as soluções da nuvem com os objetivos de cada empresa, mostrando como a AWS pode ajudar a atingir metas como inovação, redução de custos e crescimento sustentável.

## AWS Partner: Economias na nuvem AWS

- Esse curso mostrou como a AWS pode trazer economia para os clientes, especialmente quando comparada a ambientes locais (on-premises).

- Aprendemos a explicar de forma simples como funciona o modelo de pagamento por uso, e como isso pode ajudar empresas a gastarem apenas com o que realmente utilizam, evitando desperdícios.

- Também foram abordadas estratégias para otimizar custos usando escalabilidade automática, desligamento de recursos fora do horário de uso e migração de cargas para serviços gerenciados.

- Ferramentas como o AWS Pricing Calculator e estudos de caso ajudaram a visualizar melhor como apresentar esses ganhos aos clientes.

## AWS Cloud Quest: Cloud Practitioner

- Esse foi um curso mais dinâmico e prático, com uma proposta gamificada para aprender os conceitos básicos da nuvem AWS.

- Através de uma cidade virtual, assumimos o papel de um profissional de nuvem e resolvemos problemas de clientes simulados, o que ajudou a aplicar conceitos na prática.

- Foram abordados temas como computação, armazenamento, banco de dados, segurança e redes, sempre com foco em situações reais.

- Essa abordagem mais interativa ajudou a fixar melhor os serviços da AWS e entender como eles se encaixam no dia a dia de uma empresa que usa nuvem.

# Desafio

- [Arquivos](./Desafio/Arquivos/)
- [README.MD](./Desafio/README.md)

# Exercícios

## Etapa 1 - Lab AWS S3

Nessa etapa, criamos um bucket no Amazon S3 para hospedar um site estático. Configuramos o bucket para usar um arquivo index.html como página inicial e um arquivo 404.html para erros. Ajustamos as permissões do bucket, liberando o acesso público por meio do bloqueio de acesso e adicionando uma política que permite leitura pública dos arquivos. Em seguida, fizemos o upload do arquivo index.html e do CSV para o bucket, os organizando em pastas. Por fim, testamos o site acessando o endpoint gerado pelo S3, confirmando que o conteúdo está disponível online.

## Etapa 2 - Lab AWS Athena

Nessa etapa, usamos o AWS Athena para consultar dados armazenados no S3. Primeiro, verificamos se o arquivo nomes.csv estava no bucket criado, fazendo upload se necessário. Criamos uma pasta chamada queries para salvar os resultados das consultas. No Athena, configuramos esse bucket para armazenar os resultados e criamos um banco de dados chamado meubanco. Depois, construímos uma tabela externa baseada no arquivo CSV, definindo os tipos de dados e o formato correto para o Athena interpretar. Por fim, testamos a consulta para buscar dados específicos e criamos uma query para listar os 3 nomes mais usados por década desde 1950. 

## Etapa 3 - Lab AWS Lambda

Nesta etapa, criamos uma função Lambda em Python 3.9 para acessar um arquivo CSV no S3 e contar suas linhas usando as bibliotecas Pandas e Boto3. Como a Lambda não inclui Pandas por padrão, implementamos uma camada (Layer) para adicionar essa dependência. Utilizamos Docker com uma imagem Amazon Linux para instalar Pandas e suas dependências na estrutura correta (pasta python), compactamos tudo em um arquivo zip e copiamos para o ambiente local. Depois, enviamos esse arquivo para um bucket S3 e criamos a camada no console Lambda apontando para o zip no S3. Finalmente, vinculamos essa camada à função Lambda e executamos o teste com sucesso, retornando o número de linhas do arquivo CSV. Ajustes de memória e tempo de execução da função foram necessários para a execução com sucesso.

## Etapa 4 - Limpeza de Recursos

Após concluir os laboratórios e salvar todas as evidências/códigos no GitHub, realize a limpeza dos recursos criados para evitar custos desnecessários. Isso inclui, principalmente, excluir todos os arquivos usados ou gerados durante os laboratórios no bucket S3.

# Evidências

Aqui estão as capturas de tela que comprovam a execução do laboratório:

## Etapa 1: Lab AWS S3

![s3_1_s3](./Exercicios/Lab%20AWS%20S3/s3_1_s3.png)

![s3_2_criar_bucket](./Exercicios/Lab%20AWS%20S3/s3_2_criar_bucket.png)

![s3_3_nome_bucket](./Exercicios/Lab%20AWS%20S3/s3_3_nome_bucket.png)

![s3_4_regiao](./Exercicios/Lab%20AWS%20S3/s3_4_regiao.png)

![s3_5_nome_criado](./Exercicios/Lab%20AWS%20S3/s3_5_nome_criado.png)

![s3_6_propriedades](./Exercicios/Lab%20AWS%20S3/s3_6_propriedades.png)

![s3_7_site_estatico](./Exercicios/Lab%20AWS%20S3/s3_7_site_estatico.png)

![s3_8_ativar_hospedagem](./Exercicios/Lab%20AWS%20S3/s3_8_ativar_hospedagem.png)

![s3_9_tipo_hospedagem_index_html](./Exercicios/Lab%20AWS%20S3/s3_9_tipo_hospedagem_index_html.png)

![s3_10_error_html](./Exercicios/Lab%20AWS%20S3/s3_10_error_html.png)

![s3_11_save](./Exercicios/Lab%20AWS%20S3/s3_11_save.png)

![s3_12_endpoint](./Exercicios/Lab%20AWS%20S3/s3_12_endpoint.png)

![s3_13_permissioes](./Exercicios/Lab%20AWS%20S3/s3_13_permissioes.png)

![s3_14_bloquear_acesso](./Exercicios/Lab%20AWS%20S3/s3_14_bloquear_acesso.png)

![s3_15_desativar_bloqueio](./Exercicios/Lab%20AWS%20S3/s3_15_desativar_bloqueio.png)

![s3_17_politica_bucket](./Exercicios/Lab%20AWS%20S3/s3_17_politica_bucket.png)

![s3_18_salvar_politica](./Exercicios/Lab%20AWS%20S3/s3_18_salvar_politica.png)

![s3_19_index_html](./Exercicios/Lab%20AWS%20S3/s3_19_index_html.png)

![s3_20_index_html_codigo](./Exercicios/Lab%20AWS%20S3/s3_20_index_html_codigo.png)

![s3_21_upload_html_bucket_pasta_dados](./Exercicios/Lab%20AWS%20S3/s3_21_upload_html_bucket_pasta_dados.png)

![s3_22_upload_csv_dados](./Exercicios/Lab%20AWS%20S3/s3_22_upload_csv_dados.png)

![s3_23_404_html](./Exercicios/Lab%20AWS%20S3/s3_23_404_html.png)

![s3_24_upload_404](./Exercicios/Lab%20AWS%20S3/s3_24_upload_404.png)

![s3_25_rename_erro_html](./Exercicios/Lab%20AWS%20S3/s3_25_rename_erro_html.png)

![s3_26_resultado_final](./Exercicios/Lab%20AWS%20S3/s3_26_resultado_final.png)

![s3_27_teste_botao_download](./Exercicios/Lab%20AWS%20S3/s3_27_teste_botao_download.png)

## Etapa 2 - Lab AWS Athena

![athena_l_cabecalho_csv](./Exercicios/Lab%20AWS%20Athena/athena_1_cabecalho_csv.png)

![athena_2_queries_criacao](./Exercicios/Lab%20AWS%20Athena/athena_2_queries_criacao.png)

![athena_3_config](./Exercicios/Lab%20AWS%20Athena/athena_3_config.png)

![athena_4_browser](./Exercicios/Lab%20AWS%20Athena/athena_4_browser.png)

![athena_5_select_queries](./Exercicios/Lab%20AWS%20Athena/athena_5_select_queries.png)

![athena_6_local_consultas](./Exercicios/Lab%20AWS%20Athena/athena_6_local_consultas.png)

![athena_7_consulta1_criacao_db](./Exercicios/Lab%20AWS%20Athena/athena_7_consulta1_criacao_db.png)

![athena_8_dados](./Exercicios/Lab%20AWS%20Athena/athena_8_dados.png)

![athena_9_consulta2_tabela](./Exercicios/Lab%20AWS%20Athena/athena_9_consulta2_tabela.png)

![athena_10_consulta3_select_15](./Exercicios/Lab%20AWS%20Athena/athena_10_consulta3_select_15.png)

![athena_11_resultados_select_15](./Exercicios/Lab%20AWS%20Athena/athena_11_resultados_select_15.png)

![athena_12_consulta4_top3_decada](./Exercicios/Lab%20AWS%20Athena/athena_12_consulta4_top3_decada.png)

![athena_13_consulta4_concluido](./Exercicios/Lab%20AWS%20Athena/athena_13_consulta4_concluido.png)

![athena_14_consulta4_resultad01](./Exercicios/Lab%20AWS%20Athena/athena_14_consulta4_resultado1.png)

![athena_15_consulta4_resultad02](./Exercicios/Lab%20AWS%20Athena/athena_15_consulta4_resultado2.png)


## Etapa 3 - Lab AWS Lambda

![lambda_l_criar_func](./Exercicios/Lab%20AWS%20Lambda/lambda_1_criar_func.png)

![lambda_2_dozero](./Exercicios/Lab%20AWS%20Lambda/lambda_2_dozero.png)

![lambda_3_nome_arq](./Exercicios/Lab%20AWS%20Lambda/lambda_3_nome_arq.png)

![lambda_4_lambda_func](./Exercicios/Lab%20AWS%20Lambda/lambda_4_lambda_func.png)

![lambda_5_nossa_func](./Exercicios/Lab%20AWS%20Lambda/lambda_5_nossa_func.png)

![lambda_6_nossa_func_exito](./Exercicios/Lab%20AWS%20Lambda/lambda_6_nossa_func_exito.png)

![lambda_7_teste_criacao](./Exercicios/Lab%20AWS%20Lambda/lambda_7_teste_criacao.png)

![lambda_8_exito_teste_criacao](./Exercicios/Lab%20AWS%20Lambda/lambda_8_exito_teste_criacao.png)

![lambda_9_erro_module_missing](./Exercicios/Lab%20AWS%20Lambda/lambda_9_erro_module_missing.png)

![lambda_10_dockerfile_criacao](./Exercicios/Lab%20AWS%20Lambda/lambda_10_dockerfile_criacao.png)

![lambda_11_dockerfile_conteudo](./Exercicios/Lab%20AWS%20Lambda/lambda_11_dockerfile_conteudo.png)

![lambda_12_result](./Exercicios/Lab%20AWS%20Lambda/lambda_12_docker_comand1.png) 

![lambda_13_result](./Exercicios/Lab%20AWS%20Lambda/lambda_13_docker_comand1_result.png) 

![lambda_14_docker_comand2](./Exercicios/Lab%20AWS%20Lambda/lambda_14_docker_comand2.png)

![lambda_15_docker_comand2_result](./Exercicios/Lab%20AWS%20Lambda/lambda_15_docker_comand2_result.png)

![lambda_16_docker_comand3](./Exercicios/Lab%20AWS%20Lambda/lambda_16_docker_comand3.png)

![lambda_18_docker_comand4_result](./Exercicios/Lab%20AWS%20Lambda/lambda_18_docker_comand4_result.png)

![lambda_20_docker_comand4_pwd](./Exercicios/Lab%20AWS%20Lambda/lambda_20_docker_comand4_pwd.png)

![lambda_21_docker_comand5](./Exercicios/Lab%20AWS%20Lambda/lambda_21_docker_comand5.png)

![lambda_22_docker_container_ls](./Exercicios/Lab%20AWS%20Lambda/lambda_22_docker_container_ls.png)

![lambda_23_docker_zip](./Exercicios/Lab%20AWS%20Lambda/lambda_23_docker_zip.png)

![lambda_24_docker_zip_result](./Exercicios/Lab%20AWS%20Lambda/lambda_24_docker_zip_result.png)

![lambda_25_zip](./Exercicios/Lab%20AWS%20Lambda/lambda_25_zip.png)

![lambda_26_minha_camada](./Exercicios/Lab%20AWS%20Lambda/lambda_26_minha_camada.png)

![lambda_27_upload_bucket_minha_camada](./Exercicios/Lab%20AWS%20Lambda/lambda_27_upload_bucket_minha_camada.png)

![lambda_28_camadas_menu_slect](./Exercicios/Lab%20AWS%20Lambda/lambda_28_camadas_menu_slect.png)

![lambda_29_criar_camada](./Exercicios/Lab%20AWS%20Lambda/lambda_29_criar_camada.png)

![lambda_30_url_camada_zip](./Exercicios/Lab%20AWS%20Lambda/lambda_30_url_camada_zip.png)

![lambda_31_config_camada](./Exercicios/Lab%20AWS%20Lambda/lambda_31_config_camada.png)

![lambda_32_config_camada_exito](./Exercicios/Lab%20AWS%20Lambda/lambda_32_config_camada_exito.png)

![lambda_33_camadas_empty](./Exercicios/Lab%20AWS%20Lambda/lambda_33_camadas_empty.png)

![lambda_34_camada_adicionar](./Exercicios/Lab%20AWS%20Lambda/lambda_34_camada_adicionar.png)

![lambda_35_camada_configuracao_button](./Exercicios/Lab%20AWS%20Lambda/lambda_35_camada_configuracao_button.png)

![lambda_36_lambda_function_config](./Exercicios/Lab%20AWS%20Lambda/lambda_36_lambda_function_config.png)

![lambda_37_lambda_function_memory_time](./Exercicios/Lab%20AWS%20Lambda/lambda_37_lambda_function_memory_time.png)

![lambda_38_lambda_function_deploy](./Exercicios/Lab%20AWS%20Lambda/lambda_38_lambda_function_deploy.png)

![lambda_39_lambda_function_timeout](./Exercicios/Lab%20AWS%20Lambda/lambda_39_lambda_function_timeout.png)

![lambda_40_lambda_function_sucesso](./Exercicios/Lab%20AWS%20Lambda/lambda_40_lambda_function_sucesso.png)


## Etapa 4 - Limpeza de Recursos

![limpeza_l_excluir_func](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_10_excluir_bucket_exito.png)

![limpeza_2_excluir_func_confirm](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_2_excluir_func_confirm.png)

![limpeza_3_excluir_camada](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_3_excluir_camada.png)

![limpeza_4_drop_table](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_4_drop_table.png)

![limpeza_5_drop_database](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_5_drop_database.png)

![limpeza_6_excluir_bucket](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_6_excluir_bucket.png)

![limpeza_7_esvaziar_confirm](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_7_esvaziar_confirm.png)

![limpeza_8_excluir_bucket2](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_8_excluir_bucket2.png)

![limpeza_9_excluir_bucket_confirm](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_9_excluir_bucket_confirm.png)

![limpeza_10_excluir_bucket_exito](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/limpeza_10_excluir_bucket_exito.png)



# Certificados


---

### AWS Partner - Sales Accreditation (Business)  
![AWS Partner - Sales Accreditation (Business)](./Certificados/AWS%20Partner%20-%20Sales%20Accreditation%20(Business).png)

---

### AWS Partner - Cloud Economics  
![AWS Partner - Cloud Economics](./Certificados/AWS%20Partner%20-%20Cloud%20Economics.png)

---

### AWS Cloud Quest - Practitioner  
![AWS Cloud Quest - Practitioner](./Certificados/AWS%20Cloud%20Quest%20-%20Practitioner.png)

---

### Badges
Verificação em Credly: 
[Sales Accreditaton](https://www.credly.com/badges/370647c2-7627-452a-a4e1-7d6c391b0b18/public_url), 
[Cloud Economics](https://www.credly.com/badges/da79430d-b28e-4427-b1f6-42cdf1a91949/public_url),
[Cloud Practitioner](https://www.credly.com/badges/fd534686-7e6f-45d1-8641-cb1375fe7280/public_url)

---
<div style="display: flex; gap: 20px;">
    <img src="./Certificados/bagde%20-%20sales%20accreditation.png" alt="Badge - Cloud Quest" width="150" />
    <img src="./Certificados/badge%20-%20cloud%20economics.png" alt="Badge - Cloud Economics" width="150" />
    <img src="./Certificados/badge%20-%20cloud%20quest.png" alt="Badge - Cloud Quest" width="150" />
</div>

---

### Certificado do Data & Analytics - PB - AWS - 4/10 
![UC Certificate](./Certificados/UC-1b35cfaa-3343-404a-8ae9-26ae2a45971c.jpg)
