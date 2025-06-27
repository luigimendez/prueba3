import ipywidgets as widgets
from IPython.display import display, clear_output
import random, math, time

salida = widgets.Output()

# Figuras por nivel

def generar_triangulo():
    base = random.randint(4, 10)
    altura = random.randint(3, 8)
    area = round((base * altura) / 2, 2)
    pasos = f"Área = (base * altura) / 2 = ({base} * {altura}) / 2 = {area}"
    return "Triángulo", f"Base = {base}, Altura = {altura}", area, pasos

def generar_cuadrado():
    lado = random.randint(3, 10)
    area = round(lado ** 2, 2)
    pasos = f"Área = lado² = {lado}² = {area}"
    return "Cuadrado", f"Lado = {lado}", area, pasos

def generar_rectangulo():
    base = random.randint(4, 10)
    altura = random.randint(3, 8)
    area = round(base * altura, 2)
    pasos = f"Área = base * altura = {base} * {altura} = {area}"
    return "Rectángulo", f"Base = {base}, Altura = {altura}", area, pasos

def generar_circulo():
    radio = random.randint(2, 6)
    area = round(math.pi * radio ** 2, 2)
    pasos = f"Área = π * r² = π * {radio}² = π * {radio**2} ≈ {area}"
    return "Círculo", f"Radio = {radio}", area, pasos

def generar_trapecio():
    base1 = random.randint(3, 7)
    base2 = random.randint(4, 9)
    altura = random.randint(3, 6)
    area = round(((base1 + base2) * altura) / 2, 2)
    pasos = f"Área = ((base1 + base2) * altura) / 2 = (({base1} + {base2}) * {altura}) / 2 = {area}"
    return "Trapecio", f"Base1 = {base1}, Base2 = {base2}, Altura = {altura}", area, pasos

# Niveles
niveles = {
    1: [generar_triangulo, generar_cuadrado],
    2: [generar_rectangulo],
    3: [generar_circulo, generar_trapecio]
}

# Variables globales

nivel = 1
aciertos_consecutivos = 0
puntuacion = 0
tiempos = []
ejercicio_actual = {}
inicio_tiempo = 0

# Widgets

entrada_area = widgets.Text(placeholder="Ingresa el área")
btn_verificar = widgets.Button(description="✅ Verificar")
btn_pasos = widgets.Button(description="📘 Ver pasos")
btn_siguiente = widgets.Button(description="🔄 Siguiente")
lbl_estado = widgets.Label()

# Lógica principal

def nuevo_ejercicio(_=None):
    global ejercicio_actual, inicio_tiempo
    gen = random.choice(niveles[nivel])
    nombre, datos, area, pasos = gen()
    ejercicio_actual = {
        "nombre": nombre,
        "datos": datos,
        "area": area,
        "pasos": pasos
    }
    entrada_area.value = ""
    inicio_tiempo = time.time()
    salida.clear_output()
    with salida:
        print(f"📐 Figura: {nombre}")
        print(f"🔢 Datos: {datos}")

def verificar(_):
    global puntuacion, aciertos_consecutivos, nivel
    try:
        respuesta = float(entrada_area.value)
        tiempo = round(time.time() - inicio_tiempo, 2)
        tiempos.append(tiempo)
        salida.clear_output()
        with salida:
            print(f"📐 Figura: {ejercicio_actual['nombre']}")
            print(f"🔢 Datos: {ejercicio_actual['datos']}")
            print(f"⏱️ Tiempo de respuesta: {tiempo} s")
            if abs(respuesta - ejercicio_actual['area']) < 0.5:
                puntuacion += 10
                aciertos_consecutivos += 1
                print("✅ ¡Correcto!")
                if aciertos_consecutivos >= 3 and nivel < 3:
                    nivel += 1
                    print(f"🚀 Nivel aumentado a {nivel}")
                    aciertos_consecutivos = 0
            else:
                aciertos_consecutivos = 0
                print(f"❌ Incorrecto. El área correcta es ≈ {ejercicio_actual['area']}")
            lbl_estado.value = f"🎯 Puntos: {puntuacion} | Nivel: {nivel} | Tiempo promedio: {round(sum(tiempos)/len(tiempos), 2)} s"
    except:
        with salida:
            print("⚠️ Ingresa un número válido.")

def mostrar_pasos(_):
    with salida:
        print("📘 Pasos para resolver:")
        print(ejercicio_actual['pasos'])

# Conexión de eventos

btn_verificar.on_click(verificar)
btn_pasos.on_click(mostrar_pasos)
btn_siguiente.on_click(nuevo_ejercicio)

# Interfaz

display(salida)
display(entrada_area)
display(widgets.HBox([btn_verificar, btn_pasos, btn_siguiente]))
display(lbl_estado)

nuevo_ejercicio()
