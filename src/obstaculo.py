import pygame
import random
from settings import ANCHO_PANTALLA, ALTO_PANTALLA

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, velocidad_inicial):
        super().__init__()
        # 1. Cargar la imagen del obstáculo
        self.image = pygame.image.load("assets/images/obstaculo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
        # Guardamos la velocidad que tendrá al caer
        self.velocidad = velocidad_inicial
        
        # Lo posicionamos inicialmente en un lugar aleatorio arriba
        self.reubicarse()

    def reubicarse(self):
        # Aparece en un punto X aleatorio del ancho de la pantalla
        self.rect.x = random.randint(0, ANCHO_PANTALLA - self.rect.width)
        # Aparece un poco más arriba del borde superior para que se vea entrando al río
        self.rect.y = random.randint(-150, -50)

    def update(self):
        # 2. Hacer que el obstáculo "caiga" simulando la corriente del río
        self.rect.y += self.velocidad