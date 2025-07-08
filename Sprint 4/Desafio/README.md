# Etapas

1. [Etapa I - Criação do bucket, definição das análises e upload do csv](./Arquivos/etapa1.ipynb)

2. [Etapa II - Manipulações, execução das analises e upload de resultados](./Arquivos/etapa2.ipynb)


# Desafio apresentado

O desafio consiste em trabalhar com dados públicos utilizando os serviços da AWS, com foco no armazenamento e processamento de arquivos diretamente a partir do Amazon S3. O participante deve escolher um conjunto de dados único disponível no portal de dados abertos do Governo Brasileiro, realizar tres análises definidas por ele e aplicar transformações específicas com o uso de bibliotecas como pandas, polars.

A solução será dividida em duas etapas principais, desenvolvidas em Notebooks: o primeiro será responsável por enviar o arquivo ao S3, com a utilização da biblioteca boto3, enquanto o segundo realizará as análises e transformações diretamente sobre o arquivo armazenado. Durante o processo, devem ser aplicadas operações como filtragem lógica, agregações, manipulações condicionais, conversões de tipo, datas e strings. O arquivo resultante da análise deve ser salvo de volta no mesmo bucket, sem que o arquivo local seja reutilizado após o envio inicial.



## Etapa I - Criação do bucket, definição das análises e upload do csv

Abertura do preview do CSV para visualização dos dados para elaboração das análises.

![Captura de tela 2025-07-07 214923](../Evidencias/Captura%20de%20tela%202025-07-07%20214923.png)


![Captura de tela 2025-07-07 215049](../Evidencias/Captura%20de%20tela%202025-07-07%20215049.png)

![Captura de tela 2025-07-07 215053](../Evidencias/Captura%20de%20tela%202025-07-07%20215053.png)

![Captura de tela 2025-07-07 215111](../Evidencias/Captura%20de%20tela%202025-07-07%20215111.png)

![Captura de tela 2025-07-07 215115](../Evidencias/Captura%20de%20tela%202025-07-07%20215115.png)

![Captura de tela 2025-07-07 215149](../Evidencias/Captura%20de%20tela%202025-07-07%20215149.png)

![Captura de tela 2025-07-07 215201](../Evidencias/Captura%20de%20tela%202025-07-07%20215201.png)

![Captura de tela 2025-07-07 222027](../Evidencias/Captura%20de%20tela%202025-07-07%20222027.png)

![Captura de tela 2025-07-07 215310](../Evidencias/Captura%20de%20tela%202025-07-07%20215310.png)

![Captura de tela 2025-07-07 215336](../Evidencias/Captura%20de%20tela%202025-07-07%20215336.png)

![Captura de tela 2025-07-07 215515](../Evidencias/Captura%20de%20tela%202025-07-07%20215515.png)


![Captura de tela 2025-07-07 215537](../Evidencias/Captura%20de%20tela%202025-07-07%20215537.png)

![Captura de tela 2025-07-07 215547](../Evidencias/Captura%20de%20tela%202025-07-07%20215547.png)

![Captura de tela 2025-07-07 215556](../Evidencias/Captura%20de%20tela%202025-07-07%20215556.png)

![Captura de tela 2025-07-07 215603](../Evidencias/Captura%20de%20tela%202025-07-07%20215603.png)

![Captura de tela 2025-07-07 215615](../Evidencias/Captura%20de%20tela%202025-07-07%20215615.png)

---

## Etapa II - Manipulações, execução das analises e upload de resultados

---

![Captura de tela 2025-07-07 215637](../Evidencias/Captura%20de%20tela%202025-07-07%20215637.png)

![Captura de tela 2025-07-07 215653](../Evidencias/Captura%20de%20tela%202025-07-07%20215653.png)

![Captura de tela 2025-07-07 215716](../Evidencias/Captura%20de%20tela%202025-07-07%20215716.png)

![Captura de tela 2025-07-07 215752](../Evidencias/Captura%20de%20tela%202025-07-07%20215752.png)

![Captura de tela 2025-07-07 215803](../Evidencias/Captura%20de%20tela%202025-07-07%20215803.png)

![Captura de tela 2025-07-07 215813](../Evidencias/Captura%20de%20tela%202025-07-07%20215813.png)

![Captura de tela 2025-07-07 215825](../Evidencias/Captura%20de%20tela%202025-07-07%20215825.png)

![Captura de tela 2025-07-07 215842](../Evidencias/Captura%20de%20tela%202025-07-07%20215842.png)

![Captura de tela 2025-07-07 215852](../Evidencias/Captura%20de%20tela%202025-07-07%20215852.png)

![Captura de tela 2025-07-07 215904](../Evidencias/Captura%20de%20tela%202025-07-07%20215904.png)

![Captura de tela 2025-07-07 215912](../Evidencias/Captura%20de%20tela%202025-07-07%20215912.png)

![Captura de tela 2025-07-07 215922](../Evidencias/Captura%20de%20tela%202025-07-07%20215922.png)

![Captura de tela 2025-07-07 215931](../Evidencias/Captura%20de%20tela%202025-07-07%20215931.png)

![Captura de tela 2025-07-07 215953](../Evidencias/Captura%20de%20tela%202025-07-07%20215953.png)

![Captura de tela 2025-07-07 220020](../Evidencias/Captura%20de%20tela%202025-07-07%20220020.png)

![Captura de tela 2025-07-07 220030](../Evidencias/Captura%20de%20tela%202025-07-07%20220030.png)

![Captura de tela 2025-07-07 220048](../Evidencias/Captura%20de%20tela%202025-07-07%20220048.png)

![Captura de tela 2025-07-07 220055](../Evidencias/Captura%20de%20tela%202025-07-07%20220055.png)

![Captura de tela 2025-07-07 220103](../Evidencias/Captura%20de%20tela%202025-07-07%20220103.png)

![Captura de tela 2025-07-07 220116](../Evidencias/Captura%20de%20tela%202025-07-07%20220116.png)

![Captura de tela 2025-07-07 220124](../Evidencias/Captura%20de%20tela%202025-07-07%20220124.png)

![Captura de tela 2025-07-07 220130](../Evidencias/Captura%20de%20tela%202025-07-07%20220130.png)

![Captura de tela 2025-07-07 220135](../Evidencias/Captura%20de%20tela%202025-07-07%20220135.png)

![Captura de tela 2025-07-07 220149](../Evidencias/Captura%20de%20tela%202025-07-07%20220149.png)

![Captura de tela 2025-07-07 220156](../Evidencias/Captura%20de%20tela%202025-07-07%20220156.png)

![Captura de tela 2025-07-07 220222](../Evidencias/Captura%20de%20tela%202025-07-07%20220222.png)

![Captura de tela 2025-07-07 220228](../Evidencias/Captura%20de%20tela%202025-07-07%20220228.png)

![Captura de tela 2025-07-07 220249](../Evidencias/Captura%20de%20tela%202025-07-07%20220249.png)

![Captura de tela 2025-07-07 220258](../Evidencias/Captura%20de%20tela%202025-07-07%20220258.png)

![Captura de tela 2025-07-07 220304](../Evidencias/Captura%20de%20tela%202025-07-07%20220304.png)

![Captura de tela 2025-07-07 220307](../Evidencias/Captura%20de%20tela%202025-07-07%20220307.png)

![Captura de tela 2025-07-07 220317](../Evidencias/Captura%20de%20tela%202025-07-07%20220317.png)

![Captura de tela 2025-07-07 220324](../Evidencias/Captura%20de%20tela%202025-07-07%20220324.png)

![Captura de tela 2025-07-07 220337](../Evidencias/Captura%20de%20tela%202025-07-07%20220337.png)

![Captura de tela 2025-07-07 220345](../Evidencias/Captura%20de%20tela%202025-07-07%20220345.png)

![Captura de tela 2025-07-07 220349](../Evidencias/Captura%20de%20tela%202025-07-07%20220349.png)

![Captura de tela 2025-07-07 220404](../Evidencias/Captura%20de%20tela%202025-07-07%20220404.png)

![Captura de tela 2025-07-07 220408](../Evidencias/Captura%20de%20tela%202025-07-07%20220408.png)

![Captura de tela 2025-07-07 220413](../Evidencias/Captura%20de%20tela%202025-07-07%20220413.png)


