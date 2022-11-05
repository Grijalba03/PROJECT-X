import os
from ..main import request, jsonify, app, bcrypt
from ..db import db
from ..modelos import Vehicle
from flask import Flask, url_for
from datetime import datetime
import json 


#Here is the route to call ALL OF THE VEHICLES from the DB-----------------------------------------------------

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    vehicle = Vehicle.query.all()
    vehicle = list(map( lambda vehicle: vehicle.serialize(), vehicles))  
    return jsonify(vehicle), 200 


#Here is the route to call the Vehicles INDIVIDUALLY from the DB ----------------------------------------------- 

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle_by_id(vehicle_id):
    if vehicle_id==0:
        raise APIException("The Vehicle ID cannot be 0", status_code=400)  
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle == None:
        raise APIException("User does not exist", status_code=400)  
    return jsonify(vehicle.serialize()), 200 


 #Here is the route to ADD VEHICLES to the DB ------------------------------------------------------------------

@app.route('/vehicle', methods=['POST'])
def create_new_vehicle():
    body = request.get_json()
    #validaciones
    if body is None:
        raise APIException("Body está vacío" , status_code=400)
    if body['name'] is None or body['name']=="":
        raise APIException("name es inválido" , status_code=400)

    new_vehicle = Vehicle(name=body['name'], model=body['model'], vehicle_class=body['vehicle_class'], manufacturer=body['manufacturer'], cost_in_credits=body['cost_in_credits'], length=body['length'], crew=body['crew'], passengers=body['passengers'], max_atmosphering_speed=body['max_atmosphering_speed'], cargo_capacity=body['cargo_capacity'], consumables=body['consumables'])
    vehicle = Vehicle.query.all()
    vehicle = list(map( lambda vehicle: vehicle.serialize(), vehicles))

    for i in range(len(vehicles)):
        if(vehicles[i]['name']==new_vehicles.serialize()['name']):
            raise APIException("El vehículo ya existe" , status_code=400)
            
    print(new_vehicles)
    db.session.add(new_vehicles) 
    db.session.commit()
    
    return jsonify({"mensaje": "Vehículo creado exitosamente"}), 201   


#Here is the route to DELETE VEHICLES from the DB----------------------------------------------------------------
@app.route('/vehicle/<int:item_id>', methods=['DELETE'])
def delete_vehicle_by_id(item_id):
    if item_id==0:
        raise APIException("Id no puede ser igual a 0", status_code=400)  
    vehicle = Vehicles.query.get(item_id)
    if vehicle == None:
        raise APIException("El vehículo no existe", status_code=400)  
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify("vehículo eliminado exitosamente"), 200 


#Here is the route to DELETE VEHICLES from THE FAVORITE LIST-------------------------------------------------------
@app.route('/favorites/vehicle/<int:item_id>', methods=['DELETE'])
def delete_favorite_vehicle_by_id(item_id):
    if item_id==0:
        raise APIException("Id no puede ser igual a 0", status_code=400)  
    item = Vehicle.query.get(item_id)
    if item == None:
        raise APIException("El vehículo no existe", status_code=400)  
    db.session.delete(item)
    db.session.commit()
    return jsonify("Vehículo eliminado exitosamente"), 200
