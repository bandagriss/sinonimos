# -*- coding: utf-8 -*-


from conexion import conexion
from utils import elimina_tildes, elimina_caracteres_especiales


class Sinonimos(object):
    """
    Migra los sinonimos de la RAE y los une con los de Thesaurus (LibreOffice)
    """

    def __init__(self):
        self.cursor = conexion('homonimia', 'localhost', 'roy', 'bandagriss')
        print("Conectando a la base de Datos...")

    def prueba(self):
        self.cursor.execute('SELECT * FROM conectores')
        return self.cursor.fetchall()

    def imprime(self, datos):
        for dato in datos:
            print(dato[1])

    def leerArchivoRae(self, archivo):
        archivo = open(archivo, "r+")
        return archivo

    def escribirSQL(self, archivo):
        file = open(archivo, "w")
        return file

    def convierteSql(self, archivo, sqlArchivo):
        for linea in archivo.readlines():
            palabras = linea.split(",")
            especial = elimina_caracteres_especiales(palabras[0])
            if especial == '':
                print("entro ==> ", especial, palabras)
                palabras.pop(0)
                print("nuevo => ", palabras)
            sinonimos = ''
            for palabra in palabras:
                if palabra != palabras[0]:
                    if self.verificaPalabra(palabra):
                        sinonimos = sinonimos + " " + elimina_tildes(palabra.lower())
            if sinonimos and self.verificaPalabra(palabras[0]):
                palabraL = self.buscaLibreOffice(palabras[0])
                palabraRae = ','.join(sinonimos.strip().split())
                sinonimosUnidos = self.unionDiccionarios(palabraL, palabraRae)
                if self.verificaConectores(palabras[0]):
                    sql = "INSERT INTO sinonimos (palabra, sinonimos, estado, _fecha_creacion, _fecha_modificacion) VALUES('{0}','{1}','ACTIVO', now(), now());\n".format(elimina_tildes(palabras[0].lower()), sinonimosUnidos)
                    sqlArchivo.write(sql)
            
    def verificaPalabra(self, palabra):
        palabra = palabra.strip().split(" ")
        if len(palabra) > 1:
            return False
        return True

    def verificaConectores(self, palabra):
        self.cursor.execute('SELECT count(*) from conectores where palabra = \'{0}\''.format(palabra))
        if self.cursor.fetchone()[0] > 0:
            return False
        return True

    def buscaLibreOffice(self, palabra):
        self.cursor.execute('SELECT sinonimos from sinonimos where palabra = \'{0}\''.format((palabra)))
        x = self.cursor.fetchone()
        if type(x) == tuple:
            return x[0]
        return ''

    def unionDiccionarios(self, sinonimosL, sinonimosRae):
        palabraL = sinonimosL.strip().split(',')
        palabraRae = sinonimosRae.strip().split(',')
        union = palabraL + palabraRae
        sinonimos = list(set(union))
        sinonimos = ' '.join(sinonimos)
        sinonimos = ','.join(sinonimos.strip().split())
        return sinonimos
        
        
        
        
        
        
        

s = Sinonimos()
# datos = s.prueba()
# s.imprime(datos)
archivo = s.leerArchivoRae('archivos/f_sinonimos.txt')
archivoSql = s.escribirSQL('archivos/sinonimos.sql')
s.convierteSql(archivo, archivoSql)


