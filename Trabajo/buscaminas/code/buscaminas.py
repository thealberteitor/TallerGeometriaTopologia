import sys, pygame, random
from pygame.locals import *
from ctypes import byref, c_int, pointer
import time #para sleep

#VARIABLES GLOBALES
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 255)
AOSCURO = (0, 0, 255)
BLANCO = (255, 255, 255) #BLANCO
NEGRO = (0 , 0 , 0)
AZUL = (0, 0, 255)
GRIS= (190, 190, 190) #GRIS
VERDE = (0,187,45)


abiertas=0

ultimaPosicion = [-1, -1]
global finJuego
finJuego = False


random.seed(12345)

class Text:
    def __init__(self, FontName = None, FontSize = 50):
        pygame.font.init()
        self.font = pygame.font.Font(FontName, FontSize)
        self.size = FontSize

    def render(self, surface, text, color, pos):
        text = str(text)
        x, y = pos
        for i in text.split("\r"):
            surface.blit(self.font.render(i, 1, color), (x, y))
            y += self.size

class Tablero:
    ancho = 0
    alto = 0
    borde = 0
    numero_cuadros = 0
    ancho_cuadro = 0
    alto_cuadro = 0
    tablero=[]
    text = Text()
    n_minas = 0
    #finJuego = False

    def __init__(self, ancho, alto, borde, numero_cuadros, n_minas):
        self.ancho = ancho
        self.alto = alto
        self.borde = borde
        self.numero_cuadros = numero_cuadros
        self.ancho_cuadro = ancho/numero_cuadros
        self.alto_cuadro = alto/numero_cuadros
        self.n_minas = n_minas
        #self.finJuego = False


        #X casillas que no contienen bombas
        #B casillas con Bombas

        #Se introducen X en todo el tablero.
        for i in range(numero_cuadros):
            self.tablero.append(['X']*numero_cuadros)


        #10 bombas aleatoriamente por el tablero

        for i in range(n_minas):
            f = random.randrange(numero_cuadros-1)
            c = random.randrange(numero_cuadros-1)
            while(self.tablero[f][c] == 'B'):
                f = random.randrange(numero_cuadros-1)
                c = random.randrange(numero_cuadros-1)

            self.tablero[f][c] = 'B'



    #Función que dibuja con libreria Pygame los colorines y demás
    def dibujaTablero(self, ventana, posicion):
        aumento_ancho=0
        aumento_alto=0

        #Como estamos en un toro llano, identificamos los bordes con el mismo color:
        pygame.draw.rect(ventana, AZUL, pygame.Rect(0, 0, self.borde, self.alto), 0)
        pygame.draw.rect(ventana, AZUL, pygame.Rect(self.ancho-self.borde, 0, self.borde, self.alto), 2)


        pygame.draw.rect(ventana, ROJO, pygame.Rect(0, 0, self.ancho, self.borde), 0)
        pygame.draw.rect(ventana, ROJO , pygame.Rect(0, self.alto-self.borde, self.ancho, self.borde), 0)

        for i in range(self.numero_cuadros):
            aumento_ancho += self.ancho_cuadro
            aumento_alto += self.alto_cuadro
            pygame.draw.rect(ventana, NEGRO, pygame.Rect(aumento_ancho, 0, self.borde, self.alto), 0)
            pygame.draw.rect(ventana, NEGRO, pygame.Rect(0, aumento_alto, self.ancho, self.borde), 0)

        #Segundo pinto el color interno de cada cuadro del tablero
        aumento_ancho=0
        aumento_alto=0

        for i in range(self.numero_cuadros):
            for j in range(self.numero_cuadros):
                aumento_ancho = j*self.ancho_cuadro
                aumento_alto = i*self.alto_cuadro

                #El primer if pinta el cuadro centrar a excepción de los filos
                #El segundo if pinta filos de arriba y de la izquierda
                #El tercer if pinta filos de la derecha y de abajo
                if i!=0 and j!=0 and i!=self.numero_cuadros-1 and j!=self.numero_cuadros-1:
                    if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                        ultimaPosicion[0] = i
                        ultimaPosicion[1] = j

                    self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                    if self.tablero[i][j]==' ':
                        pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                    elif self.tablero[i][j]==':)':
                        pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))


                    elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                        pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        if self.tablero[i][j]!='0':
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                    elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                        pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                        self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                    else:
                        pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                elif i==0 or j==0:
                    if i==0 and j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])


                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))


                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                    elif j==0 and i==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])


                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                    else:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])


                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                elif i==self.numero_cuadros-1 or j==self.numero_cuadros-1:
                    if i==self.numero_cuadros-1 and j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])


                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-2*self.borde), 0)
                    elif i==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])


                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-2*self.borde), 0)
                    elif j==self.numero_cuadros-1:
                        if(posicion[0]>aumento_ancho and posicion[0]<aumento_ancho+self.ancho_cuadro and posicion[1]>aumento_alto and posicion[1]<aumento_alto+self.alto_cuadro):
                            ultimaPosicion[0] = i
                            ultimaPosicion[1] = j

                        self.compruebaCasilla(ultimaPosicion[0], ultimaPosicion[1])

                        if self.tablero[i][j]==' ':
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]==':)':
                            pygame.draw.rect(ventana, VERDE, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))

                        elif self.tablero[i][j]!='X' and self.tablero[i][j]!='B':
                            pygame.draw.rect(ventana, GRIS, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)
                            if self.tablero[i][j]!='0':
                                self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.06))
                        elif self.tablero[i][j]=='B' and i==ultimaPosicion[0] and j==ultimaPosicion[1]:
                            pygame.draw.rect(ventana, ROJO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-self.borde, self.alto_cuadro-self.borde), 0)
                            self.text.render(ventana, self.tablero[i][j], BLANCO, (aumento_ancho+aumento_ancho*0.07, aumento_alto+aumento_alto*0.07))
                        else:
                            pygame.draw.rect(ventana, BLANCO, pygame.Rect(aumento_ancho+self.borde, aumento_alto+self.borde, self.ancho_cuadro-2*self.borde, self.alto_cuadro-self.borde), 0)


    def imprimeTablero(self):
        for i in self.tablero:
            print(i)

    #Función que desvela una casilla
    def compruebaCasilla(self, f, c):
        contador = 0


        if f>=0 and c>=0 and f<self.numero_cuadros and c<self.numero_cuadros and self.tablero[f][c]!='B' and self.tablero[f][c]=='X':
            compruebaBomba = False

            global abiertas
            abiertas=abiertas+1
            print(abiertas)
            if abiertas == (self.numero_cuadros*self.numero_cuadros)-self.n_minas :
                pygame.display.set_caption("Has ganado :)")

                for i in range(self.numero_cuadros):
                    for j in range(self.numero_cuadros):
                        if self.tablero[i][j]=='B':
                            #if i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B':
                            self.tablero[i][j]=':)'
                            self.compruebaCasilla(i,j)


            for i in [(f-1)%self.numero_cuadros, f%self.numero_cuadros, (f+1)%self.numero_cuadros]:
                for j in [(c-1)%self.numero_cuadros, c%self.numero_cuadros, (c+1)%self.numero_cuadros]:
                    if i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B' and compruebaBomba==False:
                        compruebaBomba=True
                        contador = contador + 1
                    elif i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B':
                        contador = contador + 1


            #pasar a su número correspondiente
            self.tablero[f][c] = chr(contador+48)


            if compruebaBomba==False:
                '''
                Se recorren todas las casillas y se descubre su valor.
                Si hay bombas en su 8 entorno la casilla toma el valor de la suma de las bombas
                En caso contrario se descubre la casilla y las de su entorno que no tengan bombas.
                el % numero_cuadros es para darle estructura toroidal (toro llano)
                '''
                for i in [(f-1)%self.numero_cuadros, f%self.numero_cuadros, (f+1)%self.numero_cuadros]:
                    for j in [(c-1)%self.numero_cuadros, c%self.numero_cuadros, (c+1)%self.numero_cuadros]:
                        self.compruebaCasilla(i,j)


        #SI la casilla es una bomba, las recorro todas y muestro las que son bombas, las identifico con ' '
        #para después pintarlas de color rojo usando la función de coloreado de arriba.
        elif f>=0 and c>=0 and f<self.numero_cuadros and c<self.numero_cuadros and self.tablero[f][c]=='B':
            #Recorro todas las pos. del tablero
            for i in range(self.numero_cuadros):
                for j in range(self.numero_cuadros):
                    if self.tablero[i][j]=='B':
                    #if i>=0 and j>=0 and i<self.numero_cuadros and j<self.numero_cuadros and self.tablero[i][j]=='B':
                        self.tablero[i][j]=' '
                        self.compruebaCasilla(i,j)

            pygame.display.set_caption("Has perdido :(")
            #global finJuego
            #finJuego = True

def main():
    pygame.init()

    dimensiones_tablero = [600, 600]
    ventana = pygame.display.set_mode(dimensiones_tablero)

    pygame.display.set_caption("Buscaminas en Toro Llano")
    clock = pygame.time.Clock()

    pos = [-1,-1]
    minas = int(sys.argv[2])
    n = int(sys.argv[1])
    #ancho, alto, borde, numero_cuadros, minas
    tablero = Tablero(600, 600, 2, n, minas)
    #tablero.imprimeTablero()

    while not finJuego:
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                #print("FIN: \n")
                #tablero.imprimeTablero()
                sys.exit(0)

        tablero.dibujaTablero(ventana, pos)

        botones = pygame.mouse.get_pressed()
        if botones[0]:
            pos = pygame.mouse.get_pos()

        pygame.display.flip()
        clock.tick(60)


    return 0



if __name__ == "__main__":
    main()

