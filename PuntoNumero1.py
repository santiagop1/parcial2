import tkinter as tk
from simpleai.search import astar, SearchProblem

#La función heurística es la suma de las distancias de cada una de las casillas 
# (excluyendo la que se encuentra vacía)
# Definición del estado objetivo y el estado inicial
GOAL = '''1-2-3
4-5-6
7-8-e'''

INITIAL = '''4-5-1
8-3-7
e-6-2'''

# Funciones para convertir entre representaciones de listas y cadenas de texto
def list_to_string(list_):
    return '\n'.join(['-'.join(row) for row in list_])

def string_to_list(string_):
    return [row.split('-') for row in string_.split('\n')]

# Función para encontrar la ubicación de un elemento en la matriz
def find_location(rows, element_to_find):
    for ir, row in enumerate(rows):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic

# Pre-cálculo de las posiciones finales de cada pieza
goal_positions = {number: find_location(string_to_list(GOAL), number) for number in '12345678e'}

# Definición del problema
class EigthPuzzleProblem(SearchProblem):
    def actions(self, state):
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        actions = []
        if row_e > 0: actions.append(rows[row_e - 1][col_e])
        if row_e < 2: actions.append(rows[row_e + 1][col_e])
        if col_e > 0: actions.append(rows[row_e][col_e - 1])
        if col_e < 2: actions.append(rows[row_e][col_e + 1])
        return actions

    def result(self, state, action):
        rows = string_to_list(state)
        row_e, col_e = find_location(rows, 'e')
        row_n, col_n = find_location(rows, action)
        rows[row_e][col_e], rows[row_n][col_n] = rows[row_n][col_n], rows[row_e][col_e]
        return list_to_string(rows)

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        rows = string_to_list(state)
        distance = sum(abs(row_n - goal_positions[number][0]) + abs(col_n - goal_positions[number][1]) 
                       for number, (row_n, col_n) in zip('12345678e', [find_location(rows, number) for number in '12345678e']))
        return distance

# Función para imprimir el estado del tablero de forma bonita
def print_state(description, state):
    print(description)
    print('\n'.join([' '.join(row).replace('e', ' ') for row in string_to_list(state)]))
    print()

# Búsqueda A* para resolver el problema
result = astar(EigthPuzzleProblem(INITIAL))

# Imprimir solución
for action, state in result.path():
    if action is None:
        print_state("Estado Inicial:", state)
    else:
        print_state("Mover el número {}".format(action), state)

class PuzzleGUI(tk.Tk):
    def __init__(self, puzzle_problem, solution_path):
        super().__init__()

        self.puzzle_problem = puzzle_problem
        self.solution_path = solution_path
        self.current_step = 0
        
        self.title("8 Puzzle Solver")
        self.geometry("250x350")

        self.buttons = [[tk.Button(self, width=5, height=2, font=("Arial", 24), command=lambda r=r, c=c: self.on_button_click(r, c)) for c in range(3)] for r in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].grid(row=r, column=c)
        
        self.prev_button = tk.Button(self, text="Anterior", command=self.show_previous_state)
        self.prev_button.grid(row=4, column=0, sticky="ew")
        
        self.next_button = tk.Button(self, text="Siguiente", command=self.show_next_state)
        self.next_button.grid(row=4, column=2, sticky="ew")
        
        self.stats_label = tk.Label(self, text="", font=("Arial", 10))
        self.stats_label.grid(row=5, column=0, columnspan=3, pady=10)
        
        self.update_buttons(INITIAL)
        self.update_stats(INITIAL)

    def on_button_click(self, row, col):
        pass  # No hace nada al hacer clic en un botón del puzzle.

    def update_buttons(self, state):
        rows = string_to_list(state)
        for r in range(3):
            for c in range(3):
                text = rows[r][c] if rows[r][c] != 'e' else ''
                self.buttons[r][c].config(text=text)
        self.update_stats(state)
    
    def update_stats(self, state):
        heuristic_value = self.puzzle_problem.heuristic(state)
        rows = string_to_list(state)
        manhattan_distance = sum(abs(row_n - goal_positions[number][0]) + abs(col_n - goal_positions[number][1]) 
                                 for number, (row_n, col_n) in zip('12345678e', [find_location(rows, number) for number in '12345678e']))
        self.stats_label.config(text=f"Heurística: {heuristic_value}\nDistancia de Manhattan: {manhattan_distance}")

    def show_previous_state(self):
        if self.current_step > 0:
            self.current_step -= 1
            _, state = self.solution_path[self.current_step]
            self.update_buttons(state)

    def show_next_state(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            _, state = self.solution_path[self.current_step]
            self.update_buttons(state)

if __name__ == "__main__":
    problem = EigthPuzzleProblem(INITIAL)
    result = astar(problem)
    
    gui = PuzzleGUI(problem, result.path())
    gui.mainloop()
