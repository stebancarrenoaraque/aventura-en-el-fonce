import pygame
import sys
from settings import ANCHO_PANTALLA, ALTO_PANTALLA, FPS, VELOCIDAD_INICIAL_RIO, VELOCIDAD_FONDO
from src.canoa import Canoa
from src.obstaculo import Obstaculo
from src.hud import HUD

def main():
    # 1. INICIALIZAR PYGAME Y AUDIO
    pygame.init()
    pygame.mixer.init()
    
    # 2. CONFIGURAR LA VENTANA Y EL RELOJ
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Aventura en el Fonce")
    reloj = pygame.time.Clock()
    
    # 3. ESTADOS DEL JUEGO
    ejecutando = True
    estado = "JUGANDO"
    puntuacion = 0
    velocidad_actual_rio = VELOCIDAD_INICIAL_RIO
    
    # 4. CARGAR IMAGEN DE FONDO (Río Fonce)
    try:
        # Cargamos el fondo y lo escalamos al tamaño exacto de la pantalla
        imagen_fondo = pygame.image.load("assets/images/FONDO.png").convert()
        imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    except pygame.error:
        print("Advertencia: No se encontró assets/images/FONDO.png. Se usará un fondo azul plano.")
        imagen_fondo = None

    # Variables para controlar las posiciones de las dos imágenes de fondo
    fondo_y1 = 0
    fondo_y2 = -ALTO_PANTALLA
    
    # 5. INSTANCIAR COMPONENTES
    canoa = Canoa()
    grupo_jugador = pygame.sprite.GroupSingle(canoa)
    grupo_obstaculos = pygame.sprite.Group()
    hud = HUD()
    
    for _ in range(3):
        nuevo_obstaculo = Obstaculo(velocidad_actual_rio)
        grupo_obstaculos.add(nuevo_obstaculo)
        
    # CARGAR EFECTOS DE SONIDO
    try:
        sonido_punto = pygame.mixer.Sound("assets/sounds/PUNTO.mp3")
        sonido_choque = pygame.mixer.Sound("assets/sounds/CHOQUE.mp3")
        sonido_punto.set_volume(0.1)
        sonido_choque.set_volume(0.5)
    except pygame.error:
        sonido_punto = None
        sonido_choque = None

    # 6. BUCLE PRINCIPAL (Game Loop)
    while ejecutando:
        
        # --- A. EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            if estado == "GAME_OVER" and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
        
# --- B. LÓGICA DEL JUEGO ---
        if estado == "JUGANDO":
            # SCROLL INFINITO SINCRONIZADO: El fondo avanza a la par de la velocidad del río
            fondo_y1 += velocidad_actual_rio
            fondo_y2 += velocidad_actual_rio
            
            # Reposicionar fondos al salir de la pantalla para crear el bucle visual de agua
            if fondo_y1 >= ALTO_PANTALLA:
                fondo_y1 = -ALTO_PANTALLA
            if fondo_y2 >= ALTO_PANTALLA:
                fondo_y2 = -ALTO_PANTALLA

            # Actualizar las posiciones físicas de la canoa y las piedras/troncos
            grupo_jugador.update()
            grupo_obstaculos.update()
            
            # Verificar si los obstáculos pasaron a salvo el fondo del mapa
            for obstaculo in grupo_obstaculos:
                if obstaculo.rect.top > ALTO_PANTALLA:
                    puntuacion += 1  # ¡Sumas un punto de supervivencia!
                    
                    if sonido_punto:
                        sonido_punto.play()
                        
                    obstaculo.reubicarse()  # Reaparece arriba en una coordenada X nueva
                    
                    # DIFICULTAD PROGRESIVA: Cada 5 puntos aumentamos la velocidad de todo
                    if puntuacion % 5 == 0:
                        velocidad_actual_rio += 1  # Acelera el fondo en el siguiente frame
                        
                        # Actualizamos la velocidad individual de cada piedra en escena
                        for obs in grupo_obstaculos:
                            obs.velocidad = velocidad_actual_rio
            
            # DETECTOR DE COLISIONES (¿Canoa chocó contra obstáculos?)
            if pygame.sprite.spritecollide(canoa, grupo_obstaculos, False):
                if sonido_choque:
                    sonido_choque.play()
                estado = "GAME_OVER"  # Cambiamos el estado para congelar la lógica

        # --- C. RENDERIZADO (Dibujo en la ventana) ---
        if estado == "JUGANDO":
            # Dibujar el fondo infinito animado
            if imagen_fondo:
                pantalla.blit(imagen_fondo, (0, fondo_y1))
                pantalla.blit(imagen_fondo, (0, fondo_y2))
            else:
                pantalla.fill((30, 144, 255))  # Azul base de respaldo
                
            # Dibujar los personajes y el puntaje por encima del agua
            grupo_jugador.draw(pantalla)
            grupo_obstaculos.draw(pantalla)
            hud.mostrar_puntos(pantalla, puntuacion)
            
        elif estado == "GAME_OVER":
            # Muestra la interfaz de fin de juego del HUD
            hud.mostrar_game_over(pantalla, puntuacion)
        
        # Voltear el buffer para pintar y refrescar la pantalla
        pygame.display.flip()
        # Mantener los fotogramas estables según settings.py
        reloj.tick(FPS)

    # 8. DESTRUCCIÓN Y SALIDA SEGURA DEL PROGRAMA
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()