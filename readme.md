# Proyecto de consumo de APIS e ingesta a Redshift

La API publica que se comsume en el proyecto es de la bolsa de valores.
En la pagina https://site.financialmodelingprep.com/ encontra mas informacion sobre la API.

**Tareas del Dag:**

![Dag](https://github.com/Leonel481/CoderHouse-DataEngineer/blob/master/Imagen/ETL_data_dag.png)

**Ejemplo de envio de log al correo cuando falla la dag:**

![Dag](https://github.com/Leonel481/CoderHouse-DataEngineer/blob/master/Imagen/log_email.png)


## Reglas y transformaciones:

Se eligio los datos de acciones del indice de NASDAQ, ademas que se considero las siguientes reglas para la tabla:

 - symbol : Es el simbolo o etiqueta de la accion, el valor no puede ser nulo o None.
 - companyName : Nombre de la empresa, el valor no puede ser nulo o None.
 - marketCap : Capitalizacion del mercado de la accion.
 - sector : Sector al que pertenece la empresa.
 - industry : Industra que pertenece la empresa.
 - beta : Representa la volatilidad de la accion, se elimino aquellos que son None.
 - price : Precio de la accion.
 - lastAnnualDividend : Beneficios del año anterior.
 - volume : Volumen de acciones.
 - exchange : Indice del mercado. (NYSE, NASDAQ, EURONEXT), se eligio el indice de NASDAQ.
 - exchangeShortName : Acronimo del exchange.
 - country : Representa el pais donde se encuentra la sede central de la empresa, se elimino aquellos que son None.
 - isFund : Representa si la accion es un fondo de inversion (puede ser True, False, None), se elimino aquellos que son None.
 - isETF : Representa si la accion es un ETF (puede ser True, False, None), se elimino aquellos que son None.
 - isActivelyTrading : La accion se encuentra activa en el mercado de valores.
 - date : Fecha y hora que se realiza la consulta de la api

Nota: Para la conexion a la API es necesario una key, dicha key se genera al registrarse en la pagina o ingresar a la pagina con una cuenta google.

## Configuracion de correo para mensajes airflow:

- Configurar un correo gmail con autenticacion a 2 pasos
- Configurar una nueva contraseña en la seccion aplicaciones menos seguras
- El correo y la contraseña generada se usaran para SMTP airflow