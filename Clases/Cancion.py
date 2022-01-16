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