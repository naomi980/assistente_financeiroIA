# 🤖 Matias — Analista Financeiro Pessoal com IA

> Seu assistente inteligente para categorizar gastos, identificar pontos de atenção e te ajudar a entender para onde seu dinheiro vai.

---

## 💡 O Problema

Muitas pessoas recebem o salário, gastam ao longo do mês e, quando percebem, o dinheiro acabou — sem saber exatamente onde foi. O **Matias** resolve isso de forma simples e acessível.

---

## ✨ O que o Matias faz

- 📂 **Categoriza transações** automaticamente (moradia, alimentação, saúde, entretenimento…)
- 📊 **Analisa os gastos do mês** com base no extrato fornecido
- 🚨 **Emite alertas** quando os gastos ultrapassam os percentuais ideais por categoria
- 💡 **Oferece dicas financeiras** personalizadas ao perfil do cliente
- 📝 **Registra novas transações** via linguagem natural (`gastei` / `recebi`)
- ❌ **Não recomenda investimentos**, não toma decisões e não julga o cliente

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Interface | [Streamlit](https://streamlit.io/) |
| LLM | Ollama (local) |
| Base de Conhecimento | CSV + JSON na pasta `data/` |
| Linguagem | Python |

---

## 📁 Estrutura do Projeto

```
assistente_financeiroIA/
├── app.py                              # Aplicação principal (Streamlit + Ollama)
├── data/
│   ├── categoria_transacao.csv         # Categorias de entrada e saída
│   ├── estabelecimentos_categoria.csv  # Mapeamento estabelecimento → categoria
│   ├── percentuais_financeiros.csv     # Percentuais ideais por categoria
│   ├── transacoes.csv                  # Extrato do cliente
│   ├── alertas_financeiros.json        # Alertas de saúde financeira
│   ├── dicas_financeiras.json          # Dicas personalizadas
│   ├── regras_analise.json             # Regras de análise do Matias
│   └── respostas_padrao.json           # Respostas automáticas do agente
└── docs/
    ├── 01_documentacao_agente.md       # Persona, arquitetura e segurança
    ├── 02_base_conhecimento.md         # Estratégia de dados e contexto
    ├── 03_prompts.md                   # System prompt, exemplos e edge cases
    ├── 04_metricas.md                  # Avaliação e testes do agente
    └── 05_pitch.md                     # Pitch de apresentação do projeto
```

---

## 🚀 Como executar

```bash
# 1. Clone o repositório
git clone https://github.com/naomi980/assistente_financeiroIA.git
cd assistente_financeiroIA

# 2. Instale as dependências
pip install streamlit pandas requests

# 3. Certifique-se de ter o Ollama rodando localmente
ollama run gpt-oss

# 4. Execute a aplicação
streamlit run app.py
```

---

## 💬 Como interagir

**Registrar uma transação:**
```
gastei 60.00 restaurante Alimentacao 2026-03-08
recebi 5000.00 salario Renda 2026-03-01
```

**Fazer perguntas:**
```
Onde estou gastando mais?
Estou dentro do orçamento esse mês?
Qual categoria devo revisar?
```

---

## 🧠 Regras de Análise

| Regra | Condição | Alerta |
|---|---|---|
| Gastos > renda | `gastos_totais > renda` | Risco de endividamento |
| Muitas assinaturas | `assinaturas > 5%` | Reavaliar assinaturas |
| Sem investimentos | `investimentos == 0` | Iniciar reserva de emergência |
| Excesso em entretenimento | `entretenimento > 10%` | Reavaliar gastos |

---

## 🔒 O que o Matias NÃO faz

- ❌ Recomenda investimentos específicos
- ❌ Toma decisões pelo cliente
- ❌ Acessa dados bancários sensíveis ou senhas
- ❌ Inventa informações financeiras
- ❌ Julga os gastos do cliente

---

## 🎥 Pitch

Assista à demonstração do Matias em funcionamento:
**[▶ Ver vídeo no YouTube](https://youtu.be/3ORMDy61OeM)**

---

<p align="center">Feito com 💚 por <a href="https://github.com/naomi980">naomi980</a></p>
