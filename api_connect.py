import requests
import psycopg2

apikey = '9AyqzrSFddQOVtsB8vNpokqLabX9gdK9'

url = 'https://financialmodelingprep.com/api/v3/stock-screener'


def data(market):
    """
    Funcion para obtener los datos de las diferentes bolsas de valores. Adicionalmente se usa el filtro al endpoint isActivelyTrading=True para obtener aquellos que se encuentran activos.
    market: nombre del mercado de valores a extraer (NYSE, NASDAQ, EURONEXT, AMEX, TSX, ETF, etc)    
    """
    response = requests.get(f'{url}?exchange={market}&isActivelyTrading=True&limit=10000&{apikey}')
    stocks_data = response.json()

def create_table():


conn = psycopg2.connect(
                        host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com',
                        database='data-engineer-database',
                        port=5439,
                        user='leonel_aliaga_v_coderhouse',
                        password='R7A0Hh1XTB'
                        )

cursor = conn.cursor()
cursor.execute("SHOW SCHEMAS FROM DATABASE data-engineer-database;")



