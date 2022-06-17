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

## Algoritmo mejorado

### Reconocimiento de la red

### Enrutamiento de datagramas

## Resultados
