from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from datetime import datetime, time, date
from time import strftime
import bcrypt
import re	 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  return render(request, 'first_app/index.html')

def register(request):
  is_valid=True
  if len(request.POST['fname'])<2: 
    is_valid=False
    messages.error(request, "First name must contain at least two characters.")
  if len(request.POST['lname'])<2:
    is_valid=False
    messages.error(request, "Last name must contain at least two characters.")
  if not EMAIL_REGEX.match(request.POST['email']): 
    is_valid=False 
    messages.error(request, "Invalid email address.")
  if len(request.POST['password'])<8:
    is_valid=False
    messages.error(request, "Password must contain at least 8 characters.")
  if request.POST['password']!=request.POST['cpassword']:
    is_valid=False
    messages.error(request, "Password and password confirmation don't match.")

  if is_valid:
    hashed_pw=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    new_user=Users.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'], email=request.POST['email'], password=hashed_pw)
    messages.success(request, "You have successfully registered. Please login.")
    print(new_user)
  
  return redirect('/')

def login(request):
  is_valid=True
  if not EMAIL_REGEX.match(request.POST['mail']): 
    is_valid=False 
    messages.error(request, "Invalid email address.")
  if len(request.POST['pwd'])<8:
    is_valid=False
    messages.error(request, "Password must contain at least 8 characters.")

  if is_valid:
    try:
      user=Users.objects.get(email=request.POST['mail'])
      if bcrypt.checkpw(request.POST['pwd'].encode(), user.password.encode()):
        request.session['user_id']=user.id
        return redirect('/dashboard')
      else:
        messages.error(request, "Email and password didn't match")
        return redirect('/')

    except Users.DoesNotExist:
      messages.error(request, "A user with this email doesn't exist. Please register.")
      return redirect('/')

  return redirect('/')

def success(request):
  if not 'user_id' in request.session:
    messages.error(request, "You need to login")
    return redirect('/')
  
  else:
    user=Users.objects.get(id=request.session["user_id"])
    context={
      'user':user,
      'your_trips':Trips.objects.filter(Q(created_by=user) | Q(accepted_by=user)),
      'other_trips':Trips.objects.exclude(Q(created_by=user) | Q(accepted_by=user)),
    }
    return render(request, 'first_app/success.html', context)

def logout(request):
  request.session.clear()
  return redirect('/')

def createtrip(request):
  return render(request, 'first_app/createtrip.html')

def submit(request):
  print(request.POST)
  d = datetime.now()
  now = d.strftime("%Y-%m-%d")
  is_valid=True

  if len(request.POST['destination'])<4: 
    is_valid=False
    messages.error(request, "A trip destination must contain at least three characters.")
  if request.POST['enddate']<request.POST['startdate']:
    is_valid=False
    messages.error(request, "You can't set the end date before start date")
  if request.POST['startdate']<now:
    is_valid=False
    messages.error(request, "You can't set the start date before now")
  if len(request.POST['plan'])<4:
    is_valid=False
    messages.error(request, "A plan must contain at least three characters.")

  if is_valid:
    print(request.POST)
    new_trip=Trips.objects.create(destination=request.POST['destination'],start_date=request.POST['startdate'], end_date=request.POST['enddate'], created_by=Users.objects.get(id=request.session["user_id"]))
    messages.success(request, "You have successfully add a trip.")
    print(new_trip)
    return redirect('/dashboard')
  
  else:
    return redirect('/trips/new')

def edit(request, id):
  context = {
    "edit_trip": Trips.objects.get(id=id)
  }
  print(Trips.objects.get(id=id))
  return render(request,'first_app/edit.html', context)

def update(request, id):
  d = datetime.now()
  now = d.strftime("%Y-%m-%d")
  is_valid=True

  if len(request.POST['destination'])<4: 
    is_valid=False
    messages.error(request, "A trip destination must contain at least three characters.")
  if request.POST['enddate']<request.POST['startdate']:
    is_valid=False
    messages.error(request, "You can't set the end date before start date")
  if request.POST['startdate']<now:
    is_valid=False
    messages.error(request, "You can't set the start date before now")
  if len(request.POST['plan'])<4:
    is_valid=False
    messages.error(request, "A plan must contain at least three characters.")

  if is_valid:
    trip_to_update=Trips.objects.get(id=id)
    trip_to_update.destination=request.POST['destination']
    trip_to_update.start_date=request.POST['startdate']
    trip_to_update.end_date=request.POST['enddate']
    trip_to_update.save()
    return redirect('/dashboard')

  else:
    return redirect(f'/edit/{id}')

def show(request, id):
  context = {
    "select_trip": Trips.objects.get(id=id),
    "others": Users.objects.filter(trips_accepted=id).exclude(id=(Trips.objects.get(id=id).created_by_id))
  }
  return render(request,'first_app/show.html', context)

def join(request, id):
  this_user=Users.objects.get(id=request.session["user_id"])
  this_trip=Trips.objects.get(id=id)
  this_trip.accepted_by.add(this_user)
  this_trip.save()
  return redirect('/dashboard')

def delete(request, id):
  this_trip=Trips.objects.get(id=id)
  this_trip.delete()
  return redirect('/dashboard')

def cancel(request, id):
  this_user=Users.objects.get(id=request.session["user_id"])
  this_trip=Trips.objects.get(id=id)
  this_user.trips_accepted.remove(this_trip)
  return redirect('/dashboard')