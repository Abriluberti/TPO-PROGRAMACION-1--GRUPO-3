import random
import armamento

def colocar_fragata(cubo,fragata, tupla_inicio, tupla_final): #2x1
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    fragata=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False,fragata
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=1:
            print("La nave debe ocupar 2 espacios")
            return False,fragata
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,fragata
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            fragata.append((i+1,b+1,c+1))
        print("Fragata colocada")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x) !=1:
            print("La nave debe ocupar 2 espacios")
            return False,fragata
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,fragata
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            fragata.append((a+1,j+1,c+1))
        print("Fragata colocada")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=1:
            print("La nave debe ocupar 2 espacios")
            return False,fragata
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,fragata
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            fragata.append((a+1,b+1,k+1))
        print("Fragata colocada")
            
    return cubo,fragata
###############################################################################################################
def colocar_destructor(cubo, destructor, tupla_inicio, tupla_final): #3x1
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    destructor=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False,destructor
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=2:
            print("La nave debe ocupar 3 espacios")
            return False,destructor
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,destructor
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            destructor.append((i+1,b+1,c+1))
        print("Destructor colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=2:
            print("La nave debe ocupar 3 espacios")
            return False,destructor
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,destructor
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            destructor.append((a+1,j+1,c+1))
        print("Destructor colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=2:
            print("La nave debe ocupar 3 espacios")
            return False,destructor
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,destructor
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            destructor.append((a+1,b+1,k+1))
        print("Destructor colocado")
            
    return cubo,destructor

#############################################################################################################

def colocar_submarino(cubo, submarino, tupla_inicio, tupla_final): #3x1 y parte inferior del eje Z
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    submarino=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if c+1<=len(cubo)/2 or y+1<=len(cubo)/2:
        print("El submarino no puede colocarse tan alto")
        return False,submarino
    #Comprueba que el submarino este en la mitad inferior del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False,submarino
    #Comprueba que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=2:
            print("La nave debe ocupar 3 espacios")
            return False,submarino
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,submarino
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            submarino.append((i+1,b+1,c+1))
        print("Submarino colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=2:
            print("La nave debe ocupar 3 espacios")
            return False,submarino
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,submarino
        submarino=[]
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            submarino.append((a+1,j+1,c+1))
        print("Submarino colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=2:
            print("La nave debe ocupar 3 espacios")
            return False,submarino
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,submarino
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            submarino.append((a+1,b+1,k+1))
        print("Submarino colocado")
            
    return cubo,submarino

############################################################################################################
def colocar_crucero(cubo, crucero, tupla_inicio, tupla_final): #4x1 y Z!=1 y Z!=len(cubo)
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    crucero=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if a==0 or z==0 or a==len(cubo)-1 or z==len(cubo)-1:
        print("El crucero no puede colocarse en los bordes del eje Z")
        return False,crucero
    #Verifica que la nave no se encuentre en los bordes del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False,crucero
    #Verifica que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=3:
            print("La nave debe ocupar 4 espacios")
            return False,crucero
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,crucero
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            crucero.append((i+1,b+1,c+1))
        print("Crucero colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=3:
            print("La nave debe ocupar 4 espacios")
            return False,crucero
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,crucero
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            crucero.append((a+1,j+1,c+1))
        print("Crucero colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=3:
            print("La nave debe ocupar 4 espacios")
            return False,crucero
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,crucero
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            crucero.append((a+1,b+1,k+1))
        print("Crucero colocado")
            
    return cubo,crucero
###################################################################
def colocar_portaaviones(cubo, portaaviones, tupla_inicio, tupla_final): #5x1 y parte superior del eje Z
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    portaaviones=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if c+1>len(cubo)/2 or y+1>len(cubo)/2:
        print("El portaaviones no puede colocarse tan bajo")
        return False,portaaviones
    #Comprueba que el portaaviones este en la mitad superior del eje Z.
    
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False,portaaviones
    #Comprueba que las celdas esten en linea.
    
    # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=4:
            print("La nave debe ocupar 5 espacios")
            return False,portaaviones
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,portaaviones
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            portaaviones.append((i+1,b+1,c+1))
        print("Portaaviones colocado")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x)!=4:
            print("La nave debe ocupar 5 espacios")
            return False,portaaviones
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,portaaviones
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            portaaviones.append((a+1,j+1,c+1))
        print("Portaaviones colocado")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) !=4:
            print("La nave debe ocupar 5 espacios")
            return False,portaaviones
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False,portaaviones
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            portaaviones.append((a+1,b+1,k+1))
        print("Portaaviones colocado")
            
    return cubo,portaaviones

###############################################################################################
def colocar_estacion(cubo, estacion, tupla_inicio, tupla_final): #4x1 y Z!=1 y Z!=len(cubo)
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1
    estacion=[]
    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1
    if a==0 or a>=len(cubo) or b==0 or b>=len(cubo) or c==0 or c>=len(cubo) or z==0 or z>=len(cubo) or x==0 or x>=len(cubo) or y==0 or y>=len(cubo):
        print("La estacion no puede colocarse en los bordes del cubo")
        return False,estacion
    #Comprueba que la estacion no se encuentre tocando ningun borde del cubo.
    
    if a==z or b==x or c==y:
        print("Las celdas no deben son continuas para la estacion")
        return False,estacion
    #Verifica que las celdas NO esten en linea.
    else:
        if max(a, z) - min(a, z)!=1 or max(b,x) - min(b, x)!=1 or max(c, y) - min(c, y) !=1:
            raise ValueError("La nave debe ocupar un espacio de 2x2x2")
        elif cubo[a][b][c]=="?" or cubo[a][b][c+1]=="?" or cubo[a][b+1][c]=="?" or cubo[a][b+1][c+1]=="?" or cubo[a+1][b][c]=="?" or cubo[a+1][b][c+1]=="?" or cubo[a+1][b+1][c]=="?" or cubo[a+1][b+1][c+1]=="?":
            print("Ya hay otra nave ocupando esa posición.")
            return False,estacion
        #Verifica que ningun punto del cubo este ocupado al verificar sus 8 celdas.
        else:
            for i in range(min(a,z), max(a,z)+1):
                for j in range(min(c,y), max(c,y)+1):
                    for k in range(min(b,x), max(b,x)+1):
                        cubo[i][j][k] = "?"
                        estacion.append((i+1,k+1,j+1))
            print("Estación colocada")
    return cubo,estacion

#La siguiente función utiliza la lista "celdas" utilizada en la sección de Armamento
#Dicha lista esta formasda por tuplas que contienen las coordenadas de las celdas afectadas por las diferentes armas.
#La siguiente funcion recorre dicha lusta comparando las coordenadas del blanco con las ocupadas.

def verificar_impactos(cubo, celdas):
    punto = celdas[i]
    z = punto[0]
    y = punto[1]
    x = punto[2]
    for i in range(len(celdas)):
        if celdas[i] in fragata:
            print("Impacto")
            cubo[z][y][x]=X
            if fragata[0]==X and fragata [1]==X:
                print("Fragata hundida")
                cubo[fragata[0][0]][fragata[0][1]][fragata[0][2]]="#" #Reemplazo todas las celdas
                cubo[fragata[1][0]][fragata[1][1]][fragata[1][2]]="#"  #de la nave por # (hundido)
                flota.remove(fragata)
            
        if celdas[i] in destructor:
            print("Impacto")
            cubo[z][y][x]=X
            if destructor[0]==X and destructor[1]==X and destructor[2]==X:
                print("Destructor hundido")
                cubo[destructor[0][0]][destructor[0][1]][destructor[0][2]]="#"
                cubo[destructor[1][0]][destructor[1][1]][destructor[1][2]]="#"
                cubo[destructor[2][0]][destructor[2][1]][destructor[2][2]]="#"
                flota.remove(destructor)
            
        if celdas[i] in submarino:
            print("Impacto")
            cubo[z][y][x]=X
            if submarino[0]==X and submarino[1]==X  and submarino[2]==X:
                print("Submarino hundido")
                cubo[submarino[0][0]][submarino[0][1]][submarino[0][2]]="#"
                cubo[submarino[1][0]][submarino[1][1]][submarino[1][2]]="#"
                cubo[submarino[2][0]][submarino[2][1]][submarino[2][2]]="#"
                flota.remove(submarino)
            
        if celdas[i] in crucero:
            print("Impacto")
            cubo[z][y][x]=X
            if crucero[0]==X and crucero[1]==X and crucero[2]==X and crucero[3]==X:
                print("Crucero hundido")
                cubo[crucero[0][0]][crucero[0][1]][crucero[0][2]]="#"
                cubo[crucero[1][0]][crucero[1][1]][crucero[1][2]]="#"
                cubo[crucero[2][0]][crucero[2][1]][crucero[2][2]]="#"
                cubo[crucero[3][0]][crucero[3][1]][crucero[3][2]]="#"
                flota.remove(crucero)
        
        if celdas[i] in portaaviones:
            print("Impacto")
            if cubo[z][y][x]=="X":
                cubo[z][y][x]="x"
            if portaaviones[0]==x and portaaviones[1]==x and portaaviones[2]==x and portaaviones[3]==x and portaaviones[4]==x:
                print("Portaaviones hundido")
                cubo[portaaviones[0][0]][portaaviones[0][1]][portaaviones[0][2]]="#"
                cubo[portaaviones[1][0]][portaaviones[1][1]][portaaviones[1][2]]="#"
                cubo[portaaviones[2][0]][portaaviones[2][1]][portaaviones[2][2]]="#"
                cubo[portaaviones[3][0]][portaaviones[3][1]][portaaviones[3][2]]="#"
                cubo[portaaviones[4][0]][portaaviones[4][1]][portaaviones[4][2]]="#"
                flota.remove(portaaviones)
                
        if celdas[i] in estacion:
            print("Impacto")
            cubo[z][y][x]=X
            if estacion[0]==X and estacion[1]==X and estacion[2]==X and estacion[3]==X and estacion[4]==X and estacion[5]==X and estacion[6]==X and estacion[7]==X:
                print("Estacion hundida")
                cubo[estacion[0][0]][estacion[0][1]][estacion[0][2]]="#"
                cubo[estacion[1][0]][estacion[1][1]][estacion[1][2]]="#"
                cubo[estacion[2][0]][estacion[2][1]][estacion[2][2]]="#"
                cubo[estacion[3][0]][estacion[3][1]][estacion[3][2]]="#"
                cubo[estacion[4][0]][estacion[4][1]][estacion[4][2]]="#"
                cubo[estacion[5][0]][estacion[5][1]][estacion[5][2]]="#"
                cubo[estacion[6][0]][estacion[6][1]][estacion[6][2]]="#"
                cubo[estacion[7][0]][estacion[7][1]][estacion[7][2]]="#"
                flota.remove(estacion)
        

        elif cubo[z][y][x] == "~":
            cubo[z][y][x] = "o"
            print("Agua")

        else:
            print("Esta casilla ya fue impactada o no contiene una nave.")

    return cubo
#"derecha" and cubo[z][y][x+4] == "?"
#"izquierda" and cubo[z][y][x-1] == "?"
#"atras" and cubo[z+4][y][x] == "?") or \
#"adelante" and cubo[z-1][y][x] == "?")
#"arriba" and cubo[z][y-2][x] == "?") or \
#"abajo" and cubo[z][y+1][x] == "?")

###############################################################################################

def ubicacion_manual(cubo, catalogo, semilla=None):
    flota_1= []
    #Coloco Fragata
    print("Colocando Fragata (2x1)")
    fragata=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,fragata=colocar_fragata(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,fragata = resultado,fragata
                flota_1.append(fragata)

    
    #Coloco Destructor
    print("Colocando Destructor (3x1)")
    destructor=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,destructor=colocar_destructor(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,destructor = resultado,destructor
                flota_1.append(destructor)

    #Coloco Submarino
    print("Colocando Submarino (3x1)")
    submarino=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,submarino=colocar_submarino(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,submarino = resultado,submarino
                flota_1.append(submarino)

    #Coloco Crucero
    print("Colocando Crucero (4x1)")
    crucero=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,crucero=colocar_crucero(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,crucero = resultado,crucero
                flota_1.append(crucero)

    #Coloco Portaaviones
    print("Colocando Portaaviones (5x1)")
    portaaviones=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,portaaviones=colocar_portaaviones(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,portaaviones = resultado,portaaviones
                flota_1.append(portaaviones)

    #Coloco Estacion
    print("Colocando Estacion (2x2x2)")
    estacion=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        coordenada1=input("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ")
        tupla_inicio = tuple(int(x) for x in coordenada1.split())
        valido1=armamento._validar_punto(tupla_inicio, cubo)
        
        coordenada2=input("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ")
        tupla_final = tuple(int(x) for x in coordenada2.split())
        valido2=armamento._validar_punto(tupla_final, cubo)

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado,estacion=colocar_estacion(cubo,fragata,tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo,estacion = resultado,estacion
                flota_1.append(estacion)
    return cubo, flota_1




def ubicacion_automatica(cubo, catalogo, semilla=None):
    """
    Ubica automáticamente las naves en el cubo.

    Recibe:
        cubo: cubo donde se ubican las naves.
        catalogo: diccionario con los tipos y cantidades de naves.
        semilla: número para repetir las mismas ubicaciones.

    Devuelve:
        Una lista con los datos de las naves ubicadas.

    Excepciones:
        RuntimeError si no se encuentra una posición válida.
    """

    generador = random.Random(semilla)
    catalogo_ordenado = sorted(
        catalogo.items(),
        key=lambda elemento: elemento[1]["tamanio"],
        reverse=True
    )
    n = len(cubo)
    flota = []

    for nombre, datos in catalogo_ordenado:
        tamanio = datos["tamanio"]
        cantidad = datos["cantidad"]

        for numero in range(cantidad):
            ubicada = False

            intentos = 0

            while not ubicada and intentos < 1000:
                intentos += 1

                if nombre == "Submarino":
                    z = generador.randint(n // 2, n - 1)
                elif nombre == "Portaaviones":
                    z = generador.randint(0, n // 2 - 1)
                elif nombre == "Crucero":
                    z = generador.randint(1, n - 2)
                elif nombre == "Estacion":
                    z = generador.randint(1, n - 3)
                else:
                    z = generador.randint(0, n - 1)

                if nombre == "Estacion":
                    y = generador.randint(1, n - 3)
                    x = generador.randint(1, n - 3)

                    celdas = []

                    for cambio_z in range(2):
                        for cambio_y in range(2):
                            for cambio_x in range(2):
                                celdas.append((
                                    z + cambio_z,
                                    y + cambio_y,
                                    x + cambio_x
                                ))

                else:
                    y = generador.randint(0, n - 1)
                    x = generador.randint(0, n - 1)

                    eje = generador.choice(["x", "y", "z"])
                    direccion = generador.choice([-1, 1])

                    celdas = []

                    for i in range(tamanio):
                        nueva_z = z
                        nueva_y = y
                        nueva_x = x

                        if eje == "x":
                            nueva_x = x + i * direccion
                        elif eje == "y":
                            nueva_y = y + i * direccion
                        else:
                            nueva_z = z + i * direccion

                        celdas.append((
                            nueva_z,
                            nueva_y,
                            nueva_x
                        ))

                reglas_validas = True

                for z_celda, y_celda, x_celda in celdas:
                    if nombre == "Submarino":
                        if z_celda < n // 2:
                            reglas_validas = False

                    elif nombre == "Portaaviones":
                        if z_celda >= n // 2:
                            reglas_validas = False

                    elif nombre == "Crucero":
                        if z_celda == 0 or z_celda == n - 1:
                            reglas_validas = False

                    elif nombre == "Estacion":
                        if (z_celda == 0 or z_celda == n - 1
                                or y_celda == 0 or y_celda == n - 1
                                or x_celda == 0 or x_celda == n - 1):
                            reglas_validas = False

                if reglas_validas and posicion_valida(cubo, celdas):
                    for z_celda, y_celda, x_celda in celdas:
                        cubo[z_celda][y_celda][x_celda] = "?"

                    celdas_partida = []

                    for z_celda, y_celda, x_celda in celdas:
                        celdas_partida.append((
                            z_celda + 1,
                            x_celda + 1,
                            y_celda + 1
                        ))

                    nave = {
                        "nombre": nombre,
                        "celdas": celdas_partida,
                        "impactos": set(),
                        "hundida": False,
                        "resistencia": tamanio
                    }

                    flota.append(nave)
                    ubicada = True

            if not ubicada:
                raise RuntimeError(
                    "No se pudo ubicar la nave: " + nombre
                )

    return flota
def posicion_valida(cubo, celdas):
    """
    Recibe el cubo y una lista de coordenadas de la nave.
    Devuelve True si las celdas están libres y no tocan otras naves.
    """

    n = len(cubo)

    for z, y, x in celdas:

        if z < 0 or z >= n or y < 0 or y >= n or x < 0 or x >= n:
            return False

        if cubo[z][y][x] != "~":
            return False

        for vecino_z in range(z - 1, z + 2):
            for vecino_y in range(y - 1, y + 2):
                for vecino_x in range(x - 1, x + 2):

                    if vecino_z >= 0 and vecino_z < n:
                        if vecino_y >= 0 and vecino_y < n:
                            if vecino_x >= 0 and vecino_x < n:

                                if cubo[vecino_z][vecino_y][vecino_x] == "?":
                                    if (vecino_z, vecino_y, vecino_x) not in celdas:
                                        return False

    return True


# Catalogo de naves

CATALOGO_NAVES = {
    "Fragata": {
        "tamanio": 2,
        "cantidad": 3,
        "funcion": colocar_fragata
    },
    "Destructor": {
        "tamanio": 3,
        "cantidad": 2,
        "funcion": colocar_destructor
    },
    "Submarino": {
        "tamanio": 3,
        "cantidad": 2,
        "funcion": colocar_submarino
    },
    "Crucero": {
        "tamanio": 4,
        "cantidad": 1,
        "funcion": colocar_crucero
    },
    "Portaaviones": {
        "tamanio": 5,
        "cantidad": 1,
        "funcion": colocar_portaaviones
    },
    "Estacion": {
        "tamanio": 8,
        "cantidad": 1,
        "funcion": colocar_estacion
    }
}