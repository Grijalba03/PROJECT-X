import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..modelos import Person, Favorite_Person
from flask import Flask, url_for
from datetime import datetime
import json 
 

 #Here is the route to call ALL OF THE CHARACTERS from the DB -----------------------------------------------------------------------

@app.route('/person', methods=['GET'])
def get_person():
    person = Person.query.all()
    #print(users)
    person = list(map( lambda person: person.serialize(), person)) 
    #print(users)  
    return jsonify(person), 200

#Here is the route to call the Characters INDIVIDUALLY from the DB------------------------------------------------------------------

@app.route('/person/<int:person_id>', methods=['GET'])
def get_person_by_id(person_id):
    if person_id==0:
        raise APIException("The person ID cannot be 0", status_code=400)  
    person = Person.query.get(people_id)
    if person == None:
        raise APIException("User does not exist", status_code=400)  
    return jsonify(person.serialize()), 200 

#Here is the route to ADD CHARACTERS to the DB---------------------------------------------------------------------------------------- 
@app.route('/person', methods=['POST'])
def create_new_person():
    body = request.get_json()
    #validaciones
    if body is None:
        raise APIException("Body está vacío" , status_code=400)
    if body['name'] is None or body['name']=="":
        raise APIException("name es inválido" , status_code=400)

    new_character = Person(name=body['name'], height=body['height'], mass=body['mass'], hair_color=body['hair_color'], skin_color=body['skin_color'], eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'], homeworld=body['homeworld'])
    characters = Person.query.all()
    characters = list(map( lambda character: character.serialize(), characters))

    print(new_character)
    #print(new_user.serialize())
    db.session.add(new_character) 
    db.session.commit()
    
    return jsonify({"mensaje": "Personaje creado exitosamente"}), 201 

#Here is the route t DELETE CHARACTERS from the DB------------------------------------------------------------------------------------------- 
@app.route('/person/<int:item_id>', methods=['DELETE'])
def delete_person_by_id(item_id):
    if item_id==0:
        raise APIException("Id no puede ser igual a 0", status_code=400)  
    character = Person.query.get(item_id)
    if character == None:
        raise APIException("El personaje no existe", status_code=400)  
    db.session.delete(item)
    db.session.commit()
    return jsonify("personaje eliminado exitosamente"), 200 



#Here is the route to DELETE CHARACTER from the FAVORITE LIST----------------------------------------------------------------------------------
@app.route('/favorites/person/<int:item_id>', methods=['DELETE'])
def delete_favorite_person_by_id(item_id):
    if item_id==0:
        raise APIException("Id no puede ser igual a 0", status_code=400)  
    item = Person.query.get(item_id)
    if item == None:
        raise APIException("El personaje no existe", status_code=400)  
    db.session.delete(item)
    db.session.commit()
    return jsonify("Personaje eliminado exitosamente"), 200    



#Here is the route to UPDATE CHARACTERS in the DB------------------------------------------------------------------------------------------------ 
@app.route('/person/<int:person_id>', methods=['PUT'])
def put_person_by_id(person_id):
    if person_id==0:
        raise APIException("Id no puede ser igual a 0", status_code=400)  
    person = Person.query.get(person_id)#buscar por ID es la manera mas eficiente de realizar busquedas en las bases de datos
    if person == None:
        raise APIException("El usuario no existe", status_code=400) 
    body = request.get_json()
    #validaciones
    if body is None:
        raise APIException("Body está vacío" , status_code=400)
    #validamos si viene el campo name en el body o no (despues de hacer el request.get_json())
    if not body['name'] is None:
        person.name = body['name']
    db.session.commit()     
    return jsonify(person.serialize()), 200


#Here is the route to FIND CHARACTERS in the DB------------------------------------------------------------------------------------------------------ 
@app.route('/person/busqueda', methods=['POST'])
def busqueda_person():
    body = request.get_json()
    #validaciones
    if body is None:
        raise APIException("Body está vacío" , status_code=400)
    if not body['name'] is None:    
        found = Person.query.filter(Person.name==body['name']).all() #va a encontrar todas las coincidencias        
        found = list(map( lambda item: item.serialize(), found))
        print(found)
    if found == None:
        raise APIException("El personaje no existe", status_code=400)  
    return jsonify(found), 200     

