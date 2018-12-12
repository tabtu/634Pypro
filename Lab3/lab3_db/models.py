from django.db import models

# Create your tests here.

from django.contrib.auth.models import User

# Updated by Tab Tu, May.16.2017

class Author(models.Model):
    CITY_CHOICE = (
        (' ', '---'),
        ('T', 'Toronto'),
        ('W', 'Windsor'),
    )
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    #age = models.IntegerField()
    city = models.CharField(max_length=20, choices=CITY_CHOICE, default='---')
    def __str__(self):
        return self.firstname + ' ' + self.lastname

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    in_stock = models.BooleanField(default=True)
    numpages = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class Student(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'), # First value is stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    age = models.IntegerField()
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Vian(models.Model):
    hobby = models.CharField(max_length=50)

class Course(models.Model):
    course_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    textbook = models.ForeignKey(Book)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return "#" + self.course_no + ": " + self.title