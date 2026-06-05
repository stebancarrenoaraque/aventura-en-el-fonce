import pygame
from settings import ANCHO_PANTALLA, ALTO_PANTALLA, BLANCO, NEGRO

class HUD:
    def __init__(self):
        # Inicializamos la fuente por defecto de Pygame
        # (Si tienes un archivo .ttf en assets, puedes cambiar None por la ruta del archivo)
        self.fuente_puntos = pygame.font.Font(None, 36)
        self.fuente_game_over = pygame.font.Font(None, 50)

    def mostrar_puntos(self, pantalla, puntuacion):
        # Renderizar el texto de los puntos (Texto, Antialiasing, Color)
        texto = self.fuente_puntos.render(f"Puntos: {puntuacion}", True, BLANCO)
        # Lo dibujamos en la esquina superior izquierda con un pequeño margen
        pantalla.blit(texto, (20, 20))

    def mostrar_game_over(self, pantalla, puntuacion):
        # Fondo oscuro semitransparente o un rectángulo para que se note el Game Over
        pantalla.fill(NEGRO)
        
        # Texto de Fin de Juego
        texto_go = self.fuente_game_over.render("¡GAME OVER!", True, (255, 0, 0))
        rect_go = texto_go.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 30))
        
        # Texto de puntuación final
        texto_puntos = self.fuente_puntos.render(f"Puntuación Final: {puntuacion}", True, BLANCO)
        rect_puntos = texto_puntos.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 30))
        
        # Texto para salir
        texto_salir = self.fuente_puntos.render("Presiona ESC para salir", True, (150, 150, 150))
        rect_salir = texto_salir.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 90))
        
        # Dibujar los textos en la pantalla
        pantalla.blit(texto_go, rect_go)
        pantalla.blit(texto_puntos, rect_puntos)
        pantalla.blit(texto_salir, rect_salir)