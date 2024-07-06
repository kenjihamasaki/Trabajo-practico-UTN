import pygame
import pygame_textinput
import json
import random
from clases.button import Button
from clases.text_input import *
import sys


pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BG = pygame.image.load("trabajo_practico/assets/Background.jpg")
BG_dif = pygame.image.load("trabajo_practico/assets/Background_difuminado.png")
BG_2 = pygame.transform.scale(BG, (400,300))
imagen_1 = pygame.image.load("trabajo_practico/assets/headset_24dp.png")
imagen_1 = pygame.transform.scale(imagen_1, (50, 50))
imagen_2 = pygame.image.load("trabajo_practico/assets/headset_off_24dp.png")
imagen_2 = pygame.transform.scale(imagen_2, (50, 50))
ima_ES = pygame.image.load("trabajo_practico/assets/espana.png")
ima_ES = pygame.transform.scale(ima_ES, (50, 50))
ima_EU = pygame.image.load("trabajo_practico/assets/estados-unidos.png")
ima_EU = pygame.transform.scale(ima_EU, (50, 50))
manager_2 = TextInputManager(validator = lambda input: len(input) <= 11)
textinput = pygame_textinput.TextInputVisualizer(manager=manager_2)
sonido = pygame.mixer.Sound("trabajo_practico/assets/Late Night.mp3")
sonido_2 = pygame.mixer.Sound("trabajo_practico/assets/Evil Morty Theme (128 kbps).mp3")
sonido_3 = pygame.mixer.Sound("trabajo_practico/assets/subir-nivel.mp3")
sonido_4 = pygame.mixer.Sound("trabajo_practico/assets/gta-san-andreas.mp3")
sonido.play(-1)
sonido_2.play()
sonido_3.play()
sonido_4.play()
sonido.set_volume(0.1)
sonido_2.set_volume(0)
sonido_3.set_volume(0)
sonido_4.set_volume(0)
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("Ahorcado")

manager = TextInputManager(validator = lambda input: len(input) <= 1)
textinput_2 = pygame_textinput.TextInputVisualizer(manager=manager)
linea = pygame.draw.line(window, (0,0,0), (300,100), (300, 200), 10)
font = pygame.font.SysFont("Arial Narrow", 40)
font1 = pygame.font.SysFont("Arial Narrow", 110)
text = font.render("Puntaje: ", True, (0, 0, 0))
lista_palabras_usadas = []


with open("trabajo_practico/json/ahorcado.json", "r") as archivo:
    ahorcado = json.load(archivo)["ahorcado"]

with open("trabajo_practico/json/top_5.json", "r") as archivo:
    data = json.load(archivo)["top"]

def swap(lista, indice_uno, indice_dos):
    auxiliar = lista[indice_uno]
    lista[indice_uno] = lista[indice_dos]
    lista[indice_dos] = auxiliar
    
    return lista  

def ordenar(lista:list, clave:str, ascendente:bool=True)-> list: 
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):
            if ascendente and int(lista[i][clave] )> int(lista[j][clave]) or not ascendente and int(lista[i][clave]) < int(lista[j][clave]):
                swap(lista, i, j)
    return lista

def modificar_datos_json(nombre:str,  clave,lista, dato):
    data = dato
    data.append(lista)
    data = ordenar(data, "score", False)
    data.pop()
    data = {clave:data}
    
    with open(nombre, 'w+') as file:
        json.dump(data, file, indent=4, ensure_ascii=False )

def get_font(size):
    return pygame.font.Font("trabajo_practico/assets/font.ttf", size)

def obtener_palabra_random(lista, idioma):
    palabra = random.choice(lista)

    if len(lista_palabras_usadas) == len(lista):
        palabra = False

    else:
        while palabra["id"] in lista_palabras_usadas:
            palabra = random.choice(lista)

        lista_palabras_usadas.append(palabra["id"])
        palabra = palabra[idioma]
    
    return palabra

def slot_palabra(palabra:str, retorno:list , idioma):

    if palabra == False:
        if idioma == "ES":
            retorno = "Felicidades"
        elif idioma == "EN":
            retorno = "Congratulation"
    else:
        for letra in palabra:
            retorno.append("-")

    return retorno

def mostrar_lista(lista:list):
	retorno_uno = ""
	for i in lista:
		retorno_uno += i
	return retorno_uno

def score(idioma:str, img):
    running = True
    imagen = img
    if idioma == "ES":
        score = "Puntaje"
        name = "Apodo"
    elif idioma == "EN":
        score = "Score"
        name = "Nickname"

    while running:
        events = pygame.event.get()
        textinput.update(events)
        for event in events:
            pygame.display.update()
            if event.type == pygame.QUIT:
                sys.exit()
            window.blit(BG,(0,0))
            menu_mouse_pos = pygame.mouse.get_pos()
            sound_button = Button(image=imagen, pos=(750, 35), text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image= None, pos=(693.3, 33.5), text_input="X", font=get_font(20), base_color="#d7fcd4", hovering_color="Red")
            menu_button = Button(image= None, pos=(600, 33.5), text_input="menu", font=get_font(20), base_color="#d7fcd4", hovering_color="white")

            for button in [sound_button, quit_button, menu_button]:
                button.changeColor(menu_mouse_pos)
                button.update(window)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if sound_button.checkForInput(menu_mouse_pos):
                    if imagen == imagen_2:
                        imagen = imagen_1
                        sonido.set_volume(0.1) 
                    elif imagen == imagen_1:
                        imagen = imagen_2
                        sonido.set_volume(0)

                if quit_button.checkForInput(menu_mouse_pos):
                    sys.exit()
                
                if menu_button.checkForInput(menu_mouse_pos):
                    main_menu()     
            pygame.draw.ellipse(window,("#AD0800"), (670, 10, 45, 45), 5)
            pygame.draw.rect(window, ("#294D3F"), (550, 13, 100, 40), 5)
            pygame.draw.rect(window, ("black"), (50, 70, 690, 500), 5)
            text = get_font(30).render(f"{score}", True, (0, 0, 0))
            text_1= get_font(30).render(f"{name}", True, (0, 0, 0))
            text_2 = get_font(35).render(f"Top 5", True, (0, 0, 0))
            text_3= get_font(25).render(f"{data[0][idioma]}", True, (0, 0, 0))
            text_4= get_font(25).render(f"{data[1][idioma]}", True, (0, 0, 0))
            text_5= get_font(25).render(f"{data[2][idioma]}", True, (0, 0, 0))
            text_6= get_font(25).render(f"{data[3][idioma]}", True, (0, 0, 0))
            text_7= get_font(25).render(f"{data[4][idioma]}", True, (0, 0, 0))
            text_3_1= get_font(25).render(f"{data[0]["score"]}", True, (0, 0, 0))
            text_4_1= get_font(25).render(f"{data[1]["score"]}", True, (0, 0, 0))
            text_5_1= get_font(25).render(f"{data[2]["score"]}", True, (0, 0, 0))
            text_6_1= get_font(25).render(f"{data[3]["score"]}", True, (0, 0, 0))
            text_7_1= get_font(25).render(f"{data[4]["score"]}", True, (0, 0, 0))
            window.blit(text,(430,80))
            window.blit(text_1,(150,80))
            window.blit(text_2,(280,20))
            window.blit(text_3,(100,140))
            window.blit(text_4,(100,230))
            window.blit(text_5,(100,320))
            window.blit(text_6,(100,410))
            window.blit(text_7,(100,500))
            window.blit(text_3_1,(530,140))
            window.blit(text_4_1,(530,230))
            window.blit(text_5_1,(530,320))
            window.blit(text_6_1,(530,410))
            window.blit(text_7_1,(530,500))
        pygame.display.flip()  

def nickname(idioma:str, img, puntaje:int):
    running = True
    imagen = img
    nombre= ""
    posicion = (300, 297)
    if idioma == "ES":
        name = "Ingrese un apodo"
        limit = "Limite: 11 letras"
    if idioma == "EN":
        name= "Insert a nickname"
        limit = "Limit: 11 letters"
    while running:
        events = pygame.event.get()
        textinput.update(events)
        for event in events:
            pygame.display.update()
            if event.type == pygame.QUIT:
                sys.exit()
            window.blit(BG_dif, (0, 0))
            window.blit(BG_2,(200,120))
            menu_mouse_pos = pygame.mouse.get_pos()
            sound_button = Button(image=imagen, pos=(750, 35), text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image= None, pos=(693.3, 33.5), text_input="X", font=get_font(20), base_color="#d7fcd4", hovering_color="Red")
            menu_button = Button(image= None, pos=(600, 33.5), text_input="menu", font=get_font(20), base_color="#d7fcd4", hovering_color="white")

            for button in [sound_button, quit_button, menu_button]:
                button.changeColor(menu_mouse_pos)
                button.update(window)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if sound_button.checkForInput(menu_mouse_pos):
                    if imagen == imagen_2:
                        imagen = imagen_1
                        sonido.set_volume(0.1) 
                    elif imagen == imagen_1:
                        imagen = imagen_2
                        sonido.set_volume(0)

                if quit_button.checkForInput(menu_mouse_pos):
                    sys.exit()
                
                if menu_button.checkForInput(menu_mouse_pos):
                    main_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                nombre = textinput.value
                textinput.value = ""
                puntaje = puntaje
                if nombre == "":
                    datos= {"score": puntaje,"EN": "unknown","ES": "Desconocido"}
                else:    
                    datos= {"score": puntaje,"EN": nombre,"ES": nombre}
                modificar_datos_json("trabajo_practico/json/top_5.json", "top", datos, data)
                score(idioma, imagen)
        window.blit(textinput.surface, posicion)
        text2 = get_font(20).render(f"{name}: ", True, (0, 0, 0))
        text3 = get_font(10).render(f"{limit}: ", True, (0, 0, 0))
        pygame.draw.ellipse(window,("#AD0800"), (670, 10, 45, 45), 5)
        pygame.draw.rect(window, ("#294D3F"), (550, 13, 100, 40), 5)  
        pygame.draw.rect(window, ("black"), (270, 290, 250, 40), 5)    
        window.blit(text2,(240,200))
        window.blit(text3,(240,230))
        pygame.display.flip()

def jugar(idioma:str, img):
    
    contador_3 = 0
    contador_4 = 0
    puntaje = 0
    running = True
    palabra = ""
    palabra_secreta = ""
    bandera_terminado = False
    contador_2 = 0
    retorno = []
    palabra = obtener_palabra_random(ahorcado, idioma)
    nueva_palabra = slot_palabra(palabra,retorno, idioma)
    palabra_secreta = mostrar_lista(nueva_palabra)
    print(palabra)
    posicion_2 = (600,300)
    
    posicion_3 = (-100,-100)
    posicion_4 = (-100,-100)
    posicion_4_1= (-100, -100)
    posicion_4_2=(-100, -100, -100, -100)
    posicion_5 = (-100,-100)
    posicion_5_1=(-100, -100)
    posicion_6 = (-100,-100)
    posicion_6_1=(-100, -100)
    posicion_7 = (-100,-100)
    posicion_7_1=(-100, -100)
    posicion_8 = (-100,-100)
    posicion_8_1=(-100, -100)
    posicion_9 = (-420,-110)
    posicion_9_1 = (-100,-100)
    posicion_9_2 = (-100,-100)
    posicion_10 = (-100,-100)
    posicion_11 = (-100, -100, -100, -100)
    posicion_12 =(595,291,30,40)
    posicion_13 =(460,230,300,120)
    posicion_14 = (481,250)
    
    imagen = img
    if idioma == "ES":
        name = "nombre"
        scores = "puntaje"
        game_over = "Perdistes"
        word = "La palabra era"
        insert_letter = "Ingrese una letra :"
        next_text= "Siguiente"
    if idioma == "EN":
        name= "name"
        scores = "scores"
        game_over = "Game Over"
        word = "The word is"
        insert_letter = "Insert a letter :"
        next_text = "Next"
    while running:

        
        events = pygame.event.get()
        
        textinput.update(events)
        textinput_2.update(events)

        for event in events:
            window.blit(BG, (0,0))
            
            menu_mouse_pos = pygame.mouse.get_pos()
            sound_button = Button(image=imagen, pos=(750, 35), text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
            next_button = Button(image= None, pos=posicion_10, text_input= next_text, font=get_font(20), base_color="#d7fcd4", hovering_color="White")
            quit_button = Button(image= None, pos=(693.3, 33.5), text_input="X", font=get_font(20), base_color="#d7fcd4", hovering_color="Red")
            menu_button = Button(image= None, pos=(600, 33.5), text_input="menu", font=get_font(20), base_color="#d7fcd4", hovering_color="white")

            for button in [sound_button, next_button, quit_button, menu_button]:
                button.changeColor(menu_mouse_pos)
                button.update(window)
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            
                if sound_button.checkForInput(menu_mouse_pos):
                    if imagen == imagen_2:
                        imagen = imagen_1
                        sonido.set_volume(0.1) 
                    elif imagen == imagen_1:
                        imagen = imagen_2
                        sonido.set_volume(0)
                
                if next_button.checkForInput(menu_mouse_pos):
                    if imagen == imagen_2:
                        sonido.set_volume(0) 
                    elif imagen == imagen_1:
                        sonido.set_volume(0.1)
                    sonido_2.set_volume(0)
                    sonido_3.set_volume(0)
                    sonido_4.set_volume(0)
                    if contador_2 < 6 and bandera_terminado == False: 
                        retorno = []
                        contador_2 = 0
                        palabra = obtener_palabra_random(ahorcado, idioma)
                        nueva_palabra = slot_palabra(palabra,retorno, idioma)
                        palabra_secreta = mostrar_lista(nueva_palabra)
                        print(palabra)
                        posicion_3 = (-100,-100)
                        posicion_4 = (-100,-100)
                        posicion_4_1=(-100, -100)
                        posicion_4_2=(-100, -100, -100, -100)
                        posicion_5 = (-100,-100)
                        posicion_5_1=(-100, -100)
                        posicion_6 = (-100,-100)
                        posicion_6_1=(-100, -100)
                        posicion_7 = (-100,-100)
                        posicion_7_1=(-100, -100)
                        posicion_8 = (-100,-100)
                        posicion_8_1=(-100, -100)
                        posicion_10 = (-100,-100)
                        posicion_11 = (-100, -100, -100, -100)
                        if palabra_secreta== "Congratulation" or palabra_secreta == "Felicidades":  
                            sonido_4.set_volume(0.1)
                            sonido_4.stop()
                            sonido_4.play() 
                            sonido.set_volume(0)  
                            posicion_2 = (-100, -100)
                            posicion_12 = (-100, -100, -100, -100)
                            posicion_13 = (-100, -100, -100, -100)
                            posicion_14 = (-100,-100)
                            posicion_10 = (650, 500)
                            posicion_11 = (550, 480 , 200, 40)
                            bandera_terminado = True
                    elif contador_2 >=6 or bandera_terminado == True:
                        if imagen == imagen_2:
                            sonido.set_volume(0) 
                        elif imagen == imagen_1:
                            sonido.set_volume(0.1)
                        nickname(idioma, imagen, puntaje)

                
                if quit_button.checkForInput(menu_mouse_pos):
                    sys.exit()
                
                if menu_button.checkForInput(menu_mouse_pos):
                    main_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                letra = textinput_2.value
                letra = letra.lower()
                print(letra)   
                contador = 0            
                for i in range(len(palabra)):
                    if letra != retorno[i]:
                        if letra == palabra[i]:
                            retorno[i] = letra
                            contador +=1
                            puntaje += 1
                        else:
                            retorno[i] = retorno[i]  
                    else:
                        contador += 1 
                if contador == 0 and letra != "":
                    contador_2 +=1
                if contador_2 ==1:
                    posicion_3 = (252,200)
                if contador_2 ==2:
                    posicion_4 = (250,200)
                    posicion_4_1 = (250, 340)
                    posicion_4_2 = (241, 235, 20, 100 )
                if contador_2 == 3:
                    posicion_5 = (250,250)
                    posicion_5_1 = (200, 280)
                if contador_2 == 4:
                    posicion_6 = (250,250)
                    posicion_6_1 = (300, 280)
                if contador_2 == 5:
                    posicion_7 = (250,340)
                    posicion_7_1 = (230, 400)
                if contador_2 == 6:
                    posicion_8 = (250,340)
                    posicion_8_1 = (280, 400)
                    posicion_9 = (420,110)
                    posicion_9_1 = (380, 150)
                    posicion_9_2 = (420,190)
                    posicion_2 = (-100, -100)
                    posicion_12 = (-100, -100, -100, -100)
                    posicion_13 = (-100, -100, -100, -100)
                    posicion_14 = (-100,-100)
                    posicion_10 = (650, 500)
                    posicion_11 = (550, 480 , 200, 40)
                    sonido_2.set_volume(0.1)
                    sonido_2.stop()
                    sonido_2.play()
                    sonido.set_volume(0)
                    
                nueva_palabra = retorno
                palabra_secreta = mostrar_lista(nueva_palabra)
                if palabra == palabra_secreta:
                    sonido_3.set_volume(0.1)
                    sonido_3.stop()
                    sonido_3.play()
                    sonido.set_volume(0)
                    posicion_10 = (650, 500)
                    posicion_11 = (550, 480 , 200, 40)



                        
            
            if event.type == pygame.QUIT:
                sys.exit()
        
        pygame.draw.line(window, ("#4D3F29"), (250,100), (250, 170), 10)
        pygame.draw.line(window, ("#4D3F29"), (250,104), (100, 104), 10)
        pygame.draw.line(window, ("#4D3F29"), (104,440), (104, 104), 10)
        pygame.draw.rect(window, ("#4D3F29"), (10, 440 , 300, 40), 10)
        pygame.draw.ellipse(window,("#AD0800"), (670, 10, 45, 45), 5)
        pygame.draw.rect(window, ("#294D3F"), (550, 13, 100, 40), 5)
        pygame.draw.rect(window, ("black"), posicion_12, 3)
        pygame.draw.rect(window, ("black"), posicion_13, 3)
        pygame.draw.rect(window, ("#2AC85C"), posicion_11, 5)
        pygame.draw.circle(window, ("black"), posicion_3, 35)
        pygame.draw.line(window, ("black"), posicion_4, posicion_4_1, 10)  
        pygame.draw.rect(window, ("black"), posicion_4_2, 5)      
        pygame.draw.line(window, ("black"), posicion_5, posicion_5_1, 10)  
        pygame.draw.line(window, ("black"), posicion_6, posicion_6_1, 10) 
        pygame.draw.line(window, ("black"), posicion_7, posicion_7_1, 10) 
        pygame.draw.line(window, ("black"), posicion_8, posicion_8_1, 10)

        window.blit(textinput_2.surface, posicion_2)
        text = get_font(20).render(f"{scores}: {puntaje}", True, (0, 0, 0))
        text1 = get_font(35).render(f"{palabra_secreta}", True, (0, 0, 0))
        text3 = get_font(20).render(f"{game_over}", True, (0, 0, 0))   
        text4 = get_font(20).render(f"{word}: ", True, (0, 0, 0))
        text5 = get_font(20).render(f"{palabra}", True, (0, 0, 0))
        text6 = get_font(13).render(f"{insert_letter}", True, ("#d7fcd4"))
        window.blit(text,(10,10))
        window.blit(text1,(150,520))
        window.blit(text3, posicion_9)
        window.blit(text4, posicion_9_1)
        window.blit(text5, posicion_9_2)
        window.blit(text6, posicion_14)
        pygame.display.update()

        pygame.display.flip()

def main_menu():
    
    running=True
    imagen_idioma = ima_ES
    imagen = imagen_1
    idioma = "ES"
    play = "JUGAR"
    scores = "PUNTAJE"
    quit_salir = "SALIR"
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        
        

        window.blit(BG, (0, 0))
        
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(60).render("MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(400, 120))

        play_button = Button(image=None, pos=(400, 250), text_input= play, font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        scores_button = Button(image=None, pos=(400, 390), text_input= scores, font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=None, pos=(400, 520), text_input= quit_salir, font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        sound_button = Button(image=imagen, pos=(750, 35), text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        idioma_button = Button(image=imagen_idioma, pos=(35, 35), text_input="", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        window.blit(menu_text, menu_rect)

        for button in [play_button, scores_button, quit_button, sound_button, idioma_button]:
            button.changeColor(menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    jugar(idioma, imagen)
                if scores_button.checkForInput(menu_mouse_pos):
                    score(idioma, imagen)
                if quit_button.checkForInput(menu_mouse_pos):
                    running = False
                    sys.exit()
                if sound_button.checkForInput(menu_mouse_pos):
                    if imagen == imagen_2:
                        imagen = imagen_1
                        sonido.set_volume(0.1) 
                    elif imagen == imagen_1:
                        imagen = imagen_2
                        sonido.set_volume(0)
                if idioma_button.checkForInput(menu_mouse_pos):
                    if imagen_idioma == ima_ES:
                        imagen_idioma = ima_EU
                        idioma = "EN"
                    elif imagen_idioma == ima_EU:
                        imagen_idioma = ima_ES
                        idioma = "ES"
            if idioma == "ES":
                play = "JUGAR"
                scores = "PUNTAJE"
                quit_salir = "SALIR"
            elif idioma == "EN":
                play = "PLAY"
                scores = "SCORES"
                quit_salir = "Exit"
                        

        pygame.display.update()


main_menu()



                    
                        
        
                        