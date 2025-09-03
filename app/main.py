# app/main.py

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

# --- Configuração da Página ---
st.set_page_config(
    layout="wide",
    page_title="Monitor de IA no Piauí",
    page_icon="📊"
)

# --- Título e Descrição ---
st.title("📊 Monitor de Percepção Pública sobre IA no Piauí")
st.markdown("Este painel monitora notícias sobre Inteligência Artificial no Piauí, analisando o sentimento predominante na mídia.")

# --- Carregamento dos Dados ---
# O dashboard agora lê o arquivo CSV já processado.
# Isso evita reprocessar os dados a cada interação.
@st.cache_data
def carregar_dados_processados():
    # O caminho para o arquivo CSV
    caminho_csv = os.path.join(os.path.dirname(__file__), 'db', 'noticias_processadas.csv')
    try:
        df = pd.read_csv(caminho_csv)
        return df
    except FileNotFoundError:
        st.error("Arquivo 'noticias_processadas.csv' não encontrado.")
        st.info("Por favor, execute os scripts 'coleta_dados.py' e 'analisar_sentimento.py' para gerar os dados.")
        return pd.DataFrame()

df_noticias = carregar_dados_processados()

# Só exibe o dashboard se os dados foram carregados com sucesso
if not df_noticias.empty:
    # --- Layout em Colunas ---
    col1, col2 = st.columns((1, 1))

    with col1:
        # Gráfico de Pizza com a distribuição de sentimentos
        st.subheader("Distribuição de Sentimentos")
        contagem_sentimentos = df_noticias['sentimento'].value_counts()
        fig_pizza = px.pie(
            contagem_sentimentos,
            values=contagem_sentimentos.values,
            names=contagem_sentimentos.index,
            title="Sentimento Geral das Notícias",
            color=contagem_sentimentos.index,
            color_discrete_map={
                'Positivo': '#2ca02c',  # Verde
                'Negativo': '#d62728',  # Vermelho
                'Neutro': '#7f7f7f'      # Cinza
            }
        )
        fig_pizza.update_layout(legend_title_text='Sentimentos')
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col2:
        # Nuvem de Palavras com os termos mais frequentes
        st.subheader("Nuvem de Palavras-Chave")
        # Concatena todos os títulos para formar o texto da nuvem
        texto_nuvem = " ".join(titulo for titulo in df_noticias['titulo'])

        wordcloud = WordCloud(
            background_color="white",
            width=800,
            height=400,
            colormap='viridis',
            max_words=100
        ).generate(texto_nuvem)

        fig_nuvem, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_nuvem)

    # Tabela interativa com os dados coletados
    st.subheader("Notícias Coletadas")
    # Exibe colunas relevantes e permite que o usuário veja os links
    st.dataframe(
        df_noticias[['titulo', 'sentimento', 'link']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "link": st.column_config.LinkColumn("Link da Notícia")
        }
    )

    # --- Rodapé com o aviso sobre as limitações ---
    st.markdown("---")
    st.caption(
        "**Aviso de Transparência:** A análise de sentimento é realizada pelo modelo de linguagem "
        "GPT-4o-mini da OpenAI. Embora avançada, a análise pode não capturar perfeitamente "
        "sarcasmo ou contextos culturais complexos."
    )