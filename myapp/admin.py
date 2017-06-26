from django.contrib import admin

from  .models import Author, Book, Course, Student, Topic
# Register your models here.

class CourseInline(admin.TabularInline):
     model = Course

class StudentCourseInline(admin.StackedInline):
     model = Student.student.through
     extra = 5

def make_in_stock(modeladmin, request, queryset):
    queryset.update(in_stock=True)
make_in_stock.short_description = "Mark selected book(s) as in stock"

def make_not_in_stock(modeladmin, request, queryset):
    queryset.update(in_stock=False)
make_not_in_stock.short_description = "Mark selected book(s) as out of stock"

class BookAdmin(admin.ModelAdmin):
    inlines=[
        CourseInline,
    ]
    list_display=('title','author','numpages','in_stock','colored_title')
    list_display_links = ('title','author')
    search_fields = ('title',)
    fields=('title','author','numpages','in_stock')
    list_filter=('in_stock',)
    view_on_site = True
    ordering = ['title']
    actions = [make_in_stock,make_not_in_stock]


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        StudentCourseInline,
    ]

    list_display = ('first_name', 'last_name', 'get_courses')
    list_display_links = ('first_name','last_name')
    search_fields = ('first_name','last_name')
    fields = ('first_name', 'last_name','address','city','age','province','student')
    list_filter = ('province','city')
    view_on_site = True
    ordering = ['first_name', 'last_name']


admin.site.register(Author)
admin.site.register(Book,BookAdmin)
admin.site.register(Course)
admin.site.register(Student,StudentAdmin)
admin.site.register(Topic)


