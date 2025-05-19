# ML-Challenge-Python

Proyecto a presentar sobre un script que consume una API de información sobre conversión entre monedas y los guarda en un archivo csv.

## Requisitos

- Python 3.13.3 o superior.
- PIP para poder instalar las librerias necesarias.

## Ejecución

Clonamos el repositorio en una carpeta dentro de nuestra computadora.

Luego, copiamos el archivo `.env.example`, lo renombramos a `.env` y completamos las variables presentes en el archivo. Para este proyecto en especifico, lo completamos de la siguiente forma:

```
API_URL= "https://economia.awesomeapi.com.br/json/last/"
CURRENCY_LIST= "USD-BRL,EUR-BRL,BTC-BRL"
```

> *Nota: Si desea consultar otras conversiones, visitar [este link](https://economia.awesomeapi.com.br/xml/available).* Si desea agregar otra conversion, asegurese de que la lista siga el formato establecido en [este articulo](https://docs.awesomeapi.com.br/api-de-moedas#retorna-moedas-selecionadas-atualizado-em-tempo-real).

Despues de haber establecido las variables de entorno, debemos crear el enviroment para ejecutar el script e instalar las librerias necesarias. 

Para hacerlo, vamos a la terminal y nos ubicaremos en la carpeta raiz del projecto.

Ejecutaremos los siguientes comandos:

**Crear el enviroment:**

``` bash
python -m venv .venv
```

**Activar el enviroment**

``` bash
.venv/Scripts/activate
```

**Instalar las librerias necesarias**

``` bash
pip install -r requirements.txt
```

Por ultimo, ejecutamos el script:
``` bash
python ./extraccion_monedas.py
```

## Funcionamiento

Cuando ejecutamos el script, el mismo consumira datos de la API establecida dentro del archivo `.env`, consultando la lista de conversiones presente en el mismo archivo.

Luego de consultar los datos, el script se encargara de guardar los datos en el archivo `datos_monedas.csv` dentro de la carpeta *data* dentro del projecto (esta se creara si no existe). Si actualmente el archivo contiene datos, en la ejecución se tomara esa información y se unira con la consultada en la ejecución actual. Tambien revisara que no haya duplicados.

En caso de que haya un error con la consulta a la API, se informara por consola.

## Composición de los datos

En el archivo csv generado por el script, encontrara las siguientes columnas:

- **moneda_base**: la moneda en la que se basa la conversión.
- **moneda_destino**: la moneda a la cual realizar la conversión.
- **valor_compra**: el valor de compra.
- **valor_venta**: el valor de venta.
- **data_hora**: la hora a la que esta registrada la información, en horario UTC y con el formato `yyyy-MM-dd HH:mm:ss`

Para ver un ejemplo, puede visitar el archivo `ej_datos_monedas.csv`