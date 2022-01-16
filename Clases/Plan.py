
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
