from django.contrib import admin
from  .models import Author, Book, Course, Student, Topic
# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Topic)

class BookAdmin(admin.ModelAdmin)
    title
    author
    number of pages
    in_stock status
