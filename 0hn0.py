from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def mostrarMatriz(matriz):
    numFilas=len(matriz)
    numCols=len(matriz[0])
    filaTexto=""
    for i  in range(numFilas):
        for j in range(numCols):
            if(matriz[i][j].value==None):
                filaTexto=filaTexto+"["+str(matriz[i][j])+"]"
            else:
                filaTexto=filaTexto+"["+str(matriz[i][j].value)+"]"
        filaTexto += "\n"
    return filaTexto

def convertirTipo(lista):
    listaResult=[]
    for i in range(0,len(lista),1):
        if (lista[i]=="."):
            listaResult.append(Dot("Red",True,None))
        else:
            if(lista[i]=="*"):
                listaResult.append(Dot("Blue",True,None))
            else:
                if(lista[i]==""):
                    listaResult.append(Dot("Grey",True,None))
                else:
                        listaResult.append(Dot("Blue",False,lista[i]))
    return listaResult

class Dot:
    def __init__(self, color, updatable=True, value=None):
        if ((value!=None)and((color=="Grey")or(color=="Red"))):
            raise Exception ("Parametros incorrectos")
        self.color=color
        self.updatable=updatable
        self.value=value
        
    def __str__(self):
        if(self.value!=None):
            return "["+str(self.value)+"]"
        else:
            if(self.color!="Grey"):
                return self.color[0]
            else:
                return " "


class Board:
    def __init__(self,filename):
        self.board=Board.fromFile(filename)
    
    @staticmethod
    def fromFile(filename):
        tablero=[]
        fichero=open(filename,"r")
        linea=fichero.readline()
        while(linea!=""):
            lista=linea.strip("\n").split(",")
            fila=convertirTipo(lista)
            tablero.append(fila)
            linea=fichero.readline()
        fichero.close()
        return tablero
    
    def __str__(self):
        return mostrarMatriz(self.board)
    
    def addDot(self,x,y,color):
        if(self.board[x][y].updatable):
            self.board[x][y]=Dot(color,True,None)
            return True
        else:
            return False
            
    def isCompleted(self):
        Completado=True
        for i in range(0,len(self.board),1):
            for j in range(0,len(self.board),1):
                if (self.board[i][j].color=="Grey"):
                    Completado=False
                else:
                    if (self.board[i][j].value!=None):
                        contador=self.cuantasAzulesve(i,j)[1]          
                        if(contador!=int(self.board[i][j].value)):
                            Completado=False
        return Completado
    
    def isCompletable(self):
        Completable=True
        if(not(self.isCompleted())):
            for i in range(0,len(self.board),1):
                for j in range(0,len(self.board),1):
                    if (self.board[i][j].value!=None):
                        contadormax=self.cuantasAzulesve(i,j)[0]
                        contadormin=self.cuantasAzulesve(i,j)[1]
                        if ((contadormax<int(self.board[i][j].value))or(contadormin>int(self.board[i][j].value))):
                            Completable=False
        return Completable
        
    def toImage(self):
        LongitudTablero=400
        imagen=Image.new("RGB",(LongitudTablero,LongitudTablero),(255,255,255))
        draw=ImageDraw.Draw(imagen)
        font=ImageFont.truetype("micross.ttf",40)
        for i in range(0,LongitudTablero,1):
            for j in range(0,LongitudTablero,1):
                self.drawCircle(imagen,i,j,draw,font)
        return imagen

    def drawCircle(self,imagen,i,j,draw,font):
        LongitudTablero=400
        myBoard=self.board
        LimiteCasillas=LongitudTablero/len(myBoard)
        Radio=0.8*(LimiteCasillas/2)
        Fila=int(i//LimiteCasillas)
        Columna=int(j//LimiteCasillas)
        CentroCasilla=((((Columna)*LimiteCasillas)+LimiteCasillas/2),(((Fila)*LimiteCasillas)+LimiteCasillas/2))
        if((i%LimiteCasillas==0)or(j%LimiteCasillas==0)or(i==LongitudTablero-1)or(j==LongitudTablero-1)):
            imagen.putpixel((i,j),(0,0,0))
        else:
            if((((j-CentroCasilla[0])**2)+((i-CentroCasilla[1])**2))<=(Radio**2)):
                if(myBoard[Fila][Columna].color=="Blue"):
                    imagen.putpixel((j,i),(110,190,222)) 
                    if(myBoard[Fila][Columna].value!=None):
                        draw.text((CentroCasilla[0]-10,CentroCasilla[1]-20),str(myBoard[Fila][Columna].value),(255,255,255),font)                  
                else:
                    if(myBoard[Fila][Columna].color=="Red"):
                        imagen.putpixel((j,i),(221,59,76))
                    else:
                        imagen.putpixel((j,i),(238,238,238))
            
    def cuantasAzulesve(self,i,j):
        contadormax=0
        contadormin=0
        derecha=1
        izquierda=1
        arriba=1
        abajo=1
        grisizquierda=False
        grisderecha=False
        grisarriba=False
        grisabajo=False
        while((j+derecha<len(self.board))and(self.board[i][j+derecha].color!="Red")):
            contadormax=contadormax+1
            if(self.board[i][j+derecha].color=="Grey"):
                grisderecha=True
            if((self.board[i][j+derecha].color=="Blue")and(not(grisderecha))):
                contadormin=contadormin+1
            derecha=derecha+1
        while((j-izquierda>-1)and(self.board[i][j-izquierda].color!="Red")):
            contadormax=contadormax+1
            if(self.board[i][j-izquierda].color=="Grey"):
                grisizquierda=True
            if((self.board[i][j-izquierda].color=="Blue")and(not(grisizquierda))):
                contadormin=contadormin+1
            izquierda=izquierda+1
        while((i+abajo<len(self.board))and(self.board[i+abajo][j].color!="Red")):
            contadormax=contadormax+1
            if(self.board[i+abajo][j].color=="Grey"):
                grisabajo=True
            if((self.board[i+abajo][j].color=="Blue")and(not(grisabajo))):
                contadormin=contadormin+1
            abajo=abajo+1
        while((i-arriba>-1)and(self.board[i-arriba][j].color!="Red")):
            contadormax=contadormax+1
            if(self.board[i-arriba][j].color=="Grey"):
                grisarriba=True
            if((self.board[i-arriba][j].color=="Blue")and(not(grisarriba))):
                contadormin=contadormin+1
            arriba=arriba+1
        return (contadormax,contadormin)
    
    def Haygrises(self):
        Grises=False
        for i in range(0,len(self.board),1):
            for j in range(0,len(self.board),1):
                if (self.board[i][j].color=="Grey"):
                    Grises=True
        return Grises
        
    def autosolveRecursive(self):
        if(self.isCompleted()):
            return (True,self)
        else:
            if(self.Haygrises()):
                if(self.isCompletable()):
                    for i in range(0,len(self.board),1):
                        for j in range(0,len(self.board),1):
                            if (self.board[i][j].color=="Grey"):
                                self.addDot(i,j,"Blue")
                                if(self.autosolveRecursive()[0]):
                                    return (True,self)
                                else:
                                    self.addDot(i,j,"Red")
                                    if(self.autosolveRecursive()[0]):                                    
                                        return (True,self)
                                    else:
                                        self.addDot(i,j,"Grey")
                                        return (False,None)
                else:
                    return(False,None)
            else:
                return (False,None)
                      
def autosolve(filename):
    Tablero=Board(filename)
    print ("Initial board: ")
    print(Tablero)
    solution=Tablero.autosolveRecursive()
    if (solution[0]):
        print("Solution: ")
        print(solution[1])
    else:
        print("Found no solution")
    return solution

def playgame(filename):
    myBoard=Board(filename)
    doExit=False
    while((not(doExit))and (not(myBoard.isCompleted()))):
        print(myBoard)
        userInput=input("Your input: ")
        if(userInput=="show"):
            myBoard.toImage
        else:
            if(userInput=="exit"):
                doExit=True
            else:
                if(userInput[0:3]=="add"):
                    myBoard.addDot(int(userInput[4]),int(userInput[6]),userInput[8:len(userInput)])
        if(not(myBoard.isCompletable())):
            print("The board is not completable, try removing some dots")
    if(doExit):
        print("Bye!")
    else:
        if(myBoard.isCompleted()):
            print("The board is completed, congratulations!")
            