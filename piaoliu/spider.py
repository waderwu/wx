import requests

def get_information_by_isbn(isbn):
    url = 'https://api.douban.com/v2/book/isbn/%s'%isbn
    r = requests.get(url)
    text = eval(r.text)
    return (text['author'],text['title'],text['rating']['average'],text['summary'],text['alt'])
