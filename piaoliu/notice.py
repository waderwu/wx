from django.core.mail import send_mail

def back_notice(jieyue):
    user = jieyue.currentUser.user
    name = user.username
    email = user.email
    book = jieyue.currentBook
    bookname = book.doubanxinxi.bookName
    shoudback = jieyue.shouldBackDate().strftime('%Y-%m-%d')
    message = '%s同学你好，你借阅的图书《%s》，应该在%s归还，看完之后请及时归还。\n 有问题联系waderwu@163.com' % (name, bookname, shoudback)
    send_mail('图书漂流活动——催书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )


def order_notice(yuyue):
    user = yuyue.user.user
    name = user.username
    email = user.email
    book = yuyue.book
    bookname = book.doubanxinxi.bookName
    orderdate = yuyue.orderDate.strftime('%Y-%m-%d')
    message = '%s同学你好，你在%s预约的图书《%s》，已经还回来了，请及时到3-102来取。\n 有问题联系waderwu@163.com' % (name, orderdate, bookname)
    send_mail('图书漂流活动——预约书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )


def borrow_notice(borrow):
    user = borrow.currentUser.user
    name = user.username
    email = user.email
    book = borrow.currentBook
    bookname = book.doubanxinxi.bookName
    borrowDate = borrow.borrowDate.strftime('%Y-%m-%d')
    shouldback = borrow.shouldBackDate().strftime('%Y-%m-%d')
    message = '%s同学你好，你在%s借了图书《%s》，最迟需要在%s归还图书\n 注：如果你在5分钟之内同时收到借书成功和还书成功的邮件（没有的话请忽略此注释），说明你收到了来拿预约书的通知，但是你没有来取书，系统取消了你上次预约的资格 .\n 有问题联系waderwu@163.com' % (name, borrowDate,bookname,shouldback)
    #message = '%s同学你好，你今天借了图书《%s》，最迟需要在30天后归还图书' % (name, bookname)
    send_mail('图书漂流活动——借书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )

def have_back_notice(borrow):
    user = borrow.currentUser.user
    name = user.username
    email = user.email
    book = borrow.currentBook
    bookname = book.doubanxinxi.bookName
    message = '%s同学你好，你在借的图书《%s》，已经归还。\n 如果你在5分钟之内同时收到借书成功和还书成功的邮件（没有的话请忽略此注释），说明你收到了来拿预约书的通知，但是你没有来取书，系统取消了你上次预约的资格。\n 有问题联系waderwu@163.com' % (name,bookname)
    send_mail('图书漂流活动——还书通知', message, 'yishuwang2016@163.com',
              [email], fail_silently=False, )
