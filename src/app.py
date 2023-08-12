"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if users is None:
        raise APIException(f"There's no user in the database", status_code=400)
    users_serialized = list(map(lambda x : x.serialize(), users))
    print(users_serialized)
    response_body = ({'msg': 'Completed', 'users': users_serialized})
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    single_user = User.query.get(user_id)
    if single_user is None:
        raise APIException(f"The user id {user_id} doesn't exist", status_code=400)
    print(single_user.serialize())
    response_body = {
        'user_id': user_id,
        'user_info': single_user.serialize()
    }
    return jsonify(response_body), 200

# Gets the list of planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets_serialized = list(map(lambda x: x.serialize(), planets))
    return jsonify({'msg': 'Completed', 'planets': planets_serialized})

# Gets the information of a single planet
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        raise APIException(f"The planet id {planet_id} doesn't exist", status_code=400)
    print(single_planet.serialize())
    response_body = {
        'planet_id': planet_id,
        'planet_info': single_planet.serialize()
    }
    return jsonify(response_body), 200

# Gets the list of characters
@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    people_serialized = list(map(lambda x: x.serialize(), people))
    return jsonify({'msg': 'Completed', 'people': people_serialized})

# Gets the information of a single character
@app.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):
    single_person = Character.query.get(person_id)
    if single_person is None:
        raise APIException(f"The character with id {person_id} doesn't exist", status_code=400)
    print(single_person.serialize())
    response_body = {
        'character_id': person_id,
        'character_info': single_person.serialize()
    }
    return jsonify(response_body), 200

# Gets the list of vehicles
@app.route('/vehicles', methods=['GET'])
def get_vehicle():
    vehicles = Vehicle.query.all()
    vehicles_serialized = list(map(lambda x: x.serialize(), vehicles))
    return jsonify({'msg': 'Completed', 'vehicles': vehicles_serialized})

# Gets the information of a single vehicle
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_single_vehicle(vehicle_id):
    single_vehicle = Vehicle.query.get(vehicle_id)
    if single_vehicle is None:
        raise APIException(f"The vehicle with id {vehicle_id} doesn't exist", status_code=400)
    print(single_vehicle.serialize())
    response_body = {
        'vehicle_id': vehicle_id,
        'vehicle_info': single_vehicle.serialize()
    }
    return jsonify(response_body), 200

#Checks current user's favorites
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()
    if not user_favorites:
        raise APIException(f"User with id {user_id} has no favorites", status_code=400)
    favorites_serialized = list(map(lambda x: x.serialize(), user_favorites))
    response_body = {'msg': 'Completed', 'favorites': favorites_serialized}
    return jsonify(response_body), 200

# Adds to the favorite planet's list
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    body = request.get_json(silent=True)
    if body is None:
        raise APIException('You must send information inside the body', status_code=400)
    if 'user_id' not in body:
        raise APIException('You must send the user id', status_code=400)
    user_id = body['user_id']
    # Checks if it was already favorited by the user
    existing_favorite = Favorite.query.filter_by(user_id=user_id, favorite_type='planet', favorite_id=planet_id).first()
    if existing_favorite:
        return jsonify({'message': 'Planet is already a favorite for this user'}), 409
    #Adds favorite to the list
    favorite = Favorite(user_id=user_id, favorite_type='planet', favorite_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet added successfully'}), 201

# Removes a planet from the favorite planets' list
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet = Favorite.query.filter_by(favorite_type='planet', favorite_id=planet_id).first()
    if favorite_planet is None:
        raise APIException("The planet doesn't exist", status_code=400)
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify({'msg': 'Favorite planet deleted successfully'}), 200

# Adds a character to the favorite characters' list
@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    body = request.get_json(silent=True)
    if body is None:
        raise APIException('You must send information inside the body', status_code=400)
    if 'user_id' not in body:
        raise APIException('You must send the user id', status_code=400)
    user_id = body['user_id']
    # Checks if it was already favorited by the user
    existing_favorite = Favorite.query.filter_by(user_id=user_id, favorite_type='character', favorite_id=character_id).first()
    if existing_favorite:
        return jsonify({'message': 'Character is already a favorite for this user'}), 409
    # Adds favorite to the list
    favorite = Favorite(user_id=user_id, favorite_type='character', favorite_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite character added successfully'}), 201

# Removes a character from the favorite characters' list
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    favorite_character = Favorite.query.filter_by(favorite_type='character', favorite_id=character_id).first()
    if favorite_character is None:
        raise APIException("The character doesn't exist", status_code=400)
    db.session.delete(favorite_character)
    db.session.commit()
    return jsonify({'msg': 'Favorite character deleted successfully'}), 200

# Adds a vehicle to the favorite vehicles' list
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    body = request.get_json(silent=True)
    if body is None:
        raise APIException('You must send information inside the body', status_code=400)
    if 'user_id' not in body:
        raise APIException('You must send the user id', status_code=400)
    user_id = body['user_id']
    # Checks if it was already favorited by the user
    existing_favorite = Favorite.query.filter_by(user_id=user_id, favorite_type='vehicle', favorite_id=vehicle_id).first()
    if existing_favorite:
        return jsonify({'message': 'Vehicle is already a favorite for this user'}), 409
    # Adds favorite to the list
    favorite = Favorite(user_id=user_id, favorite_type='vehicle', favorite_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite vehicle added successfully'}), 201

# Removes a vehicle from the favorite vehicles' list
@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    favorite_vehicle = Favorite.query.filter_by(favorite_type='vehicle', favorite_id=vehicle_id).first()
    if favorite_vehicle is None:
        raise APIException("The vehicle doesn't exist", status_code=400)
    db.session.delete(favorite_vehicle)
    db.session.commit()
    return jsonify({'msg': 'Favorite vehicle deleted successfully'}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

