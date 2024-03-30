import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
apikey = os.getenv("apikey")
username = os.getenv("username")
password = os.getenv("password")


#Endpoint principal a usar
url = 'https://financialmodelingprep.com/api/v3/stock-screener'


def data(market):
    """
    Funcion para obtener los datos de las diferentes bolsas de valores. Adicionalmente se usa el filtro al endpoint isActivelyTrading=True para obtener aquellos que se encuentran activos.
    market: nombre del mercado de valores a extraer (NYSE, NASDAQ, EURONEXT, AMEX, TSX, ETF, etc)    
    """
    response = requests.get(f'{url}?exchange={market}&isActivelyTrading=True&limit=10000&{apikey}')
    stocks_data = response.json()

    #agregando fecha y hora que se extrajo la data
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    for stock in stocks_data:
        stock['date'] = date_string
    







conn = psycopg2.connect(
                        host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
                        database='data-engineer-database',
                        port=5439,
                        user=username,
                        password=password
                        )

cursor = conn.cursor()


cursor.execute("""
                CREATE TABLE leonel_aliaga_v_coderhouse.stocks_prices (
                    symbol VARCHAR(20),
                    companyName VARCHAR(100),
                    sector VARCHAR(100),
                    industry VARCHAR(100),
                    beta DOUBLE PRECISION,
                    price DOUBLE PRECISION,
                    lastAnnualDividend DOUBLE PRECISION,
                    volume DOUBLE PRECISION,
                    exchange VARCHAR(100),
                    exchangeShortName VARCHAR(10),
                    country VARCHAR(5),
                    isEtf BOOLEAN,
                    isFund BOOLEAN,
                    isActivelyTrading BOOLEAN,
                    date TIMESTAMP
                )
                """)


#INGESTANDO BASE DE DATOS


if __name__ == '__main__':
    data('NASDAQ')