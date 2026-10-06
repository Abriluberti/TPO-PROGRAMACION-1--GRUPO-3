#Cada elemento dentro del cubo (Z) es una matriz. Cada fila de esa matriz es una Y y cada columna es una X.
cubo=crear_cubo(8)
print (cubo)
#plano=dibujar_plano_z(cubo, 3)
#print (plano)

def colocar_fragata(cubo): #2x1
    x=input("Elije la coordenada X de la proa de la Fragata (2x1):")
    while x.isdigit()==False or int(x)<1 or int(x)>8:
        print("Error - Coordenada fuera del cubo")
        x=input("Elije la coordenada X entre 1 y 8:")
    x=int(x)
    x=x-1
    
    y=input("Elije la coordenada Y de la proa de la Fragata (2x1):")
    while y.isdigit()==False or int(y)<1 or int(y)>8:
        print("Error - Coordenada fuera del cubo")
        y=input("Elije la coordenada Y entre 1 y 8:")
    y=int(y)
    y=y-1
    
    z=input("Elije la coordenada Z de la proa de la Fragata (2x1):")
    while z.isdigit()==False or int(z)<1 or int(z)>8:
        print("Error - Coordenada fuera del cubo")
        z=input("Elije la coordenada Z entre 1 y 8:")
    z=int(z)
    z=z-1
    
    while cubo[z][y][x] == "?": #Verifico que el espacio no este ocupado
        print("Error: ya hay una nave ocupando esa posición.")
        x = input("Elije otra coordenada X entre 1 y 8:")
        while x.isdigit()==False or int(x)<1 or int(x)>8:
            print("Error - Coordenada fuera del cubo")
            x = input("Elije otra coordenada X entre 1 y 8:")
        x=int(x)
        x=x-1
        
        y=input("Elije otra coordenada Y entre 1 y 8:")
        while y.isdigit()==False or int(y)<1 or int(y)>8:
            print("Error - Coordenada fuera del cubo")
            y=input("Elije otra coordenada Y entre 1 y 8:")
        y=int(y)
        y=y-1
        
        z=input("Elije otra coordenada Z entre 1 y 8:")
        while z.isdigit()==False or int(z)<1 or int(z)>8:
            print("Error - Coordenada fuera del cubo")
            z = input("Elije otra coordenada Z entre 1 y 8:")
        z=int(z)
        z=z-1
 
    sentido=str(input("Elige 'vertical' u 'horizontal':"))
    while sentido!="vertical" and sentido!="horizontal":
        print("Error: ingrese un sentido válido")
        sentido=str(input("Elige 'vertical' u 'horizontal':"))
    if sentido=="vertical":
        direccion=str(input("Elige si la nave se extiende hacia 'arriba' o 'abajo':"))
        while (direccion!="arriba" and direccion!="abajo") or (direccion == "arriba" and y == 0) or (direccion == "abajo" and y >= 7) or \
      (direccion == "arriba" and cubo[z][y-1][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+1][x] == "?"):
            if direccion != "arriba" and direccion != "abajo": #Verifico que este bien escrito
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'arriba' o 'abajo':"))
            if direccion == "arriba" and y == 0: #Verifico que este dentro del cubo
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'abajo'"))
            if direccion == "abajo" and y >= 7:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'arriba'"))
            if direccion == "arriba" and cubo[z][y-1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.") #Verifico que el espacio esté libre
                direccion=str(input("Elige 'abajo'"))
            if direccion == "abajo" and cubo[z][y+1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba'"))
        cubo[z][y][x]="?"
        if direccion=="arriba":
            cubo[z][y-1][x]="?"
        if direccion=="abajo":
            cubo[z][y+1][x]="?"
    if sentido=="horizontal":
        direccion=str(input("Elige si la nave se extiende hacia la 'derecha', 'izquierda', 'atras' o 'adelante'"))
        while (direccion != "derecha" and direccion != "izquierda" and
       direccion != "atras" and direccion != "adelante") or \
      (direccion == "derecha" and x >= 7) or \
      (direccion == "izquierda" and x <= 0) or \
      (direccion == "atras" and z >= 7) or \
      (direccion == "adelante" and z <= 0) or \
      (direccion == "derecha" and cubo[z][y][x+1] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-1] == "?") or \
      (direccion == "atras" and cubo[z+1][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-1][y][x] == "?"):
                if direccion != "derecha" and direccion != "izquierda" and direccion != "atras" and direccion != "adelante":
                    print("Error: ingrese una dirección válida") #Verifico que este bien escrito
                    direccion=str(input("Elige 'derecha', 'izquierda', 'atras' o 'adelante'"))
                if direccion == "derecha" and x >=7:
                    print("Error: la nave sale del cubo. Ingrese otra dirección.") #Verifico que este dentro del cubo
                    direccion=str(input("Elige 'izquierda', 'atras' o 'adelante'"))
                if direccion == "izquierda" and x <=0:
                    print("Error: la nave sale del cubo. Ingrese otra dirección")
                    direccion=str(input("Elige 'derecha', 'atras' o 'adelante'"))
                if direccion == "atras" and z >=7:
                    print("Error: la nave sale del cubo. Ingrese otra dirección.")
                    direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante'"))
                if direccion == "adelante" and z <= 0:
                    print("Error: la nave sale del cubo. Ingrese otra dirección.")
                    direccion=str(input("Elige 'derecha', 'izquierda' o 'atras'"))
                if direccion == "derecha" and cubo[z][y][x+1] == "?": #Verifico que el espacio esté libre
                    print("Error: ya hay una nave ocupando esa posición.")
                    direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))
                if direccion == "izquierda" and cubo[z][y][x-1] == "?":
                    print("Error: ya hay una nave ocupando esa posición.")
                    direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))
                if direccion == "atras" and cubo[z+1][y][x] == "?":
                    print("Error: ya hay una nave ocupando esa posición.")
                    direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))
                if direccion == "adelante" and cubo[z-1][y][x] == "?":
                    print("Error: ya hay una nave ocupando esa posición.")
                    direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))
        cubo[z][y][x]="?"
        if direccion=="derecha":
            cubo[z][y][x+1]="?"
        if direccion=="izquierda":
            cubo[z][y][x-1]="?"
        if direccion=="atras":
            cubo[z+1][y][x]="?"
        if direccion=="adelante":
            cubo[z-1][y][x]="?"
    return cubo
###############################################################################################################
def colocar_destructor(cubo):
    x=input("Elije la coordenada X de la proa del Destructor (3x1):")
    while x.isdigit()==False or int(x)<1 or int(x)>8:
        print("Error - Coordenada fuera del cubo")
        x=input("Elije la coordenada X entre 1 y 8:")
    x=int(x)
    x=x-1

    y=input("Elije la coordenada Y de la proa del Destructor (3x1):")
    while y.isdigit()==False or int(y)<1 or int(y)>8:
        print("Error - Coordenada fuera del cubo")
        y=input("Elije la coordenada Y entre 1 y 8:")
    y=int(y)
    y=y-1

    z=input("Elije la coordenada Z de la proa del Destructor (3x1):")
    while z.isdigit()==False or int(z)<1 or int(z)>8:
        print("Error - Coordenada fuera del cubo")
        z=input("Elije la coordenada Z entre 1 y 8:")
    z=int(z)
    z=z-1

    while cubo[z][y][x] == "?":
        print("Error: ya hay una nave ocupando esa posición.")

        x=input("Elije otra coordenada X entre 1 y 8:")
        while x.isdigit()==False or int(x)<1 or int(x)>8:
            print("Error - Coordenada fuera del cubo")
            x=input("Elije otra coordenada X entre 1 y 8:")
        x=int(x)
        x=x-1

        y=input("Elije otra coordenada Y entre 1 y 8:")
        while y.isdigit()==False or int(y)<1 or int(y)>8:
            print("Error - Coordenada fuera del cubo")
            y=input("Elije otra coordenada Y entre 1 y 8:")
        y=int(y)
        y=y-1

        z=input("Elije otra coordenada Z entre 1 y 8:")
        while z.isdigit()==False or int(z)<1 or int(z)>8:
            print("Error - Coordenada fuera del cubo")
            z=input("Elije otra coordenada Z entre 1 y 8:")
        z=int(z)
        z=z-1

    sentido=str(input("Elige 'vertical' u 'horizontal':"))

    while sentido!="vertical" and sentido!="horizontal":
        print("Error: ingrese un sentido válido")
        sentido=str(input("Elige 'vertical' u 'horizontal':"))

    if sentido=="vertical":

        direccion=str(input("Elige si la nave se extiende hacia 'arriba' o 'abajo':"))

        while (direccion!="arriba" and direccion!="abajo") or \
      (direccion == "arriba" and y <= 1) or \
      (direccion == "abajo" and y >= 6) or \
      (direccion == "arriba" and cubo[z][y-1][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-2][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+1][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+2][x] == "?"):

            if direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'arriba' o 'abajo':"))

            if direccion == "arriba" and y <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and y >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "arriba" and cubo[z][y-1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and cubo[z][y+1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

        cubo[z][y][x]="?"

        if direccion=="arriba":
            cubo[z][y-1][x]="?"
            cubo[z][y-2][x]="?"

        if direccion=="abajo":
            cubo[z][y+1][x]="?"
            cubo[z][y+2][x]="?"

    if sentido=="horizontal":

        direccion=str(input("Elige si la nave se extiende hacia la 'derecha', 'izquierda', 'atras' o 'adelante':"))

        while (direccion != "derecha" and direccion != "izquierda" and
       direccion != "atras" and direccion != "adelante") or \
      (direccion == "derecha" and x >= 6) or \
      (direccion == "izquierda" and x <= 1) or \
      (direccion == "atras" and z >= 6) or \
      (direccion == "adelante" and z <= 1) or \
      (direccion == "derecha" and cubo[z][y][x+1] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+2] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-1] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-2] == "?") or \
      (direccion == "atras" and cubo[z+1][y][x] == "?") or \
      (direccion == "atras" and cubo[z+2][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-1][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-2][y][x] == "?"):

            if direccion != "derecha" and direccion != "izquierda" and direccion != "atras" and direccion != "adelante":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'derecha', 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and x >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and x <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and z >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and z <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "derecha" and cubo[z][y][x+1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and cubo[z+1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and cubo[z-1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

        cubo[z][y][x]="?"

        if direccion=="derecha":
            cubo[z][y][x+1]="?"
            cubo[z][y][x+2]="?"

        if direccion=="izquierda":
            cubo[z][y][x-1]="?"
            cubo[z][y][x-2]="?"

        if direccion=="atras":
            cubo[z+1][y][x]="?"
            cubo[z+2][y][x]="?"

        if direccion=="adelante":
            cubo[z-1][y][x]="?"
            cubo[z-2][y][x]="?"

    return cubo

#############################################################################################################

def colocar_submarino(cubo):
    x=input("Elije la coordenada X de la proa del Submarino (3x1):")
    while x.isdigit()==False or int(x)<1 or int(x)>8:
        print("Error - Coordenada fuera del cubo")
        x=input("Elije la coordenada X entre 1 y 8:")
    x=int(x)
    x=x-1

    y=input("Elije la coordenada Y de la proa del Submarino entre 5 y 8 (3x1):")
    while y.isdigit()==False or int(y)<5 or int(y)>8:
        print("Error - Submarino fuera del agua")
        y=input("Elije la coordenada Y entre 5 y 8:")
    y=int(y)
    y=y-1

    z=input("Elije la coordenada Z de la proa del Submarino (3x1):")
    while z.isdigit()==False or int(z)<1 or int(z)>8:
        print("Error - Coordenada fuera del cubo")
        z=input("Elije la coordenada Z entre 1 y 8:")
    z=int(z)
    z=z-1

    while cubo[z][y][x] == "?":
        print("Error: ya hay una nave ocupando esa posición.")

        x=input("Elije otra coordenada X entre 1 y 8:")
        while x.isdigit()==False or int(x)<1 or int(x)>8:
            print("Error - Coordenada fuera del cubo")
            x=input("Elije otra coordenada X entre 1 y 8:")
        x=int(x)
        x=x-1

        y=input("Elije otra coordenada Y entre 5 y 8:")
        while y.isdigit()==False or int(y)<5 or int(y)>8:
            print("Error - Submarino fuera del agua")
            y=input("Elije otra coordenada Y entre 5 y 8:")
        y=int(y)
        y=y-1

        z=input("Elije otra coordenada Z entre 1 y 8:")
        while z.isdigit()==False or int(z)<1 or int(z)>8:
            print("Error - Coordenada fuera del cubo")
            z=input("Elije otra coordenada Z entre 1 y 8:")
        z=int(z)
        z=z-1

    sentido=str(input("Elige 'vertical' u 'horizontal':"))

    while sentido!="vertical" and sentido!="horizontal":
        print("Error: ingrese un sentido válido")
        sentido=str(input("Elige 'vertical' u 'horizontal':"))

    if sentido=="vertical":

        direccion=str(input("Elige si la nave se extiende hacia 'arriba' o 'abajo':"))

        while (direccion!="arriba" and direccion!="abajo") or \
      (direccion == "arriba" and y <= 1) or \
      (direccion == "abajo" and y >= 6) or \
      (direccion == "arriba" and y-2 < len(cubo)//2) or \
      (direccion == "abajo" and y+2 >= len(cubo)) or \
      (direccion == "arriba" and cubo[z][y-1][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-2][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+1][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+2][x] == "?"):

            if direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'arriba' o 'abajo':"))

            if direccion == "arriba" and y <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and y >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "arriba" and y-2 < len(cubo)//2:
                print("Error: el submarino sobresale del agua.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and y+2 >= len(cubo):
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "arriba" and cubo[z][y-1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and cubo[z][y+1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

        cubo[z][y][x]="?"

        if direccion=="arriba":
            cubo[z][y-1][x]="?"
            cubo[z][y-2][x]="?"

        if direccion=="abajo":
            cubo[z][y+1][x]="?"
            cubo[z][y+2][x]="?"

    if sentido=="horizontal":

        direccion=str(input("Elige si la nave se extiende hacia la 'derecha', 'izquierda', 'atras' o 'adelante':"))

        while (direccion != "derecha" and direccion != "izquierda" and
       direccion != "atras" and direccion != "adelante") or \
      (direccion == "derecha" and x >= 6) or \
      (direccion == "izquierda" and x <= 1) or \
      (direccion == "atras" and z >= 6) or \
      (direccion == "adelante" and z <= 1) or \
      (direccion == "derecha" and cubo[z][y][x+1] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+2] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-1] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-2] == "?") or \
      (direccion == "atras" and cubo[z+1][y][x] == "?") or \
      (direccion == "atras" and cubo[z+2][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-1][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-2][y][x] == "?"):

            if direccion != "derecha" and direccion != "izquierda" and direccion != "atras" and direccion != "adelante":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'derecha', 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and x >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and x <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and z >= 6:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and z <= 1:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "derecha" and cubo[z][y][x+1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and cubo[z+1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and cubo[z-1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

        cubo[z][y][x]="?"

        if direccion=="derecha":
            cubo[z][y][x+1]="?"
            cubo[z][y][x+2]="?"

        if direccion=="izquierda":
            cubo[z][y][x-1]="?"
            cubo[z][y][x-2]="?"

        if direccion=="atras":
            cubo[z+1][y][x]="?"
            cubo[z+2][y][x]="?"

        if direccion=="adelante":
            cubo[z-1][y][x]="?"
            cubo[z-2][y][x]="?"

    return cubo

############################################################################################################
def colocar_crucero(cubo):
    x=input("Elije la coordenada X de la proa del Crucero (4x1):")
    while x.isdigit()==False or int(x)<1 or int(x)>8:
        print("Error - Coordenada fuera del cubo")
        x=input("Elije la coordenada X entre 1 y 8:")
    x=int(x)
    x=x-1

    y=input("Elije la coordenada Y de la proa del Crucero (4x1):")
    while y.isdigit()==False or int(y)<1 or int(y)>8:
        print("Error - Coordenada fuera del cubo")
        y=input("Elije la coordenada Y entre 1 y 8:")
    y=int(y)
    y=y-1

    z=input("Elije la coordenada Z de la proa del Crucero entre 2 y 7 (4x1):")
    while z.isdigit()==False or int(z)<2 or int(z)>len(cubo)-1:
        print("Error: el crucero debe estar entre los Z de 2 a",len(cubo)-1)
        z=input("Elije la coordenada Z entre 2 y",len(cubo)-1,":")
    z=int(z)
    z=z-1

    while cubo[z][y][x] == "?":
        if cubo[z][y][x] == "?":
            print("Error: ya hay una nave ocupando esa posición.")

        x=input("Elije otra coordenada X entre 1 y 8:")
        while x.isdigit()==False or int(x)<1 or int(x)>8:
            print("Error - Coordenada fuera del cubo")
            x=input("Elije otra coordenada X entre 1 y 8:")
        x=int(x)
        x=x-1

        y=input("Elije otra coordenada Y entre 1 y 8:")
        while y.isdigit()==False or int(y)<1 or int(y)>8:
            print("Error - Coordenada fuera del cubo")
            y=input("Elije otra coordenada Y entre 1 y 8:")
        y=int(y)
        y=y-1

        z=input("Elije otra coordenada Z entre 2 y 7:")
        while z.isdigit()==False or int(z)<2 or int(z)>len(cubo)-1:
            print("Error: el crucero debe estar entre los Z de 2 a",len(cubo)-1)
            z=input("Elije otra coordenada Z entre 2 y",len(cubo)-1,":")
        z=int(z)
        z=z-1

    sentido=str(input("Elige 'vertical' u 'horizontal':"))

    while sentido!="vertical" and sentido!="horizontal":
        print("Error: ingrese un sentido válido")
        sentido=str(input("Elige 'vertical' u 'horizontal':"))

    if sentido=="vertical":

        direccion=str(input("Elige si la nave se extiende hacia 'arriba' o 'abajo':"))

        while (direccion!="arriba" and direccion!="abajo") or \
      (direccion == "arriba" and y <= 2) or \
      (direccion == "abajo" and y >= 5) or \
      (direccion == "arriba" and cubo[z][y-1][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-2][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-3][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+1][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+2][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+3][x] == "?"):

            if direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'arriba' o 'abajo':"))

            if direccion == "arriba" and y <= 2:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and y >= 5:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "arriba" and cubo[z][y-1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-3][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and cubo[z][y+1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+3][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

        cubo[z][y][x]="?"

        if direccion=="arriba":
            cubo[z][y-1][x]="?"
            cubo[z][y-2][x]="?"
            cubo[z][y-3][x]="?"

        if direccion=="abajo":
            cubo[z][y+1][x]="?"
            cubo[z][y+2][x]="?"
            cubo[z][y+3][x]="?"

    if sentido=="horizontal":

        direccion=str(input("Elige si la nave se extiende hacia la 'derecha', 'izquierda', 'atras' o 'adelante':"))

        while (direccion != "derecha" and direccion != "izquierda" and
       direccion != "atras" and direccion != "adelante") or \
      (direccion == "derecha" and x >= 5) or \
      (direccion == "izquierda" and x <= 2) or \
      (direccion == "atras" and z >= len(cubo)-4) or \
      (direccion == "adelante" and z <= 3) or \
      (direccion == "derecha" and cubo[z][y][x+1] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+2] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+3] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-1] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-2] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-3] == "?") or \
      (direccion == "atras" and cubo[z+1][y][x] == "?") or \
      (direccion == "atras" and cubo[z+2][y][x] == "?") or \
      (direccion == "atras" and cubo[z+3][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-1][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-2][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-3][y][x] == "?"):

            if direccion != "derecha" and direccion != "izquierda" and direccion != "atras" and direccion != "adelante":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'derecha', 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and x >= 5:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and x <= 2:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and z >= len(cubo)-4:
                print("Error: la nave ocuparía el último Z. Ingrese otra dirección.") #Verifico que no este en Z=8
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and z <= 3:
                print("Error: la nave ocuparía el primer Z. Ingrese otra dirección.") #Verifico que no este en Z=1
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "derecha" and cubo[z][y][x+1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+3] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-3] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and cubo[z+1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+3][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and cubo[z-1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-3][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

        cubo[z][y][x]="?"

        if direccion=="derecha":
            cubo[z][y][x+1]="?"
            cubo[z][y][x+2]="?"
            cubo[z][y][x+3]="?"

        if direccion=="izquierda":
            cubo[z][y][x-1]="?"
            cubo[z][y][x-2]="?"
            cubo[z][y][x-3]="?"

        if direccion=="atras":
            cubo[z+1][y][x]="?"
            cubo[z+2][y][x]="?"
            cubo[z+3][y][x]="?"

        if direccion=="adelante":
            cubo[z-1][y][x]="?"
            cubo[z-2][y][x]="?"
            cubo[z-3][y][x]="?"

    return cubo
###################################################################
def colocar_portaaviones(cubo):
    mitad = len(cubo)//2
    
    x=input("Elije la coordenada X de la proa del Portaaviones (5x1):")
    while x.isdigit()==False or int(x)<1 or int(x)>len(cubo):
        print("Error - Coordenada fuera del cubo")
        x=input("Elije la coordenada X entre 1 y " + str(len(cubo)) + ":")
    x=int(x)
    x=x-1

    y=input("Elije la coordenada Y de la proa del Portaaviones entre 1 y " + str(mitad) + " (5x1):")
    while y.isdigit()==False or int(y)<1 or int(y)>mitad:
        print("Error - La nave debe estar en la mitad inferior del eje Y")
        y=input("Elije una coordenada Y entre 1 y " + str(mitad) + ":")
    y=int(y)
    y=y-1

    z=input("Elije la coordenada Z de la proa del Portaaviones (5x1):")
    while z.isdigit()==False or int(z)<1 or int(z)>len(cubo):
        print("Error - Coordenada fuera del cubo")
        z=input("Elije la coordenada Z entre 1 y " + str(len(cubo)) + ":")
    z=int(z)
    z=z-1

    while cubo[z][y][x] == "?":
        print("Error: ya hay una nave ocupando esa posición.")

        x=input("Elije otra coordenada X:")
        while x.isdigit()==False or int(x)<1 or int(x)>len(cubo):
            print("Error - Coordenada fuera del cubo")
            x=input("Elije otra coordenada X entre 1 y " + str(len(cubo)) + ":")
        x=int(x)
        x=x-1

        y=input("Elije otra coordenada Y entre 1 y " + str(mitad) + " (5x1):")
        while y.isdigit()==False or int(y)<1 or int(y)>mitad:
            print("Error - La nave debe estar en la mitad inferior del eje Y")
            y=input("Elije otra coordenada Y entre 1 y " + str(mitad) + " (5x1):")
        y=int(y)
        y=y-1

        z=input("Elije otra coordenada Z:")
        while z.isdigit()==False or int(z)<1 or int(z)>len(cubo):
            print("Error - Coordenada fuera del cubo")
            z=input("Elije otra coordenada Z entre 1 y " + str(len(cubo)) + ":")
        z=int(z)
        z=z-1

    sentido=str(input("Elige 'vertical' u 'horizontal':"))

    while sentido!="vertical" and sentido!="horizontal":
        print("Error: ingrese un sentido válido")
        sentido=str(input("Elige 'vertical' u 'horizontal':"))

    if sentido=="vertical":

        direccion=str(input("Elige si la nave se extiende hacia 'arriba' o 'abajo':"))

        while (direccion!="arriba" and direccion!="abajo") or \
      (direccion == "arriba" and y-4 < 0) or \
      (direccion == "abajo" and y+4 >= mitad) or \
      (direccion == "arriba" and cubo[z][y-1][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-2][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-3][x] == "?") or \
      (direccion == "arriba" and cubo[z][y-4][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+1][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+2][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+3][x] == "?") or \
      (direccion == "abajo" and cubo[z][y+4][x] == "?"):

            if direccion != "arriba" and direccion != "abajo":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'arriba' o 'abajo':"))

            if direccion == "arriba" and y-4 < 0: #Verifico que la nave no sobresalga del cubo
                print("Error: la nave sale del cubo.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and y+4 >= mitad: #Verifico que la nave no se encuentre por debajo del limite permitido
                print("Error: la nave sale de la mitad inferior del eje Y.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "arriba" and cubo[z][y-1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-3][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "arriba" and cubo[z][y-4][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'abajo':"))

            if direccion == "abajo" and cubo[z][y+1][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+2][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+3][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

            if direccion == "abajo" and cubo[z][y+4][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'arriba':"))

        cubo[z][y][x]="?"

        if direccion=="arriba":
            cubo[z][y-1][x]="?"
            cubo[z][y-2][x]="?"
            cubo[z][y-3][x]="?"
            cubo[z][y-4][x]="?"

        if direccion=="abajo":
            cubo[z][y+1][x]="?"
            cubo[z][y+2][x]="?"
            cubo[z][y+3][x]="?"
            cubo[z][y+4][x]="?"

    if sentido=="horizontal":

        direccion=str(input("Elige si la nave se extiende hacia la 'derecha', 'izquierda', 'atras' o 'adelante':"))

        while (direccion != "derecha" and direccion != "izquierda" and
       direccion != "atras" and direccion != "adelante") or \
      (direccion == "derecha" and x >= len(cubo)-4) or \
      (direccion == "izquierda" and x <= 3) or \
      (direccion == "atras" and z >= len(cubo)-4) or \
      (direccion == "adelante" and z <= 3) or \
      (direccion == "derecha" and cubo[z][y][x+1] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+2] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+3] == "?") or \
      (direccion == "derecha" and cubo[z][y][x+4] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-1] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-2] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-3] == "?") or \
      (direccion == "izquierda" and cubo[z][y][x-4] == "?") or \
      (direccion == "atras" and cubo[z+1][y][x] == "?") or \
      (direccion == "atras" and cubo[z+2][y][x] == "?") or \
      (direccion == "atras" and cubo[z+3][y][x] == "?") or \
      (direccion == "atras" and cubo[z+4][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-1][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-2][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-3][y][x] == "?") or \
      (direccion == "adelante" and cubo[z-4][y][x] == "?"):

            if direccion != "derecha" and direccion != "izquierda" and direccion != "atras" and direccion != "adelante":
                print("Error: ingrese una dirección válida")
                direccion=str(input("Elige 'derecha', 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and x >= len(cubo)-4:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and x <= 3:
                print("Error: la nave sale del cubo. Ingrese otra dirección")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and z >= len(cubo)-4:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and z <= 3:
                print("Error: la nave sale del cubo. Ingrese otra dirección.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "derecha" and cubo[z][y][x+1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+3] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "derecha" and cubo[z][y][x+4] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'izquierda', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-1] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-2] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-3] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "izquierda" and cubo[z][y][x-4] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'atras' o 'adelante':"))

            if direccion == "atras" and cubo[z+1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+3][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "atras" and cubo[z+4][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'adelante':"))

            if direccion == "adelante" and cubo[z-1][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-2][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-3][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

            if direccion == "adelante" and cubo[z-4][y][x] == "?":
                print("Error: ya hay una nave ocupando esa posición.")
                direccion=str(input("Elige 'derecha', 'izquierda' o 'atras':"))

        cubo[z][y][x]="?"

        if direccion=="derecha":
            cubo[z][y][x+1]="?"
            cubo[z][y][x+2]="?"
            cubo[z][y][x+3]="?"
            cubo[z][y][x+4]="?"

        if direccion=="izquierda":
            cubo[z][y][x-1]="?"
            cubo[z][y][x-2]="?"
            cubo[z][y][x-3]="?"
            cubo[z][y][x-4]="?"

        if direccion=="atras":
            cubo[z+1][y][x]="?"
            cubo[z+2][y][x]="?"
            cubo[z+3][y][x]="?"
            cubo[z+4][y][x]="?"

        if direccion=="adelante":
            cubo[z-1][y][x]="?"
            cubo[z-2][y][x]="?"
            cubo[z-3][y][x]="?"
            cubo[z-4][y][x]="?"

    return cubo

###############################################################################################
def colocar_estacion(cubo):
    print("Selecciona la posición de la arista superior izquierda y frontal de la estación espacial")
    
    x=input("Elije la coordenada X de la arista sup. Izq. y Frontal (2x2x2):")
    while x.isdigit()==False or int(x)<2 or int(x)>len(cubo)-2:
        print("Error - La nave no puede ocupar los bordes del cubo.")
        x=input("Elije la coordenada X entre 2 y " +str(len(cubo)-2)+":")
    x=int(x)
    x=x-1

    y=input("Elije la coordenada Y de la arista sup. Izq. y Frontal (2x2x2):")
    while y.isdigit()==False or int(y)<2 or int(y)>len(cubo)-2:
        print("Error - La nave no puede ocupar los bordes del cubo.")
        y=input("Elije la coordenada Y entre 2 y " +str(len(cubo)-2)+":")
    y=int(y)
    y=y-1
    
    z=input("Elije la coordenada Z de la arista sup. Izq. y Frontal (2x2x2):")
    while z.isdigit()==False or int(z)<2 or int(z)>len(cubo)-2:
        print("Error - La nave no puede ocupar los bordes del cubo.")
        z=input("Elije la coordenada Z entre 2 y "  +str(len(cubo)-2)+":")
    z=int(z)
    z=z-1

    while cubo[z][y][x]=="?" or \
          cubo[z+1][y][x]=="?" or \
          cubo[z][y][x+1]=="?" or \
          cubo[z+1][y][x+1]=="?" or \
          cubo[z][y+1][x]=="?" or \
          cubo[z+1][y+1][x]=="?" or \
          cubo[z][y+1][x+1]=="?" or \
          cubo[z+1][y+1][x+1]=="?":
        print("Error: ya hay una nave ocupando alguna de las posiciones.")
        x=input("Elije otra coordenada X:")
        while x.isdigit()==False or x<2 or x>len(cubo)-2:
            print("Error - La nave no puede ocupar los bordes del cubo.")
            x=input("Elije otra coordenada X entre 2 y " +str(len(cubo)-2)+":")
        x=int(x)
        x=x-1

        y=input("Elije otra coordenada Y:")
        while y.isdigit()==False or y<2 or y>len(cubo)-2:
            print("Error - La nave no puede ocupar los bordes del cubo.")
            y=input("Elije otra coordenada Y entre 2 y " +str(len(cubo)-2)+":")
        y=int(y)
        y=y-1

        z=input("Elije otra coordenada Z:")
        while z.isdigit()==False or z<2 or z>len(cubo)-2:
            print("Error - La nave no puede ocupar los bordes del cubo.")
            z=input("Elije otra coordenada Z entre 2 y " +str(len(cubo)-2)+":")
        z=int(z)
        z=z-1

    cubo[z][y][x]="?"
    cubo[z+1][y][x]="?"
    cubo[z][y][x+1]="?"
    cubo[z+1][y][x+1]="?"
    cubo[z][y+1][x]="?"
    cubo[z+1][y+1][x]="?"
    cubo[z][y+1][x+1]="?"
    cubo[z+1][y+1][x+1]="?"


    return cubo

cubo=colocar_fragata(cubo)

#cubo=colocar_destructor(cubo)
#cubo=colocar_submarino(cubo)
#cubo=colocar_crucero(cubo)
#cubo=colocar_portaaviones(cubo)
#cubo=colocar_estacion(cubo)

plano1=dibujar_plano_z(cubo,1)
plano2=dibujar_plano_z(cubo,2)
plano3=dibujar_plano_z(cubo,3)
plano4=dibujar_plano_z(cubo,4)
plano5=dibujar_plano_z(cubo,5)
plano6=dibujar_plano_z(cubo,6)
plano7=dibujar_plano_z(cubo,7)
plano8=dibujar_plano_z(cubo,8)
print (plano1)
print (plano2)
print (plano3)
print (plano4)
print (plano5)
print (plano6)
print (plano7)
print (plano8)
    