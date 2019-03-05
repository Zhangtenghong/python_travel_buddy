from django.db import models

class Users(models.Model):
  first_name=models.CharField(max_length=100)
  last_name=models.CharField(max_length=100)
  email=models.CharField(max_length=100)
  password=models.CharField(max_length=255)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

class Trips(models.Model):
  destination=models.CharField(max_length=225)
  start_date=models.CharField(max_length=100)
  end_date=models.CharField(max_length=100)
  plan=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  created_by=models.ForeignKey(Users, related_name="trips_created", null=True)
  accepted_by=models.ManyToManyField(Users, related_name="trips_accepted", null=True)
