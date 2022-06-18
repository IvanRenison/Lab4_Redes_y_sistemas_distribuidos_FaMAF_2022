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

El propósito del proyecto es comprender los distintos tipos de algoritmos de enrutamiento que se pueden utilizar y el efecto que tienen sobre el desempeño de la red.

## Algoritmo naive

En el algoritmo inicial todos los paquetes se envían a través del vecino a la izquierda del nodo, es decir, todos los paquetes se envían en la dirección contraria al sentido de las agujas del reloj.

En este algoritmo inicial no hay ningún tipo de lógica para escoger el camino más óptimo, simplemente se envían todos los paquetes de la misma forma sin tomar en cuenta la distancia del enrutador de origen al enrutador del destino.

## Algoritmo mejorado

Para mejorar el enrutamiento se implementó un algoritmo sencillo que aprovecha el hecho de que la topología sea en forma de anillo, el algoritmo se divide en dos partes:

### Reconocimiento de la red

Inicialmente, antes de comenzar la transferencia de paquetes, cada enrutador genera un paquete de reconocimiento de red, este paquete tiene como encabezados el ID del enrutador de destino y la cantidad de saltos que hace el paquete. Cuando un enrutador genera este paquete se coloca a sí mismo como enrutador de destino, e inicia el campo de saltos en 0. Este paquete viaja por toda la red (utilizando el algoritmo naive), aumentando el campo de saltos cada vez que pasa por un enrutador, y una vez llega al enrutador de destino (que es el mismo que originó el paquete), extrayendo el valor en el campo de saltos va a saber la cantidad de enrutadores que hay en la red.

La simplicidad del reconocimiento de red se da porque se sabe que la topología tiene forma de anillo, además se asume que los enrutadores están en orden, es decir, si hay 8 enrutadores los mismos están ordenados de forma que sus IDs son consecutivos. Se trabaja con los enrutadores ordenados debido a que incluso si los enrutadores no estuviesen en orden, y por ende se tuviese que calcular la distancia a cada uno, el algoritmo seguiría funcionando de la misma manera, solamente se tendría que hacer un paso extra para conocer la distancia a cada enrutador.

### Enrutamiento de datagramas

En esta parte se escoge el camino más corto, primero calculamos la distancia como `distancia = |emisor - destino|` (utilizando el número del ID porque los enrutadores están ordenados en el sentido de las agujas del reloj). Con la distancia,  sí `distancia < cantidad de enrutadores/2` entonces el camino mas corto es el el sentido contrario a las agujas del reloj, si `distancia > cantidad de enrutadores/2` el camino mas corto es en el sentido de las agujas del reloj y si ambos son iguales, la distancia es le misma en ambos sentidos y por ende se escoge al azar por que camino enviar el paquete, de forma que se distribuye la carga.

## Resultados

A continuación se realizará una comparación directa en el desempeño de ambos algoritmos en 2 casos de prueba distintos.

Las métricas que seran analizadas son el tiempo que tarda cada nodo en recibir paquetes (Demora) y los tamaños que alcanza cada buffer de los nodos (Tamaños de buffer) durante el tiempo de simulación.

Pero primero, recordemos lo que hace cada algoritmo.

En resumidas cuentas, el algoritmo naive siempre mandará sus paquetes en *sentido reloj*, mientras que el algoritmo mejorado primero reconocerá la red y luego mandará cada paquete por el mejor camino.

### Caso de estudio 1

El primer caso de prueba se tienen 2 fuentes, `Nodo 0` y `Nodo 3`, y un resumidero, `Nodo 5` en un anillo de tamaño 8, revisando el [diagrama](#introducción) se puede ver que el mejor camino que puede tomar `Nodo 0` es en *sentido reloj*, mientras que para `Nodo 2` es *sentido contra-reloj*.

| Algoritmo Naive                                                                      | Algoritmo mejorado                                                                      |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| ![Demora caso 1 naive](Gráficos_parte1_caso1/Demora%20de%20paquetes%20recibidos.svg) | ![Demora caso 1 mejorado](Gráficos_parte2_caso1/Demora%20de%20paquetes%20recibidos.svg) |
| ![Tamaño caso 1 naive](Gráficos_parte1_caso1/Tamaos%20de%20buffer.svg)               | ![Tamaño caso 1 mejorado](Gráficos_parte2_caso1/Tamaos%20de%20buffer.svg)               |

Como se puede observar, la demora máxima en el algoritmo mejorado es un 10% de la del algoritmo naive. En principio esto se debe a que en el algoritmo naive no se elige la mejor ruta para mandar desde `Nodo 2` hasta `Nodo 5`, pero también sucede que en un tramo de la ruta se mandarán paquetes provenientes tanto de `Nodo 0`, como de `Nodo 2`, lo cuál genera mucho mas retraso.

Para los tamaños de buffer se puede observar un fenómeno generado por la misma causa, en `Nodo 0` se generan paquetes listos para ser enviados, pero también es la ruta tomada por todos los paquetes enviados por `Nodo 5`, como consecuencia, el buffer de `Nodo 0` alcanza un tamaño muy elevado.

Esto no es un problema para el algoritmo mejorado, ya que, como ambos nodos tienen distintos caminos óptimos no habrá ningún camino en común entre los paquetes generados por `Nodo 0` y `Nodo 2`, en consecuencia el máximo tamaño de buffer alcanzado por el algoritmo mejorado es el 5% de lo alcanzado por el algoritmo naive.

Hasta ahora se mostró el diferente impacto en la red que genera cada algoritmo, en un caso simple, pero ¿Se contemplará un comportamiento parecido en un caso mas complejo?

### Caso de estudio 2

Ahora, `Nodo 5` seguirá siendo el único receptor en la red, pero todos los demás nodos serán emisores, como consecuencia esperable los buffers de los nodos se verán mucho mas ocupados que antes.

| Algoritmo Naive                                                                      | Algoritmo mejorado                                                                      |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| ![Demora caso 1 naive](Gráficos_parte1_caso2/Demora%20de%20paquetes%20recibidos.svg) | ![Demora caso 1 mejorado](Gráficos_parte2_caso2/Demora%20de%20paquetes%20recibidos.svg) |
| ![Tamaño caso 1 naive](Gráficos_parte1_caso2/Tamaos%20de%20buffer.svg)               | ![Tamaño caso 1 mejorado](Gráficos_parte2_caso2/Tamaos%20de%20buffer.svg)               |

Esta vez se puede contemplar que las escalas son mucho mas comparables a simple vista. En cuanto a la demora, se puede observar que los mejores casos con mínima demora son casi iguales, eso tiene sentido porque ambos tienen nodos adyacentes al destino, en el algoritmo mejorado se tienen mas valores rondando por los mejores casos porque habrán mas nodos cercanos al destino que usarán la ruta optima.

Para los tamaños de buffer se puede ver que el algoritmo mejorado aprovecha mejor los buffers, en general, por los que transitaba mayor tráfico experimentan mucha menos carga, y los nodos por donde circulaban pocos paquetes poseen ahora una mayor carga.

## Discusiones

Claramente para este proyecto el algoritmo escogido es bastante limitado, el hecho de poder calcular la cantidad de nodos en la red de una manera tan sencilla se debe a que la topología tiene forma de anillo, además sabiendo esto, sabemos que la red forma una circunferencia, por ende calcular el camino más corto también es bastante sencillo, y no hay necesidad de correr algún algoritmo para calcular el camino más corto como _Dijkstra_.

En la implementación, los enrutadores están enumerados, y en el anillo están en orden, por lo que el escaneo de la red es mas simple. Si no estubieran en orden, para hacer el reconocimiento de la red, se realizaría igual, solo que el paquete de reconocimiento de la red, ademas de servir para que el envidador averigüe el tamaño del anillo, serviría para que cada nodo por el que va pasando sepa la distancia que hay hasta el envidador por ese lado (y después cuando sepa el tamaño del anillo puede calcular cual es la distancia hacía el otro lado).

Para implementar el algoritmo para una red con una topología más general (como la del punto estrella), se debe realizar un algoritmo más complejo, ya que no es tan sencillo saber cuantos enrutadores hay en la red, también sería necesario crear y transmitir paquetes que brinden suficiente información sobre la red, para que cada enrutador pueda crear un grafo interno de la red y correr algún algoritmo como _Dijkstra_ sobre el mismo, de esta forma puede calcular el camino más corto a cada enrutador y colocarlo en una tabla de enrutamiento.

## Referencias

- [OMNeT++ Documentation](https://omnetpp.org/documentation/)
- Andrew S. Tanenbaum (2013) Redes de computadoras. 5ta edición
- Juan Fraire (2021) [Redes y Sistemas Distribuidos - Introducción a OMNeT++](https://www.youtube.com/watch?v=6J_0ZKquNWU&t=1766s)
- [Understanding .msg files in omnet++ and veins](https://stackoverflow.com/questions/65542635/understanding-msg-files-in-omnet-and-veins)