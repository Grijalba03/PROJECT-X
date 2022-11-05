from ..db import db
import os

class Planet(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) 
    diameter = db.Column(db.Float) 
    rotation_Period = db.Column(db.Float)
    orbital_Period = db.Column(db.Float)
    gravity = db.Column(db.String(100))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(100))
    terrain = db.Column(db.String(100))
    surface_Water = db.Column(db.Integer)
    planets_favorite = db.relationship("Favorite_Planet", backref="planet") 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,  
            "diameter": self.diameter,
            "rotation_Period": self.rotation_Period,
            "orbital_Period": self.orbital_Period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_Water": self.surface_Water   
        } 


class Favorite_Planet(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #con el nombre de la tabla user y atributo id
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))


    def serialize(self):
        return {
            "id": self.id,
            "user_email": User.query.get(self.user_id).serialize()['email'],
            "planet_name": Planets.query.get(self.planet_id).serialize()['name'],   
           
        }            