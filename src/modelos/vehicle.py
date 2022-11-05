from ..db import db 
import os

class Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    model = db.Column(db.String(100))
    vehicle_class = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    cost_in_credits = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.String(100))
    max_atmosphering_speed = db.Column(db.String(100))
    cargo_capacity = db.Column(db.String(100))
    consumables = db.Column(db.String(100))
    vehicle_favorite = db.relationship("Favorite_Vehicle", backref="vehicle") 


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,  
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,   
            "consumables": self.consumables   
               
        } 


class Favorite_Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #con el nombre de la tabla user y atributo id
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))    

    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.user_id).serialize()['email'],
            "vehicle_name": Vehicle.query.get(self.vehicle_id).serialize()['name']
            
        }  