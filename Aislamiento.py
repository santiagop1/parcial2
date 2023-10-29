import sys
import pygame
import random

# Inicializar Pygame y configuración de la fuente
pygame.init()
pygame.font.init()

# Configuración del juego
NUM_CASILLAS = 8
ANCHO_CASILLA = 50
ALTO_CASILLA = 50
ANCHO = NUM_CASILLAS * ANCHO_CASILLA
ALTO = NUM_CASILLAS * ALTO_CASILLA
ANCHO_VENTANA = ANCHO + 300

# Colores
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (255, 0, 0)
COLOR_AZUL = (0, 0, 255)

# Inicializar pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO))
pygame.display.set_caption("Juego de Aislamiento")

# Inicializar tablero
tablero = [[0] * NUM_CASILLAS for _ in range(NUM_CASILLAS)]

# Funciones del juego
def dibujar_tablero():
    for fila in range(NUM_CASILLAS):
        for columna in range(NUM_CASILLAS):
            pygame.draw.rect(pantalla, COLOR_NEGRO, (columna * ANCHO_CASILLA, fila * ALTO_CASILLA, ANCHO_CASILLA, ALTO_CASILLA), 1)
            if tablero[fila][columna] == 1:
                pygame.draw.circle(pantalla, COLOR_ROJO, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ALTO_CASILLA + ALTO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)
            elif tablero[fila][columna] == 2:
                pygame.draw.circle(pantalla, COLOR_AZUL, (columna * ANCHO_CASILLA + ANCHO_CASILLA // 2, fila * ALTO_CASILLA + ALTO_CASILLA // 2), ANCHO_CASILLA // 2 - 5)

def turno_jugador():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            columna = x // ANCHO_CASILLA
            fila = y // ALTO_CASILLA
            if tablero[fila][columna] == 0:
                tablero[fila][columna] = 1
                return True
    return False

def turno_computadora():
    movimientos_posibles = [(fila, columna) for fila in range(NUM_CASILLAS) for columna in range(NUM_CASILLAS) if tablero[fila][columna] == 0]
    if movimientos_posibles:
        fila, columna = random.choice(movimientos_posibles)
        tablero[fila][columna] = 2

def movimientos_posibles(tablero, jugador):
    movimientos = 0
    for fila in range(NUM_CASILLAS):
        for columna in range(NUM_CASILLAS):
            if tablero[fila][columna] == jugador:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= fila + dy < NUM_CASILLAS and 0 <= columna + dx < NUM_CASILLAS and tablero[fila + dy][columna + dx] == 0:
                            movimientos += 1
    return movimientos

def funcion_heuristica(tablero):
    movimientos_jugador = movimientos_posibles(tablero, 1)
    movimientos_computadora = movimientos_posibles(tablero, 2)
    return movimientos_computadora - movimientos_jugador

def comprobar_victoria(tablero, jugador):
    for fila in tablero:
        if all(casilla == jugador for casilla in fila):
            return True
    for columna in range(NUM_CASILLAS):
        if all(tablero[fila][columna] == jugador for fila in range(NUM_CASILLAS)):
            return True
    return False

def mostrar_puntuaciones():
    fuente = pygame.font.Font(None, 36)
    movimientos_jugador = movimientos_posibles(tablero, 1)
    movimientos_computadora = movimientos_posibles(tablero, 2)
    texto_jugador = fuente.render(f'Jugador: {movimientos_jugador}', True, COLOR_NEGRO)
    texto_computadora = fuente.render(f'Computadora: {movimientos_computadora}', True, COLOR_NEGRO)
    pantalla.blit(texto_jugador, (ANCHO + 10, 50))
    pantalla.blit(texto_computadora, (ANCHO + 10, 100))

# Bucle principal del juego
def juego():
    turno = 0
    ganador = None
    while True:
        pantalla.fill(COLOR_BLANCO)
        dibujar_tablero()
        mostrar_puntuaciones()

        if ganador:
            fuente = pygame.font.Font(None, 74)
            texto_ganador = fuente.render(f'Ganador: {ganador}', True, COLOR_NEGRO)
            pantalla.blit(texto_ganador, (50, ALTO // 2 - 50))
        else:
            if turno % 2 == 0:
                if turno_jugador():
                    if comprobar_victoria(tablero, 1):
                        ganador = "Rojo"
                    else:
                        turno += 1
            else:
                turno_computadora()
                if comprobar_victoria(tablero, 2):
                    ganador = "Azul"
                else:
                    turno += 1

        pygame.display.flip()

# Iniciar el juego
juego()


