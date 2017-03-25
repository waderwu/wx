from django.core.mail import send_mail

def back_notice(jieyue):
    user = jieyue.currentUser.user
    name = user.username
    email = user.email
    book = jieyue.currentBook
    bookname = book.bookName
    shoudback = jieyue.shouldBackDate().strftime('%Y-%m-%d')
    message = '%s同学你好，你借阅的图书《%s》，应该在%s归还，看完之后请及时归还' % (name, bookname, shoudback)
    send_mail('图书漂流活动——还书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )


def order_notice(yuyue):
    user = yuyue.user.user
    name = user.username
    email = user.email
    book = yuyue.book
    bookname = book.bookName
    orderdate = yuyue.orderDate.strftime('%Y-%m-%d')
    message = '%s同学你好，你在%s预约的图书《%s》，已经还回来了，请及时到3-102来取' % (name, orderdate, bookname)
    send_mail('图书漂流活动——预约书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )


def borrow_notice(borrow):
    user = borrow.currentUSer.user
    name = user.username
    email = user.email
    book = borrow.currentBook
    bookname = book.bookName
    borrowDate = borrow.borrowDate.strftime()
    shouldback = borrow.shouldBackDate().strftime()
    message = '%s同学你好，你在%s借了图书《%s》，最迟需要在%s归还图书' % (name, borrowDate, bookname,shouldback)
    send_mail('图书漂流活动——借书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )

def have_back_notice(borrow):
    user = borrow.currentUSer.user
    name = user.username
    email = user.email
    book = borrow.currentBook
    bookname = book.bookName
    message = '%s同学你好，你在借的图书《%s》，已经归还图书' % (name,bookname)
    send_mail('图书漂流活动——借书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )
