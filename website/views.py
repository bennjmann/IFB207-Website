from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template('index.html', destinations=destinations )


@mainbp.route('/<id>')
def selected(id):
    destinations = db.session.scalars(db.select(Destination)).all()
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    return render_template('index.html', selected_destination=destination, destinations=destinations)

@mainbp.route('/bookings')
def booking():
    return render_template('user-bookings.html')



@mainbp.route('/search')
def search(search=""):
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        destinations = db.session.scalars(db.select(Destination).where(Destination.description.like(query)))
        if (destinations):
            destinations = ""
        return render_template('index.html', destinations=destinations) #
    else:
        return redirect(url_for('main.index'))