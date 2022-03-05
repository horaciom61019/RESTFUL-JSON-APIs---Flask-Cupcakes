"""Flask app for Cupcakes"""

from crypt import methods
from flask import Flask, jsonify, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake
# from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret" 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """ Render Home page """

    return render_template("index.html")


@app.route('/api/cupcakes')
def return_cupcakes():
    """ 
    Return JSON of all cupcakes in data base 

    Returns JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}
    """

    cupcakes = [cupcake.serialize_cupcake() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    """ 
    Add a cupcake, return new cupcake data 

    Returns JSON {cupcake: {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize_cupcake()), 201)


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """
    Return data for specific cupcake

    Return JSON {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.serialize_cupcake())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def edit_cupcake(cupcake_id):
    """
    Edit cupcake data, retur updated data in JSON

    Return {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize_cupcake()) 


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """
    Deleted cupcake, return confirmation message

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted") 