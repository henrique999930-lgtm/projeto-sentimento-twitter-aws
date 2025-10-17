# 🌡️ Projeto: Termômetro de Sentimento da Web

### **Uma solução de Engenharia de Dados ponta-a-ponta na nuvem AWS, que transforma o fluxo caótico de dados do Twitter em inteligência de mercado acionável e em tempo real.**

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Amazon%20AWS-Cloud%20Native-232F3E?style=for-the-badge&logo=amazon-aws" alt="AWS">
  <img src="https://img.shields.io/badge/Apache%20Spark-PySpark-E25A1C?style=for-the-badge&logo=apache-spark" alt="PySpark">
  <img src="https://img.shields.io/badge/Streamlit-Interactive%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
</p>

---

## 🎯 O Desafio de Negócio

No cenário digital atual, a opinião pública nas redes sociais é um ativo de valor inestimável, mas volátil e massivo. Empresas que conseguem capturar e analisar esse sentimento em tempo real ganham uma vantagem competitiva absurda. O desafio é: como construir um sistema escalável, automatizado e custo-efetivo para transformar milhões de tweets em insights claros e objetivos?

## 🏛️ Arquitetura da Solução

Este projeto implementa um pipeline de dados moderno e serverless na AWS, desenhado para máxima eficiência e escalabilidade. Cada etapa do fluxo foi construída com as melhores práticas de engenharia de dados, conforme ilustrado abaixo.

```mermaid
graph TD;
    subgraph "Fase 1: Coleta";
        A[<B>API do X/Twitter</B><br>Fonte de Dados Brutos];
    end
    subgraph "Fase 2: Armazenamento (Data Lake)";
        B[<B
