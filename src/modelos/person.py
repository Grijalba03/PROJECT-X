from ..db import db
import os

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float)
    mass = db.Column(db.Float)
    hair_color  = db.Column(db.String(20))
    skin_color  = db.Column(db.String(20))
    eye_color  = db.Column(db.String(20))
    birth_year = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    homeworld = db.Column(db.String(250))
    people_favorite = db.relationship("Favorite_Person", backref="person") 

    def __repr__(self):
        return '<Person %r>' % self.name

    def serialize(self):     #personerialize------------------------------------------------------------------
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld
        }


class Favorite_Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #con el nombre de la tabla user y atributo id
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    #Esta es una tabla pivote para relacionar User y People, relación muchos a muchos

    def serialize(self): #Favorite_People_Serialize-------------------------------------------------------------------------------------------------------------------------------------------
        return {
            "id": self.id,
            "user_email": User.query.get(self.user_id).serialize()['email'],
            "character_name": Person.query.get(self.person_id).serialize()['name']          
        } 