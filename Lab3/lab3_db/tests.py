from django.test import TestCase

# Create your tests here.

from lab3_db.models import Author, Book, Course, Student
import datetime

#a. List all the books in the db.
l5a = Book.objects.all()
#b. List all the authors in the db.
l5b = Author.objects.all()
#c. List all the courses in the db.
l5c = Course.objects.all()
#a. List all Authors whose first name is  ‘John’
l6a = Author.objects.filter(firstname='John')
#b. List all Books whose has an author with first name  is ‘John’
l6b = Book.objects.filter(author__firstname='John')
#c. List all Books with the word ‘Networks’ in its title.
l6c = Book.objects.filter(title__contains='Networks')
#d. List all Books that have the word ‘Networks’ in its title and are used in a course
l6d = Book.objects.filter(course__title__contains='Network')
#e. List all the Courses that use the book  'Python Programming'
l6e = Course.objects.filter(textbook__title='Python Programming')
#f. List the Authors born after 1978
l6f = Author.objects.filter(birthdate__gte=datetime.date(1979, 1, 1))
#g. List the Authors born in January
l6g = Author.objects.filter(birthdate__month=1)
#h. List the Courses that use a book written by Alan Jones
l6h = Course.objects.filter(textbook__author__firstname='Alan').filter(textbook__author__lastname='Jones')
#i. List the Books currently in stock
l6i = Book.objects.filter(in_stock=True)
#j. List the Books written by Mary Hall
l6j = Book.objects.filter(author__firstname='Mary').filter(author__lastname='Hall')
#k. Get the first name of the Author of the textbook used in course 567.
l6k = Author.objects.get(book__course__course_no=567).firstname
#l. List all students registered in course 567
l6l = Student.objects.filter(student__course_no=567)
#m. List all the courses the Josh is registered in.
l6m = Course.objects.filter(student__first_name='Josh')
#n. List the textbook used in the course that Luis is registered in
l6n = Book.objects.filter(course__student__first_name='Luis')
#o. List all students with last name ‘James’.
l6o = Student.objects.filter(last_name='James')