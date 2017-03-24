from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from piaoliu.models import Student ,Book , BorrowBook
from django.contrib.auth.models import User
from django.contrib import auth
import piaoliu.forms

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = piaoliu.forms.search_form(request.POST)
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
            form = piaoliu.forms.search_form()
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
            return HttpResponseRedirect('/')
    else:
        form = piaoliu.forms.search_form()
        return render(request ,'index.html',
    {
        'welcome':'nihao,i am moban',
        'form':form,
    }
                      )
#出现了no such table
#解决方法 python manage.py migrate --run-syncdb
def register(request):
    if request.method=='POST':
        errors=[]
        form=piaoliu.forms.RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "register.html",{'form':form,'errors':errors})
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        banji = form.cleaned_data['banji']
        xuehao = form.cleaned_data['xuehao']
        wechat = form.cleaned_data['wechat']
        phoneNumber = form.cleaned_data['phoneNumber']

        password1 = form.cleaned_data['password1']
        password2= form.cleaned_data['password2']
        if password1!=password2:
            errors.append("两次输入的密码不一致!")
            return render(request, "register.html",{'form':form,'errors':errors})
        filterResult=User.objects.filter(username=username)
        if len(filterResult)>0:
           errors.append("用户名已存在")
           return render(request, "register.html",{'form':form,'errors':errors})
        user = User.objects.create_user(username,email,password1)
        user.save()
        student = Student.objects.create(user=user,xuehao=xuehao,banji=banji,wechat=wechat,phoneNumber=phoneNumber)
        #登录前需要先验证
        newUser=auth.authenticate(username=username,password=password1)
        if newUser is not None:
            auth.login(request, newUser)
            return HttpResponseRedirect("/")
    else:
        form =piaoliu.forms.RegisterForm()
        return render(request, "register.html",{'form':form,'title':'注册','year':datetime.now().year})

    return render(request, "register.html")


