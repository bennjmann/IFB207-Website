from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Comment, Event, Booking
from .forms import CommentForm, CreateEventForm, BookingForm
from . import db, app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import login_required, current_user

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route('/<id>')
def show(id):
    event = db.session.scalar(
        db.select(Event).where(Event.id == id))
    # create the comment form
    form = CommentForm()
    form2 = BookingForm()
    return render_template('destinations/show.html', event=event, form=form, form2=form2)

@destbp.route('/user-bookings')
@login_required
def bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id)
    events = Event.query.all()
    commentForm = CommentForm()
    return render_template('destinations/user-bookings.html', bookings=bookings, event=events, form=commentForm)

@destbp.route('/create-events', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateEventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(name=form.name.data,
                      status=form.status.data,
                      type=form.type.data,

                      date=form.date.data,
                      time=form.time.data,
                      duration=form.duration.data,

                      description=form.description.data,
                      image=db_file_path,

                      ticket_cost=form.ticket_cost.data,
                      total_tickets=form.total_tickets.data,

                      user_id=current_user.id)
        db.session.add(event)

        db.session.commit()
        flash('Event has been created', 'success')
        return redirect(url_for('destination.show', id=event.id))
    return render_template('destinations/create-event.html', form=form)

@destbp.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    events = Event.query.all()
    return render_template('destinations/events.html', event=events)

@destbp.route('/book/<current_id>', methods=['GET', 'POST'])
@login_required
def book(current_id):
    event = Event.query.filter_by(id=current_id).first()
    tickets = Booking.query.count()
    bookingForm = BookingForm()
    if bookingForm.validate_on_submit():
        if int(bookingForm.quantity.data) > event.total_tickets:
            flash('Number of tickets exceeds available tickets', 'danger')
            return redirect(url_for('event.book', id=event.id))
        else:
            booking = Booking(quantity=bookingForm.quantity.data,
                              user_id=current_user.id,
                              event_id=event.id,
                              price=event.ticket_cost * int(bookingForm.quantity.data),
                              purchase_at=datetime.now())
            db.session.add(booking)
            db.session.commit()
            flash('Booking has been confirmed', 'success')
            return redirect(url_for('destination.show', id=current_id))
    #return render_template('bookings.html', event=event, form=bookingForm, tickets=tickets)

def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename

    # upload file
    upload_dir = os.path.join(app.root_path, 'static', 'img', 'event')
    
    # create the upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)

    upload_path = os.path.join(upload_dir, filename)
    fp.save(upload_path)

    # store relative path in DB
    db_upload_path = '/static/img/event/' + secure_filename(filename)
    return db_upload_path

@destbp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(event):
    form = CommentForm()
    # get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == event))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(
            text=form.text.data,
            user_id=current_user.id,
            event_id=event.id,
        )
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        flash('Your comment has been added', 'success')
        # print('Your comment has been added', 'success')
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=event.id))