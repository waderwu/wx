from django.contrib import admin
from django.core import urlresolvers

from piaoliu.models import Student,Book,BorrowBook,douban,orderBook

# Register your models here.
class BorrowBookInline(admin.TabularInline):
    model = BorrowBook

class orderBookInline(admin.TabularInline):
    model = orderBook

class StudentAdmin(admin.ModelAdmin):
    def amount(self,obj):
        #user = self.model.objects.get(id=obj.id)
        #obj 就是当前一个对象的实例 borrowbook_set 就是和当前user相关的borrowbook的集合 count（）就是查询结果有多少个
        amount = obj.borrowbook_set.all().count()
        return amount

    def email(self,obj):
        email = obj.user.email
        return email

    #fields = ('id', 'userid', 'xuehao', 'banji', 'name', 'phoneNumber', 'email', 'wechat')
    list_display = ('id','userid','xuehao','banji','user','email','phoneNumber','wechat','amount')
    search_fields = ('user__username', 'xuehao','banji','phoneNumber')
    inlines = [BorrowBookInline,orderBookInline]


admin.site.register(Student,StudentAdmin)


class BookAdmin(admin.ModelAdmin):
    def borrowed(self,obj):
        book = obj.borrowbook_set.all()
        amount = book.count()
        return amount
    list_display = ('id','bookName','length','description','isbn','state','borrowed')
    #可以在book的页面编辑borrowBook
    inlines = [BorrowBookInline,orderBookInline]
admin.site.register(Book,BookAdmin)

class BorrowBookAdmin(admin.ModelAdmin):
    empty_value_display = '未还'
    list_display = ('id','currentBook','link_to_book','currentUser','link_to_user','borrowDate','actualBackDate')
    #增加之后链接到可改变的页面
    #list_display_links = ('borrowDate',)
    #增加之后变成可修改的
    #list_editable = ('currentBook','currentUser')

    #右边有了一个过滤的bar，后面的那个逗号要加
    list_filter = ('currentBook','currentUser',)
    #增加搜索框 一定要是char类型
    search_fields = ('currentUser__name','currentBook__bookName')

    #点击user可以跳转到user具体页面
    def link_to_user(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_student_change', args=[obj.currentUser.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.currentUser.user.username)

    def link_to_book(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_book_change', args=[obj.currentBook.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.currentBook.bookName)

    link_to_book.allow_tags = True
    link_to_user.allow_tags = True

admin.site.register(BorrowBook,BorrowBookAdmin)


class doubanAdmin(admin.ModelAdmin):
    list_display = ('id','isbn','subjectId','recommendBook')
    search_fields = ('isbn',)
admin.site.register(douban,doubanAdmin)

class orderBookAdmin(admin.ModelAdmin):
    list_display = ('id','user','link_to_user','book','link_to_book','orderDate','state')
    search_fields = ('user__user__username','book__bookName')
    list_filter = ('book', 'user',)

    def link_to_user(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_student_change', args=[obj.user.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.user.user.username)

    def link_to_book(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_book_change', args=[obj.book.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.book.bookName)

    link_to_book.allow_tags = True
    link_to_user.allow_tags = True

admin.site.register(orderBook,orderBookAdmin)