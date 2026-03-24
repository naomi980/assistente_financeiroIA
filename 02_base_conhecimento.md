# Base de Conhecimento

> [!TIP]
> **Prompt usado para esta etapa:**
> ```
> Preciso organizar a base de conhecimento do meu agente financeiro educativo.
> Tenho estes arquivos de dados: [liste os arquivos].
> Me ajude a:
> (1) entender o que cada arquivo contém;
> (2) decidir como usar cada um;
> (3) criar um exemplo de contexto formatado para incluir no prompt.


## Dados Utilizados

| Arquivo | Formato | Para que serve no Matias? |
|---------|---------|---------------------|
| `categoria_transacao.csv` | CSV | Contextualiza as categorias de entrada e saída que o cliente pode ter |
| `estabelecimentos_categoria.csv` | CSV | Atribui os estabelecimentos em que o cliente pode gastar numa categoria |
| `percentuais_financeiros.csv` | CSV | Apresenta o percentual de gasto em cada categoria |
| `transacoes.csv` | CSV | Apresenta as transacoes realizadas pelo cliente |
| `regras_analise.json` | JSON | Representa a inteligência do Matias |
| `alertas_financeiros.json` | JSON | Alerta o cliente para situações que podem comprometer sua saúde financeira|
| `respostas_padrao.json` | JSON | Retorna respostas automáticas para determinadas ações|
| `dicas_financeiras.json` | JSON | Dá dicas financeiras ao cliente|

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import pandas as 
import json

categorias = pd.read_csv(".\data\categoria_transacao.csv")
estabelecimentos = pd.read_csv(".\data\estabelecimentos_categoria.csv")
transacoes = pd.read_csv(".\data\transacoes.csv")
percentuais = pd.read_csv(".\data\percentuais_financeiros.csv")
alertas = json.load(open(".\data\alertas_financeiros.json"))
dicas = json.load(open(".\data\dicas_financeiras.json"))
regras = json.load(open(".\data\regras_analise.json"))
respostas_padrao = json.load(open(".\data\respostas_padrao.json"))
``` 


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, garantindo que o Agente tenha o melhor contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informações sejam carregadas dinamicamente para que possamos ganhar flexibilidade.

```text
CATEGORIAS DE TRANSAÇÕES

categoria, descricao, tipo
Renda, salário, provento, aluguel, entrada
Moradia, aluguel, água, energia eletrica, gás, internet, saída
Alimentacao, mercado, restaurantes, delivery, saída
Transporte, transporte público, gasolina, uber, saída
Saude, plano de saúde, remédios, academia, terapia, saída
Entretenimento, cinema, viagens, hobbies, shows, compras online, roupa, eletrônicos, saída
Assinaturas, netflix, spotify, apps, saída
Investimentos, tesouro direto, ações, FII, ETF, saída
Educacao, cursos, certificados, faculdade, saída

ESTABELECIMENTOS DAS CATEGORIAS

estabelecimento, categoria
ifood, Alimentacao
uber, Transporte
mercado, Alimentacao
metro, Transporte
onibus, Transporte
posto, Transporte
farmacia, Saude
amazon, Entretenimento
C&A, Entretenimento
renner, Entretenimento
centauro, Entretenimento
netflix, Assinaturas
spotify, Assinaturas
primevideo, Assinaturas
crunchroll, Assinaturas
rico, Investimentos
xp, Investimentos
tesouro direto, Investimentos
coursera, Educacao
eventim, Entretenimento
ticketmaster, Entretenimento
cinemark, Entretenimento

PERCENTUAIS DE GASTOS DAS CATEGORIAS

categoria, percentual_ideal, percentual_maximo
Moradia, 40, 55
Alimentacao, 15, 20
Transporte, 10, 15
Saude, 10, 15
Entretenimento, 5, 10
Assinaturas, 2,5
Invetimentos, 10, 20
Educacao, 10, 15

TRANSAÇÕES REALIZADAS PELO CLIENTE NO MÊS

data, descricao, categoria, valor, tipo
2026-03-01, Salário, receita, 5000.00, entrada
2026-03-04, aluguel, Moradia, 2000.00, saída
2026-03-06, mercado, Alimentacao, 400.00, saída
2026-03-08, cinema, Entretenimento, 30.00, saída
2026-03-08, restaurante, Alimentacao, 60.00, saída
2026-03-14, energia elétrica, Moradia, 30.00, saída
2026-03-15, plano de saúde, Saude, 700.00, saída
2026-03-20, academia, Saude, 200.00, saída
2026-03-21, netflix, Assinaturas, 30.00, saída

REGRAS DAS ANÁLISES FINANCEIRAS

[
    {
        "regra": "gastos_maiores_que_renda",
        "condicao": "gastos_totais > renda",
        "mensagem": "Seus gastos estão maiores que sua renda. Isso pode gerar endividamento!"
    },
    {
        "regra": "muitas_assinaturas",
        "condicao": "assinaturas > 5",
        "mensagem": "Você possui muitas assinaturas. Oportunidade para reavaliar assinaturas atuais e economizar!"
    },
    {
        "regra": "sem_investimentos",
        "condicao": "investimentos == 0",
        "mensagem": "Você ainda não possui investimentos. Começar uma reserva de emergência pode ser um bom primeiro passo!"
    },
    {
        "regra": "muito_gasto_com_entretenimento",
        "condicao": "entretenimento > 10",
        "mensagem": "Você está gastando muito com entretenimento. Oportunidade para reavaliar gastos."
    }
]

RESPOSTAS PADRÕES DO AGENTE

{
  "confirmacao_gasto": [
    "Já registrei esse gasto.",
    "Gasto registrado com sucesso.",
    "Esse valor já foi adicionado aos seus gastos."
  ],
  "inicio_analise": [
    "Vou analisar seus gastos e já te mostro um resumo.",
    "Vou organizar suas despesas e verificar para onde seu dinheiro foi."
  ],
  "fim_analise": [
    "Pronto, analisei seus gastos.",
    "Aqui está o resumo financeiro do seu mês."
  ]
}

DICAS FINANCEIRAS

[
    "Evite fazer compras em muitas parcelas e com juros",
    "Revise suas assinaturas a cada 3 meses",
    "Tenha uma reserva de emergência de pelo menos 6 meses de gastos.",
    "Guarde dinheiro assim que receber seu salário.",
    "Pequenos gastos frequentes podem impactar no fim do mês."
]
``` 

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo de contexto montado abaixo, se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim, o consumo de tokens. Entretando, vale lembrar que mais importante do que economizar tokens, é ter todas as informações relevantes disponíveis em seu contexto. 

```
CATEGORIA DOS GASTOS:
- Moradia (água, energia elétrica, gás, internet)
- Alimentação (mercado, restaurantes, delivery)
- Transporte (transporte público, gasolina, uber)
- Saúde (plano de saúde, remédios, academia, terapia)
- Entretenimento (cinema, viagens, hobbies, shows, compras online, roupa, eletrônicos)
- Assinaturas (netflix, spotify, apps)
- Investimentos (tesouro direto, ações, FII, ETF)
- Educação (cursos, certificados, faculdade)

PERCENTUAL IDEAL DE GASTO EM CADA CATEGORIA: 
- Moradia: 40%
- Alimentação: 15%
- Transporte: 10%
- Saúde: 10%
- Entretenimento: 5%
- Assinaturas: 2%
- Investimentos: 10%
- Educação: 10%

RESUMO DE GASTOS:
- Moradia - R$ 2.030,00
- Alimentação - R$ 460,00
- Entretenimento - R$ 30,00
- Saúde - R$ 900,00
- Assinaturas - R$ 30,00
- Total de saídas: R$ 3.450,00
...
```
