# Dentro de app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Importa as funções dos outros arquivos
from app.src.coleta_dados import buscar_noticias_google_news
from app.src.analisar_sentimento import analisar_sentimento

st.set_page_config(layout="wide")

# Título do Dashboard
st.title("📊 Monitor de Percepção Pública sobre IA no Piauí")
st.markdown("Um painel para monitorar notícias sobre Inteligência Artificial no Piauí.")

# --- Coleta e Processamento dos Dados ---
# Usamos @st.cache_data para evitar buscar os dados toda vez que a página recarregar
@st.cache_data
def carregar_dados():
    df = buscar_noticias_google_news(termo_pesquisa="Inteligência Artificial Piauí", max_resultados=15)
    if not df.empty:
        df['texto_completo'] = df['titulo'] + ' ' + df['descricao'].fillna('')
        df['sentimento'] = df['texto_completo'].apply(analisar_sentimento)
    return df

df_noticias = carregar_dados()

if df_noticias.empty:
    st.error("Nenhuma notícia foi encontrada. Verifique a conexão ou o termo de busca.")
else:
    # --- Layout do Dashboard em Colunas ---
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de Pizza com a distribuição de sentimentos
        st.subheader("Distribuição de Sentimentos")
        contagem_sentimentos = df_noticias['sentimento'].value_counts()
        fig_pizza = px.pie(
            contagem_sentimentos, 
            values=contagem_sentimentos.values, 
            names=contagem_sentimentos.index,
            color=contagem_sentimentos.index,
            color_discrete_map={'Positivo':'green', 'Negativo':'red', 'Neutro':'grey'}
        )
        st.plotly_chart(fig_pizza, use_container_width=True)

    with col2:
        # Nuvem de Palavras com os termos mais frequentes
        st.subheader("Nuvem de Palavras-Chave")
        texto_nuvem = " ".join(titulo for titulo in df_noticias['titulo'])
        wordcloud = WordCloud(background_color="white", width=800, height=400).generate(texto_nuvem)

        fig_nuvem, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_nuvem)

    # Tabela interativa com os dados coletados
    st.subheader("Notícias Coletadas")
    st.dataframe(df_noticias[['titulo', 'sentimento', 'link']])

    # Rodapé com o aviso sobre as limitações da análise 
    st.caption("Aviso: Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos.")