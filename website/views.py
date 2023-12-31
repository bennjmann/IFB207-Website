from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import or_, and_
from .models import Event, Booking
from . import db
from flask_login import current_user

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
    user_bookings = db.session.query(Booking.id, Booking.purchase_at, Event.name, Event.image, Booking.price, Booking.quantity).join(Event).where(Booking.user_id == current_user.id)
    return render_template('bookings.html', bookings=user_bookings)
    
# example url http://domain.com/search?search=keyword&type=all&date=all&duration=60&max_cost=50.0#search
@mainbp.route('/search')
def search():
    search_query = request.args.get('search', default="")
    date = request.args.get('date', default="")
    event_type = request.args.get('type', default="")
    duration = request.args.get('duration', type=int, default=0)
    max_cost = request.args.get('max_cost', type=float, default=float('inf'))

    query_conditions = []

    if search_query:
        query_conditions.append(or_(Event.name.like(f"%{search_query}%"), Event.description.like(f"%{search_query}%")))
    
    # options: (today, this_week, this_month, this_year)
    if date:
        if date == 'today':
            query_conditions.append(Event.date >= datetime.now().date())
        elif date == 'this_week':
            query_conditions.append(Event.date >= datetime.now() -timedelta(days=7))
        elif date == 'this_month':
            query_conditions.append(Event.date >= datetime.now() - timedelta(days=30))
        elif date == 'this_year':
            query_conditions.append(Event.date >= datetime.now() - timedelta(days=365))

    # options: (All, Live, Recorded, Workshop, Lecture)
    if event_type in ['Live', 'Recorded', 'Workshop', 'Lecture']:
        query_conditions.append(Event.type == event_type)

    # options: (under_20, 20_to_60, over_1_hour)
    if duration:
        if duration == 'under_20':
            query_conditions.append(Event.duration <= 20)
        elif duration == '20_to_60':
            query_conditions.append(and_(Event.duration > 20, Event.duration <= 60))
        elif duration == 'over_1_hour':
            query_conditions.append(Event.duration > 60)

    if max_cost < float('inf'):
        query_conditions.append(Event.ticket_cost <= max_cost)

    if query_conditions:
        destinations = db.session.query(Event).filter(and_(*query_conditions)).all()
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))