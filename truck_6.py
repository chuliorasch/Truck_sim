from itertools import combinations_with_replacement
import sys, re, os
import numpy as np 
import math


def time_corr(tt): # correccion de tiempo para ser costrado en formato hora
    
    tt[0]=21+int(tt[2]/60)
    if tt[0]>=24:
        tt[0]=tt[0]-24
    tt[1]=tt[2]%60 


debug=0

n=10                                    #numero de camiones

t=[21,0,0]                              #tiempo inicial [hr,min,min.totales]

truck=np.zeros((n),dtype=int)           #array para tiempo de cada camion
truck_state=np.zeros((n),dtype=int)     #estado/lugar en el que se encuentra el camion
priority=np.zeros((n,2),dtype=int)

ctrl=[5,8]                              #tiempos de control
ctrl_state=[0,0]                        #estado del ingeniero [0 = libre, 1=trabajandp]

travel=[20,30]                          #tiempos de viajes

shovel=[12,12,20]                       #tiempos de carga
shovel_state=[0,0,0]                    #estado de carga [0=libre, 1=cargando]

belt=[2,2,7]                            #tiempos de descarga
belt_state=[0,0,0]                      #estado descarga y chancado

stop_t_truck=np.zeros((n,2),dtype=int)  #tiempos de los camiones estando detenidos/ a la espera

flags=[0,0,0]                           #contador de camion en cada seccion

var=np.zeros((3,3),dtype=int)           #variables iterantes

process_t=np.zeros((3,3),dtype=int)     #contador de tiempo en seccion
truck_it=np.zeros((n,2),dtype=int)      #tiempo de camion en seccion


os.system("clear")
a=int(input("consultar por: Camion = 1, Mayor demora = 2: "))

if a == 1: 
    os.system("clear")
    b=int(input("\nIngrese numero de camion: "))
    os.system("clear")
    print('\nIngrese lugar donde quiere consultar')
    e=int(input('\nSalida control = 1, Llegada carguio = 2, Salida carguio y transporte = 3, Llegada a descarga y chancado = 4:, trabajo completo = 5:'))
    e=(e*2)+1#3579
    if e ==11:
        e=10
    c=120
    d=120

elif a==2:
    b=10 
    e=11
    c=120
    d=120



while  truck_state[b-1] != [e]: # Mientras no el camion no llegue al estado consultado:
    
    
    #-----------------------------------------------------------------------------------------------
    #Control
    #   Senior Engineer
    
    if (process_t[0,0]==ctrl[0]) and (var[0,0]<n) and (truck_state[var[0,0]]==1):   # 3ro : Se cumplio el tiempo de trabajo?  
        truck_state[var[0,0]]=2                                                     #       Esta el camion en la estacion?
        process_t[0,0]=0
        truck[var[0,0]]+=1
        var[0,0]=flags[0]   
        ctrl_state[0]=0
    
    if (ctrl_state[0]==1) and (var[0,0]<n):                                         # 2do : Esta el camion en  la estacion?
        truck[var[0,0]]+=1
        process_t[0,0]+=1

    if (process_t[0,0]==0) and (var[0,0]<n) and (truck_state[var[0,0]]==0):         # 1ro : El tiempo del camion en el lugar es =0?
        truck_state[var[0,0]]=1                                                     #       Han pasado todos los camiones?      
        var[0,0]=flags[0]                                                           #       Esta el camion antes de entrar a la estacion?
        flags[0]+=1
        ctrl_state[0]=1
        process_t[0,0]+=1
    
    
    if var[0,0]==var[1,0]: var[1,0]=flags[0]                                        # Es el valor de itinerancia igual al anterior? si lo es pasamos al sgte
    
    #   new Engineer ---------------------------
    
    if (process_t[1,0]==ctrl[1]) and (var[1,0]<n) and (truck_state[var[1,0]]==1) :
        truck_state[var[1,0]]=2
        process_t[1,0]=0
        truck[var[1,0]]+=1 
        var[1,0]=flags[0]
        ctrl_state[1]=0
        
    if (ctrl_state[1]==1) and (var[1,0]<n):
        truck[var[1,0]]+=1
        process_t[1,0]+=1   

    if (process_t[1,0]==0)  and (var[1,0]<n) and (truck_state[var[1,0]]==0):
        truck_state[var[1,0]]=1
        var[1,0]=flags[0]
        flags[0]+=1
        ctrl_state[1]=1 
        process_t[1,0]+=1
         
    #-----------------------------------------------------------------------
    # Primer viaje 
    
    for q in range(len(truck_state)):                                           

        if (truck_state[q]==3) and ((truck[q]-truck_it[q,0])==travel[0]-1):     # 3ro: termino el tiempo de viaje el camion?   
            truck_state[q]=4
            truck[q]+=1

        if truck_state[q]==3:                                                   # 2do: esta viajando el camion?
            truck[q]+=1

        if truck_state[q] == 2:                                                 # 1ro: Salio el camion de la estacion anterior?
            truck_it[q,0]=truck[q]
            truck_state[q]=3
        
    
    #-----------------------------------------------------------------------
    #Estacion de Carga:

    # Pala 1:

    if (process_t[0,1]==shovel[0]) and (var[0,1]<n) and (truck_state[var[0,1]]==5):     # 3ro : Se cumplio el tiempo de trabajo?
        truck_state[var[0,1]]=6                                                         #       Esta el camion en la estacion?
        process_t[0,1]=0
        truck[var[0,1]]+=1
        var[0,1]=flags[1]   
        shovel_state[0]=0
        
    
    if (shovel_state[0]==1) and (var[0,1]<n):                                           # 2do : Esta el camion en  la estacion?
        truck[var[0,1]]+=1
        process_t[0,1]+=1

    for i in range(n):                                                                  # 1ro : Igual a la estacion anterior, pero esta vez se pregunta si hay algun camion esta esperando y cuanto lleva esperando                                                        

        if (process_t[0,1]==0) and (var[0,1]<n) and (truck_state[var[0,1]]==4) and (priority[i,0]==np.amax(priority[:,0])) and (priority[i,0]!=0):  # ve el caso que haya 1 o mas camiones esperando
            var[0,1]=i                                                              
            truck_state[var[0,1]]=5                                             
            shovel_state[0]=1
            process_t[0,1]+=1
            priority[i,0]=0
            for j in range(n):
                if truck_state[j]==4:
                    flags[1]=j
                    break
        
        if (process_t[0,1]==0) and (var[0,1]<n) and (truck_state[var[0,1]]==4) and (not(any(priority[:,0]))): # ve el caso de que llegue el camion cuando recien se haya desocupado la estacion
            truck_state[var[0,1]]=5
            var[0,1]=flags[1]
            flags[1]+=1
            shovel_state[0]=1
            process_t[0,1]+=1
  
    if var[1,1]==var[0,1] or var[1,1]==var[2,1] : var[1,1]=flags[1] ## Es el valor de itinerancia igual al anterior? si lo es pasamos al sgte


    # Pala 2:

    if (process_t[1,1]==shovel[1]) and (var[1,1]<n) and (truck_state[var[1,1]]==5):
        truck_state[var[1,1]]=6
        process_t[1,1]=0
        truck[var[1,1]]+=1
        var[1,1]=flags[1]   
        shovel_state[1]=0

    if (shovel_state[1]==1) and (var[1,1]<n):
        truck[var[1,1]]+=1
        process_t[1,1]+=1

    for i in range(n):
        
        if (process_t[1,1]==0) and (var[1,1]<n) and (truck_state[var[1,1]]==4) and (priority[i,0]==np.amax(priority[:,0])) and (priority[i,0]!=0):
            var[1,1]=i
            truck_state[var[1,1]]=5
            shovel_state[1]=1
            process_t[1,1]+=1
            priority[i,0]=0
            for j in range(n):
                if truck_state[j]==4:
                    flags[1]=j
                    break

        if (process_t[1,1]==0) and (var[1,1]<n) and (truck_state[var[1,1]]==4) and (not(any(priority[:,0]))):
            truck_state[var[1,1]]=5
            var[1,1]=flags[1]
            flags[1]+=1
            shovel_state[1]=1
            process_t[1,1]+=1   

    if var[2,1]==var[1,1] or var[2,1]==var[0,1]: var[2,1]=flags[1]

    # Pala 3:

    if (process_t[2,1]==shovel[2]) and (var[2,1]<n) and (truck_state[var[2,1]]==5):
        truck_state[var[2,1]]=6
        process_t[2,1]=0
        truck[var[2,1]]+=1
        var[2,1]=flags[1]   
        shovel_state[2]=0

    if (shovel_state[2]==1) and (var[2,1]<n):
        truck[var[2,1]]+=1
        process_t[2,1]+=1
    
    for i in range(n):
        
        if (process_t[2,1]==0) and (var[2,1]<n) and (truck_state[var[2,1]]==4) and (priority[i,0]==np.amax(priority[:,0])) and (priority[i,0]!=0):
            var[2,1]=i
            truck_state[var[2,1]]=5
            shovel_state[2]=1
            process_t[2,1]+=1
            priority[i,0]=0
            
            for j in range(n):
                if truck_state[j]==4:
                    flags[1]=j
                    break

        if (process_t[2,1]==0) and (var[2,1]<n) and (truck_state[var[2,1]]==4) and (not(any(priority[:,0]))) :
            truck_state[var[2,1]]=5
            var[2,1]=flags[1]
            flags[1]+=1
            shovel_state[2]=1
            process_t[2,1]+=1
  
          
    #---------------------------------------------------------------------
    #Segundo Viaje

    for p in range(len(truck_state)):

        if (truck_state[p]==7) and ((truck[p]-truck_it[p,1])>=travel[1]-1): 
            truck_state[p]=8
            truck[p]+=1

        if truck_state[p]==7:
            truck[p]+=1

        if truck_state[p] == 6:
            truck_it[p,1]=truck[p]
            truck_state[p]=7
    #---------------------------------------------------------------------
    #Estacion de Descarga:

    # Aca se ven la llegada de camiones igual que en la seccion de palas con la diferencia que la implementacion es diferente 

    for var[0,2] in range(n): 

        
        # Correa 1:

        if (process_t[0,2]>=belt[0]) and (truck_state[var[0,2]]==9):
            truck_state[var[0,2]]=10
            process_t[0,2]=0
            truck[var[0,2]]+=belt[0]
            belt_state[0]=0


        if (belt_state[0]==1) and (truck_state[var[0,2]]==9):
            truck[var[0,2]]+=1
            process_t[0,2]+=1


        

        if (belt_state[0]==0) and (truck_state[var[0,2]]==8) and (priority[var[0,2],1]!=0) and (priority[var[0,2],1]==np.amax(priority[:,1])) :
            truck_state[var[0,2]]=9
            belt_state[0]=1
            process_t[0,2]+=1
            priority[var[0,2],1]=0
            
                
        if (belt_state[0]==0) and (truck_state[var[0,2]]==8) and (not(any(priority[:,1]))):
            truck_state[var[0,2]]=9
            belt_state[0]=1
            process_t[0,2]+=1
            
        # Correa 2:
      

        if (process_t[1,2]>=belt[1]) and (truck_state[var[0,2]]==9):
            truck_state[var[0,2]]=10
            process_t[1,2]=0
            truck[var[0,2]]+=belt[1]  
            belt_state[1]=0


        if (belt_state[1]==1)and (truck_state[var[0,2]]==9):
            truck[var[0,2]]+=1
            process_t[1,2]+=1


        

        if (belt_state[1]==0) and (truck_state[var[0,2]]==8) and (priority[var[0,2],1]!=0) and (priority[var[0,2],1]==np.amax(priority[:,1])) :
            truck_state[var[0,2]]=9
            belt_state[1]=1
            process_t[1,2]+=1
            priority[var[0,2],1]=0
            
                
        if (belt_state[1]==0) and (truck_state[var[0,2]]==8) and (not(any(priority[:,1]))):
            truck_state[var[0,2]]=9
            belt_state[1]=1
            process_t[1,2]+=1

        # Correa 3:

      

        if (process_t[2,2]>=belt[2]) and (truck_state[var[0,2]]==9):
            truck_state[var[0,2]]=10
            process_t[2,2]=0
            truck[var[0,2]]+=belt[2]  
            belt_state[2]=0


        if (belt_state[2]==1)and (truck_state[var[0,2]]==9):
            truck[var[0,2]]+=1
            process_t[2,2]+=1


        

        if (belt_state[2]==0) and (truck_state[var[0,2]]==8) and (priority[var[0,2],1]!=0) and (priority[var[0,2],1]==np.amax(priority[:,1])) :
            truck_state[var[0,2]]=9
            belt_state[2]=1
            process_t[2,2]+=1
            priority[var[0,2],1]=0
            
                
        if (belt_state[2]==0) and (truck_state[var[0,2]]==8) and (not(any(priority[:,1]))):
            truck_state[var[0,2]]=9
            belt_state[2]=1
            process_t[2,2]+=1       



    #Conteo de tiempo detenido esperando que se desocupe:


    for r in range(len(truck_state)): 

        #Estacion de carga:

        if truck_state[r] == 4:
            stop_t_truck[r,0]+=1
            priority[r,0]+=1

        #Correas para Descarga:

        if truck_state[r] == 8:    
            stop_t_truck[r,1]+=1
            priority[r,1]+=1
            



    if debug==1:
        print("time",'\t\t','var','\t\t','proc time','\t',"flags",'\t\t','min','\t','tr/trst')
        print( t[0],":",str(t[1]).rjust(2,'0'),"\t",var[:,0],'\t',process_t[:,0],'\t',flags,'\t',t[2],'\t',truck)
        print('\t\t',var[:,1],'\t',process_t[:,1],'\t\t\t\t',truck_state)
        print('\t\t',var[:,2],'\t',process_t[:,2],'\t\t\t\t',stop_t_truck[:,0]) 
        print('\t\t','\t','\t\t\t\t\t\t',stop_t_truck[:,1],'\n')    
    
    if debug==2:
        
        print("time",'\t\t','var','\t\t','proc time','\t',"flags",'\t\t','min','\t','tr/trst')
        print( t[0],":",str(t[1]).rjust(2,'0'),"\t",var[:,0],'\t',process_t[:,0],'\t',flags,'\t',t[2],'\t',truck)
        print('\t\t',var[:,1],'\t',process_t[:,1],'\t\t\t\t',truck_state)
        print('\t\t',var[:,2],'\t',process_t[:,2],'\t\t\t\t',stop_t_truck[:,0]) 
        print('\t\t','\t','\t\t\t\t\t\t',stop_t_truck[:,1],'') 
        print('\t\t','\t','\t\t\t\t\t\t',priority[:,0],'') 
        print('\t\t','\t','\t\t\t\t\t\t',priority[:,1],'\n') 
        
      
    
    
    t[2]+=1   
    time_corr(t) # correccion de tiempo para ser costrado en formato hora

    
    #Breaks:
    
    # Si todos los camiones llegan al estado final (posdescarga):
    if sum(truck_state)==10*n: break 
    #Si el tiempo excede los c minutos:
    if t[2] ==c: break



if debug==0:     
    os.system("clear")
if a ==1:
    print('\nLlegada al destino: ',t[0],":",str(t[1]-1).rjust(2,'0'),'\n')   
elif a == 2 :
    print("\nDemora acumulada por los camiones antes de carga: ",sum(stop_t_truck[:,0]),"minutos")
    print("Demora acumulada por los camiones antes de descarga: ",sum(stop_t_truck[:,1]),"minutos\n")
    if sum(stop_t_truck[:,0])==0: print('\nLa tercera pala no se ocupa')
    if sum(stop_t_truck[:,1])==0: print('\nLa tercera correa no se ocupa\n\n\n\n')
