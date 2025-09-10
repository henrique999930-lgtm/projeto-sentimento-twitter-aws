# Importa as bibliotecas necessárias
import os
import sys
import tweepy
import boto3          # SDK da AWS para Python
import json           # Para formatar os dados em JSON
from datetime import datetime

# --- ÁREA DE CARREGAMENTO DE CREDENCIAIS ---
print("Carregando credenciais do ambiente...")
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
if not bearer_token:
    print("ERRO: A variável de ambiente 'TWITTER_BEARER_TOKEN' não foi encontrada.")
    sys.exit(1)
print(">>> Sucesso! Chave 'Bearer Token' carregada.")


# --- CONEXÃO COM A API DO TWITTER (v2) ---
print("\nConectando à API do Twitter...")
try:
    client = tweepy.Client(bearer_token)
    print(">>> Conexão bem-sucedida!")
except Exception as e:
    print(f"ERRO: Falha ao conectar na API. Detalhes: {e}")
    sys.exit(1)


# --- EXECUÇÃO DA BUSCA POR TWEETS ---
query = '"Inteligência Artificial" -is:retweet lang:pt'
print(f"\nBuscando tweets com o termo: {query}")
try:
    response = client.search_recent_tweets(
        query=query, max_results=10, tweet_fields=["created_at", "text", "lang"]
    )
    tweets = response.data
    if not tweets:
        print(">>> Nenhum tweet encontrado para a busca recente.")
        sys.exit(0)
except Exception as e:
    print(f"ERRO: Falha ao buscar tweets. Detalhes: {e}")
    sys.exit(1)

print(f"\n--- {len(tweets)} Tweets Coletados ---")


# --- PREPARAÇÃO E UPLOAD PARA O S3 ---

# Nome do seu bucket S3 (JÁ CONFIGURADO COM O QUE VOCÊ CRIOU)
BUCKET_NAME = "termometro-sentimento-henri-20250910" 

print(f"\nPreparando dados para salvar no S3 (Bucket: {BUCKET_NAME})...")

# Converte os objetos de tweet em um formato que pode ser salvo como JSON
tweets_data = []
for tweet in tweets:
    tweets_data.append({
        "id": tweet.id,
        "text": tweet.text,
        "created_at": tweet.created_at.isoformat(),
        "lang": tweet.lang
    })

# Gera um nome de arquivo único com base na data e hora atuais
now = datetime.now()
filename = f"tweets_{now.strftime('%Y%m%d_%H%M%S')}.json"

# Cria a estrutura de pastas particionada (padrão de Data Lake)
s3_key = f"raw/tweets/ano={now.year}/mes={now.month:02d}/dia={now.day:02d}/hora={now.hour:02d}/{filename}"

# Tenta fazer o upload para o S3
try:
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json.dumps(tweets_data, ensure_ascii=False, indent=4)
    )
    print(f">>> Sucesso! Arquivo '{filename}' salvo em 's3://{BUCKET_NAME}/{s3_key}'")
except Exception as e:
    print(f"ERRO: Falha ao fazer upload para o S3. Detalhes: {e}")
    sys.exit(1)

print("\n--- Fim da Coleta e Armazenamento ---")