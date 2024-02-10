import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar el tamaño de la ventana
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Posición inicial de la robotina
robotina_pos = [200, 200]

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Eventos del teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robotina_pos[0] -= 10  # Mover a la izquierda
            if event.key == pygame.K_RIGHT:
                robotina_pos[0] += 10  # Mover a la derecha
            if event.key == pygame.K_UP:
                robotina_pos[1] -= 10  # Mover hacia arriba
            if event.key == pygame.K_DOWN:
                robotina_pos[1] += 10  # Mover hacia abajo
    
    # Rellenar el fondo
    screen.fill(BLACK)
    
    # Dibujar la robotina
    pygame.draw.rect(screen, WHITE, pygame.Rect(robotina_pos[0], robotina_pos[1], 20, 20))
    
    # Actualizar la ventana
    pygame.display.flip()

pygame.quit()
