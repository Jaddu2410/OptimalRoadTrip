import datetime

from roadtrip.models import PlaceModel,TourModel,MessageModel,RequestModel,RegistrationModel,WayPointsModel
from roadtrip.service import findbestroute
from roadtrip.forms import PlaceForm,LoginForm,TourForm,RegistrationForm,UpdateProfileForm
from django.shortcuts import render
from django.db.models import Q

def registration(request):

    if request.method == "POST":

        registrationForm = RegistrationForm(request.POST,request.FILES)

        if registrationForm.is_valid():

            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.email = registrationForm.cleaned_data["email"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.address = registrationForm.cleaned_data["address"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]

            user = RegistrationModel.objects.filter(username=regModel.username).first()

            if user is not None:
                return render(request, 'registration.html', {"message": "User All Ready Exist"})
            else:
                regModel.save()
                return render(request, 'index.html', locals())
        else:
            return render(request, 'registration.html', {"message": "Please Fill Form Data"})
    else:
        return render(request, 'registration.html', {"message": "Invalid Request"})

def login(request):

    if request.method == "GET":

        loginForm = LoginForm(request.GET)

        if loginForm.is_valid():

            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]

            print(uname,upass)

            if uname == "admin" and upass == "admin":
                print("in if")
                request.session['username'] = "admin"
                request.session['role'] = "admin"
                return render(request, "tours.html", {"tours": TourModel.objects.all()})
            else:
                print("in else")
                user = RegistrationModel.objects.filter(username=uname, password=upass).first()
                if user is not None:
                    request.session['username'] = uname
                    request.session['role'] = "user"
                    return render(request, "tours.html", {"tours": TourModel.objects.all()})
                else:
                    return render(request, 'index.html', {"message": "Invalid username or Password"})
        else:
            return render(request, 'index.html', {"message": "Please Enter Username and Password"})
    else:
        return render(request, 'index.html', {"message": "Invalid Request"})

def viewprofile(request):
    user=RegistrationModel.objects.get(username=request.session['username'])
    return render(request, 'viewprofile.html',{"profile": user})

def updateprofile(request):

    if request.method == "POST":

        updateProfileForm = UpdateProfileForm(request.POST)

        if updateProfileForm.is_valid():

            email = updateProfileForm.cleaned_data["email"]
            mobile = updateProfileForm.cleaned_data["mobile"]
            address = updateProfileForm.cleaned_data["address"]
            password = updateProfileForm.cleaned_data["password"]
            RegistrationModel.objects.filter(username=request.session['username']).update(email=email,mobile=mobile,address=address,password=password)

    user = RegistrationModel.objects.get(username=request.session['username'])
    return render(request, 'viewprofile.html', {"profile":user})

def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request, 'index.html', {})

#==============================================================================

def addplace(request):

    if request.method == "POST":

        placeForm = PlaceForm(request.POST,request.FILES)

        print("in place form")

        if placeForm.is_valid():

            placeModel = PlaceModel()
            placeModel.name = placeForm.cleaned_data["name"]
            placeModel.description = placeForm.cleaned_data["description"]
            placeModel.image = placeForm.cleaned_data["image"]
            placeModel.lat = placeForm.cleaned_data["lat"]
            placeModel.long = placeForm.cleaned_data["long"]
            placeModel.address = placeForm.cleaned_data["address"]

            placeModel.save()

            places = []

            for place in PlaceModel.objects.all():
                place.image = str(place.image).split("/")[1]
                places.append(place)

            return render(request, 'places.html', {"places":places})
        else:
            return render(request, 'addplace.html', {"message": "in valid data"})
    else:
        return render(request, 'addplace.html', {"message": "in valid request"})

def viewplaces(request):

    places=[]

    for place in PlaceModel.objects.all():
        place.image = str(place.image).split("/")[1]
        places.append(place)

    return render(request, "places.html", {"places":places})

def deleteplace(request):
    place=request.GET['placeid']
    PlaceModel.objects.get(id=place).delete()
    WayPointsModel.objects.filter(placeid=place).delete()
    return render(request, 'places.html', {'places': PlaceModel.objects.all()})

#=====================================================================================
def addTour(request):

    places = []

    for place in PlaceModel.objects.all():
        place.image = str(place.image).split("/")[1]
        places.append(place)


    print(len(places))

    return render(request, "addtour.html", {"places":places})

def addTourAction(request):

    tourForm = TourForm(request.POST, request.FILES)

    if tourForm.is_valid():

        name = tourForm.cleaned_data['name']
        waypoints =request.POST.getlist('waypoints')
        startdateofjourney =tourForm.cleaned_data['startdateofjourney']
        enddateofjourney = tourForm.cleaned_data['enddateofjourney']
        price = tourForm.cleaned_data['price']
        travelon = tourForm.cleaned_data['travelon']
        contact = tourForm.cleaned_data['contact']
        traveltype = tourForm.cleaned_data['traveltype']

        TourModel(name=name, startdateofjourney=startdateofjourney, enddateofjourney=enddateofjourney, price=price,
                  traveltype=traveltype, travelon=travelon, contact=contact).save()
        tour = TourModel.objects.latest('id')
        for waypoint in waypoints:
            place=PlaceModel.objects.filter(id=waypoint).first()
            WayPointsModel(tourid=tour.id,lat=place.lat,long=place.long,placeid=place.id).save()

        return render(request, "tours.html", {"tours":TourModel.objects.all()})
    else:
        return render(request, 'tours.html.html', {"message": "in valid request"})

def viewtours(request):
    return render(request, "tours.html", {"tours":TourModel.objects.all()})

def viewtourplaces(request):

    tourid=request.GET['tourid']

    places = []

    for waypoint in WayPointsModel.objects.all():
        if waypoint.tourid==tourid:
            place=PlaceModel.objects.get(id=waypoint.placeid)
            place.image = str(place.image).split("/")[1]
            places.append(place)

    return render(request, "places.html", {"places": places})

def searchtour(request):
    return render(request, "tours.html", {"tours": TourModel.objects.filter(traveltype=request.GET['tourtype'])})

def deletetour(request):
    tour_id = request.GET['tour']
    TourModel.objects.get(id=tour_id).delete()
    WayPointsModel.objects.filter(tourid=tour_id).delete()
    return render(request, "tours.html", {"tours": TourModel.objects.all()})
#===============================================================================================

def predictbestpath(request):

    city_coordinates=dict()
    tour_id = request.GET['tour']

    i=0

    for point in WayPointsModel.objects.all():
        if point.tourid==tour_id:
            city_coordinates.update({i: [float(point.lat),float(point.long)]})
            i=i+1

    print(city_coordinates)
    result = findbestroute(city_coordinates)

    finalresult =list()
    for res in result:
        finalresult.append(city_coordinates[res])

    start=str(finalresult[0][0])+","+str(finalresult[0][1])
    end=finalresult[len(finalresult)-1]
    end=str(end[0])+","+str(end[1])

    del finalresult[-1]
    del finalresult[0]

    waypoints=list()
    for res in finalresult:
        waypoints.append(str(res[0])+","+str(res[1]))

    return render(request,"drawwaypoints.html",{"waypoints":waypoints,"start":start,"end":end})


#===================================================================================================

def addmessage(request):
    MessageModel(message=request.GET['message'],datetime=datetime.datetime.now(),username=request.session['username'],type="sent").save()

    if request.session['username']=="admin":
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(~Q(type="inbox"))})
    else:
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(username=request.session['username'])})

def replymessage(request):
    return render(request, 'reply.html', {"user":request.GET['userid']})

def postreply(request):

    MessageModel(message=request.GET['message'], datetime=datetime.datetime.now(), username=request.GET['userid'],
                 type="inbox").save()

    if request.session['username']=="admin":
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(~Q(type="inbox"))})
    else:
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(username=request.session['username'])})

def viewmessages(request):

    if request.session['username']=="admin":
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(~Q(type="inbox"))})
    else:
        return render(request, "messages.html",
                      {"messages": MessageModel.objects.filter(username=request.session['username'])})


def deletemessage(request):
    message_id = request.GET['message']
    MessageModel.objects.get(id=message_id).delete()
    return render(request, "messages.html", {"messages":MessageModel.objects.filter(username=request.session['username'])})


#===================================================================================================

def requesttour(request):
    return render(request, 'request.html', {"tour":request.GET['tour']})

def viewtourrequests(request):

    tour=request.GET['tour']
    users=[]

    for tourrequest in RequestModel.objects.filter(tourid=tour):
        user=RegistrationModel.objects.get(username=tourrequest.userid)
        user.description=tourrequest.description
        users.append(user)

    return render(request, 'viewtourrequests.html', {"users":users})

def registertour(request):

    tour=request.GET['tour']
    description=request.GET['description']

    RequestModel(userid=request.session['username'],tourid=tour,description=description,requestdate=datetime.datetime.now()).save()
    return render(request, "tours.html", {"tours":TourModel.objects.all()})