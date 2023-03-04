import pygame, random, time, math
import tkinter.messagebox as msg
from pygame.locals import *
#Inicializar pygame
pygame.init()
global numero_enemigo, velocidad#Variables globales
#Configurar la ventana de inicio y el título
size = (600,400)
caption= "El Cuadrado"
velocidad = 0.42
#Crear ventana de inicio
screen= pygame.display.set_mode(size)
pygame.display.set_caption(caption)
#Ejecutar el loop principal
running= True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	screen.fill((255,255,255))#Llenar la pantalla con color blanco
	font = pygame.font.Font(None, 36)#Dibujar el titulo "El cuadrado"
	text = font.render("El Cuadrado", True,(0, 0, 0))
	text_rect = text.get_rect()
	text_rect.centerx = screen.get_rect().centerx
	text_rect.centery = 100
	screen.blit(text, text_rect)
	play_button = pygame.Rect(250, 200, 100, 50)# Draw the play button
	pygame.draw.rect(screen, (0, 255, 0), play_button)
	play_text = font.render("Jugar", True, (255, 255, 255))
	play_text_rect = play_text.get_rect()
	play_text_rect.centerx = play_button.centerx
	play_text_rect.centery = play_button.centery
	screen.blit(play_text, play_text_rect)
	quit_button = pygame.Rect(250, 300, 100, 50)# Draw the quit 
	pygame.draw.rect(screen, (255, 0, 0), quit_button)
	quit_text = font.render("Salir", True, (255, 255, 255))
	quit_text_rect = quit_text.get_rect()
	quit_text_rect.centerx = quit_button.centerx
	quit_text_rect.centery = quit_button.centery
	screen.blit(quit_text, quit_text_rect)
	if event.type == pygame.MOUSEBUTTONDOWN:#Comenzar
		mouse_pos = event.pos
		if play_button.collidepoint(mouse_pos):
			running = False
	pygame.display.update()# Actualizar la pantalla
pygame.quit()# Cerrar Menu principal#
############################
playable_size = (1500, 800)#Crear la ventana de juego
playable_pos = (100, 150)
playable_caption = "El Cuadrado - Jugar"
playable_screen = pygame.display.set_mode(playable_size)
pygame.display.set_caption(playable_caption)
pygame.init()#Comenzar un nuevo loop para la ventana de juego
playable_running = True
fullscreen = False#Pantalla completa
playable_screen.fill((200, 200, 200))#Color	de fondo
square_size = (25, 25)#Crear cuadrado# la posición 0,0 es la posición del pico superior izquierdo del cuadrado
square_pos = [725, 325]#Posición inicial del cuadrado(Centro del mapa)
square_color = (0, 0, 200) # azul oscuro
negro = (0, 0, 0)
wall_color = ( 165, 42, 42)#Crear una pared marrón
wall_list = [pygame.Rect(0,0,10,700), pygame.Rect(10,0,1500,10),pygame.Rect(1490,0,10,700), pygame.Rect(10,690,1490,10)]#Dimensiones de la pared (X1,Y1,X2,Y2)|(0,0) está arriba a la izquierda
#Crear enemigo
numero_enemigo = 0#Numero total de enemigos -1
radio = 12#radio del enemigo. El centro del enemigo es su enemigo_pos(x,y)
sentido = [-1,1]#Sentido del ejeY
lista_enemigos = []#Crear lista de enemigos
class Enemigo:#Crear el nombre del enemigo
    def __init__(self, name, x, y, velx, vely, sentidoy):
        self.name = name
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.sentidoy = sentidoy
enemigo_size = 12
enemigo_color = negro	
numero_monedas = 0
factor_slowdown = 1
def generar_enemigo(name,tiempo):#Funcion de generar el enemigo
	global numero_enemigo, sentidoy, square_pos, seconds
	seconds = tiempo / 1000
	sumar = seconds - seconds/10
	if int(sumar) == numero_enemigo*2:
		cerca = True
		while cerca == True:
			x = random.randint(23, 1387)
			y = random.randint(23, 678)		
			if abs(x - square_pos[0]) > 200:
				if abs(y - square_pos[1]) > 200:
					cerca = False
		enemigo_pos = [x,y]
		velx = (random.randint(-50, 50)) / factor_slowdown
		sentidoy = random.choice(sentido)
		vely = ((50 - abs(velx)) * sentidoy) / factor_slowdown
		velocidadxy = [velx, vely]
		circle = Enemigo(name, x, y, velx, vely, sentidoy)
		nenemigo = "enemigo"+str(numero_enemigo)
		lista_enemigos.append(enemigo_pos)
		lista_enemigos.append(velocidadxy)
		numero_enemigo += 1
		return
def movimiento_enemigo(lista_enemigos,i):#Mover los enemigos
	j = 2*i
	check_colision(square_pos, square_size, lista_enemigos, radio, j)			
	if lista_enemigos[j][0] <= 22:#Esquina superior
		lista_enemigos[j+1][0] = abs(lista_enemigos[j+1][0])
	if lista_enemigos[j][0] >= 1476:
		lista_enemigos[j+1][0] = -abs(lista_enemigos[j+1][0])
	if lista_enemigos[j][1] <= 22:
		lista_enemigos[j+1][1] = abs(lista_enemigos[j+1][1])
	if lista_enemigos[j][1] >= 678:
		lista_enemigos[j+1][1] = -abs(lista_enemigos[j+1][1])
	lista_enemigos[j][0] += lista_enemigos[j+1][0] / 150#actualizar posición de la lista
	lista_enemigos[j][1] += lista_enemigos[j+1][1] / 150
	pygame.draw.circle(playable_screen, enemigo_color,lista_enemigos[j],enemigo_size)
square_center = (square_pos[0], square_pos[1])
def esquinas(square_center,j):#Checkea colisión en esquinas
	if math.sqrt((square_center[0] - lista_enemigos[j][0])*(square_center[0] - lista_enemigos[j][0])+
	(square_center[1] - lista_enemigos[j][1]) * (square_center[1] - lista_enemigos[j][1])) <= 12:
		perder(numero_monedas,counter)
def check_colision(square_pos, square_size, lista_enemigos, radio, j):	
	square_center = (square_pos[0], square_pos[1])#Esquina top-left
	esquinas(square_center, j)
	square_center = (square_pos[0], square_pos[1]+25)#Esquina bot-left
	esquinas(square_center, j)
	square_center = (square_pos[0]+25, square_pos[1]+25)#Esquina bot-right
	esquinas(square_center, j)
	square_center = (square_pos[0]+25, square_pos[1])#Esquina top-right
	esquinas(square_center, j)	
	square_center = (square_pos[0] + 12.5, square_pos[1] + 12.5)
	if abs(square_center[0] - lista_enemigos[j][0]) <= 24.5:
		if abs(square_center[1] - lista_enemigos[j][1]) <= 12.5:
			perder(numero_monedas,counter)
	if abs(square_center[1] - lista_enemigos[j][1]) <= 24.5:
		if abs(square_center[0] - lista_enemigos[j][0]) <= 12.5:
			perder(numero_monedas,counter)		
def pantalla():
	playable_screen.fill((200, 200, 200))#Generar pantalla
def cuadrado():
	pygame.draw.rect(playable_screen, square_color, (square_pos[0], square_pos[1], square_size[0], square_size[1]))
def tiempo():
	global elapsed_time, counter
	elapsed_time = pygame.time.get_ticks() - start_time
	seconds = elapsed_time / 1000
	counter = "{:.2f}".format(seconds)
	counter = float(counter) + 1
	counter = "{:.2f}".format(counter)
	text_surface = font.render(str(counter), True, (0,0,0))
	text_rect = text_surface.get_rect()
	text_rect.topleft = (50,750)
	pygame.draw.rect(playable_screen, (0,0,255), text_rect.inflate(10,10), 5)#5 is the width of the frame
	playable_screen.blit(text_surface, (50,750))
	clock.tick(3000)
def pared():
	pygame.draw.rect(playable_screen, wall_color, wall)	
def perder(total_puntos, total_tiempo):
	msg.showinfo("Derrota(", "Has perdido!\nTiempo vivo: "+str(total_tiempo)+"\n" + "Monedas recogidas: "+str(total_puntos))
	pygame.quit()
	#crear ventana donde aparezca tu tiempo y tu puntuación
estado_moneda = False
moneda_size = (12, 18)
moneda_color = (0, 122, 0)
def colision_moneda(square_pos,moneda_pos):
	global estado_moneda
	square_center = (square_pos[0] + 12.5, square_pos[1] + 12.5)
	moneda_center = (moneda_pos[0]+6, moneda_pos[1] + 9)
	if abs(square_center[0] - moneda_center[0]) <= 18.5:
		if abs(square_center[1] - moneda_center[1]) <= 21.5:
			estado_moneda = False
	if abs(square_center[1] - moneda_center[1]) <= 21.5:
		if abs(square_center[0] - moneda_center[0]) <= 18.5:
			estado_moneda = False			
def generar_moneda():
	global moneda_pos, estado_moneda, numero_monedas
	x = random.randint(23, 1387)
	y = random.randint(23, 678)
	moneda_pos = [x, y]
	numero_monedas +=1
	estado_moneda = True
def moneda():
	global moneda_pos,estado_moneda
	if estado_moneda == False:
		generar_moneda()
	else:
		pygame.draw.rect(playable_screen, moneda_color, (moneda_pos[0], moneda_pos[1], moneda_size[0], moneda_size[1]))
		colision_moneda(square_pos,moneda_pos)
def puntuacion():
	global numero_monedas
	puntuacion_surface = font.render(str(numero_monedas-1), True, (0,122,0))
	puntuacion_rect = puntuacion_surface.get_rect()
	puntuacion_rect.topleft = (400,750)
	pygame.draw.rect(playable_screen, (0,0,255), puntuacion_rect.inflate(10,10), 5)#5 is the width of the frame
	playable_screen.blit(puntuacion_surface, (400,750))
#def h_slowdown():
	
left_keydown = False#Botones presionados
down_keydown = False
right_keydown = False
up_keydown = False
speedleft = velocidad#Variable velocidad
speedright = velocidad
speeddown = velocidad
speedup = velocidad
clock = pygame.time.Clock()#Reloj
counter = 0#Contador
font = pygame.font.Font(None, 36)#Fuente del contador
start_time = pygame.time.get_ticks()
while playable_running:#Main loop#
	for event in pygame.event.get():#Botones
		if event.type == pygame.QUIT:
			playable_running = False
		elif event.type == pygame.KEYDOWN:#Cuando pulsas una tecla
			if event.key == K_f: #Fullscreen en F
				if fullscreen:
					pygame.display.set_mode(playable_size)
					fullscreen = False
				else:
					pygame.display.set_mode(playable_size, pygame.FULLSCREEN)
					fullscreen = True
			if event.key == pygame.K_LEFT:#Movimiento con flechas
					left_keydown = True
			if event.key == pygame.K_RIGHT:
					right_keydown = True
			if event.key == pygame.K_UP:
					up_keydown = True
			if event.key == pygame.K_DOWN:
					down_keydown = True
		elif event.type == pygame.KEYUP:#Cuando sueltas una tecla
			if event.key == K_LEFT:
				left_keydown = False
			if event.key == K_DOWN:
				down_keydown = False
			if event.key == K_RIGHT:
				right_keydown = False
			if event.key == K_UP:
				up_keydown = False
	if left_keydown == True:#Movimiento cuando está presionado
		if square_pos[0] <= 10:#Colision izquierda
			speedleft = 0 #Con muro izquierdo
		else:
			speedleft = velocidad / factor_slowdown
		square_pos[0] -= speedleft
	if down_keydown == True:
		if square_pos[1] >= 665:
			speeddown = 0
		else:
			speeddown = velocidad / factor_slowdown
		square_pos[1] += speeddown
	if right_keydown == True:
		if square_pos[0] >= 1465:
			speedright = 0
		else:
			speedright = velocidad /factor_slowdown
		square_pos[0] += speedright
	if up_keydown == True:
		if square_pos[1] <= 10:
			speedup = 0
		else:
			speedup = velocidad / factor_slowdown
		square_pos[1] -= speedup
	pantalla()#Generar pantalla
	tiempo()#Generar contador
	cuadrado()#Generar cuadrado
	moneda()#Generar moneda
	puntuacion()#Generar puntuacion
	for i in range(numero_enemigo):#Generar enemigos
		movimiento_enemigo(lista_enemigos,i)
	for wall in wall_list:#Generar Pared
		pared()
	if numero_enemigo < 25:
		generar_enemigo("enemigo"+str(numero_enemigo), elapsed_time)#Genera un enemigo teniendo en cuenta el contador
	pygame.display.update()#Actualizar loop
pygame.quit()#Salir de la ventana de juego
