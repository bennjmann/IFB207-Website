from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Comment, Event, Booking
from .forms import CommentForm, EventForm, BookingForm
from . import db, app
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_login import login_required, current_user

destbp = Blueprint('destination', __name__, url_prefix='/destinations')


@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(
        db.select(Event).where(Event.id == id))
    # create the comment form
    form = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=form)


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
    eventForm = EventForm()
    if eventForm.validate_on_submit():
        db_file_path = check_upload_file(eventForm)
        event = Event(name=eventForm.event_name.data,
                      status=eventForm.status.data,
                      type=eventForm.type.data,

                      date=eventForm.date.data,
                      time=eventForm.time.data,
                      duration=eventForm.duration.data,

                      description=eventForm.description.data,
                      image=db_file_path,

                      ticket_cost=eventForm.ticket_cost.data,
                      total_tickets=eventForm.total_tickets.data,

                      user_id=current_user.id)
        db.session.add(event)

        db.session.commit()
        return redirect(url_for('event.create-event'))
    return render_template('destinations/create-event.html', form=eventForm)


@destbp.route('/events', methods=['GET', 'POST'])
@login_required
def events():
    events = Event.query.all()
    return render_template('destinations/events.html', event=events)

@destbp.route('/book/<id>', methods=['GET', 'POST'])
@login_required
def book(id):
    event = Event.query.filter_by(event_id=id).first()
    tickets = Booking.query.count()
    bookingForm = BookingForm()
    if bookingForm.validate_on_submit():
        if int(bookingForm.quantity.data) > event.total_tickets:
            flash('Number of tickets exceeds available tickets', 'danger')
            return redirect(url_for('event.book', id=event.event_id))
        else:
            booking = Booking(quantity=bookingForm.quantity.data,
                              user_id=current_user.id,
                              event_id=event.event_id,
                              price=event.ticket_cost * int(bookingForm.quantity.data),
                              purchase_at=datetime.now())
            db.session.add(booking)
            db.session.commit()
            flash('Booking has been confirmed', 'success')
            return redirect(url_for('event.bookings'))
    return render_template('destinations/bookings.html', event=event, form=bookingForm, tickets=tickets)

def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store image file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, 'static/image', secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/event/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path

@destbp.route('/<event>/comment', methods=['GET', 'POST'])
@login_required
def comment(destination):
    form = CommentForm()
    # get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Event).where(Event.id == destination))
    if form.validate_on_submit():
        # read the comment from the form
        comment = Comment(text=form.text.data, 
                          destination=destination,
                          user=current_user)
        # here the back-referencing works - comment.destination is set
        # and the link is created
        db.session.add(comment)
        db.session.commit()

        # flashing a message which needs to be handled by the html
        flash('Your comment has been added', 'success')
        # print('Your comment has been added', 'success')
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=destination.id))