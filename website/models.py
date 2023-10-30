from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='user')
    event = db.relationship('Event', backref='user')
    bookings = db.relationship('Booking', backref='user')
    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    status = db.Column(db.String(20))
    type = db.Column(db.String(80))

    date = db.Column(db.Date)
    time = db.Column(db.Time)
    duration = db.Column(db.Integer)

    image = db.Column(db.String(400))
    description = db.Column(db.String(400))
    
    ticket_cost = db.Column(db.Integer)
    total_tickets = db.Column(db.Integer)

    comments = db.relationship('Comment', backref='event')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  

    def __repr__(self):
        return "Name: {}".format(self.event_name)
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)

class Booking(db.Model):    
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Integer())
    quantity = db.Column(db.Integer())
    purchase_at = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return "<Name: {}>".format(self.name)
