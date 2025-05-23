import sqlite3
db=sqlite3.connect('db.db')
db.execute('create table if not exists USERS(USER,PASSWORD,CURRENT)')
db.execute('create table if not exists TABLES(AREA,TABLES integer)')
db.execute('create table if not exists CATEGORIES(CATEGORY)')
db.execute('create table if not exists PRODUCTS(CATEGORY,PRODUCT,PRICE float)')
db.execute('create table if not exists ORDERS(AREA,SEAT integer,PRODUCT,QUANTITY integer,PRICE float)')
db.close()
from flet import *
from flet_route import Routing,path
from pages.LOGIN import Login
from pages.HOME import Home
def main(page:Page):
    app_routes=[path(url='/',view=Login,clear=True),
                path(url='/HOME',view=Home,clear=True),
                path(url='/LOGIN',view=Login,clear=True)]
    Routing(page=page,app_routes=app_routes)
    page.go(page.route)
app(main)