import json
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

#--------------------CONFIGURAÇÃO---------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"
#-------------------CARREGAR DADOS----------------------------------------
categorias = pd.read_csv("./data/categoria_transacao.csv")
estabelecimentos = pd.read_csv("./data/estabelecimentos_categoria.csv")
transacoes = pd.read_csv("./data/transacoes.csv")
percentuais = pd.read_csv("./data/percentuais_financeiros.csv")
alertas = json.load(open("./data/alertas_financeiros.json"))
dicas = json.load(open("./data/dicas_financeiras.json"))
regras = json.load(open("./data/regras_analise.json"))
respostas_padrao = json.load(open("./data/respostas_padrao.json"))

#---------------REGISTRAR NOVO GASTO--------------------------------------
def registrar_transacao(mensagem):
    try:
        partes = mensagem.split()

        tipo_msg = partes[0]
        valor = float(partes[1])
        descricao = partes[2]
        categoria = partes[3]
        data = partes[4]
        #data = datetime.strptime(data, "%Y-%m-%d").strftime("%Y-%m-%d")

        ano, mes, dia = data.split("-")
        if len(ano) != 4:
            raise ValueError
        

        if tipo_msg == "gastei":
            tipo = "saída"
        elif tipo_msg == "recebi":
            tipo = "entrada"
        else:
            return "Digite 'gastei' ou 'recebi'."

        nova_transacao = pd.DataFrame([[
            data, descricao, categoria, valor, tipo
        ]], columns=["data","descricao","categoria","valor","tipo"])

        transacoes = pd.read_csv("./data/transacoes.csv")
        transacoes.columns = transacoes.columns.str.strip()

        transacoes = pd.concat([transacoes, nova_transacao], ignore_index=True)
        transacoes.to_csv("./data/transacoes.csv", index=False)

        return "Transação registrada com sucesso!"
    except ValueError: 
        return "Adicione data no formato: ano-mês-dia"
    except Exception as e:
        return f"Erro: {e}"

#----------------MONTAR CONTEXTO------------------------------------------
def montar_contexto():
    transacoes = pd.read_csv("./data/transacoes.csv")

    # converter data
    transacoes["data"] = pd.to_datetime(
        transacoes["data"],
        errors="coerce"
    )

    transacoes = transacoes.dropna(subset=["data"])
    # mês atual
    hoje = pd.Timestamp.today()
    mes_atual = hoje.month
    ano_atual = hoje.year

    transacoes_mes = transacoes[
        (transacoes["data"].dt.month == mes_atual) &
        (transacoes["data"].dt.year == ano_atual)
    ]

    contexto = f"""
    TRANSAÇÕES DO MÊS:
    {transacoes_mes.tail(10).to_string(index=False)}

    TODAS AS TRANSAÇÕES:
    {transacoes.tail(10).to_string(index=False)}

    CATEGORIAS FINANCEIRAS:
    {categorias.to_string(index=False)}

    PERCENTUAIS FINANCEIROS IDEAIS:
    {percentuais.to_string(index=False)}

    ALERTAS FINANCEIROS DISPONÍVEIS:
    {alertas}

    DICAS FINANCEIRAS:
    {dicas}

    REGRAS DE ANÁLISE FINANCEIRA:
    {regras}

    RESPOSTAS PADRÃO DO AGENTE:
    {respostas_padrao}
    """

    return contexto

#--------------------SYSTEM PROMPT--------------------------------
SYSTEM_PROMPT = """Você é o Matias, um analista financeiro pessoal amigável e didático.

OBJETIVO:
Auxiliar o cliente a controlar melhor suas despesas, categorizando-as e identificando as categorias de maiores gastos, utilizando os dados do cliente, como extrato bancário.
[Cole aqui seu system prompt completo]

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos;
2. Caso o usuário forneça novos dados de gastos, armazene essa informação;
3. Nunca invente informações financeiras;
4. Se não souber algo, admita e ofereça alternativas;
5. NUNCA recomende investimentos específicos;
6. Nunca diga o que o cliente deve fazer;
7. Linguagem acessível;
8. Use os dados fornecidos para dar exemplos personalizados.

"""
#-------------CHAMAR OLLAMA----------------------------------------------------------
def perguntar(msg):
    contexto = montar_contexto()

    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}
    """

    r = requests.post(
        OLLAMA_URL,
        json={"model": MODELO, "prompt": prompt, "stream": False}
    )
    
    return r.json()["response"]

#-------------------INTERFACE--------------------------------------------------
st.title("Matias, seu Analista Financeiro Pessoal")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)

    if pergunta.startswith("gastei") or pergunta.startswith("recebi"):
        resposta = registrar_transacao(pergunta)
        st.chat_message("assistant").write(resposta)

    else:
        with st.spinner("..."):
            resposta = perguntar(pergunta)
            st.chat_message("assistant").write(resposta)