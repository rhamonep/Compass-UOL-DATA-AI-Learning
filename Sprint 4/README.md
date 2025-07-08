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

![Captura de tela 2025-07-07 112728](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112728.png)

![Captura de tela 2025-07-07 112741](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112741.png)

![Captura de tela 2025-07-07 112758](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112758.png)

![Captura de tela 2025-07-07 112804](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112804.png)

![Captura de tela 2025-07-07 112839](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112839.png)

![Captura de tela 2025-07-07 112844](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112844.png)

![Captura de tela 2025-07-07 112858](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112858.png)

![Captura de tela 2025-07-07 112918](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112918.png)

![Captura de tela 2025-07-07 112944](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20112944.png)

![Captura de tela 2025-07-07 113032](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113032.png)

![Captura de tela 2025-07-07 113042](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113042.png)

![Captura de tela 2025-07-07 113059](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113059.png)

![Captura de tela 2025-07-07 113141](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113141.png)

![Captura de tela 2025-07-07 113150](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113150.png)

![Captura de tela 2025-07-07 113157](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113157.png)

![Captura de tela 2025-07-07 113209](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113209.png)

![Captura de tela 2025-07-07 113311](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113311.png)

![Captura de tela 2025-07-07 113333](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113333.png)

![Captura de tela 2025-07-07 113425](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113425.png)

![Captura de tela 2025-07-07 113444](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113444.png)

![Captura de tela 2025-07-07 113613](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113613.png)

![Captura de tela 2025-07-07 113657](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113657.png)

![Captura de tela 2025-07-07 113750](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113750.png)

![Captura de tela 2025-07-07 113906](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20113906.png)

![Captura de tela 2025-07-07 114002](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20114002.png)

![Captura de tela 2025-07-07 114014](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20114014.png)

![Captura de tela 2025-07-07 114034](./Exercicios/Lab%20AWS%20S3/Captura%20de%20tela%202025-07-07%20114034.png)


## Etapa 2 - Lab AWS Athena


![Captura de tela 2025-07-07 114227](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114227.png)

![Captura de tela 2025-07-07 114306](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114306.png)

![Captura de tela 2025-07-07 114338](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114338.png)

![Captura de tela 2025-07-07 114355](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114355.png)

![Captura de tela 2025-07-07 114420](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114420.png)

![Captura de tela 2025-07-07 114427](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114427.png)

![Captura de tela 2025-07-07 114452](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114452.png)

![Captura de tela 2025-07-07 114501](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114501.png)

![Captura de tela 2025-07-07 114816](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114816.png)

![Captura de tela 2025-07-07 114855](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114855.png)

![Captura de tela 2025-07-07 114904](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20114904.png)

![Captura de tela 2025-07-07 115331](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20115331.png)

![Captura de tela 2025-07-07 115342](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20115342.png)

![Captura de tela 2025-07-07 115347](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20115347.png)

![Captura de tela 2025-07-07 115351](./Exercicios/Lab%20AWS%20Athena/Captura%20de%20tela%202025-07-07%20115351.png)

## Etapa 3 - Lab AWS Lambda

# Evidências do Lab AWS Lambda

![Captura de tela 2025-07-07 115501](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115501.png)

![Captura de tela 2025-07-07 115517](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115517.png)

![Captura de tela 2025-07-07 115548](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115548.png)

![Captura de tela 2025-07-07 115636](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115636.png)

![Captura de tela 2025-07-07 115657](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115657.png)

![Captura de tela 2025-07-07 115705](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115705.png)

![Captura de tela 2025-07-07 115736](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115736.png)

![Captura de tela 2025-07-07 115741](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115741.png)

![Captura de tela 2025-07-07 115755](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20115755.png)

![Captura de tela 2025-07-07 120020](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120020.png)

![Captura de tela 2025-07-07 120031](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120031.png)

![Captura de tela 2025-07-07 120103](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120103.png)

![Captura de tela 2025-07-07 120139](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120139.png)

![Captura de tela 2025-07-07 120145](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120145.png)

![Captura de tela 2025-07-07 120154](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120154.png)

![Captura de tela 2025-07-07 120251](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120251.png)

![Captura de tela 2025-07-07 120322](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120322.png)

![Captura de tela 2025-07-07 120341](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120341.png)

![Captura de tela 2025-07-07 120406](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120406.png)

![Captura de tela 2025-07-07 120422](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120422.png)

![Captura de tela 2025-07-07 120450](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120450.png)

![Captura de tela 2025-07-07 120541](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120541.png)

![Captura de tela 2025-07-07 120738](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120738.png)

![Captura de tela 2025-07-07 120749](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120749.png)

![Captura de tela 2025-07-07 120754](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120754.png)

![Captura de tela 2025-07-07 120917](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120917.png)

![Captura de tela 2025-07-07 120935](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120935.png)

![Captura de tela 2025-07-07 120958](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20120958.png)

![Captura de tela 2025-07-07 121030](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121030.png)

![Captura de tela 2025-07-07 121103](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121103.png)

![Captura de tela 2025-07-07 121142](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121142.png)

![Captura de tela 2025-07-07 121220](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121220.png)

![Captura de tela 2025-07-07 121305](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121305.png)

![Captura de tela 2025-07-07 121321](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121321.png)

![Captura de tela 2025-07-07 121558](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121558.png)

![Captura de tela 2025-07-07 121619](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121619.png)

![Captura de tela 2025-07-07 121421](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121421.png)

![Captura de tela 2025-07-07 121439](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121439.png)

![Captura de tela 2025-07-07 121455](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121455.png)

![Captura de tela 2025-07-07 121705](./Exercicios/Lab%20AWS%20Lambda/Captura%20de%20tela%202025-07-07%20121705.png)


## Etapa 4 - Limpeza de Recursos

![Captura de tela 2025-07-07 121734](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121734.png)

![Captura de tela 2025-07-07 121739](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121739.png)

![Captura de tela 2025-07-07 121807](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121807.png)

![Captura de tela 2025-07-07 121844](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121844.png)

![Captura de tela 2025-07-07 121906](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121906.png)

![Captura de tela 2025-07-07 121938](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121938.png)

![Captura de tela 2025-07-07 121958](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20121958.png)

![Captura de tela 2025-07-07 122013](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20122013.png)

![Captura de tela 2025-07-07 122019](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20122019.png)

![Captura de tela 2025-07-07 122035](./Exercicios/Lab%20AWS%20Limpeza%20de%20Recursos/Captura%20de%20tela%202025-07-07%20122035.png)


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
