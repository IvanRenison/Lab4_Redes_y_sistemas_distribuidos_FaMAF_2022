# Enrutamiento y control de una red

### Resumen

En esta trabajo se estudian y comparan 2 algoritmos de enrutmaiento para redes anillo de tamaño fijo.

### Autores

- Fuentes, Tiffany
- Renison, Iván
- Schachner, Alvaro

## Índice

1. [Introducción](#introducción)
2. [El enrutamiento naive](#el-enrutamiento-naive)
3. [El enrutamiento mejorado](#el-enrutamiento-mejorado)
   1. [Reconocimiento de la red](#reconocimiento-de-la-red)
   2. [Enrutamiento de datagramas](#enrutamiento-de-datagramas)
4. [Resultados](#resultados)

## Introducción

En este trabajo se utilizara una red en forma de anillo en el que cada nodo está conectado a otros dos nodos. Por ejemplo, así sería el esquema de un anillo de 8 elementos:

![Anillo de tamaño 8.png](./Imágenes%20informe/Anillo%20de%20tamaño%208.png)

Internamente cada nodo cuenta con una capa de aplicación que genera y recibe paquetes y una capa de transporte que hace dos cosas:

- Mandar hacia algún lado los paquetes provenientes de la capa de aplicación.

- Recibir paquetes de sus vecinos y re-enviarlos al otro vecino o a la capa de aplicación según algún algoritmo.

## Algoritmo naive

En la simulación utilizamos una topografía en forma de anillo, para cada vecino se tienen 2 interfaces para comunicación, una para enviar mensajes y otro para recibir. En el algoritmo inicial todos los paquetes se enviaban a través del vecino a la izquierda del nodo, es decir, todos los paquetes se enviaban contrario al sentido de las agujas del reloj. 

En este algoritmo inicial no había ningún tipo de lógica para escoger el camino más óptimo, simplemente se enviaban todos los paquetes de la misma forma sin tomar en cuenta la distancia del enrutador de destino.

## Algoritmo mejorado

Para mejorar el enrutamiento implementamos un algoritmo sencillo que aprovecha el hecho de que la topología sea en forma de anillo, el algoritmo se divide en dos partes:

### Reconocimiento de la red

Inicialmente, antes de comenzar la transferencia de paquetes, cada enrutador genera un paquete de reconocimiento de red, este paquete tiene como encabezados el ID del enrutador de destino y la cantidad de saltos que hace el paquete. Cuando un enrutador genera este paquete se coloca a sí mismo como enrutador de destino, y inicia el campo de saltos en 0. Este paquete viaja por toda la red (utilizando el algoritmo naïve), aumentando el paquete de saltos cada vez que pasa por un enrutador, y una vez llega al enrutador de destino (que es el mismo que originó el paquete), extrayendo el valor en el campo de saltos va a saber la cantidad de enrutadores que hay en la red.

La simplicidad del reconocimiento de red se da porque se sabe que la topología tiene forma de anillo, además se asume que los enrutadores están en orden, es decir, si hay 8 enrutadores los mismos están ordenados de forma que sus IDs son consecutivos. Se asume esto debido a que incluso si los enrutadores no estuviesen en orden, y por ende se tuviese que calcular la distancia a cada uno, el algoritmo seguiría funcionando de la misma manera, solamente se tendría que hacer un paso extra para conocer la distancia a cada enrutador.

En caso de que fuese necesario conocer las distancias hacia los otros enrutadores, es decir que no se puede asumir un cierto orden, se realizaría de igual forma el primer paso de reconocimiento de red para saber cuantos enrutadores hay en la red, usando esto se sabe cuantas entradas se necesita para la tabla de reenvios (la cual se puede implementar con un arreglo, o un diccionario), luego de esto cada enrutador debe generar un paquete de aviso a la red, este paquete tiene como encabezados el ID del enrutador emisor, la cantidad de saltos que hace el paquete y un campo para la edad. La edad es la cantidad de saltos que puede dar el paquete antes de descartarse, se inicializa con el valor _cantidad de enrutadores - 1_ para que pase por todos los enrutadores de la red (excepto el que crea el paquete) y luego se descarte.

Cada vez que un enrutador recibe uno de estos paquetes, utilizando el campo del enrutador emisor puede registrar en la tabla de reenvíos la entrada correspondiente para el emisor del paquete, y utiliza

### Enrutamiento de datagramas

## Resultados
