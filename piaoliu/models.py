from django.db import models
from datetime import timedelta

# Create your models here.
class User(models.Model):
    userid = models.CharField(max_length=30)
    banji = models.CharField(max_length=30)
    xuehao = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    wechat = models.CharField(max_length=30)
    #可以在admin，BorrowBook新建的时候，显示出姓名
    def __str__(self):
        return self.name

class Book (models.Model):
    bookName = models.CharField(max_length=30)
    #一本书所花费的时间 类型是时间间隔
    length = models.IntegerField(default=30)
    description = models.TextField(max_length=200)
    isbn = models.CharField(max_length=30)
    #0代表可以外借 1 代表已经借出去了
    state = models.IntegerField(default=0)
    def __str__(self):
        return self.bookName

    def save(self,*args,**kwargs):
        super(Book,self).save(*args,**kwargs)
        instance = douban.objects.create(isbn=self.isbn,subjectId='12345',recommendBook='baiyexing')
        instance.save()

class BorrowBook(models.Model):
    currentUser = models.ForeignKey(User)
    currentBook = models.ForeignKey(Book)
    #借阅日期
    borrowDate = models.DateField(auto_now_add=True)
    #实际归还日期
    actualBackDate = models.DateField(blank = True,null = True)
    #
    def shouldBackDate(self):
        return self.borrowDate +timedelta( days = self.currentBook.length)

class douban(models.Model):
    isbn = models.CharField(max_length=30)
    subjectId = models.CharField(max_length=30)
    recommendBook  = models.TextField(max_length=200)



