from django.contrib import admin

from  .models import Author, Book, Course, Student, Topic, HashKey
# Register your models here.

class BookInline(admin.TabularInline):
    model= Book

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

class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]

    list_display = ('firstname', 'lastname', 'birthdate','city')
    list_display_links = ('firstname','lastname')
    search_fields = ('firstname','lastname')
    fields = ('firstname', 'lastname', 'birthdate','city')
    list_filter = ('birthdate','city')
    view_on_site = True
    ordering = ['firstname', 'lastname']

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        StudentCourseInline,
    ]

    list_display = ('course_no','title', 'textbook')
    list_display_links = ('course_no',)
    search_fields = ('course_no',)
    fields = ('course_no', 'title', 'textbook')
    list_filter = ('textbook',)
    view_on_site = True
    ordering = ['course_no']

def make_intro_course(modeladmin, request, queryset):
    queryset.update(intro_course=True)
make_intro_course.short_description = "Mark selected topic(s) as introductory level course"

def make_not_intro_course(modeladmin, request, queryset):
    queryset.update(intro_course=False)
make_not_intro_course.short_description = "Mark selected book(s) as not introductory level course"

class TopicAdmin(admin.ModelAdmin):

    list_display = ('subject', 'intro_course', 'time','num_responses','avg_age')
    list_display_links = ('subject',)
    search_fields = ('subject',)
    fields = ('subject', 'intro_course', 'time','num_responses','avg_age')
    list_filter = ('intro_course','time')
    view_on_site = True
    ordering = ['num_responses',]
    actions = [make_intro_course,make_not_intro_course]

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(HashKey)
