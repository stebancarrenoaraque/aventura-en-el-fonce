import pygame
from settings import ANCHO_PANTALLA, ALTO_PANTALLA, VELOCIDAD_CANOA

class Canoa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 1. Cargar la imagen desde la 
        self.image = pygame.image.load("assets/images/canoa.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (50, 80))
        
        # 2. Obtener el rectángulo de colisión y posicionarlo
        self.rect = self.image.get_rect()
        
        # Posición inicial: Abajo en el centro de la pantalla
        self.rect.centerx = ANCHO_PANTALLA // 2
        self.rect.bottom = ALTO_PANTALLA - 30

    def update(self):
        # 3. Detectar las teclas presionadas
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VELOCIDAD_CANOA
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VELOCIDAD_CANOA
            
        # 4. Límites de la pantalla (Para que la canoa no se salga del Río Fonce)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA