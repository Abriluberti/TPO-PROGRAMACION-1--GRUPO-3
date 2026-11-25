import random
import armamento
import tablero

def colocar(cubo,diccionario,tupla_inicio, tupla_final):
    a=tupla_inicio[0]-1
    b=tupla_inicio[1]-1
    c=tupla_inicio[2]-1

    z=tupla_final[0]-1
    x=tupla_final[1]-1
    y=tupla_final[2]-1


    if diccionario["reglas"]!=False:
        if diccionario["reglas"]=="submarino":
            if c+1<=len(cubo)/2 or y+1<=len(cubo)/2:
                    print("El submarino no puede colocarse tan alto")
                    return False
                #Comprueba que el submarino este en la mitad inferior del eje Z.

    if diccionario["reglas"]=="crucero":
        if a==0 or z==0 or a==len(cubo)-1 or z==len(cubo)-1:
            print("El crucero no puede colocarse en los bordes del eje Z")
            return False
            #Verifica que la nave no se encuentre en los bordes del eje Z.

    if diccionario["reglas"]=="portaaviones":
        if c+1>len(cubo)/2 or y+1>len(cubo)/2:
            print("El portaaviones no puede colocarse tan bajo")
            return False
        #Comprueba que el portaaviones este en la mitad superior del eje Z.

    if diccionario["reglas"]=="estacion":
        if a==0 or a>=len(cubo) or b==0 or b>=len(cubo) or c==0 or c>=len(cubo) or z==0 or z>=len(cubo) or x==0 or x>=len(cubo) or y==0 or y>=len(cubo):
            print("La estacion no puede colocarse en los bordes del cubo")
            return False
        #Comprueba que la estacion no se encuentre tocando ningun borde del cubo.
            
        if a==z or b==x or c==y:
            print("Las celdas no deben son continuas para la estacion")
            return False
        #Verifica que las celdas NO esten en linea.
            
        else:
            if max(a, z) - min(a, z)!=1 or max(b,x) - min(b, x)!=1 or max(c, y) - min(c, y) !=1:
                raise ValueError("La nave debe ocupar un espacio de 2x2x2")
            elif cubo[a][b][c]=="?" or cubo[a][b][c+1]=="?" or cubo[a][b+1][c]=="?" or cubo[a][b+1][c+1]=="?" or cubo[a+1][b][c]=="?" or cubo[a+1][b][c+1]=="?" or cubo[a+1][b+1][c]=="?" or cubo[a+1][b+1][c+1]=="?":
                print("Ya hay otra nave ocupando esa posición.")
                return False
            #Verifica que ningun punto del cubo este ocupado al verificar sus 8 celdas.
                
            else:
                for i in range(min(a,z), max(a,z)+1):
                    for j in range(min(c,y), max(c,y)+1):
                        for k in range(min(b,x), max(b,x)+1):
                            cubo[i][j][k] = "?"
                            diccionario["celdas"].append((i+1,k+1,j+1))
                print("Estacion colocada")
        return cubo

#Verifico que las celdas sean continuas
    if (a!=z and b!=x) or (a!=z and c!=y) or (b!=x and c!=y):
        print("Las celdas no son continuas")
        return False



        # Si varía en el eje Z (profundidad)
    if b == x and c == y:
        if max(a, z) - min(a, z)!=diccionario["tamanio"]-1:
            print("La nave debe ocupar ", diccionario["tamanio"], "espacios")
            return False
        for i in range(min(a, z), max(a, z) + 1):
            if cubo[i][c][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False
        for i in range(min(a, z), max(a, z) + 1):
            cubo[i][c][b] = "?"
            diccionario["celdas"].append((i+1,b+1,c+1))
        print(diccionario["nombre"], "colocada")

    # Si varía en el eje X (longitud)
    if a == z and c == y:
        if max(b, x) - min(b, x) != diccionario["tamanio"]-1:
            print("La nave debe ocupar ", diccionario["tamanio"], "espacios")
            return False
        for j in range(min(b, x), max(b, x) + 1):
            if cubo[a][c][j] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False
        for j in range(min(b, x), max(b, x) + 1):
            cubo[a][c][j] = "?"
            diccionario["celdas"].append((a+1,j+1,c+1))
        print(diccionario["nombre"], "colocada")

    # Si varía en el eje Y (altura)
    if a == z and b == x:
        if max(c, y) - min(c, y) != diccionario["tamanio"]-1:
            print("La nave debe ocupar ", diccionario["tamanio"], "espacios")
            return False
        for k in range(min(c, y), max(c, y) + 1):
            if cubo[a][k][b] == "?":
                print("Ya hay otra nave ocupando esa posición.")
                return False
        for k in range(min(c, y), max(c, y) + 1):
            cubo[a][k][b] = "?"
            diccionario["celdas"].append((a+1,b+1,k+1))
        print(diccionario["nombre"], "colocada")
            
    return cubo

#La siguiente función utiliza la lista "celdas" utilizada en la sección de Armamento
#Dicha lista esta formada por tuplas que contienen las coordenadas de las celdas afectadas por las diferentes armas.
#La siguiente funcion recorre dicha lista comparando las coordenadas del blanco con las ocupadas.

def verificar_impactos(cubo, celdas, CATALOGO_NAVES, flota):
    punto = celdas[i]
    z = punto[0]
    y = punto[1]
    x = punto[2]
    for i in range(len(celdas)):

#Chequeo Fragata
        if celdas[i] in CATALOGO_NAVES["Fragata"]["celdas"]:
            print("Impacto")
            cubo[z][y][x]=X
            if CATALOGO_NAVES["Fragata"]["celdas"][0]==X and CATALOGO_NAVES["Fragata"]["celdas"][1]==X:
                print("Fragata hundida")
                cubo[CATALOGO_NAVES["Fragata"]["celdas"][0][0]][CATALOGO_NAVES["Fragata"]["celdas"][0][1]][CATALOGO_NAVES["Fragata"]["celdas"][0][2]]="#" #Reemplazo todas las celdas
                cubo[CATALOGO_NAVES["Fragata"]["celdas"][1][0]][CATALOGO_NAVES["Fragata"]["celdas"][1][1]][CATALOGO_NAVES["Fragata"]["celdas"][1][2]]="#"  #de la nave por # (hundido)
                flota.remove(CATALOGO_NAVES["Fragata"]["celdas"])
                CATALOGO_NAVES["Fragata"]["estado"] = "hundida"

#Chequeo Destructor
        if celdas[i] in CATALOGO_NAVES["Destructor"]["celdas"]:
            print("Impacto")
            cubo[z][y][x]=X
            if CATALOGO_NAVES["Destructor"]["celdas"][0]==X and CATALOGO_NAVES["Destructor"]["celdas"][1]==X and CATALOGO_NAVES["Destructor"]["celdas"][2]==X:
                print("Destructor hundido")
                cubo[CATALOGO_NAVES["Destructor"]["celdas"][0][0]][CATALOGO_NAVES["Destructor"]["celdas"][0][1]][CATALOGO_NAVES["Destructor"]["celdas"][0][2]]="#"
                cubo[CATALOGO_NAVES["Destructor"]["celdas"][1][0]][CATALOGO_NAVES["Destructor"]["celdas"][1][1]][CATALOGO_NAVES["Destructor"]["celdas"][1][2]]="#"
                cubo[CATALOGO_NAVES["Destructor"]["celdas"][2][0]][CATALOGO_NAVES["Destructor"]["celdas"][2][1]][CATALOGO_NAVES["Destructor"]["celdas"][2][2]]="#"
                flota.remove(CATALOGO_NAVES["Destructor"]["celdas"])
                CATALOGO_NAVES["Destructor"]["estado"] = "hundida"

#Chequeo Submarino
        if celdas[i] in CATALOGO_NAVES["Submarino"]["celdas"]:
            print("Impacto")
            cubo[z][y][x]=X
            if CATALOGO_NAVES["Submarino"]["celdas"][0]==X and CATALOGO_NAVES["Submarino"]["celdas"][1]==X  and CATALOGO_NAVES["Submarino"]["celdas"][2]==X:
                print("Submarino hundido")
                cubo[CATALOGO_NAVES["Submarino"]["celdas"][0][0]][CATALOGO_NAVES["Submarino"]["celdas"][0][1]][CATALOGO_NAVES["Submarino"]["celdas"][0][2]]="#"
                cubo[CATALOGO_NAVES["Submarino"]["celdas"][1][0]][CATALOGO_NAVES["Submarino"]["celdas"][1][1]][CATALOGO_NAVES["Submarino"]["celdas"][1][2]]="#"
                cubo[CATALOGO_NAVES["Submarino"]["celdas"][2][0]][CATALOGO_NAVES["Submarino"]["celdas"][2][1]][CATALOGO_NAVES["Submarino"]["celdas"][2][2]]="#"
                flota.remove(CATALOGO_NAVES["Submarino"]["celdas"])
                CATALOGO_NAVES["Submarino"]["estado"] = "hundida"

#Chequeo Crucero
        if celdas[i] in CATALOGO_NAVES["Crucero"]["celdas"]:
            print("Impacto")
            cubo[z][y][x]=X
            if CATALOGO_NAVES["Crucero"]["celdas"][0]==X and CATALOGO_NAVES["Crucero"]["celdas"][1]==X and CATALOGO_NAVES["Crucero"]["celdas"][2]==X and CATALOGO_NAVES["Crucero"]["celdas"][3]==X:
                print("Crucero hundido")
                cubo[CATALOGO_NAVES["Crucero"]["celdas"][0][0]][CATALOGO_NAVES["Crucero"]["celdas"][0][1]][CATALOGO_NAVES["Crucero"]["celdas"][0][2]]="#"
                cubo[CATALOGO_NAVES["Crucero"]["celdas"][1][0]][CATALOGO_NAVES["Crucero"]["celdas"][1][1]][CATALOGO_NAVES["Crucero"]["celdas"][1][2]]="#"
                cubo[CATALOGO_NAVES["Crucero"]["celdas"][2][0]][CATALOGO_NAVES["Crucero"]["celdas"][2][1]][CATALOGO_NAVES["Crucero"]["celdas"][2][2]]="#"
                cubo[CATALOGO_NAVES["Crucero"]["celdas"][3][0]][CATALOGO_NAVES["Crucero"]["celdas"][3][1]][CATALOGO_NAVES["Crucero"]["celdas"][3][2]]="#"
                flota.remove(CATALOGO_NAVES["Crucero"]["celdas"])
                CATALOGO_NAVES["Crucero"]["estado"] = "hundida"

#Chequeo Poortaaviones
        if celdas[i] in CATALOGO_NAVES["Portaaviones"]["celdas"]:
            print("Impacto")
            if cubo[z][y][x]=="X":
                print("Impacto")
                cubo[z][y][x]="x"
            if CATALOGO_NAVES["Portaaviones"]["celdas"][0]==x and CATALOGO_NAVES["Portaaviones"]["celdas"][1]==x and CATALOGO_NAVES["Portaaviones"]["celdas"][2]==x and CATALOGO_NAVES["Portaaviones"]["celdas"][3]==x and CATALOGO_NAVES["Portaaviones"]["celdas"][4]==x:
                print("Portaaviones hundido")
                cubo[CATALOGO_NAVES["Portaaviones"]["celdas"][0][0]][CATALOGO_NAVES["Portaaviones"]["celdas"][0][1]][CATALOGO_NAVES["Portaaviones"]["celdas"][0][2]]="#"
                cubo[CATALOGO_NAVES["Portaaviones"]["celdas"][1][0]][CATALOGO_NAVES["Portaaviones"]["celdas"][1][1]][CATALOGO_NAVES["Portaaviones"]["celdas"][1][2]]="#"
                cubo[CATALOGO_NAVES["Portaaviones"]["celdas"][2][0]][CATALOGO_NAVES["Portaaviones"]["celdas"][2][1]][CATALOGO_NAVES["Portaaviones"]["celdas"][2][2]]="#"
                cubo[CATALOGO_NAVES["Portaaviones"]["celdas"][3][0]][CATALOGO_NAVES["Portaaviones"]["celdas"][3][1]][CATALOGO_NAVES["Portaaviones"]["celdas"][3][2]]="#"
                cubo[CATALOGO_NAVES["Portaaviones"]["celdas"][4][0]][CATALOGO_NAVES["Portaaviones"]["celdas"][4][1]][CATALOGO_NAVES["Portaaviones"]["celdas"][4][2]]="#"
                flota.remove(CATALOGO_NAVES["Portaaviones"]["celdas"])
                CATALOGO_NAVES["Portaaviones"]["estado"] = "hundida"

#Chequeo estacion
        if celdas[i] in CATALOGO_NAVES["Estacion"]["celdas"]:
            print("Impacto")
            cubo[z][y][x]="X"
            if CATALOGO_NAVES["Estacion"]["celdas"][0]==X and CATALOGO_NAVES["Estacion"]["celdas"][1]==X and CATALOGO_NAVES["Estacion"]["celdas"][2]==X and CATALOGO_NAVES["Estacion"]["celdas"][3]==X and CATALOGO_NAVES["Estacion"]["celdas"][4]==X and CATALOGO_NAVES["Estacion"]["celdas"][5]==X and CATALOGO_NAVES["Estacion"]["celdas"][6]==X and CATALOGO_NAVES["Estacion"]["celdas"][7]==X:
                print("Estacion hundida")
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][0][0]][CATALOGO_NAVES["Estacion"]["celdas"][0][1]][CATALOGO_NAVES["Estacion"]["celdas"][0][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][1][0]][CATALOGO_NAVES["Estacion"]["celdas"][1][1]][CATALOGO_NAVES["Estacion"]["celdas"][1][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][2][0]][CATALOGO_NAVES["Estacion"]["celdas"][2][1]][CATALOGO_NAVES["Estacion"]["celdas"][2][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][3][0]][CATALOGO_NAVES["Estacion"]["celdas"][3][1]][CATALOGO_NAVES["Estacion"]["celdas"][3][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][4][0]][CATALOGO_NAVES["Estacion"]["celdas"][4][1]][CATALOGO_NAVES["Estacion"]["celdas"][4][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][5][0]][CATALOGO_NAVES["Estacion"]["celdas"][5][1]][CATALOGO_NAVES["Estacion"]["celdas"][5][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][6][0]][CATALOGO_NAVES["Estacion"]["celdas"][6][1]][CATALOGO_NAVES["Estacion"]["celdas"][6][2]]="#"
                cubo[CATALOGO_NAVES["Estacion"]["celdas"][7][0]][CATALOGO_NAVES["Estacion"]["celdas"][7][1]][CATALOGO_NAVES["Estacion"]["celdas"][7][2]]="#"
                flota.remove(CATALOGO_NAVES["Estacion"]["celdas"])
        

        elif cubo[z][y][x] == "~":
            cubo[z][y][x] = "o"
            print("Agua")

        else:
            print("Esta casilla ya fue impactada o no contiene una nave.")

    return cubo

###############################################################################################
def pedir_coordenada(mensaje, tam_cubo):
    while True:
        entrada = input(mensaje)
        partes = entrada.split()

        # 1. Verificamos que haya exactamente 3 elementos separados por espacios
        if len(partes) != 3:
            print("Error: Debes ingresar exactamente 3 números separados por espacios (ej: 1 2 3).")
            continue

        # 2. Intentamos convertir los 3 elementos a enteros
        try:
            tupla = tuple(int(x) for x in partes)
        except ValueError:
            print("Error: Solo se permiten números enteros separados por espacios.")
            continue

        # Si pasó todas las pruebas, devolvemos la tupla limpia
        return tupla

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
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1 = tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2 = tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Fragata"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Fragata"]["celdas"])

    
    #Coloco Destructor
    print("Colocando Destructor (3x1)")
    destructor=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Destructor"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Destructor"]["celdas"])

    #Coloco Submarino
    print("Colocando Submarino (3x1)")
    submarino=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Submarino"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Submarino"]["celdas"])

    #Coloco Crucero
    print("Colocando Crucero (4x1)")
    crucero=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Crucero"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Crucero"]["celdas"])

    #Coloco Portaaviones
    print("Colocando Portaaviones (5x1)")
    portaaviones=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Portaaviones"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Portaaviones"]["celdas"])

    #Coloco Estacion
    print("Colocando Estacion (2x2x2)")
    estacion=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        tupla_inicio = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'DESDE': ", len(cubo))
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        
        tupla_final = pedir_coordenada("Ingresá 3 dígitos separados por espacios de la coordenada 'HASTA': ", len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Estacion"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_1.append(CATALOGO_NAVES["Estacion"]["celdas"])
    return cubo, flota_1




def ubicacion_automatica(cubo, catalogo, semilla=None):
    flota_2= []
    #Coloco Fragata
    print("Colocando Fragata (2x1)")
    fragata=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(1,len(cubo))
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(1,len(cubo))
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(1,len(cubo))
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)

        lista_final=[]
        coordenada4=random.choice([coordenada1, coordenada1+1, coordenada1-1])
        if coordenada4!=coordenada1:
            coordenada5=coordenada2
            coordenada6=coordenada3
        if coordenada4==coordenada1:
            coordenada5=random.choice([coordenada2, coordenada2+1, coordenada2-1])
            if coordenada5!=coordenada2:
                coordenada6=coordenada3
            if coordenada5==coordenada2:
                coordenada6=random.choice([coordenada3+1, coordenada3-1])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)
        
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Fragata"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Fragata"]["celdas"])

    
    #Coloco Destructor
    print("Colocando Destructor (3x1)")
    destructor=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(1,len(cubo))
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(1,len(cubo))
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(1,len(cubo))
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)
    
        lista_final=[]
        coordenada4=random.choice([coordenada1, coordenada1+2, coordenada1-2])
        if coordenada4!=coordenada1:
            coordenada5=coordenada2
            coordenada6=coordenada3
        if coordenada4==coordenada1:
            coordenada5=random.choice([coordenada2, coordenada2+2, coordenada2-2])
            if coordenada5!=coordenada2:
                coordenada6=coordenada3
            if coordenada5==coordenada2:
                coordenada6=random.choice([coordenada3+2, coordenada3-2])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)

        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Destructor"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Destructor"]["celdas"])

    #Coloco Submarino
    print("Colocando Submarino (3x1)")
    submarino=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(1,len(cubo))
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(1,len(cubo))
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(int(len(cubo)/2),8)
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)
    
        lista_final=[]
        coordenada4=random.choice([coordenada1, coordenada1+2, coordenada1-2])
        if coordenada4!=coordenada1:
            coordenada5=coordenada2
            coordenada6=coordenada3
        if coordenada4==coordenada1:
            coordenada5=random.choice([coordenada2, coordenada2+2, coordenada2-2])
            if coordenada5!=coordenada2:
                coordenada6=coordenada3
            if coordenada5==coordenada2:
                coordenada6=random.choice([coordenada3+2, coordenada3-2])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)

        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Submarino"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Submarino"]["celdas"])

    #Coloco Crucero
    print("Colocando Crucero (4x1)")
    crucero=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(1,len(cubo))
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(1,len(cubo))
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(1,len(cubo))
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)
        
        lista_final=[]
        coordenada4=random.choice([coordenada1, coordenada1+3, coordenada1-3])
        if coordenada4!=coordenada1:
            coordenada5=coordenada2
            coordenada6=coordenada3
        if coordenada4==coordenada1:
            coordenada5=random.choice([coordenada2, coordenada2+3, coordenada2-3])
            if coordenada5!=coordenada2:
                coordenada6=coordenada3
            if coordenada5==coordenada2:
                coordenada6=random.choice([coordenada3+3, coordenada3-3])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)

        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))

        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Crucero"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Crucero"]["celdas"])

    #Coloco Portaaviones
    print("Colocando Portaaviones (5x1)")
    portaaviones=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(1,len(cubo))
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(1,len(cubo))
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(1,len(cubo))
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)
        
        lista_final=[]
        coordenada4=random.choice([coordenada1, coordenada1+4, coordenada1-4])
        if coordenada4!=coordenada1:
            coordenada5=coordenada2
            coordenada6=coordenada3
        if coordenada4==coordenada1:
            coordenada5=random.choice([coordenada2, coordenada2+4, coordenada2-4])
            if coordenada5!=coordenada2:
                coordenada6=coordenada3
            if coordenada5==coordenada2:
                coordenada6=random.choice([coordenada3+4, coordenada3-4])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)
        
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))
        
        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Portaaviones"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Portaaviones"]["celdas"])

    #Coloco Estacion
    print("Colocando Estacion (2x2x2)")
    estacion=[]
    colocada=False
    valido1= False
    valido2= False
    while colocada== False:
        lista_inicio=[]
        coordenada1=random.randint(2,len(cubo)-1)
        lista_inicio.append(coordenada1)
        coordenada2=random.randint(2,len(cubo)-1)
        lista_inicio.append(coordenada2)
        coordenada3=random.randint(2,len(cubo)-1)
        lista_inicio.append(coordenada3)
        tupla_inicio=tuple(lista_inicio)
        
        lista_final=[]
        coordenada4=random.choice([coordenada1+1, coordenada1-1])
        #if coordenada4==coordenada1+1:
            #coordenada5=coordenada2
            #coordenada6=coordenada3
        #if coordenada4==coordenada1:
        coordenada5=random.choice([coordenada2+1, coordenada2-1])
            #if coordenada5!=coordenada2:
                #coordenada6=coordenada3
            #if coordenada5==coordenada2:
        coordenada6=random.choice([coordenada3+1, coordenada3-1])
        lista_final.append(coordenada4)
        lista_final.append(coordenada5)
        lista_final.append(coordenada6)
        tupla_final=tuple(lista_final)
        
        valido1=tablero.punto_valido(tupla_inicio, len(cubo))
        valido2=tablero.punto_valido(tupla_final, len(cubo))
        
        if valido1 == False or valido2 == False:
            print("Coordenadas inválidas. Deben ser enteros entre 1 y " + str(len(cubo)))
        elif valido1 == True and valido2 == True:
            resultado=colocar(cubo,CATALOGO_NAVES["Estacion"],tupla_inicio, tupla_final)
            if resultado!= False:
                colocada=True
                cubo= resultado
                flota_2.append(CATALOGO_NAVES["Estacion"]["celdas"])
    return cubo, flota_2

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
        "nombre": "Fragata",
        "tamanio": 2,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": False
    },
    "Destructor": {
        "nombre": "Destructor",
        "tamanio": 3,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": False
    },
    "Submarino": {
        "nombre": "Submarino",
        "tamanio": 3,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": "submarino"
    },
    "Crucero": {
        "nombre": "Crucero",
        "tamanio": 4,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": "crucero"
    },
    "Portaaviones": {
        "nombre": "Portaaviones",
        "tamanio": 5,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": "portaaviones"
    },
    "Estacion": {
        "nombre": "Estacion",
        "tamanio": 8,
        "cantidad": 1,
        "celdas": [],
        "estado": "sano",
        "reglas": "estacion"
    }
}