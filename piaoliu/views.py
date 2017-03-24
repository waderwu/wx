from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from piaoliu.models import User , Book , BorrowBook

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = search_form(request.POST)
        if form.is_valid():
            bookName = form.cleaned_data['keyword']
            books = Book.objects.filter(bookName=bookName)
            borrows = BorrowBook.objects.filter(currentBook__bookName=bookName,actualBackDate__isnull=True)
            '''
            for book in books:
                borrow = book.borrowbook_set.all().filter(actualBackDate='')
                if not borrow:
                    borrows = borrow
            '''
            form = search_form()
            if not books:
                return render(
                request,
                'index.html',
                {
                    'warning':'不好意思现在没有这本书',
                    'form':form,
                }
            )
            return render(
                request,
                'index.html',
                {
                    'books':books,
                    'form':form,
                    'borrows':borrows,
                }
            )
        else:
            form = search_form()
            return HttpResponseRedirect('/')
    else:
        form = search_form()
        return render(request ,'index.html',
    {
        'welcome':'nihao,i am moban',
        'form':form,
    }
                      )
#出现了no such table
#解决方法 python manage.py migrate --run-syncdb
def register(request):
    name = request.GET['name']
    userid = request.GET['userid']
    banji = request.GET['banji']
    xuehao = request.GET['xuehao']
    phoneNumber = request.GET['phoneNumber']
    email = request.GET['email']
    wechat = request.GET['wechat']
    yonghu = User.objects.create(name=name,userid=userid,banji=banji,xuehao=xuehao,phoneNumber=phoneNumber,email=email,wechat=wechat)
    yonghu.save()
    return HttpResponse("success")


class search_form(forms.Form):
    keyword = forms.CharField(max_length=50)
