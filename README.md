# toba-qom
1. Instalar dependencias

```
pip install -r requirements.txt
```


1. Descargar contenido

Descarga todos los htmls en el directorio data/

```
from retrieve import scrap_site

scrap_site('https://www.bible.com/bible/150/GEN.1.RVR95', 'es_RVR95')
```

1. Procesar

Escribe un archivo json con los datos limpios

```
import preprocess
preprocess.preprocess_data('data/es_RVR95')
```

Crea un DataFrame de pandas a partir del json

```
es_df = preprocess.get_pandas_from_json('data/es_RVR95/processed_data.json')

```


Mergea dos DataFrames

```
import pandas as pd
pd.merge(es_df, toba_df, on='id')

```
