import requests
import psycopg2
from psycopg2.extras import execute_batch
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
    Funcion para obtener los datos de las diferentes bolsas de valores. Adicionalmente se usa el filtro al endpoint isActivelyTrading=True para obtener aquellos que se encuentran activos. Finalmente carga los datos en una tabla de redshift
    market: nombre del mercado de valores a extraer (NYSE, NASDAQ, EURONEXT, AMEX, TSX, ETF, etc)    
    """
    response = requests.get(f'{url}?exchange={market}&isActivelyTrading=True&limit=10000&apikey={apikey}')
    stocks_data = response.json()

    # agregando fecha y hora que se extrajo la data
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    for stock in stocks_data:
        stock['date'] = date_string

        
    #Conexion y creacion de la tabla

    conn = psycopg2.connect(
                            host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
                            database='data-engineer-database',
                            port=5439,
                            user=username,
                            password=password
                            )

    cursor = conn.cursor()



    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS leonel_aliaga_v_coderhouse.stocks_prices (
                        symbol VARCHAR(20) NOT NULL,
                        companyName VARCHAR(100) NOT NULL,
                        marketCap DOUBLE PRECISION,
                        sector VARCHAR(100),
                        industry VARCHAR(100),
                        beta DOUBLE PRECISION,
                        price DOUBLE PRECISION,
                        lastAnnualDividend DOUBLE PRECISION,
                        volume INTEGER,
                        exchange VARCHAR(100),
                        exchangeShortName VARCHAR(10),
                        country VARCHAR(10),
                        isEtf BOOLEAN,
                        isFund BOOLEAN,
                        isActivelyTrading BOOLEAN,
                        date TIMESTAMP
                    )
                    """)



    #Ingesta de los datos por batch
    ingesta_batch = """
                    INSERT INTO leonel_aliaga_v_coderhouse.stocks_prices (symbol, companyName, marketCap, sector, industry, beta, price, lastAnnualDividend, volume, exchange, exchangeShortName, country, isEtf, isFund, isActivelyTrading, date)
                    VALUES (%(symbol)s, %(companyName)s, %(marketCap)s, %(sector)s, %(industry)s, %(beta)s, %(price)s, %(lastAnnualDividend)s,%(volume)s, %(exchange)s, %(exchangeShortName)s, %(country)s, %(isEtf)s, %(isFund)s, %(isActivelyTrading)s,%(date)s)
                    """
    execute_batch(conn.cursor(), ingesta_batch, stocks_data)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':

    data('NASDAQ')