#/usr/bin/python3 
import requests 
token = 'laoshijiushiyaojiancha'
r = requests.get('http://127.0.0.1:8000/check/?token=%s'%token)
