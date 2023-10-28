from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', destinations=destinations )


@mainbp.route('/<id>')
def selected(id):
    destinations = db.session.scalars(db.select(Event)).all()
    destination = db.session.scalar(db.select(Event).where(Event.id==id))
    return render_template('index.html', selected_destination=destination, destinations=destinations)

@mainbp.route('/bookings')
def booking():
    return render_template('bookings.html')


@mainbp.route('/search')
def search(search=""):
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        destinations = db.session.scalars(db.select(Event).where(Event.description.like(query)))
        if (destinations):
            destinations = ""
        return render_template('index.html', destinations=destinations) #
    else:
        return redirect(url_for('main.index'))