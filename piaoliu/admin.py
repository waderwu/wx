from django.contrib import admin
from django.core import urlresolvers

from piaoliu.models import User,Book,BorrowBook,douban

# Register your models here.
class BorrowBookInline(admin.TabularInline):
    model = BorrowBook

class UserAdmin(admin.ModelAdmin):
    def amount(self,obj):
        #user = self.model.objects.get(id=obj.id)
        #obj 就是当前一个对象的实例 borrowbook_set 就是和当前user相关的borrowbook的集合 count（）就是查询结果有多少个
        amount = obj.borrowbook_set.all().count()
        return amount

    #fields = ('id', 'userid', 'xuehao', 'banji', 'name', 'phoneNumber', 'email', 'wechat')
    list_display = ('id','userid','xuehao','banji','name','phoneNumber','email','wechat','amount')
    search_fields = ('name', 'xuehao','banji','phoneNumber','userid',)
    inlines = [BorrowBookInline, ]


admin.site.register(User,UserAdmin)


class BookAdmin(admin.ModelAdmin):
    def borrowed(self,obj):
        book = obj.borrowbook_set.all()
        amount = book.count()
        return amount
    list_display = ('id','bookName','length','description','isbn','state','borrowed')
    #可以在book的页面编辑borrowBook
    inlines = [BorrowBookInline,]
admin.site.register(Book,BookAdmin)

class BorrowBookAdmin(admin.ModelAdmin):
    empty_value_display = '未还'
    list_display = ('id','currentBook','link_to_book','currentUser','link_to_uer','borrowDate','actualBackDate')
    #增加之后链接到可改变的页面
    #list_display_links = ('borrowDate',)
    #增加之后变成可修改的
    #list_editable = ('currentBook','currentUser')

    #右边有了一个过滤的bar，后面的那个逗号要加
    list_filter = ('currentBook','currentUser',)
    #增加搜索框 一定要是char类型
    search_fields = ('currentUser__name','currentBook__bookName')

    #点击user可以跳转到user具体页面
    def link_to_uer(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_user_change', args=[obj.currentUser.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.currentUser.name)

    def link_to_book(self, obj):
        link = urlresolvers.reverse('admin:piaoliu_book_change', args=[obj.currentBook.id])  # model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link, obj.currentBook.bookName)

    link_to_book.allow_tags = True
    link_to_uer.allow_tags = True

admin.site.register(BorrowBook,BorrowBookAdmin)


class doubanAdmin(admin.ModelAdmin):
    list_display = ('id','isbn','subjectId','recommendBook')
admin.site.register(douban,doubanAdmin)