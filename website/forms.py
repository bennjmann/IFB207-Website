from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Length, Optional
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'png', 'jpg'}

# User Login
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[
                            InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# User Register
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[
                           Email("Please enter a valid email")])

    phone_number = IntegerField(
        "Phone Number", validators=[ Length(10), Optional() ]
    )

    address = TextAreaField(
        "House Address", validators=[Optional()]
    )

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

# User Comment
class CommentForm(FlaskForm):
    text = TextAreaField('Comment', [InputRequired()])
    submit = SubmitField('Create')

# Create Event
class CreateEventForm(FlaskForm):
    name = StringField('Event Title', validators=[InputRequired()])
    status = SelectField('Status', choices=[("Open"), ("Inactive"),("Sold Out"), ("Cancelled")], validators=[InputRequired()])
    type = SelectField('Genres', choices=[("Live"), ("Recorded"), ("Workshop"), ("Lecture")], validators=[InputRequired()])
    image = FileField('Event Image', validators=[FileRequired(message='Image Required'), FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])

    description = TextAreaField('Description', validators=[InputRequired()])

    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    time = TimeField('Start Time', validators=[InputRequired()])
    duration = IntegerField('Duration (mnts)', validators=[InputRequired()])

    ticket_cost = IntegerField('Cost Of Ticket', validators=[InputRequired()])
    total_tickets = IntegerField('Total Number Of Tickets', validators=[InputRequired()])
    
    submit = SubmitField("Create")

# Book Event
class BookingForm(FlaskForm):
    quantity = IntegerField('Number Of Tickets', validators=[InputRequired(), NumberRange(min=1)])
    submit = SubmitField('Book')
