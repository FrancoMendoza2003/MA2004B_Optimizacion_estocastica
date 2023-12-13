import pandas as pd
import numpy as np

# Cantidad de clientes
nClientes= 100
nTiempo= 8
Camiones=1
nRampas=1


VCarro=7.36

def simulacion():
    df= pd.read_excel('distancias_extras.xlsx',index_col='Unnamed: 0')
    df = df.astype(float)

    #Guardar fila 0
    fila0=pd.DataFrame(df.loc[0])
    fila0=fila0.T

    #Borrar fila 0
    df = df.drop(index=0)

    #Escoger una muestra de 100 nodos aleatorios

    # Concatenar la fila de 0 siempre
    dF=df.sample(n=nClientes)
    dF = pd.concat([fila0, dF], ignore_index=False)

    # Dejar solamente las columnas correspondientes a las filas
    nodos=list(dF.index)
    nodoss=[(x) for x in nodos]
    dF=dF[nodoss]

    #Cambiar el nombre de las columnas y filasde 0 a 100
    dF=dF.reset_index(drop=True)
    dF.columns
    new_column_names = {old_name: i for i, old_name in enumerate(dF.columns)}
    dF.rename(columns=new_column_names, inplace=True)

    dict_from_df = dF.to_dict(orient='index')

    #Evitar que el nodo viaje a sí mismo
    for i in dict_from_df.keys():
        dict_from_df[i].pop(i)

    dr= pd.read_excel('rutas_auto.xlsx',index_col='Unnamed: 0')
    #dr = dr.astype(float)
    dr=dr.reset_index(drop=True)
    new_column_names = {old_name: i for i, old_name in enumerate(dr.columns)}
    dr.rename(columns=new_column_names, inplace=True)

    dR=dr.loc[nodos]
    # Dejar solamente las columnas correspondientes a las filas
    nodoS=list(dR.index)
    dR=dR[nodoS]
    #Cambiar el nombre de las columnas y filas de 0 a 100
    dR=dR.reset_index(drop=True)
    dR.columns
    new_column_names = {old_name: i for i, old_name in enumerate(dR.columns)}
    dR.rename(columns=new_column_names, inplace=True)

    dict_from_dr = dR.to_dict(orient='index')

    #Evitar que el nodo viaje a sí mismo
    for i in dict_from_dr.keys():
        dict_from_dr[i].pop(i)
    dict_from_dr

    dt= pd.read_excel('matriz_tiempo.xlsx',index_col='Unnamed: 0')
    #dt = dt.astype(float)
    dt=dt.reset_index(drop=True)
    new_column_names = {old_name: i for i, old_name in enumerate(dt.columns)}
    dt.rename(columns=new_column_names, inplace=True)

    dT=dt.loc[nodos]
    # Dejar solamente las columnas correspondientes a las filas
    nodoS=list(dT.index)
    dT=dT[nodoS]
    #Cambiar el nombre de las columnas y filas de 0 a 100
    dT=dT.reset_index(drop=True)
    dT.columns
    new_column_names = {old_name: i for i, old_name in enumerate(dT.columns)}
    dT.rename(columns=new_column_names, inplace=True)

    dict_from_dt = dT.to_dict(orient='index')

    #Evitar que el nodo viaje a sí mismo
    for i in dict_from_dt.keys():
        dict_from_dt[i].pop(i)
    dict_from_dt

    dP= pd.read_csv('info_productos.csv',index_col='Producto')
    dictProductos = dP.to_dict(orient='index')

    compras=pd.read_excel("simulacion_final_completa.xlsx",index_col='Cliente')



    # Obtain 100 random rows from the DataFrame
    CC = compras.sample(n=nClientes+1)#compras.sample(n=100, random_state=42)# Set a random seed for reproducibility
    CC = CC.reset_index(drop=True)
    dCompra=CC.to_dict(orient='index')
    dCompra[0]=VCarro

    #Copiar dCompra para tener el estado inicial
    import copy
    E=copy.deepcopy(dCompra)
    clients=list(E.keys())
    clients.remove(0)
    for i in clients:
        E[i]['Unidades']=0

    def calcularVolumen(cliente):
            totalV=0
            if cliente == 0:
                    return -VCarro
                    exit()
            #for j in dCompra[cliente]:

                
            cant=dCompra[cliente]['Unidades']
            totalV+=dictProductos[dCompra[cliente]['Producto']][' Volumen mtro3']*cant
                
            return totalV
    '''
    def tRes(a,state):
        if a == 'Bodega':
            if (state[-1][3]<=0.5):
                return -8
                exit()
            return 0
            exit()
        return dict_from_df[state[-1][0]][a]
    '''
    def tRes(a,state,res):
        if a == 0:
            if res ==0:
                return -(nTiempo-1)
                exit()
        return dict_from_dt[state[-1][0]][a]

    #---------------------------------------------------------------------------------------------------------------
    #    Esqueleto de PSA para el problema de tour de Europa
    #---------------------------------------------------------------------------------------------------------------

    from simpleai.search import SearchProblem, depth_first, breadth_first, uniform_cost, greedy, astar
    from simpleai.search.viewers import BaseViewer, ConsoleViewer, WebViewer

    import time
    import copy

    #---------------------------------------------------------------------------------------------------------------
    #   Definición del problema
    #---------------------------------------------------------------------------------------------------------------

    class Tour(SearchProblem):
        """ 
            Clase que es usada para definir el problema del Tour de Europa. Los estados son representados 
            con los nombres de las ciudades.
        """

        def __init__(self, origen):
            """ Constructor de la clase. Inicializa el problema de acuerdo a ...
        
                origen: ciudad de partida
                destino: ciudad meta
            """
            
            # Llama al constructor de su superclase SearchProblem (estado inicial = ciudad origen).
            #Capactidad de volumen
            self.capacidad=VCarro
            self.tiempo=nTiempo-1
            self.idCamion=1
            self.dia=1
            self.rampas=nRampas
            #Pedido entregado 
            pedidos=0
            #Tiempo restante en la jornada laboral
            #tiempo=8
            self.statuscamiones = [nTiempo] * Camiones
            
            if self.rampas==2:
                for i in range(0, len(self.statuscamiones), self.rampas):
                    self.statuscamiones[i] = self.statuscamiones[i + 1] = (self.statuscamiones[i]-(i+1))
            
            elif self.rampas==3:
                for i in range(0, len(self.statuscamiones), self.rampas):
                    self.statuscamiones[i] = self.statuscamiones[i + 1] = self.statuscamiones[i + 2]  = (self.statuscamiones[i]-(i+1))
                
            elif self.rampas ==1:
                for i in range(len(self.statuscamiones)):
                    self.statuscamiones[i]-=(i+1)
            
            self.statuscamiones=tuple(self.statuscamiones)

            origen=[(0,0,self.capacidad,self.tiempo,self.statuscamiones,self.idCamion,self.dia)]
            origen=tuple(origen)
            SearchProblem.__init__(self, origen)
            #self.destino=len(ciudades_vecinas)
            
            # Define el estado meta = ciudad destino.
            #self.goal_state = ('Paris', 'Burdeos', 'Estrasburgo', 'San Sebastian', 'Lyon', 'Ginebra', 'Barcelona', 'Grenoble', 'Cannes')#'Cannes'
        
        def actions(self, state):
            """ 
                Este método regresa una lista con las acciones posibles que pueden ser ejecutadas de 
                acuerdo con el estado especificado.
                
                state: Nombre de la ciudad actual
            
            """
            posible = list(dict_from_df[state[-1][0]].keys())
            posible = posible[:nClientes]
            posible = [int(element) for element in posible]
            p=copy.deepcopy(posible)

            #Evitar pasarse del volumen
            listt=[]
            for j in p:
                #time.sleep(1)
                #print(state[-1][2]-calcularVolumen(i))
                if((state[-1][2]-calcularVolumen(j))<0):
                    listt.append(j)
                    #print("no se puede")
            for i in listt:
                if i in posible:
                    posible.remove(i)
            
            #print(posible)
            #Evitar pasarse del tiempo
            listt=[]
            for j in p:
                #time.sleep(1)
                #print(state[-1][2]-calcularVolumen(i))
                #print(j)
                
                if(state[-1][0]!=0):
                    if(j!=0):
                        if((state[-1][3]-dict_from_dt[state[-1][0]][j])<=dict_from_dt[j][0]):
                        
                            listt.append(j)
                        #print("no se puede")
            for i in listt:
                if i in posible:
                    posible.remove(i)
            #print(state)
            if(state[-1][0]!=0):
                pass
                #print(dict_from_dt[state[-1][0]][0])
            #print(posible)
            #print(p)
            #self.ress=99
            #Evitar repetidos
            lista=[]
            for i in state:
                if i[0]!=0:
                    lista.append(i[0])
        
            for i in lista:
                if i in posible:
                    posible.remove(i)
            
        
            
            posible = [int(element) for element in posible]
            
            #print(posible)
            
        
            
            return posible #Regresar lista con el nombre de nodos posibles

            '''
            #Borrar los nodos ya visitados en otra ruta
            if(state[-1][2]>0.0005):
                posible = list(dict_from_df[state[-1][0]].keys())
                posible = posible[:nClientes]
                posible = [int(element) for element in posible]
                lista=[]
                for i in state:
                    if i[0]!=0:
                        lista.append(i[0])
            
                for i in lista:
                    if i in posible:
                        posible.remove(i)
                
                p = [int(element) for element in posible]

                
            
                
                return p #Regresar lista con el nombre de nodos posibles
            elif (state[-1][2]<=0.0005) :#or (state[-1][3]<=0.5) :
                posible=[0]
                return posible
            '''

        def result(self, state, action):
            """ 
                Este método regresa el nuevo estado obtenido despues de ejecutar la acción.

                state: Una ciudad origen (la actual).
                action: Ciudad especificada por action
            """
            
            
            #print(type(action))
            #Copiar el estado actual
            s=list(state)
            s=s.copy()
            dia=state[-1][6]
            if(action==0):
                dia+=1
                #print('algoo')
                demand=dCompra[action]
            if(action !=0):
                demand=tuple(dCompra[action].items())
            
            #restriccion=self.ress
            
            volumenTrasladado=s[-1][2]-calcularVolumen(action)
            restriccion=0
            if volumenTrasladado>=VCarro:
                volumenTrasladado=VCarro
                restriccion=1

            

            
            tiempoRestante=s[-1][3]-(tRes(action,state,restriccion))
            if tiempoRestante>=(nTiempo):
                tiempoRestante=(nTiempo)
                
            ##
            tiempos=state[-1][4]
            tiempos=list(tiempos)
            
                
            
            tiempos[(state[-1][5])-1]=tiempoRestante
            #tiempos=tuple(tiempos)
            restriccion=0
            ## 

            ###
            numCamion=state[-1][5]
            if action ==0:
                numCamion+=1
                
                if numCamion>Camiones:
                    numCamion=1
                """
                if numCamion>2:
                    if numCamion>=Camiones:
                        numCamion=1
                elif numCamion<=2:
                """
            if Camiones==1:
                    if dia != state[-1][6]:
                        if self.rampas==1:
                            for i in range(len(tiempos)):
                                tiempos[i]=nTiempo
                                tiempos[i]-=(i+1)
                                tiempoRestante=nTiempo-1
                        if self.rampas==2:
                            for i in range(0, len(tiempos), self.rampas):
                                tiempos[i] = tiempos[i + 1] = (tiempos[i]-(i+1))

            

            if Camiones != state[-1][5]:
                
                tiempoRestante=state[-1][4][numCamion-1]
                for i in range(len(tiempos)):
                    tiempos[numCamion-1]=tiempoRestante
                    tiempos[i]=nTiempo-1
                if numCamion==1:
                    dia+=1
                    if self.rampas==1:
                        for i in range(len(tiempos)):
                            tiempos[i]=nTiempo
                            tiempos[i]-=(i+1)
                            tiempoRestante=nTiempo-1
                    if self.rampas==2:
                        for i in range(0, len(tiempos), self.rampas):
                            tiempos[i] = tiempos[i + 1] = (tiempos[i]-(i+1))


            tiempos=tuple(tiempos)
            

            
            
            

            

            #Lista para guardar toda la información del resultado
            traslado=list()
            traslado.append(action)
            traslado.append(demand)
            #print(action)
            traslado.append(volumenTrasladado)
            traslado.append(tiempoRestante)
            traslado.append(tiempos)
            traslado.append(numCamion)
            traslado.append(dia)
            #traslado.append(tiempoRestante)
            traslado=tuple(traslado)
            s.append(traslado)
            #print(s)
            state=tuple(s)
        
            
            
            #state=tuple(state)

            return state

        def is_goal(self, state):
            """ 
                This method evaluates whether the specified state is the goal state.

                state: The state to be tested.
            """
            
        
            entregado=copy.deepcopy(E)
            
            #
            #time.sleep(0.5)
            #print(entregado)
            for i in state:
                if(i[0]!=0):
                    entregado[i[0]]["Unidades"]+=i[1][0][1]
                    #for j in i[1]:
            #print(state)
            #print(entregado)
            #print(state)
                        
            
        
            
            if   entregado==dCompra:#entregado['c1']==Demanda['c1'] and entregado['c2']==Demanda['c2'] and entregado['c3']==Demanda['c3'] and entregado['c4']==Demanda['c4'] and entregado['c5']==Demanda['c5']:
                if state[-1][0]==0:
                    return True
            else:

                return False
            
        def cost(self, state, action, state2):
            """ 
                Este método recibe dos estados y una acción, y regresa el costo de 
                aplicar la acción del primer estado al segundo.

                state: ciudad actual
                action: ciudad a donde me muevo
                state2: ciudad donde finalizas
            """
            return dict_from_dr[state[-1][0]][action] #Regresar el costo de la acción de acuerdo al estado anterior
            
        def heuristic(self, state):
            """ 
                Este método regresa un estimado de la distancia desde el estado a la meta.

                state: ...
            """
        
            listo=[]
            for i in state:
                if i[0]!=0:
                    listo.append((i[0]))
            L=list(dict_from_df[0].keys())
            L=L[:nClientes]
            
            for i in listo:
                if i in L:
                    L.remove(i)
            suma=0
            for i in L:
                suma+=dict_from_df[0][i]
            #if suma==0:
            # 
            
            

            return suma
            

            
            
        
        

    # Despliega los resultados
    def display(result):
        
        if result is not None:
            for i, (action, state) in enumerate(result.path()):
                if action == None:
                    print('Configuración inicial')
                elif i == len(result.path()) - 1:
                    print(i,'- Después de moverse a', action)
                    print('¡Meta lograda con costo =', result.cost,'!')
                else:
                    print(i,'- Después de moverse a', action)

                print('  ', state)
                Rutas=state
            return Rutas
        else:
            print('Mala configuración del problema')
            return 0

    #---------------------------------------------------------------------------------------------------------------
    #   Programa
    #---------------------------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------------------------------------
    #   Programa
    #---------------------------------------------------------------------------------------------------------------



    my_viewer = None
    my_viewer = BaseViewer()       # Solo estadísticas
    #my_viewer = ConsoleViewer()    # Texto en la consola
    #my_viewer = WebViewer()        # Abrir en un browser en la liga http://localhost:8000

    # Crea un PSA y lo resuelve con la búsqueda primero en anchura
    result = greedy(Tour('Paris'), graph_search=True, viewer=my_viewer)
    #result = breadth_first(Tour('Paris'), graph_search=True, viewer=my_viewer)


    if my_viewer != None:
        print('Stats:')
        print(my_viewer.stats)

    print()

    print('>> Búsqueda Primero en Anchura <<')
    Rutas=display(result)



    #---------------------------------------------------------------------------------------------------------------
    #   Fin del archivo
    #---------------------------------------------------------------------------------------------------------------0.

    Trayecto=[]
    RutaCompleta=[]
    contadorR=0
    n=0
    sumVol=0
    sumTiempo=0
    sumdias=0
    for i in range(len(Rutas)):
        if Rutas[i][0] == 0 and n>0 :
            contadorR+=1
            numRuta=('R'+str(contadorR))
            numCamion=('C'+str(Rutas[i-1][5]))
            dia=("Dia: "+str(Rutas[i-1][6]))
            sobVol=("Sobrante m3: "+str(Rutas[i-1][2]))
            sobTiempo=("Sobrante hr: "+str(Rutas[i-1][3]))
            sumVol+=Rutas[i-1][2]
            sumTiempo+=Rutas[i-1][3]
            sumdias=Rutas[i-1][6]
            RutaCompleta.append(numRuta)
            RutaCompleta.append(numCamion)
            RutaCompleta.append(dia)
            RutaCompleta.append(sobVol)
            RutaCompleta.append(sobTiempo)
            RutaCompleta.append(Trayecto)
            Trayecto=[]
            
        
        Trayecto.append(Rutas[i][0])
        n+=1
        
    promVol=sumVol/contadorR
    promTiempo=sumTiempo/contadorR  

    print(RutaCompleta)
    print(result.cost)
    print(promVol)
    print(promTiempo)
    print(sumdias)
    print(contadorR)
    return result.cost,promVol,promTiempo,sumdias,contadorR

sumaC=0
sumaV=0
sumaT=0
sumaD=0
sumaR=0
conteo=0
for i in range(500):
    C,V,T,D,R=simulacion()
    sumaC+=C
    sumaV+=V
    sumaT+=T
    sumaD+=D
    sumaR+=R
    conteo+=1
    print("Sim #",conteo)
promedioC=sumaC/conteo
promedioV=sumaV/conteo
promedioT=sumaT/conteo
promedioD=sumaD/conteo
promedioR=sumaR/conteo
print("Promedio Costo: ",promedioC)
print("Promedio Volumen sobrante: ",promedioV)
print("Promedio Tiempo sobrante: ",promedioT)
print("Promedio Dias: ",promedioD)
print("Promedio Num Rutas: ",promedioR)