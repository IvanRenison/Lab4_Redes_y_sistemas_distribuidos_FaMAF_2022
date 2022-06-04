import os
import shutil
import sys

carpeta_código = "src"

def carpeta_resultados(nombre_simulación: str):
    return f"Resultados_{nombre_simulación}"

def carpeta_gráficos(nombre_simulación: str):
    return f"Gráficos_{nombre_simulación}"

def correr_simulaciones(nombre: str):
    """
        Corre las simulaciones, usa el argumento para el nombre de la carpeta de los resultados
    """
    ejecutable = f"{carpeta_código}{os.sep}{carpeta_código}" # El make hace que el ejecutable tenga el mismo nombre que la carpeta en la que está
    if os.name == "nt": # En windows agregar .exe
        ejecutable += ".exe"

    omnet_ini = f"{carpeta_código}{os.sep}omnetpp.ini"

    omnet_output = f"{carpeta_código}{os.sep}results"

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

    # Ejecutar la simulación
    x = os.system(f".{os.sep}{ejecutable} -f {omnet_ini} -n {carpeta_código} -u Cmdenv")
    if x != 0:
        raise Exception(f"Error al ejecutar simulación '{ejecutable}'")

    # Mover los resultados a la carpeta correcta
    shutil.move(omnet_output, carpeta_resultados(nombre))

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
    assert lineas[2] == f"    <inputs>{os.linesep}" and lineas[5] == f"    </inputs>{os.linesep}"

    # modificar <input pattern="..."/> en general_anf
    lineas[3] = f'        <input pattern="{carpeta_resultados(nombre)}/results/General-*.vec"/>{os.linesep}'
    lineas[4] = f'        <input pattern="{carpeta_resultados(nombre)}/results/General-*.sca"/>{os.linesep}'
    with open(general_anf, "w") as f_general_anf:
        # Escribir las lineas
        f_general_anf.writelines(lineas)

    # Crear los gráficos
    x = os.system(f"opp_charttool imageexport {general_anf}")
    assert x == 0

    # Mover los gráficos a la carpeta de gráficos
    svg_files = filter(lambda x: x.endswith(".svg"), os.listdir())
    for svg_file in svg_files:
        shutil.move(svg_file, f"{carpeta_gráficos(nombre)}{os.sep}{svg_file}")


def main(args: list):
    if len(args) != 1:
        print("USO: python3 runTest.py NOMBRE_SIMULACION")
        raise Exception("Argumentos inválidos")
    nombre_simulación: str = args[0]
    correr_simulaciones(nombre_simulación)
    exportar_gráficos(nombre_simulación)

if __name__ == "__main__":
    # Obtener argumentos
    args = sys.argv[1:]
    main(args)

