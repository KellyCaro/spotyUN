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

