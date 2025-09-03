# 📊 Monitor de Percepção Pública sobre IA no Piauí

Este projeto é uma solução completa para coletar, analisar e visualizar a percepção pública sobre o tema **"Inteligência Artificial no Piauí"**.  
A solução monitora duas fontes de dados distintas: notícias do Google Notícias e menções de perfis específicos no Instagram.

O objetivo é fornecer um **dashboard interativo** que consolida essas informações, permitindo uma análise clara do sentimento predominante na mídia e nas redes sociais.

---

## 🚀 Funcionalidades

- **Coleta de Múltiplas Fontes:**  
  Busca notícias via RSS do Google (requisito principal) e, como funcionalidade bónus, coleta também menções no Instagram utilizando a API da Apify.

- **Análise de Sentimento com IA:**  
  Utiliza o modelo `gpt-4o-mini` da OpenAI para uma classificação de sentimento precisa e contextual.

- **Dashboard Interativo:**  
  Interface rica criada com Streamlit, com filtros dinâmicos por fonte de dados.

- **Pipeline de Dados Organizado:**  
  Scripts separados e bem definidos para cada etapa do processo (coleta, análise e visualização).

---

## 🛠️ Estrutura do Projeto
```bash
.
├── app/
│   ├── src/
│   │   ├── coleta_dados.py
│   │   ├── coleta_instagram.py
│   │   └── analisar_sentimento.py
│   ├── db/
│   │   ├── noticias_coletadas.csv
│   │   ├── noticias_processadas.csv
│   │   ├── instagram_posts_mencoes.csv
│   │   └── instagram_processados.csv
│   └── main.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── DECISIONS.md

---

## ⚙️ Como Executar o Projeto

### ✅ Pré-requisitos

- Python 3.8+
- Chave de API da OpenAI
- Token de API da Apify

### 📦 Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_SEU_REPOSITORIO>

 Criar e Ativar o Ambiente Virtual
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

🔑 Criar o Arquivo .env
OPENAI_API_KEY="sua_chave_da_openai_aqui"
APIFY_API_TOKEN="seu_token_da_apify_aqui"

📥 Instalar as Dependências
pip install -r requirements.txt

📝 Executar o Pipeline de Dados
# Passo 1: Coleta dos dados
python app/src/coleta_dados.py
python app/src/coleta_instagram.py

# Passo 2: Análise de sentimento
python app/src/analisar_sentimento.py

🖥️ Iniciar o Dashboard
streamlit run app/main.py



