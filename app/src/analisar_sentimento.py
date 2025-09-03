# Dentro de analise_sentimento.py

import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# --- CARREGA AS VARIÁVEIS DE AMBIENTE DO ARQUIVO .ENV ---
# Esta função procurará por um arquivo .env no diretório e o carregará
load_dotenv()

# --- CONFIGURAÇÃO DA API OPENAI ---
# O código agora busca a chave que foi carregada pelo load_dotenv()
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
        "Você é um especialista em análise de sentimentos de notícias. "
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

# --- Bloco para testar a função ---
if __name__ == '__main__':
    try:
        df = pd.read_csv('C:/Users/snoop/Documents/CODE/monitor_ia/app/db/noticias_coletadas.csv')

        df['texto_completo'] = df['titulo'] + ' ' + df['descricao'].fillna('')

        print("Iniciando a análise de sentimento com a API da OpenAI (usando dotenv)...")
        print("Isso pode levar alguns minutos, dependendo do número de notícias...")

        df['sentimento'] = df['texto_completo'].apply(analisar_sentimento_openai)

        print("\nAnálise de sentimento concluída!")
        print("Pré-visualização dos dados com sentimento:")
        print(df[['titulo', 'sentimento']].head())

        df.to_csv('C:/Users/snoop/Documents/CODE/monitor_ia/app/db/noticias_processadas.csv', index=False)
        print("\nDados processados salvos em 'noticias_processadas.csv'")

    except FileNotFoundError:
        print("Arquivo 'noticias_coletadas.csv' não encontrado. Execute o script 'coleta_dados.py' primeiro.")