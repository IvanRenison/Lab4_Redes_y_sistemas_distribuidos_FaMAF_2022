import os
import shutil
import sys

def os_system_with_print(command):
    print(f"$ {command}")
    return os.system(command)

def shutil_move_with_print(src, dst):
    print(f"$ mv '{src}' '{dst}'")
    shutil.move(src, dst)

carpeta_código = "src"

# Parametros variables para configurar en el .ini
parametros_variables: dict = {
    interArrivalTime:
        f"Network.node[{{0, 1, 2, 3, 4, 6, 7}}].app.interArrivalTime = exponential({interArrivalTime})"
    for interArrivalTime in list(map(lambda x: round(0.02 + x * 0.02, ndigits=3), range(750)))
}

parametros_gráficos_detallados = [1.0]

# Chequear que los parametros_gráficos_detallados sean claves de parametros_variables
assert all(map(lambda x: x in parametros_variables.keys(), parametros_gráficos_detallados))

def carpeta_resultados(nombre_simulación):
    return f"Resultados_{nombre_simulación}"

def carpeta_resultados_parametro(parametro, nombre_simulación):
    return f"{carpeta_resultados(nombre_simulación)}/{parametro}"

def carpeta_gráficos(nombre_simulación):
    return f"Gráficos_{nombre_simulación}"

def correr_simulaciones(nombre):
    """
        Corre las simulaciones, usa el argumento para el nombre de la carpeta de los resultados
    """
    # Hacer make
    os_system_with_print(f"make --directory '{carpeta_código}'")

    ejecutable = f"{carpeta_código}/{carpeta_código}" # El make hace que el ejecutable tenga el mismo nombre que la carpeta en la que está

    omnet_ini = f"{carpeta_código}/omnetpp.ini"
    extra_ini = f"{carpeta_código}/extra.ini"

    omnet_output = f"{carpeta_código}/results"

    # Chequer que existan los archivos y carpetas necesarios
    if not os.path.exists(ejecutable):
        raise Exception(f"No se encuentra '{ejecutable}'")
    if not os.path.exists(omnet_ini):
        raise Exception(f"No se encuentra '{omnet_ini}'")

    # Si la carpeta ya existe eliminarla, para asegurar que no queden resultados viejos
    if os.path.exists(carpeta_resultados(nombre)):
        shutil.rmtree(carpeta_resultados(nombre))

    # Crear la carpeta para resultados
    os.mkdir(carpeta_resultados(nombre))

    # Ejecutar lsa simulaciones
    for n in parametros_variables.keys():
        parametro = parametros_variables[n]

        # Poner en un archivo la configuración del generationInterval
        with open(extra_ini, "w") as f_extra_ini:
            f_extra_ini.write(parametro)

        x = os_system_with_print(f"./{ejecutable} -f {omnet_ini} -f {extra_ini} -n {carpeta_código} -u Cmdenv")
        if x != 0:
            raise Exception(f"Error al ejecutar simulación '{ejecutable}'")

        # Mover los resultados a la carpeta correcta
        shutil_move_with_print(omnet_output, carpeta_resultados_parametro(n, nombre))
    
    os.remove(extra_ini)

def exportar_gráficos(nombre: str):
    """
        Crea los gráficos, usa el argumento para el nombre de la carpeta de los resultados
    """
    general_anf = "General.anf"

    # Chequear que exista el archivo anf
    if not os.path.exists(general_anf):
        raise Exception(f"No se encuentra '{general_anf}'")

    # crear la carpeta si no existe
    if not os.path.exists(carpeta_gráficos(nombre)):
        os.mkdir(carpeta_gráficos(nombre))

    with open(general_anf, "r") as f_general_anf:
        lineas = f_general_anf.readlines()

    # Verificar que las lineas que se van a modificar sean de adentro del input
    assert lineas[2] == f"    <inputs>\n" and lineas[5] == f"    </inputs>\n"

    for n in parametros_gráficos_detallados:
        # modificar <input pattern="..."/> en general_anf
        lineas[3] = f'        <input pattern="{carpeta_resultados_parametro(n, nombre)}/General-*.vec"/>\n'
        lineas[4] = f'        <input pattern="{carpeta_resultados_parametro(n, nombre)}/General-*.sca"/>\n'
        with open(general_anf, "w") as f_general_anf:
            # Escribir las lineas
            f_general_anf.writelines(lineas)

        # Crear los gráficos
        x = os_system_with_print(f"opp_charttool imageexport {general_anf}")
        assert x == 0

        # Mover los gráficos a la carpeta de gráficos
        svg_files = filter(lambda x: x.endswith(".svg"), os.listdir())
        for svg_file in svg_files:
            shutil_move_with_print(svg_file, f"{carpeta_gráficos(nombre)}/{svg_file[:-4]} (parametro={n}).svg")

def gráficos_matplotlib(nombre_simulacion: str):
    """
        Crea los gráficos de `gráficos.py`
    """
    # Crear json
    archivo_json = f"datos_{nombre_simulacion}.json"
    x = os.system(f"opp_scavetool export {carpeta_resultados(nombre_simulacion)}/*/*.sca -o {archivo_json}")
    assert x == 0

    # Llamar a la función que hace los gráficos
    import gráficos
    gráficos.gráficos(archivo_json, nombre_simulacion)


def main(args: list):
    if len(args) != 1:
        print("USO: python3 runTest.py NOMBRE_SIMULACION")
        raise Exception("Argumentos inválidos")
    nombre_simulación: str = args[0]
    correr_simulaciones(nombre_simulación)
    exportar_gráficos(nombre_simulación)
    gráficos_matplotlib(nombre_simulación)

if __name__ == "__main__":
    # Obtener argumentos
    args = sys.argv[1:]
    main(args)

