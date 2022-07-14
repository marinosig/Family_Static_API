"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def find_member(member_id):
    member = jackson_family.get_member(member_id)

    if  member: 
        return jsonify(member), 200
    
    return '<h1>Not found !!</h1>', 404


@app.route('/member', methods=['POST'])
def add_new_member():
    body_first_name = request.json.get("first_name")
    body_age = request.json.get("age")
    body_lucky_numbers = request.json.get("lucky_numbers")
    body_id = request.json.get("id")
    
    newmember = {
        "first_name": body_first_name,
        "last_name": "Jackson",
        "age": body_age,
        "lucky_numbers": body_lucky_numbers,
        "id": body_id or jackson_family._generateId()
    }

    jackson_family.add_member(newmember)

    return jsonify(newmember), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_a_member(member_id):
    response = jackson_family.delete_member(member_id)

    if response:
        return jsonify({ "done": response}), 200

    return jsonify({ "Not_Found": True}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)