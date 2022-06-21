import json
from typing import Tuple
import matplotlib.pyplot as plt

import runSimulations


# (json_data: dict[str,]) -> dict[float, (int, int)]
def obtener_paquetes_enviadosYRecibidos(json_data: dict) -> dict:
    """
        Obtiene los paquetes enviados en cada simulación
        Devuelve un diccionario con clave intervalo generación y valor (paquetes enviados, paquetes recibidos)
    
        Toma la json_data que fue generado por omnet con `opp_scavetool` (y prosesada con json.loads)
    """
    res = {}
    for sim in json_data.values():

        interArrivalTime_text = sim["config"][4]["Network.node[*].app.interArrivalTime"]
        # Chequear que se haya obtenido mas o menos lo correcto
        assert interArrivalTime_text.startswith("exponential(") and interArrivalTime_text.endswith(")")
        interArrivalTime_number_text = interArrivalTime_text[12:-1]
        interArrivalTime = float(interArrivalTime_number_text)

        # Obtener suma de paquetes enviados y recividos
        paquetes_recibidos = 0
        paquetes_enviados = 0
        for module in sim["scalars"]:   
            if module["name"] == "Sent packets":
                paquetes_enviados += int(module["value"])
            if module["name"] == "Received packets":
                paquetes_recibidos += int(module["value"])

        res[interArrivalTime] = (paquetes_enviados, paquetes_recibidos)
    
    return res

# (datos: dict[float, (int, int)]) -> Tuple[list[float], list[float]]
def datos_gráfico_aprovechamiento(datos: dict) -> Tuple:
    """
        Devuelve una lista para hacer un gráfico con:
            Eje x = intervalo de generación
            Eje y = paquetes recibidos/paquetes enviados
    """
    # ordenar por clave
    xys = sorted(datos.items(), key=lambda x: x[0])
    res = ([], [])
    for intervalo, (paquetes_enviados, paquetes_recibidos) in xys:
        res[0].append(intervalo)
        res[1].append(paquetes_recibidos/paquetes_enviados)
    return res

# (xs: list(float), ys: list(float))
def generar_gráfico_GI_VS_aprovechamiento(xs: list, ys: list, nombre_simulación: str):
    plt.clf()
    plt.plot(xs, ys)
    plt.xlabel("Intervalo de generación")
    plt.ylabel("paquetes recibidos / paquetes enviados")
    plt.grid()
    plt.title("Gráfico de intervalo de generación vs aprovechamiento")
    plt.savefig(f"{runSimulations.carpeta_gráficos(nombre_simulación)}/Gráfico de intervalo de generación vs aprovechamiento.svg")


def gráficos(json_file: str, nombre_simulación: str):
    with open(json_file) as f:
        json_data = json.load(f)
    datos = obtener_paquetes_enviadosYRecibidos(json_data)
    xs, ys = datos_gráfico_aprovechamiento(datos)
    xs = [0] + list(xs) 
    ys = [0] + list(ys)
    generar_gráfico_GI_VS_aprovechamiento(xs, ys, nombre_simulación)





