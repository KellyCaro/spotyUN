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

