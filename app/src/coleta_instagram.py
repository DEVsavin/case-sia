# app/src/coleta_instagram.py

import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClient

def buscar_mencoes_instagram(username: list, max_posts_por_perfil: int = 25):
    """
    Busca posts em que usuários específicos do Instagram foram mencionados ou marcados,
    usando o ator "apify/instagram-tagged-scraper".
    """
    load_dotenv()

    # --- Configuração do Cliente Apify ---
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("ERRO: O token da API da Apify (APIFY_API_TOKEN) não foi encontrado.")
        return pd.DataFrame()

    client = ApifyClient(api_token)

    # --- Ator correto para buscar menções e posts marcados ---
    actor_id = "apify/instagram-tagged-scraper"

    # --- O input correto, que exige uma lista de usernames ---
    run_input = {
        "username": username,
        "resultsLimit": max_posts_por_perfil
    }

    print(f"Iniciando a busca por menções e marcações para os perfis: {username}...")
    
    try:
        # Inicia a execução do ator e aguarda sua conclusão
        run = client.actor(actor_id).call(run_input=run_input)
        print("Coleta de dados concluída. Processando resultados...")

        # Coleta os resultados do dataset do ator
        items = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            items.append(item)
        
        if not items:
            print("Nenhum post encontrado para os perfis especificados.")
            return pd.DataFrame()

        # Converte a lista de dicionários para um DataFrame
        df = pd.DataFrame(items)
        
        # Remove duplicatas
        df.drop_duplicates(subset=['url'], inplace=True)
        
        # Seleciona e renomeia as colunas mais importantes
        colunas_relevantes = {
            'url': 'link_post',
            'caption': 'legenda',
            'timestamp': 'data_postagem',
            'likesCount': 'curtidas',
            'commentsCount': 'comentarios',
            'ownerUsername': 'usuario_do_post',
            'taggedUsers': 'usuarios_marcados'
        }
        
        colunas_existentes = [col for col in colunas_relevantes if col in df.columns]
        df_filtrado = df[colunas_existentes]
        df_renomeado = df_filtrado.rename(columns=colunas_relevantes)

        print(f"{len(df_renomeado)} posts únicos foram coletados.")
        return df_renomeado

    except Exception as e:
        print(f"Ocorreu um erro ao executar o ator da Apify: {e}")
        return pd.DataFrame()


# --- Bloco de Execução ---
if __name__ == '__main__':
    # Lista de perfis de interesse para buscar menções
    perfis_para_monitorar = ["sia.piaui"]
    
    df_instagram = buscar_mencoes_instagram(
        username=perfis_para_monitorar, 
        max_posts_por_perfil=50 # Aumentei o limite para ter mais chance de achar dados
    )

    if not df_instagram.empty:
        caminho_saida = os.path.join(os.path.dirname(__file__), '..', 'db', 'instagram_posts_mencoes.csv')
        df_instagram.to_csv(caminho_saida, index=False)
        print(f"\nDados de menções do Instagram salvos em '{caminho_saida}'")
        
        print("\nPré-visualização dos dados coletados:")
        print(df_instagram.head())