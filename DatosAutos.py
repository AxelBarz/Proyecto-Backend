# FrameWork o Librerias
from flask import Flask, request, jsonify, render_template
from flask import request
from flask_cors import CORS
import mysql.connector
import mysql.connector.errorcode
from werkzeug.utils import secure_filename
import os 
import time

#------------------------------------------------------------------

# Desbloquear Flask 
app_auto=Flask(__name__)
CORS(app_auto)

#Clase para la base de datos 
class Ventas:
    # Constructor de clase y base de datos 
    def __init__(self, host, user, password, database):
        # Establecer conexiones (Menos la base de datos)
        self.conex=mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor=self.conex.cursor()


        #Averigua si existe la base de datos 
        try:
            self.cursor.execute(f"USE {database}")  #Ejecuta la BD si existe 
        except mysql.connector.Error as err: #Error que sale si no existe la BD
            # Si no exite, se crea la BD 
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conex.database=database
            else:
                raise err 
        


        # Creado ya la Base de Datos, se crea la tabla si no existe 
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS automovil (
                        codigo INT AUTO_INCREMENT PRIMARY KEY,
                        marca VARCHAR (100) NOT NULL,
                        anio YEAR NOT NULL,
                        precio INT NOT NULL,
                        transmision VARCHAR (100) NOT NULL,
                        combustible VARCHAR (30),
                        numetel INT NOT NULL
                        )''')
        self.conex.commit()


        #cierra el cursos que se le dio al inicio y se crea uno nuevo pero con el parametro dictionary=True
        self.cursor.close()
        self.cursor=self.conex.cursor(dictionary=True)




        #SE CREAN LAS FUNCIONES DE AGREGAR, CONSULTAR, MODIFICAR, LISTAR, ELIMINAR Y MOSTRAR LOS ELEMENTOS DE LA BASES DE DATOS 
    def agregar_auto(self, marca, anio, precio, transmision, combustible, numetel):
        sql="""INSERT INTO automovil (marca, anio, precio, transmision, combustible, numetel) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
        valores=(marca, anio, precio, transmision, combustible, numetel)

        self.cursor.execute(sql, valores)#Ejecuta el codigo para hacer el agregado
        self.conex.commit() #Asegura que los cambios se hagan 
        return self.cursor.lastrowid #retorna informacion del ultimo elemneto agregado 
        

    def consultar_auto(self, codigo):
        #Se hace la consulta a partir de su codigo
        self.cursor.execute(f"SELECT * FROM automovil WHERE codigo = {codigo}")
        return self.cursor.fetchone() #retorna el primer elemento que contenga ese codigo
        

    def modificar_auto(self, codigo, nueva_marca, nuevo_anio, nuevo_precio, nueva_transmision, nuevo_combustible, nuevo_numetel):
        sql="UPDATE automovil SET marca=%s, anio=%s, precio=%s, transmision=%s, combustible=%s, numetel=%s WHERE codigo=%s"
        valores=(nueva_marca, nuevo_anio, nuevo_precio, nueva_transmision, nuevo_combustible, nuevo_numetel, codigo)
        self.cursor.execute(sql, valores)
        self.conex.commit()
        return self.cursor.rowcount > 0
        

    def listar_autos(self):
        self.cursor.execute("SELECT * FROM automovil")
        publicacion= self.cursor.fetchall()
        return publicacion
        

    def eliminar_autos(self, codigo):
        self.cursor.execute(f"DELETE FROM automovil WHERE codigo = {codigo}")
        self.conex.commit()
        return self.cursor.rowcount > 0
        

    def mostrar_autos(self, codigo):
        autos=self.consultar_auto(codigo)
        if autos:
            print("/"*40)
            print(f"Código.....: {autos['codigo']}")
            print(f"marca......: {autos['marca']}")
            print(f"año........: {autos['anio']}")
            print(f"precio.....: {autos['precio']}")
            print(f"trasnmision: {autos['transmision']}")
            print(f"combustible: {autos['combustible']}")
            print(f"numero de telefono: {autos['numetel']}")
            print("/"*40)
        else:
            print("Auto no encontrado")
        


        #CUERPO DEL PROGRAMA 
        #Crear una instancia de la clase Ventas
ventas=Ventas(host='localhost', user='root', password='', database='miappautos')


        #LISTAR TODOS LOS AUTOS 
        #El metodo devuelve una lista de todos los autos en JSON
@app_auto.route("/automovil", methods=["GET"])
def lista_autos():
    autos=ventas.listar_autos()
    return jsonify(autos)
        
        #Muestra un solo auto segun el codigo que se ingrese 
        #El metodo busca en la BD el auto con el codido escrito y devuelve un Json con el auto si lo encuentra o None si no existe 
@app_auto.route("/automovil/<int:codigo>", methods=["GET"])
def muestra_auto(codigo):
    auto=ventas.consultar_auto(codigo)
    if auto:
        return jsonify(auto), 201
    else:
        return "Auto no encontrado", 404
    

        #AGREGAR UN AUTO
@app_auto.route("/automovil", methods=["POST"])
        #La Funcion de abajo se asocia con la URL y es llamada cuando se hace una solicitud POST a /publicacion
def agregar_auto():
            #Agarra los datos del form
    marca=request.form['marca']
    anio=request.form['anio']
    precio=request.form['precio']
    transmision=request.form['transmision']
    combustible=request.form['combustible']
    numetel=request.form['numetel']

    nuevo_codigo=ventas.agregar_auto(marca, anio, precio, transmision, combustible, numetel)
    if nuevo_codigo:
                
        #si el auto se agrega, se devuelve un mensaje de exito y un codigo HTTP 201
        return jsonify({"mensaje": "Auto agregado correctamente.", "codigo":nuevo_codigo}), 201
    else:
                #si el auto no se agrega, se devuelve un mensaje de error y un codigo HTTP 500
        return jsonify({"mensaje": "Error al agregar el auto"}),500


        #MODIFICA EL AUTO SEGUN EL CODIGO 
@app_auto.route("/automovil/<int:codigo>", methods=["PUT"])
        #La funcion de abajo se asocia con la URL y es invocada cuando se hace la solicitud PUT a /publicacion/ seguido del codigo 
def modificar_auto(codigo):
    #recuperacion de nuevo datos 
    nueva_marca=request.form.get("marca")
    nuevo_anio=request.form.get("anio")
    nuevo_precio=request.form.get("precio")
    nueva_transmision=request.form.get("transmision")
    nuevo_combustible=request.form.get("combustible")
    nuevo_numero=request.form.get("numetel")


    #Se llama al metodo modificar pasando el codigo y los nuevos datos 
    if ventas.modificar_auto(codigo, nueva_marca, nuevo_anio, nuevo_precio, nueva_transmision, nuevo_combustible, nuevo_numero):
        #Si se actualiza exitosamente, se devuelve un mensaje de exito y el HTTP 200
        return jsonify({"mensaje": "Publicacion modificada"}),200
    else: 
        #Si no se encuentra el auto, se devuelve un mensaje de error y el HTTP 404
        return jsonify({"mensaje":"Publicacion no encontrada"})
    


        #ELIMINACION DE UNA PUBLICACION SEGUN EL CODIGO 
@app_auto.route("/automovil/<int:codigo>", methods=["DELETE"])
        ##La funcion de abajo se asocia con la URL y es invocada cuando se hace la solicitud DELETE a /publicacion/ seguido del codigo 
def eliminar_auto(codigo):
    #busqueda de el auto en la BD
    auto=ventas.consultar_auto(codigo)
    if auto: #Si existe la publicacion, verifica si exite una imagen
        #luego seguiria la eliminacion de la publicacion 
        if ventas.eliminar_autos(codigo):
            ##Si el producto se elimina, se devuelve un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje":"Publicacion eliminada"}),200
        else:
            # #Si ocurre un error, se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar la publicacion"}), 500
    else:
        #Si el producto no se encuentra, se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "publicacion no encontrada"}), 404
    
if __name__=="__main__":
    app_auto.run(debug=True)





