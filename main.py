import sqlite3,os
if not os.path.isdir('images'):os.mkdir('images')
db=sqlite3.connect('db.db')
db.execute('create table if not exists USERS(USER,PASSWORD)')
db.execute('create table if not exists TABLES(AREA,TABLES integer)')
db.execute('create table if not exists PRODUCTS(CATEGORY,PRODUCT,PRICE float,INFO,IMAGE)')
db.execute('create table if not exists WORKING(AREA,TABLE_ integer,QUANTITY integer,PRODUCT,PARTIAL float)')
db.close()
from flet import *
from pages.LOGIN import login_view
from pages.HOME import home_view
from pages.EDITOR import editor_view
def main(page: Page):
    page.theme_mode = 'DARK'
    page.window.full_screen = True
    picker=FilePicker()
    page.overlay.append(picker)
    def route_to(route):
        page.clean()
        if route=='/':page.add(login_view(page))
        elif route == '/LOGIN':page.add(login_view(page))
        elif route == '/HOME':page.add(home_view(page))
        elif route == '/EDITOR':page.add(editor_view(page,picker))
        page.update()
    page.on_route_change = lambda e: route_to(e.route)
    page.go('/LOGIN')
app(main,'images')