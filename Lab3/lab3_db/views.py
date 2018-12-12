from django.http import HttpResponse
from lab3_db.models import Author,Book,Course

# def index(request):
#     book_list = Book.objects.order_by('title')
#     context = {'book_list': book_list}
#     return render(request, "index.html", context)
#
# def detail(request):
#     book = Book.objects.get(request)
#     return book

def index(request):
    courselist = Book.objects.all() [:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of courses: ' + '</p>'
    response.write(heading1)
    for course in courselist:
        para = '<p>' + str(course) + '</p>'
        response.write(para)
    return response