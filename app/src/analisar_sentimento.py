# Dentro de analise_sentimento.py

import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- CARREGA AS VARIÁVEIS DE AMBIENTE DO ARQUIVO .ENV ---
# Esta função procurará por um arquivo .env no diretório e o carregará
load_dotenv()

# --- CONFIGURAÇÃO DA API OPENAI ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERRO: A variável de ambiente OPENAI_API_KEY não foi encontrada.")
    print("Certifique-se de que você criou um arquivo .env com sua chave.")
    exit()

client = OpenAI(api_key=api_key)


def analisar_sentimento_openai(texto: str) -> str:
    """
    Analisa o sentimento de um texto usando a API da OpenAI com o modelo gpt-4o-mini.
    Retorna 'Positivo', 'Negativo' ou 'Neutro'.
    """
    # Evita enviar textos vazios ou inválidos para a API
    if not texto or not isinstance(texto, str) or texto.strip() == '':
        return 'Neutro'

    # O "system prompt" instrui o modelo sobre como ele deve se comportar.
    system_prompt = (
        "Você é um especialista em análise de sentimentos de notícias e posts de redes sociais. "
        "Sua tarefa é classificar o texto fornecido em uma de três categorias: "
        "Positivo, Negativo ou Neutro. "
        "Responda APENAS com uma única palavra: 'Positivo', 'Negativo' ou 'Neutro'."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto}
            ],
            temperature=0,
            max_tokens=5
        )
        
        sentimento = response.choices[0].message.content.strip()
        
        if sentimento in ['Positivo', 'Negativo', 'Neutro']:
            return sentimento
        else:
            return 'Neutro'

    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API da OpenAI: {e}")
        return "Erro na análise"

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    # Define caminhos relativos para funcionar em qualquer computador
    caminho_base = os.path.dirname(__file__)
    
    # --- 1. ANÁLISE DAS NOTÍCIAS ---
    print("--- INICIANDO ANÁLISE DE SENTIMENTO DAS NOTÍCIAS ---")
    caminho_noticias_entrada = os.path.join(caminho_base, '..', 'db', 'noticias_coletadas.csv')
    caminho_noticias_saida = os.path.join(caminho_base, '..', 'db', 'noticias_processadas.csv')
    
    try:
        df_noticias = pd.read_csv(caminho_noticias_entrada)
        df_noticias['texto_completo'] = df_noticias['titulo'] + ' ' + df_noticias['descricao'].fillna('')
        
        print("Analisando notícias... Isso pode levar alguns minutos.")
        df_noticias['sentimento'] = df_noticias['texto_completo'].apply(analisar_sentimento_openai)
        
        df_noticias.to_csv(caminho_noticias_saida, index=False)
        print("\nAnálise de notícias concluída!")
        print(f"Resultados salvos em '{os.path.basename(caminho_noticias_saida)}'")
        print("Pré-visualização:")
        print(df_noticias[['titulo', 'sentimento']].head())

    except FileNotFoundError:
        print(f"\nERRO: Arquivo '{os.path.basename(caminho_noticias_entrada)}' não encontrado. Execute 'coleta_dados.py' primeiro.")

    print("\n" + "="*50 + "\n") # Separador visual

    # --- 2. ANÁLISE DO INSTAGRAM ---
    print("--- INICIANDO ANÁLISE DE SENTIMENTO DO INSTAGRAM ---")
    caminho_insta_entrada = os.path.join(caminho_base, '..', 'db', 'instagram_posts_mencoes.csv')
    caminho_insta_saida = os.path.join(caminho_base, '..', 'db', 'instagram_processados.csv')
    
    try:
        df_insta = pd.read_csv(caminho_insta_entrada)
        df_insta['legenda'] = df_insta['legenda'].fillna('')

        print("Analisando posts do Instagram... Isso pode levar alguns minutos.")
        df_insta['sentimento'] = df_insta['legenda'].apply(analisar_sentimento_openai)
        
        df_insta.to_csv(caminho_insta_saida, index=False)
        print("\nAnálise do Instagram concluída!")
        print(f"Resultados salvos em '{os.path.basename(caminho_insta_saida)}'")
        print("Pré-visualização:")
        print(df_insta[['legenda', 'sentimento']].head())

    except FileNotFoundError:
        print(f"\nERRO: Arquivo '{os.path.basename(caminho_insta_entrada)}' não encontrado. Execute 'coleta_instagram.py' primeiro.")

