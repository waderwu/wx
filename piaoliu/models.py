from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from piaoliu.notice import have_back_notice,borrow_notice,order_notice
from piaoliu.spider import get_information_by_isbn

# Create your models here.

class douban(models.Model):
    bookName = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    isbn = models.CharField(max_length=30)
    url = models.CharField(max_length=30)
    rating = models.FloatField()
    #subjectId = models.CharField(max_length=30,blank=True,null=True)
    #recommendBook  = models.TextField(max_length=200)
    # 一本书所花费的时间 类型是整数
    length = models.IntegerField(default=30,blank=True,null=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.isbn

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userid = models.CharField(max_length=30,blank=True,null=True)
    banji = models.CharField(max_length=30)
    xuehao = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=30)
    wechat = models.CharField(max_length=30,blank=True , null= True)
    #可以在admin，BorrowBook新建的时候，显示出姓名
    def __str__(self):
        return self.user.username

    def email(self):
        email = self.user.email
        return email

    def amount(self):
        amount = self.borrowbook_set.all().count()
        return amount


class Book (models.Model):
    isbn = models.CharField(max_length=30)
    #1代表可以外借 0代表已经借出去了
    state = models.IntegerField(default=1)
    doubanxinxi =models.ForeignKey(douban,blank=True,null=True)
    def __str__(self):
        return self.bookName()+"  id:"+str(self.id)

    def status(self):
        if self.state ==1:
            return "在架"
        elif self.state ==0:
            return "已外借"
        elif self.state ==2:
            return "被预约中"
        else:
            return "错误"

    def bookName(self):
        return self.doubanxinxi.bookName
    def length(self):
        return self.doubanxinxi.length

    def borrowed(self):
        book = self.borrowbook_set.all()
        amount = book.count()
        return amount

    def save(self,*args,**kwargs):
        super(Book,self).save(*args,**kwargs)
        #如果不存在对应的isbn，就自动创建一个相对应的
        if not douban.objects.filter(isbn=self.isbn):
            (author,bookName,rating,description,url) = get_information_by_isbn(self.isbn)
            url = url.replace('\\','')
            instance = douban.objects.create(isbn=self.isbn,author=author,bookName=bookName,rating=rating,description=description,url=url)
            #创建book时 先选择id为1的doubanxinxi ，然后再改回成实例
            self.doubanxinxi = instance
            self.save()


class BorrowBook(models.Model):
    currentUser = models.ForeignKey(Student)
    currentBook = models.ForeignKey(Book)
    #借阅日期
    borrowDate = models.DateField(auto_now_add=True)
    #实际归还日期
    actualBackDate = models.DateField(blank = True,null = True)
    #
    def shouldBackDate(self):
        return self.borrowDate +timedelta( days = self.currentBook.doubanxinxi.length)

    def status(self):
        if self.actualBackDate ==None:
            return "未还"
        else:
            return "已还"


    def save(self,*args,**kwargs):
        #如果原来acctural date is null 现在不是空 发邮件通知已经还了
        flag = False
        if self.pk is None:
            flag=True
        else:
            borrow = BorrowBook.objects.get(pk=self.pk)
            old_actual_date = borrow.actualBackDate
            if old_actual_date==None and self.actualBackDate !=None:
                have_back_notice(borrow)
                book = self.currentBook
                #处理预约的情况
                order = orderBook.objects.filter(book=book,state=0).order_by('id')[0]
                if order :
                    order_notice(order)
                    order.state = 1
                    order.save()
                    book.state = 2
                    book.save()
                else:
                    book.state = 1
                    book.save()


        # 还是按照原先的方式保存
        super(BorrowBook, self).save(*args, **kwargs)
        #如果是首次被建立，发邮件通知借了书，书的状态变为0 ，即已经外借
        if flag:
            borrow_notice(self)
            book = self.currentBook
            book.state = 0
            book.save()
            #如果已经通知预约了，更改预约状态为2,即已经拿书
            order = orderBook.objects.filter(book=book,user=self.currentUser,state=1)[0]
            if order:
                order.state = 2
                order.save()

class orderBook(models.Model):
    orderDate = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book)
    user = models.ForeignKey(Student)
    # 是否已经通知 0 代表未通知 1代表已经通知，2 代表已经拿书了
    state = models.IntegerField(default=0)
    def status(self):
        if self.state == 0 :
            return "未通知"
        elif self.state == 1:
            return "已通知"
        elif self.state ==2 :
            return "已拿书"



