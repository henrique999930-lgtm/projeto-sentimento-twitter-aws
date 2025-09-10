# 🌡️ Projeto: Termômetro de Sentimento da Web

## Visão Geral
Este projeto implementa um pipeline de dados ponta a ponta na nuvem AWS que captura tweets sobre "Inteligência Artificial", analisa o sentimento de cada um (Positivo, Negativo ou Neutro), e exibe os resultados em um dashboard interativo.

## Arquitetura do Pipeline
O fluxo de dados segue as melhores práticas de engenharia de dados moderna:

1.  **Coleta (Ingestão):** Um script Python (`ingestor.py`) utiliza a biblioteca Tweepy para buscar dados da API do X/Twitter em batch.
2.  **Armazenamento (Data Lake):** Os dados brutos são salvos em formato JSON em um Data Lake no AWS S3, com armazenamento particionado por data (ano/mes/dia/hora) para otimizar futuras consultas.
3.  **Processamento (ETL):** Um Job no AWS Glue executa um script PySpark que lê os dados brutos, aplica uma função de análise de sentimento com a biblioteca TextBlob, e salva os dados enriquecidos de volta no S3 em formato Parquet.
4.  **Visualização (Dashboard):** Uma aplicação web desenvolvida com Streamlit (`dashboard.py`) lê os dados processados do S3 e exibe os insights em gráficos e tabelas interativas.

## Stack de Tecnologias
* **Linguagem:** Python
* **Coleta:** Tweepy
* **Nuvem (Cloud):** AWS (S3, Glue, IAM)
* **Processamento de Big Data:** PySpark
* **Análise de Sentimento:** TextBlob
* **Dashboard (Visualização):** Streamlit, Pandas, Plotly

## Como Executar
1.  Configurar credenciais da AWS e do Twitter como variáveis de ambiente.
2.  Executar `ingestor.py` para coletar e armazenar os dados.
3.  Executar o Job do AWS Glue para processar os dados.
4.  Executar `streamlit run dashboard.py` para visualizar os resultados.