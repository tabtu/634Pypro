import django
from myapp.models import Author, Book, Course, Student
import datetime

l5a = Book.objects.all()
l5b = Author.objects.all()
l5c = Course.objects.all()

l6a = Author.objects.filter(firstname = 'John')
l6b = Book.objects.filter(author__firstname = 'John')
l6c = Book.objects.filter(title__contains='Networks')
# l6d
C = Course.objects.filter(textbook__title__contains='Network')
for i in C:
    print(i.textbook)

l6e = Course.objects.filter(textbook__title = 'Python Programming')
l6f = Author.objects.filter(birthdate__gte = datetime.date(1979, 1, 1))
l6g = Author.objects.filter(birthdate__month = 1)
l6h = Course.objects.filter(textbook__author__firstname = 'Alan').filter(textbook__author__lastname = 'Jones')
l6i = Book.objects.filter(in_stock = True)
l6j = Book.objects.filter(author__firstname = 'Mary').filter(author__lastname = 'Hall')

#l6k
C = Course.objects.get(course_no = '567').textbook
A = C.author
print(A.firstname)

l6l = Student.objects.filter(student__course_no = '567')
l6m = Course.objects.filter(student__first_name = 'Josh')

# 16n
C = Course.objects.filter(student__first_name = 'Luis')
for i in C:
    print(i.textbook.title)

l6o = Student.objects.filter(last_name = 'James')
