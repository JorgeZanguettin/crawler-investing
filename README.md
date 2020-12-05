# **Investing**

## O que é Investing?

O Investing.com é uma plataforma de mercados financeiros disponível em 44 idiomas que oferece dados em tempo real, cotações, gráficos, ferramentas financeiras, notícias de última hora e análises cobrindo 250 bolsas mundiais. Com mais de 21 milhões de usuários mensais e mais de 180 milhões de sessões, o site Investing.com é um dos três maiores sites financeiros mundiais, de acordo com o SimilarWeb e a Alexa.

## **Dados Coletados**

## Variaveis

```yaml
{
nome_criptomoeda : String,
url_criptoMoeda : String,
valor_dolar : Float,
valor_real : Float,
valor_variacao : Float,
porcentagem_variacao : Float,
data_hora_consulta : Datetime
}
```

## Amostra

| NOME_CRIPTOMOEDA | URL_CRIPTOMOEDA | VALOR_DOLAR | VALOR_REAL | VALOR_VARIACAO | PORCENTAGEM_VARIACAO | DATA_HORA_CONSULTA
| --- | --- | --- | --- | --- | --- | --- |
| bitcoin | https://br.investing.com/crypto/bitcoin | 18984.8 | 97885.62879999999 | -43.4 | -0.23% | 2020-12-05 10:35:11 |
| ethereum | https://br.investing.com/crypto/ethereum | 586.18 | 3022.3440799999994 | -4.43 | -0.76% | 2020-12-05 10:35:38 |
| litecoin | https://br.investing.com/crypto/litecoin | 82.278 | 424.225368 | -2.525 | -3.07% | 2020-12-05 10:35:56 |
| bitcoin cash | https://br.investing.com/crypto/bitcoin-cash | 282.2 | 1455.0231999999999 | -6.95 | -2.46% | 2020-12-05 10:36:23 |
| monero | https://br.investing.com/crypto/monero | 129.171 | 666.0056759999999 | -2.281 | -1.77% | 2020-12-05 10:37:13 |

## Como executar?

1. Faça o download e instalação do Python 3 [Aqui](https://www.python.org/).
2. Direcione o seu bash de preferencia a pasta raiz do repositorio e instale as dependencias utilizando o comando ```pip install -r requirements.txt``` ou ```pip3 install -r requirements.txt``` .
3. Execute o Crawler com o comando ```python investing.py NomeCriptomoeda``` ou ```python3 investing.py NomeCriptomoeda``` .
4. Pronto! Os dados coletados serão armazenados em um arquivo CSV na raiz do projeto com o nome **cotacoes.csv**.
