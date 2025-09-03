# Documento de Decisões Técnicas

Este arquivo registra as principais decisões de arquitetura e metodologia tomadas durante o desenvolvimento do projeto **"Monitor de Percepção Pública sobre IA no Piauí"**.

---

## 1. Abordagem para Análise de Sentimento

**Decisão:**  
Utilizar a API da OpenAI com o modelo `gpt-4o-mini` em vez de uma abordagem baseada em regras (lista de palavras-chave), como sugerido inicialmente no case.

**Justificativa:**

- **Precisão Contextual Superior:**  
  A abordagem baseada em palavras-chave é simples, mas limitada. Ela falha em entender contexto, sarcasmo ou sutileza da linguagem. Por exemplo, uma notícia com a frase *"o desafio da IA"* poderia ser classificada como negativa, mesmo que o restante do texto seja otimista sobre como o Piauí está superando esse desafio.

- **Robustez e Escalabilidade:**  
  O `gpt-4o-mini` é um modelo avançado de linguagem, treinado para compreender nuances textuais. Isso resulta em uma classificação de sentimento muito mais confiável e próxima da percepção humana. Além disso, a solução com API é mais escalável e se adapta a diferentes tipos de texto sem necessidade de manutenção manual de listas de palavras.

- **Alinhamento com o Mercado:**  
  Optar por uma solução de IA para analisar sentimentos demonstra domínio de ferramentas modernas, entregando resultados de qualidade superior.

---

## 2. Tratamento de Erros na Coleta de Dados

**Decisão:**  
Implementar blocos `try...except` robustos em todos os scripts de coleta (`coleta_dados.py` e `coleta_instagram.py`) para capturar falhas de rede e erros de processamento.

**Justificativa:**

- **Resiliência da Aplicação:**  
  A coleta de dados depende de serviços externos (Google Notícias, Apify) e da conexão com a internet. A aplicação foi projetada para não quebrar caso esses serviços estejam temporariamente indisponíveis ou uma requisição falhe.

- **Feedback Claro ao Usuário:**  
  Em caso de erro (`RequestException` para falhas de rede, `ParseError` para XML malformado, ou erros na API da Apify), o script informa o usuário no console e retorna sempre um DataFrame vazio.

- **Prevenção de Erros em Cascata:**  
  Retornando um DataFrame vazio, garantimos que os scripts subsequentes (`analisar_sentimento.py` e `main.py`) tenham comportamento previsível, informando que não há dados para processar, em vez de falhar inesperadamente.]
  - **Auxilio da IA:**  
 A IA ajudou a definir uma organização lógica de diretórios e nomes de arquivos, facilitando a navegação e manutenção do projeto.

