import os
from ..main import request, jsonify, app, bcrypt, jwt_required, create_access_token, get_jwt_identity
from ..db import db
from ..modelos import User
from flask import Flask, url_for
from datetime import datetime
import json

@app.route('/signup' , methods=['POST'])
def signup():
    body = request.get_json()
    #print(body['username'])     
    try:
        if body is None:
            raise APIException("Body está vacío o email no viene en el body, es inválido" , status_code=400)
        if body['email'] is None or body['email']=="":
            raise APIException("email es inválido" , status_code=400)
        if body['password'] is None or body['password']=="":
            raise APIException("password es inválido" , status_code=400)      
      

        password = bcrypt.generate_password_hash(body['password'], 10).decode("utf-8")

        new_user = User(email=body['email'], password=password, is_active=True)
        user = User.query.filter_by(email=body['email']).first()
        # users = User.query.all()
        # users = list(map( lambda user: user.serialize(), users))

        # for i in range(len(users)):
        #     if(users[i]['email']==new_user.serialize()['email']):
        #         raise APIException("El usuario ya existe" , status_code=400)
                
        print(new_user)
        #print(new_user.serialize())
        db.session.add(new_user) 
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201 

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar usuario"}), 500 

#Here is the LOGIN route------------------------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user is None:
        raise APIException("usuario no existe", status_code=401)
    
#validating user
    if not bcrypt.check_password_hash(user.password, password):
        raise APIException("usuario o password no coinciden", status_code=401)

    access_token = create_access_token(identity= user.id)
    return jsonify({"token": access_token})

#Here is the LOGOUT route-------------------------------------------------------------------------------------------------------------------------------- 

@app.route('/logout', methods=['GET']) #endpoint
@jwt_required()
def logout():
    print(get_jwt())
    jti=get_jwt()["jti"]
    now = datetime.now(timezone.utc)

    tokenBlocked = TokenBlockedList(token=jti, created_at=now)
    db.session.add(tokenBlocked)
    db.session.commit()

    return jsonify({"message":"token bloqueado"})   

#Here is the route to SUSPEND/REACTIVE users--------------------------------------------------------------------------------------------------------------
@app.route('/suspended/<int:user_id>', methods=['PUT']) #endpoint
@jwt_required()
def user_suspended(user_id):
    if get_jwt_identity() != 1:
        return jsonify({"message":"Operación no permitida"}), 403
        
    user = User.query.get(user_id)
   
    #validamos si viene el campo name en el body o no (despues de hacer el request.get_json())
    if user.is_active:
        user.is_active = False
        db.session.commit()   
        return jsonify({"message":"Usuario suspendido"}), 203
    else:
        user.is_active = True
        db.session.commit()   
        return jsonify({"message":"Usuario reactivado"}), 203 

#Here is the protected route-------------------------------------------------------------------------------------------------------------------------------- 
@app.route('/profile', methods=['GET']) #endpoint
@jwt_required() 
def profile(): 
    #claims = get_jwt()
    print("id del usuario:", get_jwt_identity()) #imprimiendo la identidad del usuario que es el id
    user = User.query.get(get_jwt_identity()) #búsqueda del id del usuario en la base de datos

    #get_jwt() regresa un diccionario, y una propiedad importante es jti
    jti=get_jwt()["jti"] 

    Blocked = BlockedList.query.filter_by(token=jti).first()
    #cuando hay coincidencia Bloked es instancia de la clase BlockedList
    #cuando No hay coincidencia tokenBlocked = None

    if isinstance(Blocked, BlockedList):
        return jsonify(msg="Acceso Denegado")

    response_body={
        "message":"token válido",
        "user_id": user.id, #get_jwt_identity(),
        "user_email": user.email,
        "description": user.description
    }

    return jsonify(response_body), 200          

#Here is the route to call the users FAVORITE LIST 

@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    favorite_person = Favorite_Person.query.all()
    favorite_person = list(map( lambda favorite_person: favorite_person.serialize(), favorite_persons))
    favorite_planet = Favorite_Planet.query.all()
    favorite_planet = list(map( lambda favorite_planet: favorite_planet.serialize(), favorite_planets))
    favorite_vehicle = Favorite_Vehicle.query.all()
    favorite_vehicle = list(map( lambda favorite_vehicle: favorite_vehicle.serialize(), favorite_vehicles))
    favorites_list =  favorite_person + favorite_planet + favorite_vehicle
    print(favorites_list)
    return jsonify(favorites_list), 200
