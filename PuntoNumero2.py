import tkinter as tk
import sys
import random
import string

# Parámetros del algoritmo genético
TAMAÑO_POBLACION = 100
TASA_MUTACION = 0.05
NUM_GENERACIONES = 1000
OBJETIVO = "HELLO WORD"
ELITISMO = True

# Inicializa la ventana principal
root = tk.Tk()
root.title("Algoritmo Genético")

# Configuración del estilo
estilo_texto = ('Arial', 12)
estilo_boton = ('Arial', 14, 'bold')

# Crea un widget de texto para mostrar la salida
text_widget = tk.Text(root, height=20, width=50, font=estilo_texto, wrap='word')
text_widget.pack(pady=20)

# Funciones del algoritmo genético
def cadena_aleatoria():
    return ''.join(random.choice(string.ascii_uppercase + ' ') for _ in range(len(OBJETIVO)))

def calcular_aptitud(cadena):
    return sum(1 for c1, c2 in zip(cadena, OBJETIVO) if c1 == c2)

def seleccionar_padre(poblacion, aptitudes):
    total_aptitud = sum(aptitudes)
    seleccion = random.uniform(0, total_aptitud)
    suma = 0
    for individuo, aptitud in zip(poblacion, aptitudes):
        suma += aptitud
        if suma >= seleccion:
            return individuo
    return poblacion[-1]

def cruzar(padre1, padre2):
    punto = random.randint(0, len(padre1) - 1)
    return padre1[:punto] + padre2[punto:]

def mutar(cadena):
    if random.random() < TASA_MUTACION:
        posicion = random.randint(0, len(cadena) - 1)
        caracter = random.choice(string.ascii_uppercase + ' ')
        return cadena[:posicion] + caracter + cadena[posicion+1:]
    return cadena

# Redirige la salida estándar para escribir en el widget de texto
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

sys.stdout = TextRedirector(text_widget)

# Función para ejecutar el algoritmo genético y actualizar la interfaz gráfica
def run_genetic_algorithm():
    poblacion = [cadena_aleatoria() for _ in range(TAMAÑO_POBLACION)]
    for generacion in range(NUM_GENERACIONES):
        aptitudes = [calcular_aptitud(individuo) for individuo in poblacion]
        
        mejor_aptitud = max(aptitudes)
        mejor_individuo = poblacion[aptitudes.index(mejor_aptitud)]
        
        print(f"Generación {generacion} - Mejor aptitud: {mejor_aptitud} - Cadena: {mejor_individuo}")
        
        if mejor_aptitud == len(OBJETIVO):
            print(f"¡Solución encontrada en la generación {generacion}!")
            break
        
        if ELITISMO:
            elite = [mejor_individuo]
        else:
            elite = []
        
        nuevos_padres = [seleccionar_padre(poblacion, aptitudes) for _ in range(TAMAÑO_POBLACION - len(elite))]
        
        if len(nuevos_padres) % 2 != 0:
            nuevos_padres.append(random.choice(nuevos_padres))
        
        poblacion = elite + [mutar(cruzar(nuevos_padres[i], nuevos_padres[i+1])) for i in range(0, len(nuevos_padres), 2)]
    else:
        print("No se encontró la solución en el número de generaciones definido.")

# Crea un botón para iniciar el algoritmo genético
run_button = tk.Button(root, text="Iniciar Algoritmo Genético", command=run_genetic_algorithm, font=estilo_boton)
run_button.pack(pady=10)

# Inicia el bucle principal de la interfaz gráfica
root.mainloop()
