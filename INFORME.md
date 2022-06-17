# Enrutamiento y control de una red

### Resumen

En esta trabajo se estudian y comparan 2 algoritmos de enrutamiento para redes anillo de tamaño fijo.

### Autores

- Fuentes, Tiffany
- Renison, Iván
- Schachner, Alvaro

## Índice

1. [Introducción](#introducción)
2. [El enrutamiento naïve](#el-enrutamiento-naive)
3. [El enrutamiento mejorado](#el-enrutamiento-mejorado)
   1. [Reconocimiento de la red](#reconocimiento-de-la-red)
   2. [Enrutamiento de datagramas](#enrutamiento-de-datagramas)
4. [Resultados](#resultados)
5. [Discusiones](#discusiones)
6. [Referencias](#referencias)

## Introducción

En este trabajo se utilizó una red en forma de anillo en el que cada nodo está conectado a otros dos nodos. Por ejemplo, así sería el esquema de un anillo de 8 elementos:

![Anillo de tamaño 8.png](./Imágenes%20informe/Anillo%20de%20tamaño%208.png)

Internamente cada nodo cuenta con una capa de aplicación que genera y recibe paquetes y una capa de transporte que hace dos cosas:

- Mandar hacia algún lado los paquetes provenientes de la capa de aplicación.

- Recibir paquetes de sus vecinos y re-enviarlos al otro vecino o a la capa de aplicación según algún algoritmo.

El propósito del proyecto es comprender los distintos tipos de algoritmos de enrutamiento que se pueden utilizar, y el efecto que tienen sobre el desempeño de la red.

## Algoritmo naive

En la simulación se utiliza una topografía en forma de anillo, para cada vecino se tienen 2 interfaces para comunicación, una para enviar mensajes y otro para recibir. En el algoritmo inicial todos los paquetes se envían a través del vecino a la izquierda del nodo, es decir, todos los paquetes se envían en la dirección contraria al sentido de las agujas del reloj. 

En este algoritmo inicial no hay ningún tipo de lógica para escoger el camino más óptimo, simplemente se envían todos los paquetes de la misma forma sin tomar en cuenta la distancia del enrutador de origen al enrutador del destino.

## Algoritmo mejorado

Para mejorar el enrutamiento se implementó un algoritmo sencillo que aprovecha el hecho de que la topología sea en forma de anillo, el algoritmo se divide en dos partes:

### Reconocimiento de la red

Inicialmente, antes de comenzar la transferencia de paquetes, cada enrutador genera un paquete de reconocimiento de red, este paquete tiene como encabezados el ID del enrutador de destino y la cantidad de saltos que hace el paquete. Cuando un enrutador genera este paquete se coloca a sí mismo como enrutador de destino, e inicia el campo de saltos en 0. Este paquete viaja por toda la red (utilizando el algoritmo naïve), aumentando el campo de saltos cada vez que pasa por un enrutador, y una vez llega al enrutador de destino (que es el mismo que originó el paquete), extrayendo el valor en el campo de saltos va a saber la cantidad de enrutadores que hay en la red.

La simplicidad del reconocimiento de red se da porque se sabe que la topología tiene forma de anillo, además se asume que los enrutadores están en orden, es decir, si hay 8 enrutadores los mismos están ordenados de forma que sus IDs son consecutivos. Se asume esto debido a que incluso si los enrutadores no estuviesen en orden, y por ende se tuviese que calcular la distancia a cada uno, el algoritmo seguiría funcionando de la misma manera, solamente se tendría que hacer un paso extra para conocer la distancia a cada enrutador.

En caso de que fuese necesario conocer las distancias hacia los otros enrutadores, es decir que no se puede asumir un cierto orden, se realizaría de igual forma el primer paso de reconocimiento de red para saber cuantos enrutadores hay en la red, usando esto se sabe cuantas entradas se necesita para la tabla de reenvios (la cual se puede implementar con un arreglo, o un diccionario), luego de esto cada enrutador debe generar un paquete de aviso a la red, este paquete tiene como encabezados el ID del enrutador emisor, la cantidad de saltos que hace el paquete y un campo para la edad. La edad es la cantidad de saltos que puede dar el paquete antes de descartarse, se inicializa con el valor $cantidad de enrutadores - 1$ para que pase por todos los enrutadores de la red (excepto el que crea el paquete) y luego se descarte.

Cada vez que un enrutador recibe uno de estos paquetes, utilizando el campo del enrutador emisor puede registrar en la tabla de reenvíos la entrada correspondiente para el emisor del paquete, y utiliza el campo de saltos para saber a que distancia esta el enrutador emisor. Con estos paquetes todos los enrutadores van a conocer las distancias hacia los otros enrutadores de la red. 

### Enrutamiento de datagramas

En esta parte se escoge el camino más óptimo (es decir el más corto), primero calculamos la distancia como $|emisor - destino|$ (utilizando el número del ID), esto porque se asume el orden de los enrutadores, y se asume que en el anillo se encuentran ordenados en el orden de las agujas del reloj. Con la distancia, al saber que la topología es en forma de anillo (es decir que hay una circunferencia), podemos ver cual es el camino más óptimo observando sí $distancia < \frac{cantidad\ de\ enrutadores}{2}$, si sucede esto, y además el ID del emisor es menor al ID de destino, entonces el camino más corto es contrario a las agujas del reloj, en caso contrario el camino más corto es en la dirección de las agujas del reloj.

En algunos casos enviar un paquete por un camino o el otro es indistinto, porque por ambos caminos el costo del recorrido es el mismo, en este caso se escoge al azar por que camino enviar el paquete, de esta forma se distribuye la carga.

En caso de que se utilizara la idea del aviso a la red para llenar una tabla de reenvíos para cada enrutador es todavía más fácil, como se tiene la distancia exacta, y se sabe que esta distancia es usando el camino en la dirección de las agujas del reloj, se verifica si  $cantidad\ de\ enrutadores - distancia < distancia$, de ser así quiere decir que el camino más corto esta en la dirección contraria a las agujas del reloj, de caso contrario quiere decir que el camino más corto es utilizando el sentido de las agujas del reloj. 

## Resultados

A continuación se realizará una comparación directa en el desempeño de ambos algoritmos en 2 casos de prueba distintos.

El primer caso de prueba se tienen 2 fuentes, `Nodo 0` y `Nodo 3`, y un resumidero, `Nodo 5` en un anillo de tamaño 8, revisando el [diagrama](#introducción) se puede ver que el mejor camino que puede tomar `Nodo 0` es en *sentido reloj*, mientras que para `Nodo 2` es *sentido contra-reloj*.

| Métrica | Algoritmo Naive | Algoritmo mejorado |
|--- |---|---|
| Demora | ![Demora caso 1 naive](Gráficos_parte1_caso1/Demora%20de%20paquetes%20recibidos.svg) |   |
| Tamaño de buffer | ![Tamaño caso 1 naive](Gráficos_parte1_caso1/Tamaos%20de%20buffer.svg) |   |

## Discusiones

Claramente para este proyecto el algoritmo escogido es bastante limitado, el hecho de poder calcular la cantidad de nodos en la red de una manera tan sencilla se debe a que la topología tiene forma de anillo, además sabiendo esto, sabemos que la red forma una circunferencia, por ende calcular el camino más corto también es bastante sencillo, y no hay necesidad de correr algún algoritmo para calcular el camino más corto como _Dijkstra_. 

Para implementar el algoritmo para una red con una topología más general (como la del punto estrella), se debe realizar un algoritmo más complejo, ya que no es tan sencillo saber cuantos enrutadores hay en la red, también sería necesario crear y transmitir paquetes que brinden suficiente información sobre la red, para que cada enrutador pueda crear un grafo interno de la red y correr algún algoritmo como _Dijkstra_ sobre el mismo, de esta forma puede calcular el camino más corto a cada enrutador y colocarlo en una tabla de enrutamiento.

## Referencias

- [OMNeT++ Documentation](https://omnetpp.org/documentation/)
- Andrew S. Tanenbaum (2013) Redes de computadoras. 5ta edición
- Juan Fraire (2021) [Redes y Sistemas Distribuidos - Introducción a OMNeT++](https://www.youtube.com/watch?v=6J_0ZKquNWU&t=1766s) 
- [Understanding .msg files in omnet++ and veins](https://stackoverflow.com/questions/65542635/understanding-msg-files-in-omnet-and-veins)