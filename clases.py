import sqlite3
from sqlite3 import Error
import pygame
import sys
from pygame.locals import *
import random
#from SongList import *
import os
import pprint
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

"""CLASE CONEXION"""
class Conexion:
    def __init__(self):
        pass



    def conexion(self):

        try:
            conexion= sqlite3.connect('basesDeDatos.db')
            return conexion
        except Error:
            print(Error)



    def sql_table(self,conexion,str):
        #se utiliza el metodo cursos, permita hacer las sentencias
        try:
            cursorObj = conexion.cursor()
            crearTablaPlan="CREATE TABLE {}".format(str)
            cursorObj.execute(crearTablaPlan)
            conexion.commit()
        except:
            pass

"""CLASE CLIENTE"""
class Cliente:
    def __init__(self):
        self.identification=None
        self.names=None
        self.lastNames=None
        self.country=None
        self.city=None
        self.phone=None
        self.creditCard=None
        self.payment=None
        self.email=None
        self.age=None
        self.userName=None
        self.password=None
        self.plan=None

    def registro(self):
        self.identification=input("numero de cedula: ")
        self.names=input("nombre: ")
        self.lastNames=input("Apellido: ")
        self.country=input("País: ")
        self.city=input("Ciudad: ")
        self.phone=input("Telefono: ")
        self.creditCard=input("Numero de tarjeta de credito: ")
        self.payment=input("Metodo de pago: ")
        self.email=input("E-mail: ")
        self.age=input("Edad: ")
        self.userName=input("Usuario: ")
        self.password=input("Contraseña: ")
        self.plan=None
        return(self.identification,self.names,self.lastNames,
               self.country,self.city,self.phone,self.creditCard,
               self.payment,self.email,self.age,self.userName,self.password,
               self.plan)
    def registerCliente(self,Client_data,conexion):
        #para la opcion 2 escribir una tupla
        cursorObj = conexion.cursor()
        datos = Client_data
        cursorObj.execute('''INSERT INTO cliente VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',datos)
        #guarda en la base de datos
        conexion.commit()
        return print("registo exitoso")

    def leer_info(self):
        self.identification=input("numero de cedula: ")
        self.names=input("nombre: ")
        self.lastNames=input("Apellido: ")
        self.country=input("País: ")
        self.city=input("Ciudad: ")
        self.phone=input("Telefono: ")
        self.creditCard=input("Numero de tarjeta de credito: ")
        self.payment=input("Metodo de pago: ")
        self.email=input("E-mail: ")
        self.age=input("Edad: ")
        self.userName=input("Usuario: ")
        self.password=input("Contraseña: ")
        self.plan=0
        #self.cliente=(self.identification, self.names, self.lastNames, self.country, self.city, self.phone, self.creditCard, self.payment, self.email, self.age, self.userName, self.password, self.plan)
        return self

    #confirma si los clientes existen en la base de datos
    def consultaClientes(self,identification,conexion):
        cursorObj = conexion.cursor()
        consultarTabla="SELECT * FROM Client WHERE identification={}".format(identification)
        cursorObj.execute(consultarTabla)
        filas= cursorObj.fetchall()
        vacio=0
        if len(filas)==0:
            print("entro")



        else:
            return filas


    #verificacion del cliente para acceso
    def verificacionCliente(self,conexion,identificacion):
        cursorObj = conexion.cursor()
        consultarUser="SELECT * FROM Client WHERE identification='{}'".format(identificacion)
        cursorObj.execute(consultarUser)
        filas= cursorObj.fetchall()
        password=contrasena
        #estos condicionales verifican si la información suministrada se encuenta en la base de datos

        if len(filas)==1:

            if filas[0][11]==password:
                datos=(True,str(filas[0][11]))
                return datos

            else:
                print("Clave y/o usuario incorrecto")

    #funcion para modificar los datos del cliente
    def updateClientData(self,ClientData,valor,identification,conexion,):
        cursorObj = conexion.cursor()
        cursorObj.execute("UPDATE cliente SET {}= '{}' WHERE identification = {}".format(ClientData,valor,identification))
        conexion.commit()

    #funcion para cambiar el plan del cliente
    def updateClientPlan(self,valor,identification,conexion):
        cursorObj = conexion.cursor()
        cursorObj.execute("UPDATE Client SET plan= '{}' WHERE identification = {}".format(valor,identification))
        conexion.commit()
        return print("Cambio de plan exitoso")

    def eliminarCliente(self,identification,conexion):
        cursorObj = conexion.cursor()
        cursorObj.execute("DELETE FROM cliente WHERE identification={}".format(identification))
        conexion.commit()



"""*********************************************************************
CLASE CANCION(RECORDER)  FUNCIONES
**********************************************************************"""

class Cancion:

    def __init__(self):
        self.code=None
        self.name=None
        self.genre=None
        self.album=None
        self.interpreter=None
        self.ruta=None


    '''CREACION DE REGISTROS EN TABLAS'''
    def register_record(self, conexion, song_data):
        cursorObj = conexion.cursor()
        datos= song_data
        insertToRecordTable = "INSERT INTO Cancion VALUES (?, ?, ?, ?, ?, ?)"
        cursorObj.execute(insertToRecordTable,datos)            #guarda en la base de datos
        conexion.commit()
        return print("registo exitoso")

    '''CONSULTA DE REGISTROS INDIVIDUALES'''
    def searchSingleRecord (self, conexion, code, data):
        cursorObj = conexion.cursor()

        if data == True:
            cancion = cursorObj.execute("SELECT * FROM Cancion WHERE code={}".format(code)).fetchall()[0]
            return cancion

        else:
            consultRecord = "SELECT * FROM Cancion WHERE code={}".format(code)
            cursorObj.execute(consultRecord)
            filas = cursorObj.fetchall()

            if len(filas) == 0:
                cancion = False

            else:
                cancion = True
            return cancion

    '''CONSULTA GENERAL DE REGISTROS'''
    def searchRecords(self,conexion):
        cursorObj =conexion.cursor()
        canciones = cursorObj.execute("SELECT * FROM Cancion").fetchall()
        return canciones






    '''LECTURA DE ATRIBUTOS OBJETOS REALES'''
    def leer_info_record(self):


            self.code = input("codigo de registro:")
            self.name = input("nombre: ")
            self.genre = input("genero: ")
            self.album = input("album: ")
            self.interpreter = input("interprete: ")
            self.ruta=input("Ruta: ")
            return self
    '''ACTUALIZACIONES DE REGISTROS'''
    def mostrarCancionesPorPlan(self, conexion,plan):
        filas = self.searchRecords(conexion)
        if plan== "1":

            for j in range(len(filas)-50):
                print("")

                for i in range(len(filas[j])-1):
                    print(filas[j][i],end=" ".ljust(4))
            print("")
        elif plan =="2":
            for j in range(len(filas)-30):
                print("")

                for i in range(len(filas[j])-1):
                    print(filas[j][i],end=" ".ljust(4))
            print("")
        elif plan =="3":
            for j in range(len(filas)):
                print("")

                for i in range(len(filas[j])-1):
                    print(filas[j][i],end=" ".ljust(4))
            print("")

    def mostrarCanciones(self, conexion):
        filas = self.searchRecords(conexion)

        for j in range(len(filas)):
            print("")

            for i in range(len(filas[j])-1):
                print(filas[j][i],end=" ".ljust(4))
        print("")
    '''Mostrar Canciones de lista especifica'''

    def mostrarCancionesDeLista(self,lista):

        for j in range(len(lista)):
            print("")

            for i in range(len(lista[j])-1):
                print(lista[j][i],end=" ".ljust(4))
        print("")

    '''REPRODUCCION DE GRABACIONES'''
    def play_song(self, codigo, conexion):
        cancion = self.searchSingleRecord( conexion, codigo, True)
        pygame.init()
        pygame.mixer.music.load(cancion[5])
        pygame.mixer.music.play(1)
        print('para parar la reproduccion escriba: p')
        accion = input()

        if accion == "p":
            pygame.mixer.music.stop()

    """funcion utilizada"""
    """funcion utilizada"""
    def listaGeneralCancionesCodigos(self, conexion,plan): # devuelve los codigos de todas las canciones en la base de datos
        filas = self.searchRecords(conexion)
        c = []
        if plan == "1":
            for i in range(len(filas)-50):
                c.append(i)
        elif plan == "2":
            for i in range(len(filas)-30):
                c.append(i)
        else:
            for i in range(len(filas)):
                c.append(i)

        return c

    def play_song_list(self, conexion, lista, aleatoriedad):
        print('funcion reproducir lista')
        miConexion = conexion
        listaCanciones = lista

        if  aleatoriedad != True :
            pygame.init()
            codigo = str(listaCanciones[0])
            cancion = self.searchSingleRecord( conexion, codigo, True)
            pygame.mixer.music.load(cancion [5])
            pygame.mixer.music.play(1)

            while True:

                for j in range(len(listaCanciones)):
                    codigo = str(listaCanciones[j])
                    cancion = self.searchSingleRecord(conexion, codigo, True)
                    pygame.init()
                    pygame.mixer.music.queue(cancion[5])

        else:
            print('modo de reproduccion aleatoria')
            aleatorio = random.randint(0,len(listaCanciones)-1)
            codigo = listaCanciones[aleatorio]
            cancion = self.searchSingleRecord(conexion, codigo, True)
            pygame.init()
            pygame.mixer.music.load(cancion[5])
            pygame.mixer.music.play(1)
            print('reproduccion de la primera cancion')

            while True:
                codigo = random.randint(1, len(listaCanciones))
                cancion = self.searchSingleRecord( conexion, codigo, True)
                pygame.init()
                pygame.mixer.music.queue(cancion[5])


    '''FUNCIONES MAIN PARA TABLAS'''
    def mainRecord(self, conexion):
        miConexion = conexion()
        print("Elija una de las siguientes opciones")
        print("1)Agregar cancion")
        print("2)buscar cancion")
        print("3)consultar canciones")
        print("4)reproducir cancion")
        selectedOption = input("Escribe aqui tu respuesta: ")

        if selectedOption == "1":
            codigo = input("introduce el codigo de la cancion: ")

            if self.searchSingleRecord( miConexion, codigo, False) == False:
                print("Tu registro de una nueva cancion inicia apartir de ahora")
                miConexion = conexion()
                song = self.leer_info_record()
                self.register_record(miConexion, song)

            else:
                print("la cancion ya esta registrada en nuestra base de datos")


        elif selectedOption == "2":

            code = input("introduce el codigo de la cancion: ")

            if self.searchSingleRecord( miConexion, code, False) == True:
                miConexion = conexion
                song = self.searchSingleRecord(miConexion, code, True)
                print("cancion:" + '''
                nombre: ''' + song[1] + '''
                genero: ''' + song[2] + '''
                album: ''' + song[3] + '''
                interprete: ''' + song[4])

            else:
                print('''la cancion aun NO esta registrada en nuestra base de datos
                                     debes ingresarla para luego modificarla''')

        elif selectedOption == "3":
            miConexion = conexion
            self.mostrarCanciones(miConexion)

        elif selectedOption == "4":
            code = input("introduce el codigo de la cancion: ")

            if self.searchSingleRecord(miConexion, code, False) == True:
                self.play_song( code,miConexion)

            else:
                print('''la cancion aun NO esta registrada en nuestra base de datos

                     debes ingresarla para luego modificarla''')


"""CLASE PLAN"""
"""*********************************************************************
OBJETO PLAN_X_CLIENTE
**********************************************************************"""
'''CREACION DE TABLAS'''
class PlanXCliente:
    def __init__(self):
        self.transaccion = None
        self.planCode = None
        self.clientID = None



    '''CREACION DE REGISTROS EN TABLAS'''
    def register_planXCliente(self, conexion, plan_data):
        cursorObj = conexion.cursor()
        datos= plan_data
        insertToPlanTable = "INSERT INTO PlanXCliente VALUES (?, ?, ?)"
        cursorObj.execute(insertToPlanTable,datos)            #guarda en la base de datos
        conexion.commit()
        return print("registo exitoso")

    '''CONSULTA DE REGISTROS INDIVIDUALES'''
    def searchSinglePlanXCliente (self, conexion, code, data):
        cursorObj = conexion.cursor()

        if data == True:
            plan = cursorObj.execute("SELECT * FROM PlanXCliente WHERE transactionCode={}".format(code)).fetchall()[0]
            return plan

        else:
            consultPlanXCliente = "SELECT * FROM PlanXCliente WHERE transactionCode={}".format(code)
            cursorObj.execute(consultPlanXCliente)
            filas = cursorObj.fetchall()

            if len(filas) == 0:
                plan = False

            else:
                plan = True
            return plan

    def searchPlanesXClientes(self, conexion):
        cursorObj =conexion.cursor()
        planesXClientes = cursorObj.execute("SELECT * FROM PlanXCliente").fetchall()
        return planesXClientes
    '''LECTURA DE ATRIBUTOS OBJETOS REALES'''
    def leer_info_planXCliente(self):
            self.transactionCode = input("codigo de registro:")
            self.planCode = input("codigo de plan: ")
            self.ClientID = input("identificacion de cliente: ")
            return self

    '''FUNCIONES MAIN PARA TABLAS'''
    def mainplanXCliente(self,conexion):
        miConexion = conexion()
        print("Elija una de las siguientes opciones")
        print("1)Agregar plan por cliente")
        print("2)buscar plan por cliente")
        print("3)consultar planes por clientes")
        selectedOption = input("Escribe aqui tu respuesta: ")

        if selectedOption == "1":
            codigoTransaccion = input("introduce el codigo de transaccion: ")

            if self.searchSinglePlanXCliente(miConexion, codigoTransaccion, False) == False:
                print("Tu registro de un nuevo plan por cliente")
                planXCliente = self.leer_info_planXCliente()
                self.register_planXCliente(miConexion, planXCliente)

            else:
                print("la transaccion ya esta registrada en nuestra base de datos")

        elif selectedOption == "2":
            codigoTransaccion = input("introduce el codigo de la transaccion: ")

            if self.searchSinglePlanXCliente(miConexion, codigoTransaccion, False) == True:
                planXCliente = self.searchSinglePlanXCliente(miConexion, codigoTransaccion, True)
                print("plan por cliente:" + '''
                        codigo de transaccion: ''' + str(planXCliente[0]) + '''
                        codigo de plan: ''' + planXCliente[1] + '''
                        identificacion de cliente: ''' + planXCliente[2])

            else:
                print('''la transaccion aun NO esta registrada en nuestra base de datos
                             debes ingresarla para luego modificarla''')

        elif selectedOption == "3":
            filas = self.searchPlanesXClientes(miConexion)

            for j in range(len(filas)):
                print("")

                for i in range(len(filas[j])):
                    print(filas[j][i], end=" ".ljust(4))
            print("")

"""*********************************************************************
OBJETO PLAN  FUNCIONES
**********************************************************************"""

class Plan:
    def __init__(self):
        self.transaccion = None
        self.planCode = None
        self.clientID = None
    '''CREACION DE REGISTROS EN TABLAS'''

    def register_plan(self, conection, plan_data):
        cursorObj = conection.cursor()
        datos= plan_data
        insertToPlanTable = "INSERT INTO Planes VALUES (?, ?, ?, ?)"
        cursorObj.execute(insertToPlanTable,datos)            #guarda en la base de datos
        conection.commit()
        return print("registo exitoso")

    '''CONSULTA DE REGISTROS INDIVIDUALES'''
    def searchSinglePlan (self, conexion, code, data):
        cursorObj = conexion.cursor()

        if data == True:
            plan = cursorObj.execute("SELECT * FROM Plan WHERE code={}".format( code)).fetchall()[0]
            return plan

        else:
            consultPlan = "SELECT * FROM Plan WHERE code={}".format( code)
            cursorObj.execute(consultPlan)
            filas = cursorObj.fetchall()

            if len(filas) == 0:
                plan = False

            else:
                plan = True
            return plan

    def searchPlanes(self, conexion):
        cursorObj =conexion.cursor()
        planes = cursorObj.execute("SELECT * FROM Plan").fetchall()
        return planes
    '''LECTURA DE ATRIBUTOS OBJETOS REALES'''
    def leer_info_plan(self):
            self.code = input("codigo de registro:")
            self.name = input("nombre: ")
            self.value = input("valor: ")
            self.amount = input("cantidad: ")
            return self

    '''Devuelve los planes disponibles'''


    def mostrarPlanes(self, conexion):
        filas = self.searchPlanes(conexion)

        for j in range(len(filas)):
            print("")

            for i in range(len(filas[j])-1):
                print(filas[j][i],end=" ".ljust(4))
        print("")

    '''FUNCIONES MAIN PARA TABLAS'''
    def mainPlan(self, conexion):
        print("Elija una de las siguientes opciones")
        print("1)Agregar plan")
        print("2)buscar plan")
        print("3)consultar planes")
        selectedOption = input("Escribe aqui tu respuesta: ")

        if selectedOption == "1":
            codigo = input("introduce el codigo del plan: ")

            if self.searchSinglePlan(conexion, codigo, False) == False:
                print("Tu registro de un nuevo plan inicia apartir de ahora")
                song = self.leer_info_plan()
                self.register_plan(conexion, song)

            else:
                print("el plan ya esta registrado en nuestra base de datos")

        elif selectedOption == "2":
            code = input("introduce el codigo del plan: ")

            if self.searchSinglePlan(conexion, code, False) == True:
                plan= self.searchSinglePlan(conexion, code, True)
                print("plan:"+'''
                nombre: '''+plan[1]+'''
                valor: '''+plan[2]+'''
                cantidad:'''+ " {}".format(plan[3]) )

            else:
                print('''la cancion aun NO esta registrada en nuestra base de datos
                     debes ingresarla para luego modificarla''')

        elif selectedOption == "3":
            self.mostrarPlanes(conexion)


"""*********************************************************************
CLASE SONGLIST
**************************************************************"""
class ListaCanciones:

    def __init__(self):
        pass


    def searchList(self,con):
        cursorOBJ= con.cursor()
        tablaConsultar='SELECT name,clientEmail,recordCode,recordName,recordPerformer FROM list'
        cursorOBJ.execute(tablaConsultar)
        filas=cursorOBJ.fetchall()
        print("------------TODAS LAS LISTAS----------------\n\nVeremos "+str(len(filas))+" filas\nNombre, Email, Codigo_cancion, Nombre_cancion, Interprete_cancion")
        for row in filas:
            print(row)

    #Busca lista por el nombre
    def searchSingleList( self,con, List_name):
        cursorOBJ= con.cursor()
        tablaConsultar='SELECT name,clientEmail,recordCode,recordName,recordPerformer FROM list WHERE name="'+List_name+'"'
        cursorOBJ.execute(tablaConsultar)
        filas=cursorOBJ.fetchall()
        print ("------------LISTAS CON EL NOMBRE "+List_name.upper()+" ----------------\n\nVeremos 1 Lista\n\n( Nombre, Email, Codigo_cancion, Nombre_cancion, Interprete_cancion )")
        for row in filas:
            print(row)

    #Busca lista por el nombre
    def deleteList(self, con, List_code):
        cursorOBJ= con.cursor()
        listaBorrar='DELETE FROM list WHERE code="'+str(List_code)+'"'
        cursorOBJ.execute(listaBorrar)
        print("Eliminamos lista con el codigo ",List_code)
        con.commit()

    #Busca lista por el nombre, depende de cada cliente
    def deleteAllList(self,con, nombre, idcliente):
        cursorOBJ= con.cursor()
        listaBorrar='DELETE FROM list WHERE name="'+nombre+'"'+' AND '+'clientIdentification='+'"'+str(idcliente)+'"'
        cursorOBJ.execute(listaBorrar)
        print("Eliminamos lista con el nombre ",nombre)
        con.commit()

    #Actualiza unicamente el nombre de la lista, , depende de cada cliente
    def updateList(self,con,List_name,nombreactualizado,idcliente):
        cursorOBJ= con.cursor()
        listaActualiza='UPDATE list SET name="'+nombreactualizado+'" WHERE name="'+List_name+'"'+' AND '+'clientIdentification='+'"'+str(idcliente)+'"'
        cursorOBJ.execute(listaActualiza)
        print("Actualiza lista con el nombre ",List_name)
        con.commit()

    #Envia un email
    def sendEmail( self,List_data,destinatario):
        # create message object instance
        msg = MIMEMultipart()
        message = "Lista creada por ti en SpotyUN.. Muchas gracias por elegirnos a continuacion el\n\nNombre de la Lista= "+List_data[1]+"\ntu identificacion = "+str(List_data[2])+"\ntu email = "+List_data[3]+"\n\nSpotyUN."

        # setup the parameters of the message
        password = "LAVACALOLA1"
        msg['From'] = "unspoty@gmail.com"
        msg['To'] = destinatario
        msg['Subject'] = "Lista creada en SpotyUN"

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print ("successfully sent email to: "+destinatario)


    #Devuelve el numero de canciones por email
    def numSongsOfEachEmail( self,con,email):
        cursorOBJ= con.cursor()
        cantidadEmails='SELECT count(clientEmail) FROM list WHERE clientEmail="'+email+ '"'
        cursorOBJ.execute(cantidadEmails)
        return int(cursorOBJ.fetchone()[0])


    def existList(self,con,nameList, idCliente):
        cursorOBJ= con.cursor()
        try:
            ##cambiar aqui por el nombre de la tabla de cliente identificacion cliente integer
            existeCliente='SELECT 1 FROM list WHERE name ="'+nameList+'" AND clientIdentification='+str(idCliente)
            cursorOBJ.execute(existeCliente)
            filas=cursorOBJ.fetchone()[0]
            return True
        except:
            return False
        return False


    #Devuelve true si existe una lista, del cliente
    def extraerListOfClient(self,con, clientIdentification,imprimir):
        cursorOBJ= con.cursor()
        tablaConsultar='SELECT * FROM list WHERE clientIdentification="'+str(clientIdentification)+'"'
        cursorOBJ.execute(tablaConsultar)
        filas=cursorOBJ.fetchall()
        if imprimir:
          print("(Codigo de Lista, Nombre Lista, Identificacion cliente, Cliente email, Codigo de cancion, Nombre de codigo, Interprete , Picture)")
          for row in filas:
            print(row)
        return filas

    #Extrae informacion de la lista que tenga la identificacion del cliente y nombre de la cancion
    def extraerListOfClientAndName(self,con, clientIdentification,nameList,imprimir):
        cursorOBJ= con.cursor()
        tablaConsultar='SELECT * FROM list WHERE clientIdentification="'+str(clientIdentification)+'"'+' AND '+'name='+'"'+nameList+'"'
        cursorOBJ.execute(tablaConsultar)
        filas=cursorOBJ.fetchall()
        if imprimir:
          print("(Codigo de Lista, Nombre Lista, Identificacion cliente, Cliente email, Codigo de cancion, Nombre de codigo, Interprete , Picture)")
          for row in filas:
            print(row)
        return filas

    #Guarda la lista en BD
    def saveList(self,con,date_list):
        cursorOBJ= con.cursor()
        cursorOBJ.execute('''INSERT INTO list VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',date_list)
        con.commit()

    #Extrae codigos de la lista dependiendo el nombre de la lista y la id del cliente
    def extraeCodigosList(self,con,identificacionCliente , nameList):
      listas=self.extraerListOfClientAndName(con,identificacionCliente ,nameList,False)
      codigos=[]
      for i in listas:
        codigos.append(i[4])
      return codigos



    #No se usa
    def extraeNombresListasOfClient(self,con,identificacionCliente):
        listas=self.extraerListOfClient(con,identificacionCliente,False)
        nombres=[]
        for i in listas:
            nombres.append(i[1])
        return list(set(nombres))

    #No se usa
    def NombreListayCanciones(self,con,identificacionCliente):
        nombres=self.extraeNombresListasOfClient(con,identificacionCliente)
        listacompleta=self.extraerListOfClient(con,identificacionCliente,False)

        listaycodigos = {}

        for i in range(len(nombres)):
            codigos=[]
            for j in listacompleta:
                if nombres[i]==j[1]:
                    codigos.append(j[4])
            listaycodigos[nombres[i]] = codigos
        return(listaycodigos)




    #devuelve diccionario con nombre y autor, con una lista del cliente
    def ListaCancionesAutoresOnly(self,con,identificacionCliente, nombrelista):
        nombres=self.extraeNombresListasOfClient(con,identificacionCliente)
        listacompleta=self.extraerListOfClient(con,identificacionCliente,False)

        listaycodigos = {}

        codigos={}
        for j in listacompleta:
            if nombrelista==j[1]:
                codigos[j[4]]="Codigo "+str(j[4]).ljust(15)+"Nombre= "+j[5].ljust(40)+"Interprete= "+j[6]
        listaycodigos[nombrelista] = codigos
        return(listaycodigos)


    #devuelve diccionario de la lista, nombre y autor,listas del cliente
    def ListaCancionesAutores(self,con,identificacionCliente):
        nombres=self.extraeNombresListasOfClient(con,identificacionCliente)
        listacompleta=self.extraerListOfClient(con,identificacionCliente,False)

        listaycodigos = {}

        for i in range(len(nombres)):
            codigos={}
            for j in listacompleta:
                if nombres[i]==j[1]:
                    codigos[j[4]]="Codigo "+str(j[4]).ljust(15)+"Nombre= "+j[5].ljust(40)+"Interprete= "+j[6]
            listaycodigos[nombres[i]] = codigos
        return(listaycodigos)


    #Verifica si existe una cancion en una lista, dependiendo del id del cliente
    def existSongOfList(self,con,nameList, idCliente,idCancion):
        cursorOBJ= con.cursor()

        try:
            existeCliente='SELECT 1 FROM list WHERE name ="'+nameList+'" AND clientIdentification='+str(idCliente)+' AND recordCode='+str(idCancion)
            cursorOBJ.execute(existeCliente)
            filas=cursorOBJ.fetchone()[0]
            return True
        except:
            return False
        return False

    #imprime diccionario
    def imprimeDiccionario(self,dicc):
        for i in dicc:
            print("\n")
            print(" ".ljust(40)+i)
            print("_"*110)
            for j in dicc[i]:
                print(dicc[i][j])
            print("_"*110)
        print("\n")

    #elimina la cancion de una lista
    def eliminaSongOfList(self,con,List_name,idCliente,codeSong):
        cursorOBJ= con.cursor()
        listaBorrar='DELETE FROM list WHERE name="'+List_name+'"'+' AND '+'clientIdentification='+str(idCliente)+' AND '+'recordCode='+str(codeSong)
        cursorOBJ.execute(listaBorrar)

        con.commit()
        return ("Eliminamos la cancion "+str(codeSong)+"de la lista "+List_name)

    #Actualiza unicamente el nombre de la lista, , depende de cada cliente
    def updateSongOfList(self,con,List_name,idcliente,codeSongOld, infoSongNew):
        codigocancion=str(infoSongNew[0])
        nombrecancion=infoSongNew[1]
        performercancion=infoSongNew[4]
        cursorOBJ= con.cursor()
        listaActualiza='UPDATE list SET recordCode='+codigocancion+', recordName="'+nombrecancion+'", recordPerformer="'+performercancion+'"  WHERE name="'+List_name+'" AND clientIdentification='+str(idcliente)+' AND recordCode='+str(codeSongOld)
        cursorOBJ.execute(listaActualiza)
        print("La lista ",List_name," fue actualizada " )
        con.commit()


"""**********************************************"""
"""CLASE BUSCADOR"""

class buscador():
    def __init__(self, conexion, lista):
        self.conexion = conexion
        self.lista = lista

    def menuOrdenador(self, conexion, lista):
        self.lista = lista
        opcion = self.ingresadatos()
        if opcion == '1':

            buscar = input("digite su busqueda: ")
            filas=self.buscador(conexion,'name', buscar)
            for i in range(len(filas)):
                print(filas[i])
        elif opcion == '2':
            buscar = input("digite su busqueda: ")
            filas=self.buscador(conexion,'genre', buscar)
            for i in range(len(filas)):
                print(filas[i])

        elif opcion == '3':
            buscar = input("digite su busqueda: ")
            filas=self.buscador(conexion,'album', buscar)
            for i in range(len(filas)):
                print(filas[i])

        elif opcion == '4':
            buscar = input("digite su busqueda: ")
            filas=self.buscador(conexion,'interpreter', buscar)
            for i in range(len(filas)):
                print(filas[i])

        elif opcion == '5':
            buscar = input("digite su busqueda: ")
            filas=self.buscador(conexion,'code', buscar)
            for i in range(len(filas)):
                print(filas[i])



    def buscador(self, conexion, modulo, busqueda):
        cursorObj = conexion.cursor()
        consultarTabla = 'SELECT * FROM  Cancion WHERE {}= "{}" '.format(modulo, busqueda)
        cursorObj.execute(consultarTabla)
        filas = cursorObj.fetchall()
        vacio = 0
        if len(filas) == 0:
            print("entro")
        else:
            return filas





    def ingresadatos(self):
        print("elije la categoria por la que quieres ordenar:")
        print("1)nombre")
        print("2)genero")
        print("3)album")
        print("5)interprete")
        print("4)codigo")
        opcion = input()
        return opcion
