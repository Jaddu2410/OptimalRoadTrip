from django.db import models
from django.db.models import Model

class RegistrationModel(Model):

    username=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    address=models.CharField(max_length=50)

    class Meta:
        db_table = "registration"

class PlaceModel(Model):

    name = models.CharField(max_length=60)
    description = models.CharField(max_length=30)
    image = models.FileField(upload_to="images")
    lat=models.FloatField()
    long = models.FloatField()
    address=models.CharField(max_length=500)

    class Meta:
        db_table = "places"


class TourModel(Model):

    name = models.CharField(max_length=60)
    startdateofjourney = models.CharField(max_length=30)
    enddateofjourney = models.CharField(max_length=30)
    price = models.CharField(max_length=30)
    travelon = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    traveltype = models.CharField(max_length=30)

    class Meta:
        db_table = "tours"

class WayPointsModel(models.Model):

    tourid = models.CharField(max_length=500)
    placeid = models.CharField(max_length=500,default="")
    lat = models.CharField(max_length=60)
    long = models.CharField(max_length=60)

    class Meta:
        db_table = "waypoints"

class MessageModel(models.Model):

    message = models.CharField(max_length=500)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    username = models.CharField(max_length=60)
    type=models.CharField(max_length=60)

    class Meta:
        db_table = "messages"

class RequestModel(models.Model):

    userid = models.CharField(max_length=500)
    requestdate = models.DateTimeField(auto_now=True, blank=False, null=False)
    tourid= models.CharField(max_length=60)
    description=models.CharField(max_length=60)

    class Meta:
        db_table = "requests"