from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    diameter = db.Column(db.Integer, unique=False)
    rotation_period = db.Column(db.Integer, unique=False)
    orbital_period = db.Column(db.Integer, unique=False)
    gravity = db.Column(db.String(80), unique=False)
    population = db.Column(db.Integer, unique=False)
    climate = db.Column(db.String(80), unique=False)
    terrain = db.Column(db.String(80), unique=False)
    surface_water = db.Column(db.Integer, unique=False)

    def __repr__(self):
        return f"Planet: {self.name} with id {self.id} "

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    hair_color = db.Column(db.String(80), unique=False)
    eye_color = db.Column(db.String(80), unique=False)
    skin_color = db.Column(db.String(80), unique=False)
    birth_year = db.Column(db.String(80), unique=False)
    gender = db.Column(db.String(80), unique=False)
    homeworld = db.Column(db.String(80), unique=False)

    def __repr__(self):
        return f"Character: {self.name} with id {self.id} "

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), unique=True)
    vehicle_class = db.Column(db.String(80), unique=False)
    manufacturer = db.Column(db.String(80), unique=False)
    cost_in_credits = db.Column(db.Integer, unique=False)
    length = db.Column(db.Float, unique=False)
    crew = db.Column(db.Integer, unique=False)
    passengers = db.Column(db.Integer, unique=False)
    max_atmosphering_speed = db.Column(db.Integer, unique=False)
    cargo_capacity = db.Column(db.Integer, unique=False)
    consumables = db.Column(db.String(80), unique=False)
    pilots = db.Column(db.String(80), unique=True)

    def __repr__(self):
        return f"Vehicle: {self.name} with id {self.id} "

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "pilots": self.pilots,
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f"User with id {self.id} "

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

# class Favorite(db.Model):
#     __tablename__ = 'favorite'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
#     user = db.relationship(User)
#     character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
#     character = db.relationship(Character)
#     planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
#     planet = db.relationship(Planet)
#     vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
#     vehicle = db.relationship(Vehicle)
    
#     def __repr__(self):
#         return f"The user with id {self.user_id} has favorited: {self.character_id}, {self.planet_id}, {self.vehicle_id} "

#     def serialize(self):
#         return {
#             "id": self.id,
#             "character_id": self.character_id,
#             "planet_id": self.planet_id,
#             "vehicle_id": self.vehicle_id,
#         }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    favorite_type = db.Column(db.String(80), nullable=False)
    favorite_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Favorite: {self.id} for User: {self.user_id}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_type": self.favorite_type,
            "favorite_id": self.favorite_id,
        }