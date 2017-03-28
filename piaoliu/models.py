from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from piaoliu.notice import have_back_notice,borrow_notice

# Create your models here.
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


class Book (models.Model):
    bookName = models.CharField(max_length=30)
    #一本书所花费的时间 类型是时间间隔
    length = models.IntegerField(default=30)
    description = models.TextField(max_length=200)
    isbn = models.CharField(max_length=30)
    #1代表可以外借 0代表已经借出去了
    state = models.IntegerField(default=1)
    def __str__(self):
        return self.bookName+"  id:"+str(self.id)

    def status(self):
        if self.state ==1:
            return "在架"
        elif self.state ==0:
            return "已外借"
        elif self.state ==2:
            return "被预约中"
        else:
            return "错误"

    def save(self,*args,**kwargs):
        super(Book,self).save(*args,**kwargs)
        #如果不存在对应的isbn，就自动创建一个相对应的
        if not douban.objects.filter(isbn=self.isbn):
            instance = douban.objects.create(isbn=self.isbn,subjectId='12345',recommendBook='baiyexing')
            instance.save()


class BorrowBook(models.Model):
    currentUser = models.ForeignKey(Student)
    currentBook = models.ForeignKey(Book)
    #借阅日期
    borrowDate = models.DateField(auto_now_add=True)
    #实际归还日期
    actualBackDate = models.DateField(blank = True,null = True)
    #
    def shouldBackDate(self):
        return self.borrowDate +timedelta( days = self.currentBook.length)

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


class douban(models.Model):
    isbn = models.CharField(max_length=30)
    subjectId = models.CharField(max_length=30,blank=True,null=True)
    recommendBook  = models.TextField(max_length=200)

class orderBook(models.Model):
    orderDate = models.DateField(auto_now_add=True)
    book = models.ForeignKey(Book)
    user = models.ForeignKey(Student)
    # 0代表还没有拿书，1代表已经拿书了
    state = models.CharField(max_length=10,default=0)

