# Dentro de coleta_dados.py

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re

def buscar_noticias_google_news(termo_pesquisa="Inteligência Artificial Piauí", max_resultados=15):
    """
    Busca notícias no feed RSS do Google Notícias para um termo de pesquisa.
    """
    # URL do feed RSS do Google Notícias
    url = f"https://news.google.com/rss/search?q={termo_pesquisa}&hl=pt-BR&gl=BR&ceid=BR:pt-419"

    try:
        # Faz a requisição HTTP
        response = requests.get(url)
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # Processa o XML
        root = ET.fromstring(response.content)
        noticias = []

        # Itera sobre os itens (notícias) no XML e extrai as informações
        for i, item in enumerate(root.findall('.//channel/item')):
            if i >= max_resultados:
                break

            titulo = item.find('title').text
            link = item.find('link').text
            descricao_html = item.find('description').text

            # Limpa tags HTML da descrição (será útil para a próxima etapa)
            descricao_limpa = re.sub('<.*?>', '', descricao_html) if descricao_html else ''

            noticias.append({
                'titulo': titulo,
                'link': link,
                'descricao': descricao_limpa
            })

        print(f"Coleta concluída! {len(noticias)} notícias encontradas.")
        return pd.DataFrame(noticias)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição HTTP: {e}")
        return pd.DataFrame() # Retorna um DataFrame vazio em caso de erro
    except ET.ParseError as e:
        print(f"Erro ao processar o XML: {e}")
        return pd.DataFrame()

# --- Bloco para testar a função ---
if __name__ == '__main__':
    df_noticias = buscar_noticias_google_news()

    if not df_noticias.empty:
        print("\nPré-visualização dos dados coletados:")
        print(df_noticias.head())
        # Salva os dados em um arquivo CSV, cumprindo um dos entregáveis 
        df_noticias.to_csv('C:/Users/snoop/Documents/CODE/monitor_ia/app/db/noticias_coletadas.csv', index=False)
        print("\nDados salvos em 'noticias_coletadas.csv'")