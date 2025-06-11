from django.forms import Form, CharField, PasswordInput, FileField

class RegistrationForm(Form):
    username = CharField(max_length=50)
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=50)

class UpdateProfileForm(Form):
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=50)

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class PlaceForm(Form):

    name = CharField(max_length=60)
    description = CharField(max_length=30)
    image = FileField()
    lat=CharField(max_length=100)
    long =CharField(max_length=100)
    address=CharField(max_length=500)

class TourForm(Form):
    name = CharField(max_length=60)
    waypoints = CharField(max_length=500)
    startdateofjourney = CharField(max_length=30)
    enddateofjourney = CharField(max_length=30)
    price = CharField(max_length=30)
    travelon = CharField(max_length=30)
    contact = CharField(max_length=30)
    traveltype = CharField(max_length=30)
