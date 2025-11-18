import pygame
import heapq
import time

# -----------------------------
# CONFIGURACIONES GENERALES
# -----------------------------
TAM_CELDA = 30
COLOR_FONDO = (30, 30, 30)

COLOR_INICIO = (0, 255, 0)
COLOR_FIN = (255, 0, 0)
COLOR_OBSTACULO = (0, 0, 0)
COLOR_CAMINO = (0, 255, 255)
COLOR_VISITADO = (100, 100, 255)
COLOR_VACIO = (200, 200, 200)

# -----------------------------
# DIBUJAR TABLERO EN PYGAME
# -----------------------------
def dibujar_tablero(ventana, tablero, inicio, fin, distancias):
    ventana.fill(COLOR_FONDO)

    filas = len(tablero)
    columnas = len(tablero[0])

    for i in range(filas):
        for j in range(columnas):
            x = j * TAM_CELDA
            y = i * TAM_CELDA

            if (i, j) == inicio:
                color = COLOR_INICIO
            elif (i, j) == fin:
                color = COLOR_FIN
            elif tablero[i][j] == float("inf"):
                color = COLOR_OBSTACULO
            elif tablero[i][j] == -1:
                color = COLOR_CAMINO
            elif distancias.get((i, j), float("inf")) != float("inf"):
                color = COLOR_VISITADO
            else:
                color = COLOR_VACIO

            pygame.draw.rect(ventana, color, (x, y, TAM_CELDA, TAM_CELDA))

            # Bordes finos
            pygame.draw.rect(ventana, (50, 50, 50), (x, y, TAM_CELDA, TAM_CELDA), 1)

    pygame.display.update()
    pygame.time.delay(80)  # Velocidad de animación


# -----------------------------
# ALGORITMO DE DIJKSTRA
# -----------------------------
def dijkstra_pygame(ventana, tablero, inicio, fin):
    filas = len(tablero)
    columnas = len(tablero[0])

    distancias = {(i, j): float("inf") for i in range(filas) for j in range(columnas)}
    distancias[inicio] = 0

    pq = [(0, inicio)]
    vino_de = {}

    while pq:
        # Procesar eventos para no congelar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        dist_actual, pos_actual = heapq.heappop(pq)

        if dist_actual > distancias[pos_actual]:
            continue

        # Dibujar paso a paso
        dibujar_tablero(ventana, tablero, inicio, fin, distancias)

        if pos_actual == fin:
            print("¡Camino encontrado!")

            # Reconstruir camino
            paso = fin
            while paso in vino_de:
                if paso != inicio and paso != fin:
                    tablero[paso[0]][paso[1]] = -1
                paso = vino_de[paso]

            # Dibujar camino final
            dibujar_tablero(ventana, tablero, inicio, fin, distancias)
            return

        f, c = pos_actual

        # 4 movimientos
        for df, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nf, nc = f + df, c + dc

            if 0 <= nf < filas and 0 <= nc < columnas:
                if tablero[nf][nc] != float("inf"):
                    nueva_dist = dist_actual + 1
                    vecino = (nf, nc)

                    if nueva_dist < distancias[vecino]:
                        distancias[vecino] = nueva_dist
                        vino_de[vecino] = pos_actual  # FIX correcto
                        heapq.heappush(pq, (nueva_dist, vecino))

    print("No se encontró camino.")


# -----------------------------
# MAIN
# -----------------------------
def main():
    pygame.init()

    ALTO = 10
    ANCHO = 20

    INICIO = (1, 1)
    FIN = (8, 9)

    # Obstáculos como en tu código original
    OBSTACULOS = (
    [(3, i) for i in range(0, 15) if i not in (3,8)] +   # ← abrimos un hueco en la fila 3
    [(6, i) for i in range(5, 20)] +
    [(i, 14) for i in range(4, 6)]
    )

    tablero = [[0 for _ in range(ANCHO)] for _ in range(ALTO)]
    for obs in OBSTACULOS:
        tablero[obs[0]][obs[1]] = float("inf")

    ventana = pygame.display.set_mode((ANCHO * TAM_CELDA, ALTO * TAM_CELDA))
    pygame.display.set_caption("Visualización del algoritmo de Dijkstra")

    dijkstra_pygame(ventana, tablero, INICIO, FIN)

    # Mantener ventana abierta al terminar
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == "__main__":
    main()
