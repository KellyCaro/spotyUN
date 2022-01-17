from Clases.Cancion import *
from Clases.Cliente import *
from Clases.Conexion import *
from Clases.Plan import *
from Clases.SongList import *

conect=Conexion()

miConexion=Conexion().conexion()
miCancion=Cancion()
miCliente=Cliente()
miPlan=Plan()
miLista=ListaCanciones()


tablaCliente=conect.sql_table(miConexion,'''Client(identification integer  PRIMARY KEY,
names text,lastNames text,country text,city text,
phone text,creditCard text,payment text,email text,age text,userName text,password text, plan text)''')
tablaCanciones=Conexion().sql_table(miConexion,"cancion(code integer PRIME KEY, name text, genre text, album text, interpreter text, ruta text)")
tablaListaC=Conexion().sql_table(miConexion,"list (code integer PRIMARY KEY AUTOINCREMENT, name text, clientIdentification integer,clientEmail text,recordCode integer,recordName text,recordPerformer text, recordPicture text)")
tablaPlan=Conexion().sql_table(miConexion,"Plan(code	integer PRIME KEY,name	text,value	text,amount	integer")
tablaPlanXCliente=Conexion().sql_table(miConexion,"PlanesXCliente(transactionCode integer PRIME KEY, planCode text, clientID text)")

"""*********************************************************************
OBJETO SONGLIST FUNCIONES
**********************************************************************"""
def ingresadatos():
    print("Hola! te damos la bienvenida a Listas de SpotyUN")
    print("1)Crear una lista de canciones")
    print("2)Consultar lista por el nombre de la lista")
    print("3)Consultar lista por nombre de cancion")
    print("4)Consultar lista por autor de cancion")
    print("5)Consultar tus listas")
    
    print("6)Eliminar lista completa")
    print("7)Actualiza el nombre de la lista")
    print("8)Eliminar cancion de lista")
    print("7)Actualiza cancion de una lista")
    print("9)Salir")
    return input()

def capturaDatos(identificacion):
    try:
        nameLista=input("\nPara CREAR LISTA ingresa un nombre de lista nuevo/ Para AGREGAR CANCIONES ingresa el nombre de la lista: ")
        datoscliente=miCliente.consultaClientes(identificacion,miConexion)
        identificacionCliente=datoscliente[0][0]#traer del objeto cliente
        emailCliente=datoscliente[0][8]#traer del objeto cliente
        #searchSinglePlan
        canciones=miCancion.searchRecords(miConexion) #busca todas las canciones y las imprime

        for i in canciones:
            print(i[0],i[1],i[2],i[3],i[4])
        codigo_cancion=int(input("Ingrese el codigo de la cancion"))
        datosCancion=miCancion.searchSingleRecord(miConexion, codigo_cancion,True)
        nombre_cancion=datosCancion[1]#traer del objeto cancion
        interprete_cancion=datosCancion[4]#traer del objeto cancion
        imagen="imagen.jpg"
        return((None,nameLista,identificacionCliente,emailCliente,codigo_cancion,nombre_cancion,interprete_cancion,imagen))

    except IndexError:
        print("El codigo de la cancion no existe ")

def capturaDatoSimple(mensaje):
    return input(mensaje)

def menuLista(identificacion):
    menu=ingresadatos()

    datoscliente=miCliente.consultaClientes(identificacion,miConexion) #tupla con los datos del cliente
    identificacionCliente=datoscliente[0][0]
    codigoplan=datoscliente[0][12]
    limitecanciones=miPlan.searchSinglePlan(miConexion,codigoplan,True)[3]#Limite de las canciones por lista

    if menu=="1":
         #tupla con los datos del cliente
        identificacionClienteCedula=datoscliente[0][0]
        codigoplan=datoscliente[0][12]
        limitecanciones=miPlan.searchSinglePlan(miConexion,codigoplan,True)[3]#Limite de las canciones por lista


        nombreycodigo=miLista.extraerListOfClient(miConexion, identificacionCliente,False)#1 y 5


        print("\n")
        miLista.imprimeDiccionario(miLista.ListaCancionesAutores(miConexion,identificacionClienteCedula))#imprime listas
        print("\nCanciones que puedes agregar por cada playList = ",limitecanciones)#imprime el limite de canciones



        datos=list(capturaDatos(identificacion))   #ingresa los datos para la lista, devuelve la info de la lista


        ingresa=False
        bucle=True

        while bucle==True:
            if ingresa==True:
                datos[4]=int(input("\nIngrese el codigo de la cancion que va a agregar"))
                datosCancion=miCancion.searchSingleRecord(miConexion, datos[4], True)
                datos[5]=datosCancion[1]#traer del objeto cancion
                datos[6]=datosCancion[4]#traer del objeto cancion
                datos[7]="imagen.jpg"
            cancionesguardadas=len(miLista.extraerListOfClientAndName(miConexion,identificacionClienteCedula,datos[1],False))#numero de canciones guardads
            if cancionesguardadas==limitecanciones:
                bucle=False
                print("\nExcedio el limite de canciones para esta lista\n\n")
                break

            #verifica que no se pase del limite y que no se repitan las canciones de la misma lista
            if cancionesguardadas<limitecanciones and not miLista.existSongOfList(miConexion,datos[1], identificacionClienteCedula,datos[4]):

                if not miLista.existList(miConexion,datos[1],identificacionClienteCedula):   #si se crea una nueva lista, se envia un Email
                    miLista.sendEmail(datos,datos[3])
                miLista.saveList(miConexion,datos)
                print("☺\n\ncancion agregada a la lista ")
                print("Ha guardado ",(cancionesguardadas+1)," canciones, de ",limitecanciones)

            else:
                print("\nNo se agrego la cancion por estar repetida o porque excedio las canciones de su plan\n")

            ingresa=True
            if (int(input("Quiere seguir agregando? marque '0' , Quiere salir de la agregacion marque '1'")))==1:
                bucle=False
            else:
                canciones=(miCancion.searchRecords(miConexion)) #busca todas las canciones y las imprime
                for i in canciones:
                    print(i[0],i[1],i[2],i[3],i[4])
    elif menu=="2":
        nombreLista=input("Ingrese el nombre de la lista a buscar")
        miLista.imprimeDiccionario(miLista.ListaCancionesAutoresOnly(miConexion,identificacionCliente,nombreLista))

    elif menu=="3":
        nombreCancion=input("Ingrese el nombre de la cancion: ")
        print("\n\nListas con el nombre de la cancion : "+nombreCancion+"\n",miLista.buscarListasPorNombredeCancion(miConexion,identificacionCliente,nombreCancion))
    elif menu=="4":
        nombreInterprete=input("Ingrese el nombre del interprete: ")
        print("\n\nListas con el nombre del interprete : "+nombreInterprete+"\n",miLista.buscarListasPorNombredeInterprete(miConexion,identificacionCliente,nombreInterprete))
        
    elif menu=="5":
        miLista.imprimeDiccionario(miLista.ListaCancionesAutores(miConexion,identificacion))

    elif menu=="6":
        nombreLista=input("Ingrese el nombre de la lista a eliminar")
        deleteAllList(miConexion,nombreLista,identificacionCliente)

    elif menu=="7":
        nombreLista=input("Ingrese el nombre de la lista a buscar")
        nombreactualiza=input("Ingrese el nuevo nombre")
        updateList(con,nombreLista,nombreactualiza, identificacionCliente)
    elif menu=="8":
        miLista.imprimeDiccionario(miLista.ListaCancionesAutores(miConexion,identificacionCliente))
        nombreLista=input("Ingrese el nombre de la lista ")
        codeSong=int(input("ingrese el codigo de la cancion que desea eliminar de la lista "))
        print(miLista.eliminaSongOfList(miConexion,nombreLista,identificacionCliente,codeSong))
    elif menu=="9":
        imprimeDiccionario(ListaCancionesAutores(miConexion,identificacionCliente))

        lista=input("ingrese el nombre de la lista que quiere actualizar")
        codigoSongOld=int(input("Ingrese el codigo de la cancion que quiere actualizar"))
        codigoSongNew=int(input("Ingrese el codigo de la nueva cancion"))
        datosCancionNueva=miCancion.searchSingleRecord(miConection, codigoSongNew,True)
        if not existSongOfList(miConexion,lista, identificacionCliente,datosCancionNueva[0]):
            updateSongOfList(miConexion,lista,identificacionCliente,codigoSongOld, datosCancionNueva)
        else:
            print("Ya existe esa cancion en tu lista")
    elif menu=="0":
        usuarioMain(identificacion)

#print(NombreListayCanciones(con,"1023961225"))
"""***************************************************************"""

"""*************************************
MENU USUARIO FINAL
**************************************"""
def usuarioMain():


    print("*******************************************")
    documento= input("Ingresa tu numero de documento: ")

    print("*******************************************")




    try:
        identificacion=miCliente.consultaClientes(documento,miConexion)[0][0]
    except:
        print("No existe ningun usuario con el numero de identificación")
        #miCliente.registerCliente(self,miCliente.leer_info(self),miConexion)
        usuarioMain()



    nombre=miCliente.consultaClientes(identificacion,miConexion)[0][1]

    todosCodigos = miCancion.listaGeneralCancionesCodigos(miConexion,miCliente.consultaClientes(documento,miConexion)[0][12])
    print("Hola {} te damos la bienvenida a Spoty UN".format(nombre))
    print("1)Escuchar musica de manera aleatoria")
    print("2)Mostrar canciones disponibles")
    print("3)Listas de canciones")
    print("4)Reproducir tus listas ")
    print("5)mi plan")
    print("6)Salir")
    selectorU = input ("Selecciona del menu la acción que deseas realizar: ")
    os.system("cls")

    if selectorU=="1":
        miCancion.mostrarCancionesPorPlan(miConexion,miCliente.consultaClientes(identificacion,miConexion)[0][12])
        miCancion.play_song_list(miConexion,todosCodigos, True)


    elif selectorU=="2":
        miCancion.mostrarCancionesPorPlan(miConexion,miCliente.consultaClientes(identificacion,miConexion)[0][12])

        print("Busquedas de canciones")
        lista = miCancion.searchRecords(miConexion)
        buscar= buscador(miConexion,lista)
        buscar.menuOrdenador(miConexion,lista)

    elif selectorU=="3":
        salir=0
        while(salir==0):
            menuLista(identificacion)
            salir=int(input("pulse 1 si desea salir, pulse 0 si desea continuar "))

    elif selectorU=="4":

        identificacionCliente=identificacion

        #print(NombreListayCanciones(con,identificacionCliente))
        miLista.imprimeDiccionario(miLista.ListaCancionesAutores(miConexion,identificacionCliente))
        selector=input("indica el nombre de la lista que deseas reproducir: ")
        codigoscanciondelistas = miLista.extraeCodigosList(miConexion,identificacionCliente,selector)
        aleatorio = input('ingresa 1 si quieres reproducir aleatoriamente, ingresa 0 para reproducir en orden: ')

        while True:

            if aleatorio == '1':
                miCancion.play_song_list(miConexion,codigoscanciondelistas,True)

                break

            elif aleatorio =='0':
                miCancion.play_song_list(codigoscanciondelistas,False)
                break

            else:
                aleatorio = input('ingresa 1 si quieres reproducir aleatoriamente, ingresa 0 para reproducir en orden: ')
        print("Esta lista no existe")


    elif selectorU=="5":
        code=miCliente.consultaClientes(documento,miConexion)[0][12]
        planActual = miPlan.searchSinglePlan(miConexion,code, True)
        print('codigo de plan: ', planActual[0],'\nnombre del plan: ',planActual[1],'\nvalor del plan: ',planActual[2],'\ncantidad de canciones maximas del plan: ',planActual[3])
        selectorPlan= input("Deseas cambiar tu plan actual presiona: \n 1)si\n 2)no\nRespuesta: ")
        while True:
            if selectorPlan=='1':
                miPlan.mostrarPlanes(miConexion)
                codigoPlan=input("Indica el codigo del plan al cual deseas cambiar: ")
                if codigoPlan=="1" or codigoPlan=="2" or codigoPlan=="3":
                    miCliente.updateClientPlan(codigoPlan,identificacion,miConexion)
                    break
                else:
                    print("Este plan no existe por favor verifique de nuevo")
            else:
                print("*************************************")
                usuarioMain()

    elif selectorU=="6":
        pass

usuarioMain()
