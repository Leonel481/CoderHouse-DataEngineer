import requests
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime
from dotenv import load_dotenv
import os
from airflow.models import XCom


def extract_transform(market,apikey, **kwargs):
    """
    Funcion para obtener los datos de las diferentes bolsas de valores. Adicionalmente se usa el filtro al endpoint isActivelyTrading=True para obtener aquellos que se encuentran activos. Finalmente carga los datos en una tabla de redshift
    market: nombre del mercado de valores a extraer (NYSE, NASDAQ, EURONEXT, AMEX, TSX, ETF, etc)    
    """
    
    #Endpoint principal a usar, en el readme se muestra informacion sobre la API y como obtener una key, ya que es una API publica.
    url = 'https://financialmodelingprep.com/api/v3/stock-screener'

    response = requests.get(f'{url}?exchange={market}&isActivelyTrading=True&limit=10000&apikey={apikey}')
    stocks_data = response.json()

    # agregando fecha y hora que se extrajo la data, ademas de reemplazar valores 'None' por vacios para las etiquetas de sector, industry, lastAnnualDividend. Se elimina aquellos que contengan 'None' en isEtf, isFund, beta, country
    data_filtered = []
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    for stock in stocks_data:
        stock['sector'] = '' if stock['sector'] is None else stock['sector']
        stock['industry'] = '' if stock['industry'] is None else stock['industry']
        stock['lastAnnualDividend'] = 0 if stock['lastAnnualDividend'] is None else stock['lastAnnualDividend']
        if stock['isEtf'] is not None and stock['isFund'] is not None and stock['beta'] is not None and stock['country'] is not None:        
            stock['date'] = date_string
            data_filtered.append(stock)
    # print(stocks_data)

    # return stocks_data
    ti = kwargs['ti']
    ti.xcom_push(key="data_filtered", value=data_filtered)


def connect_load(username,password,**kwargs):
    """
    Conexion y a la tabla
    """
    ti = kwargs['ti'] 
    conn = psycopg2.connect(
                            host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
                            database='data-engineer-database',
                            port=5439,
                            user=username,
                            password=password
                            )


    """
    Creacion de la tabla y creacion de llave primaria si no existiese, posteriormente carga de data del mercado de NASDAQ
    """
    data = ti.xcom_pull(task_ids="transformar_data", key="data_filtered")

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
                        volume DOUBLE PRECISION,
                        exchange VARCHAR(100),
                        exchangeShortName VARCHAR(10),
                        country VARCHAR(10),
                        isEtf BOOLEAN,
                        isFund BOOLEAN,
                        isActivelyTrading BOOLEAN,
                        date TIMESTAMP NOT NULL
                    )
                    """)

    conn.commit()

    # Verificar si la clave primaria ya existe
    cursor.execute("""
                    SELECT COUNT(*) FROM information_schema.key_column_usage
                    WHERE table_name = 'stocks_prices' AND table_schema = 'leonel_aliaga_v_coderhouse'
                    AND constraint_name = 'pk_stocks_prices';
                    """)

    if cursor.fetchone()[0] == 0:
        # Crear la clave primaria si no existe
        cursor.execute("""
                        ALTER TABLE leonel_aliaga_v_coderhouse.stocks_prices
                        ADD CONSTRAINT pk_stocks_prices PRIMARY KEY (symbol, date);
                        """)

    #Ingesta de los datos por batch desde el diccionario a la tabla
    ingesta_batch = """
                    INSERT INTO leonel_aliaga_v_coderhouse.stocks_prices (symbol, companyName, marketCap, sector, industry, beta, price, lastAnnualDividend, volume, exchange, exchangeShortName, country, isEtf, isFund, isActivelyTrading, date)
                    VALUES (%(symbol)s, %(companyName)s, %(marketCap)s, %(sector)s, %(industry)s, %(beta)s, %(price)s, %(lastAnnualDividend)s,%(volume)s, %(exchange)s, %(exchangeShortName)s, %(country)s, %(isEtf)s, %(isFund)s, %(isActivelyTrading)s,%(date)s)
                    """
    execute_batch(conn.cursor(), ingesta_batch, data)

    conn.commit()
    cursor.close()
    conn.close()

# def main():

#     conn = connect_redshift()
#     data = extract_transform('NASDAQ')
#     load_data(conn, data)
#     conn.close()

# if __name__ == '__main__':
#     main()
#     #crear la llave primaria compuesta
#     create_pk()
