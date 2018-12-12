from django.contrib import admin
from .models import Author, Book, Student, Course, Vian

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Vian)