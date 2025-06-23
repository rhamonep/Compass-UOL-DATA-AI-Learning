# Resumo

- Nesta sprint, os estudos foram voltados para **Docker** e **AWS**, tecnologias fundamentais no desenvolvimento e na implantação de aplicações modernas em ambientes reais.

- Com os conhecimentos de Docker e AWS, foi possível entender como empacotar aplicações localmente e também como prepará-las para rodar em ambientes de produção na nuvem

## Docker

- Começamos com o **Docker**, entendendo o que são containers, imagens, volumes e redes, além de como essas ferramentas ajudam a criar ambientes leves, portáteis e padronizados.
- Na prática, aprendemos a **criar e gerenciar containers**, escrever nossos próprios **Dockerfiles** para gerar imagens personalizadas e usar volumes para salvar dados fora do container.
- Também exploramos como os containers se comunicam usando **redes Docker**, e como gerenciar vários serviços ao mesmo tempo com o **Docker Compose**, através de arquivos `.yml`.
- Além disso, vimos os primeiros conceitos de orquestração com **Docker Swarm** e **Kubernetes**, entendendo como escalar aplicações e manter tudo funcionando em conjunto.

## AWS

- No curso *AWS Partner: Accreditation (Technical)*, tivemos uma visão geral da plataforma AWS e dos pilares do **Well-Architected Framework**, como segurança, desempenho e otimização de custos.
- Já no *AWS Technical Essentials*, conhecemos os principais serviços da AWS, como **EC2**, **S3**, **RDS**, **IAM**, **Lambda** e **VPC**, aprendendo a configurar e gerenciar recursos tanto pelo console quanto pela **AWS CLI**.
- Esses aprendizados deram uma boa base para trabalhar com aplicações em nuvem, desde a criação do ambiente até a implantação e escalabilidade com boas práticas.


# Desafio

- [Arquivos](./Desafio/Arquivos/)
- [README.MD](./Desafio/README.md)

# Exercícios



## Etapa 1

Construir uma imagem Docker a partir de um `Dockerfile` que executasse o script `carguru.py`.  

Após a criação, execute um container a partir da imagem criada.

### ENTREGÁVEIS

- [Carguru.py](./Exercicios/Etapa%201/carguru.py)
- [Dockerfile](./Exercicios/Etapa%201/Dockerfile)

## Etapa 2

Criar um novo script Python que implementa o algoritmo a seguir:

1. Receber uma string via input.

2. Gerar o hash da string por meio do algoritmo SHA-1.

3. Imprimir o hash em tela, utilizando o método hexdigest.

4. Retornar ao passo 1.

Criar uma imagem Docker chamada mascarar-dados que execute o script Python criado anteriormente.

Iniciar um container a partir da imagem, enviando algumas palavras para mascaramento.

### ENTREGÁVEIS

- [mascara-dados.py](./Exercicios/Etapa%202/mascara-dados.py)
- [Dockerfile](./Exercicios/Etapa%202/Dockerfile)

# Evidências

Aqui vão constar as evidências da execução com sucesso dos exercícios

## Etapa 1: carguru.py

Abaixo está a evidência do código sendo rodado localmente afim de verificar seu funcionamento:

![exec_local](./Exercicios/Evidencias/Etapa%201/exec_local.png)

Agora sendo criado a imagem e rodando no container:

![exec_docker](./Exercicios/Evidencias/Etapa%201/exec_docker.png)

## Etapa 2: mascara-dados

Abaixo está a evidência do código sendo rodado localmente afim de verificar seu funcionamento:

![exec_local](./Exercicios/Evidencias/Etapa%202/exec_local.png)

Agora sendo criado a imagem e rodando no container:

![exec_docker_1](./Exercicios/Evidencias/Etapa%202/exec_docker_1.png)

Pode-se ver a necessidade de rodar como terminal iterativo para receber entradas pelo teclado. Agora usando o -it:

![exec_docker_?](./Exercicios/Evidencias/Etapa%202/exec_docker_2.png)


# Certificados

### Certificado do AWS Technical Essentials

![AWS Technical Essentials](./Certificados/AWS%20Technical%20Essentials.png)

### Certificado do AWS Partner: Accreditation (Technical)

![AWS Partner: Accreditation (Technical)](./Certificados/AWS%20Partner%20Accreditation%20(Technical).png)

### Badge do AWS Partner: Accreditation (Technical)
Verificado em: [Credly](https://www.credly.com/badges/97a747f0-0a3f-45f0-ad96-6b8f1ff217d3)

![Badge](./Certificados/aws-partner-technical-accredited.png)

### Certificado do Data & Analytics - PB - AWS - 2/10

![UC-Data_Analytics](./Certificados/UC-Data_Analytics_PB_AWS_3_10.jpg)


