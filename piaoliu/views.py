from datetime import datetime,timedelta
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from piaoliu.models import Student ,Book , BorrowBook , orderBook
from django.contrib.auth.models import User
from django.contrib import auth
#从本目录下导入
import piaoliu.forms
from piaoliu.notice import back_notice

# Create your views here.

def index(request):
    if request.method == 'POST':
        form = piaoliu.forms.search_form(request.POST)
        if form.is_valid():
            bookName = form.cleaned_data['keyword']
            books = Book.objects.filter(doubanxinxi__bookName=bookName)
            borrows = BorrowBook.objects.filter(currentBook__doubanxinxi__bookName__contains=bookName,actualBackDate__isnull=True)
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
        onshelfbooks = Book.objects.filter(state=1)

        form = piaoliu.forms.search_form()
        return render(request ,'index.html',
    {
        'form':form,
        'onshelfbooks':onshelfbooks,
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
def order(request,bookid):
    if request.user.is_authenticated:
        book = Book.objects.get(id=bookid)
        user = request.user.student
        order = orderBook.objects.create(book=book,user=user)
        order.save()
        return HttpResponseRedirect('/detail/')
    else:
        return HttpResponseRedirect('/login/')

def detail(request):
    if request.user.is_authenticated:
        user = request.user.student
        borrowbooks = BorrowBook.objects.filter(currentUser=user)
        orderbooks = orderBook.objects.filter(user=user)
        return render(request,"detail.html",{'borrowbooks':borrowbooks,"orderbooks":orderbooks})
    else:
        return HttpResponseRedirect('login/')
def check(request):
    #try:
        token = request.GET['token']
        if token=='laoshijiushiyaojiancha':
            jieyues = BorrowBook.objects.all().filter(actualBackDate__isnull=True)
            for jieyue in jieyues:
                #type is <class 'datetime.date'> but datetime.today() is <class 'datetime.datetime'>
                today = datetime.today().date()
                #dela = jieyue.shouldBackDate()-today
                #print (type(dela))
                if (jieyue.shouldBackDate()>today-timedelta(days=3)):
                    back_notice(jieyue)

            return HttpResponse('ok')
        return HttpResponse('error')
    #except:
    #   return HttpResponse('forbidden')


