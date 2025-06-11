from django.contrib import admin

# Register your models here.
from roadtrip.models import PlaceModel,RequestModel,RegistrationModel,TourModel,MessageModel,WayPointsModel

admin.site.register(RegistrationModel)
admin.site.register(RequestModel)
admin.site.register(TourModel)
admin.site.register(MessageModel)
admin.site.register(WayPointsModel)
admin.site.register(PlaceModel)




