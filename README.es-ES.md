

# Conjunto de Datos SatLoc

Este repositorio contiene conjuntos de datos creados a partir del trabajo de los siguientes artículos.: 

[Hacia la localización de UAV en entornos denegados de GNSS: El conjunto de datos SatLoc y un marco de fusión adaptativa jerárquica](https://www.mdpi.com/2072-4292/17/17/3048)


## Conjunto de Datos

### Descarga

El conjunto de datos se puede descargar desde: 
 [Quark](https://pan.quark.cn/s/1cdf996537cc) con el código de acceso `yYuP`, que incluye los fotogramas capturados por el UAV y las imágenes satelitales para entrenamiento y evaluación.

### Descripción

Hemos preparado imágenes aéreas de UAV con diferentes trayectorias, así como imágenes satelitales que cubren las rutas de vuelo (almacenadas en formato .tif). La estructura de directorios es la siguiente:

```
+--- SatLoc
|	+--- Satellite Data
|		---- CS_Area1.tif
|		---- ref_sample.csv
|		+--- sat_image_ref
|	+--- UAV Data
|		+--- traj01
|		+--- ...
|		+--- ...
|   ---- eval_samplel.py

```

Para los archivos en el directorio `Satellite Data`:

- La imagen satelital contiene un DOM completo de la zona de adquisición de datos (.tif), con datos de coordenadas geográficas integrados;
- El directorio `sat_image_ref` almacena imágenes de mosaicos satelitales utilizadas para la composición del DOM, numeradas secuencialmente con 5 dígitos;
- `ref_sample.csv` almacena la correspondencia entre el número de secuencia de una imagen de mosaico satelital y sus coordenadas de píxel locales en la imagen DOM.

Para obtener el rango de latitud y longitud correspondiente a la esquina "superior izquierda - inferior derecha" de una imagen de mosaico satelital con un número de secuencia dado, consulte el código de ejemplo en `eval_samplel.py`.

El directorio `UAV Data` almacena las secuencias de imágenes capturadas por el equipo de imagen a bordo del UAV, organizadas por número de vuelo. Cada imagen se nombra según la siguiente regla:

```
Sequence_Number@Frame_Number@Longitude@Latitude
```
Debido al gran volumen de datos de vuelos, los subiremos por lotes lo antes posible.


## Citación

Si considera que este conjunto de datos es útil para su investigación, por favor cite nuestro artículo: 

```
@Article{rs17173048,
AUTHOR = {Zhou, Xiang and Zhang, Xiangkai and Yang, Xu and Zhao, Jiannan and Liu, Zhiyong and Shuang, Feng},
TITLE = {Towards UAV Localization in GNSS-Denied Environments: The SatLoc Dataset and a Hierarchical Adaptive Fusion Framework},
JOURNAL = {Remote Sensing},
VOLUME = {17},
YEAR = {2025},
NUMBER = {17},
ARTICLE-NUMBER = {3048},
URL = {https://www.mdpi.com/2072-4292/17/17/3048},
ISSN = {2072-4292},
DOI = {10.3390/rs17173048}
}
```
