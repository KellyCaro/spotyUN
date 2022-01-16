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

"""**************************************************************
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
