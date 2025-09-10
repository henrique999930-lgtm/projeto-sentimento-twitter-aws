import streamlit as st
import pandas as pd
import boto3
import pyarrow.parquet as pq
from io import BytesIO
import plotly.express as px

# --- Configurações da Página ---
st.set_page_config(
    page_title="Termômetro de Sentimento da Web",
    page_icon="🌡️",
    layout="wide"
)

# --- Constantes ---
BUCKET_NAME = "termometro-sentimento-henri-20250910"  # O nome do seu bucket S3
S3_PROCESSED_PREFIX = "processed_sentimento/tweets/"   # A pasta onde estão os dados analisados

# --- Funções de Acesso ao S3 (A Mágica Acontece Aqui) ---

# Cacheia a conexão com o S3 para não reconectar a cada interação
@st.cache_resource
def get_s3_client():
    return boto3.client('s3')

# Cacheia os dados para não precisar baixar do S3 toda hora
@st.cache_data(ttl=900) # Atualiza a cada 15 minutos (900 segundos)
def load_latest_data_from_s3(_s3_client):
    """Navega no S3 para encontrar e carregar os dados da última partição."""
    paginator = _s3_client.get_paginator('list_objects_v2')
    
    # Encontra a última pasta de 'ano'
    anos = paginator.paginate(Bucket=BUCKET_NAME, Prefix=S3_PROCESSED_PREFIX, Delimiter='/')
    latest_ano = max([p['Prefix'] for p in anos.search('CommonPrefixes')])
    
    # Encontra a última pasta de 'mes'
    meses = paginator.paginate(Bucket=BUCKET_NAME, Prefix=latest_ano, Delimiter='/')
    latest_mes = max([p['Prefix'] for p in meses.search('CommonPrefixes')])
    
    # Encontra a última pasta de 'dia'
    dias = paginator.paginate(Bucket=BUCKET_NAME, Prefix=latest_mes, Delimiter='/')
    latest_dia = max([p['Prefix'] for p in dias.search('CommonPrefixes')])
    
    # Encontra a última pasta de 'hora'
    horas = paginator.paginate(Bucket=BUCKET_NAME, Prefix=latest_dia, Delimiter='/')
    latest_hora_prefix = max([p['Prefix'] for p in horas.search('CommonPrefixes')])
    
    st.info(f"Carregando dados da última execução encontrada: {latest_hora_prefix.replace(S3_PROCESSED_PREFIX, '')}")
    
    # Lista e carrega todos os arquivos Parquet da última pasta
    response = _s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=latest_hora_prefix)
    
    all_dfs = []
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('.parquet'):
                s3_object = _s3_client.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                parquet_file = BytesIO(s3_object['Body'].read())
                df = pd.read_parquet(parquet_file)
                all_dfs.append(df)
        
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)
            
    return pd.DataFrame() # Retorna DataFrame vazio se não encontrar nada

# --- Construção do Dashboard ---

st.title("🌡️ Termômetro de Sentimento da Web")
st.markdown("Dashboard com a análise de sentimento de tweets sobre 'Inteligência Artificial'.")

s3_client = get_s3_client()
df = load_latest_data_from_s3(s3_client)

if not df.empty:
    # --- Métricas Principais ---
    total_tweets = len(df)
    st.metric(label="Total de Tweets Analisados", value=total_tweets)
    
    sentiment_counts = df['sentimento'].value_counts().reset_index()
    sentiment_counts.columns = ['sentimento', 'contagem']
    
    # --- Gráficos e Visualizações ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Sentimentos")
        fig_pie = px.pie(sentiment_counts, names='sentimento', values='contagem', 
                         color='sentimento',
                         color_discrete_map={
                             'POSITIVO': 'green',
                             'NEGATIVO': 'red',
                             'NEUTRO': 'royalblue'
                         })
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        st.subheader("Contagem por Sentimento")
        st.dataframe(sentiment_counts, use_container_width=True)

    # --- Tabela de Dados ---
    st.subheader("Amostra dos Tweets Analisados")
    st.dataframe(df[['text', 'sentimento']], use_container_width=True)

else:
    st.warning("Nenhum dado encontrado no S3. Execute o pipeline de ingestão e processamento primeiro.")