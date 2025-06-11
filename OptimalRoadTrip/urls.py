from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from roadtrip.views import registration, viewprofile, updateprofile, logout, addplace, viewplaces, deleteplace, \
    viewtourplaces, addTour, addTourAction, viewtours, deletetour, searchtour, addmessage, viewmessages, deletemessage, \
    replymessage, postreply, requesttour, registertour, viewtourrequests, predictbestpath, login

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='login'),
    path('login/', TemplateView.as_view(template_name='index.html'), name='login'),
    path('loginaction/',login, name='loginaction'),

    path('registration/', TemplateView.as_view(template_name='registration.html'), name='registration'),
    path('regaction/', registration, name='regaction'),

    path('viewprofile/',viewprofile,name='transactions'),
    path('updateprofile/',updateprofile,name='transactions'),

    path('logout/',logout,name='logout'),

    path('addplace/',TemplateView.as_view(template_name = 'addplace.html'),name='add place'),
    path('addplaceaction/',addplace,name='add place'),
    path('viewplaces/',viewplaces,name='view places'),
    path('deleteplace/',deleteplace,name='delete place'),
    path('viewtourplaces/',viewtourplaces,name='delete place'),

    path('addtour/',addTour,name='add tour'),
    path('addtouraction/',addTourAction,name='add tour action'),
    path('viewtours/',viewtours,name='view tour'),
    path('deletetour/',deletetour,name='delete tour'),
    path('searchtour/',searchtour,name='search tour'),

    path('sendmessage/',TemplateView.as_view(template_name='sendmessage.html'), name='add message'),
    path('addmessage/',addmessage, name='add message'),
    path('viewmessages/',viewmessages, name='view message'),
    path('deletemessage/', deletemessage, name='delete message'),

    path('replymessage/', replymessage, name='add message'),
    path('postreply/',postreply, name='view message'),

    path('requesttour/',requesttour, name='add message'),
    path('registertour/',registertour, name='view message'),
    path('viewtourrequests/',viewtourrequests, name='view message'),

    path('predictbestpath/',predictbestpath, name='search tour'),
]
