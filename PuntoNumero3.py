import tkinter as tk
from tkinter import ttk
import pandas as pd
import random

# Funciones para la lógica del programa (crear_datos_conferencias y asignar_salas)...


#El algoritmo de recocido simulado es una técnica de optimización heurística que se utiliza para
# encontrar soluciones aproximadas a problemas de optimización combinatoria

# Función para actualizar la interfaz gráfica
def actualizar_interfaz(tree, df_conferencias):
    for i in tree.get_children():
        tree.delete(i)
    estado = asignar_salas(df_conferencias)
    for _, conferencia in estado.iterrows():
        tree.insert('', 'end', values=(conferencia['Nombre'], conferencia['Duracion'], conferencia['Horario Preferido'], conferencia['Sala Asignada'], conferencia['Asientos Disponibles']))

    
# Crear un DataFrame con los datos de las conferencias
def crear_datos_conferencias():
    data = {
        'Nombre': [f'Conferencia {i+1}' for i in range(15)],
        'Duracion': [random.choice([1, 1.5, 2]) for _ in range(15)],
        'Horario Preferido': [random.choice(['Mañana', 'Tarde', 'Noche']) for _ in range(15)],
        'Sala Asignada': [None for _ in range(15)],
        'Asientos Disponibles': [random.randint(50, 200) for _ in range(15)]
    }
    df = pd.DataFrame(data)
    return df

# Función para mostrar la asignación en un formato de texto
def mostrar_asignacion(estado):
    texto = "Nombre | Duracion | Horario Preferido | Sala Asignada | Asientos Disponibles\n"
    texto += "-"*85 + "\n"
    for _, conferencia in estado.iterrows():
        texto += f"{conferencia['Nombre']} | {conferencia['Duracion']} | {conferencia['Horario Preferido']} | {conferencia['Sala Asignada']} | {conferencia['Asientos Disponibles']}\n"
    return texto

# Función para regenerar los datos de las conferencias y actualizar la interfaz
def regenerar_datos(tree):
    global df_conferencias
    df_conferencias = crear_datos_conferencias()
    actualizar_interfaz(tree, df_conferencias)
    
# Función para asignar salas asegurándose de que no haya solapamientos
def asignar_salas(estado):
    salas = ['Sala 1', 'Sala 2', 'Sala 3', 'Sala 4', 'Sala 5', 'Sala 6']
    horarios = ['Mañana', 'Tarde', 'Noche']
    asignaciones = {(sala, horario): None for sala in salas for horario in horarios}

    for i, conferencia in estado.iterrows():
        horario_preferido = conferencia['Horario Preferido']
        sala_asignada = None
        
        for sala in salas:
            if asignaciones[(sala, horario_preferido)] is None:
                sala_asignada = sala
                break

        if sala_asignada is not None:
            estado.at[i, 'Sala Asignada'] = sala_asignada
            asignaciones[(sala_asignada, horario_preferido)] = i
        else:
            sala_random = random.choice(salas)
            horario_random = random.choice(horarios)
            while asignaciones[(sala_random, horario_random)] is not None:
                sala_random = random.choice(salas)
                horario_random = random.choice(horarios)
            
            estado.at[i, 'Sala Asignada'] = sala_random
            asignaciones[(sala_random, horario_random)] = i

    return estado

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Conferencias")

# Configurar el estilo del Treeview
style = ttk.Style(root)
style.configure('Custom.Treeview', rowheight=30)
style.configure('Custom.Treeview.Heading', font=('Arial', 12, 'bold'))

# Crear el Treeview
columns = ('Nombre', 'Duracion', 'Horario Preferido', 'Sala Asignada', 'Asientos Disponibles')
tree = ttk.Treeview(root, columns=columns, show='headings', style='Custom.Treeview')
tree.heading('Nombre', text='Nombre')
tree.heading('Duracion', text='Duracion')
tree.heading('Horario Preferido', text='Horario Preferido')
tree.heading('Sala Asignada', text='Sala Asignada')
tree.heading('Asientos Disponibles', text='Asientos Disponibles')
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Crear un botón para generar las asignaciones
button_generar = ttk.Button(root, text="Generar", command=lambda: actualizar_interfaz(tree, df_conferencias))
button_generar.pack(pady=10)

# Crear un botón para regenerar los datos y actualizar la interfaz
button_regenerar = ttk.Button(root, text="Regenerar Datos", command=lambda: regenerar_datos(tree))
button_regenerar.pack(pady=10)

# Inicializar los datos de las conferencias
df_conferencias = crear_datos_conferencias()

# Mostrar la ventana
root.mainloop()