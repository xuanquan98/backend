from django.db import models

# Create your models here.
class CV(models.Model):
	nameCv = models.CharField(max_length=100)
	fullName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	dateOfBirth = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	link = models.CharField(max_length=100)
	skill = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)

	def __str__( self ):
		return self.nameCv


class Auth(models.Model):
	username = models.CharField(max_length=100)
	token = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True)

	def __str__( self ):
		return self.nameCv
