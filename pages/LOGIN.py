import sqlite3
from flet import *
from flet_route import Params,Basket
def Login(page:Page,params:Params,basket:Basket):
    def theme(e):
        if page.theme_mode=='DARK':page.theme_mode='LIGHT'
        else:page.theme_mode='DARK'
        page.update()
    def check(what):
        def confirm_areas(e):
            def delete_category(e):
                db=sqlite3.connect('db.db')
                db.execute('delete from CATEGORIES where CATEGORY=?',(e.control.text,))
                db.commit()
                column_categories.controls=[ElevatedButton(c[0],on_click=delete_category) for c in db.execute('select CATEGORY from CATEGORIES').fetchall()]
                db.close()
                page.update()
            def add_category(e):
                if category.value=='':alert.title=Text('EMPTY FIELD')
                else:
                    db=sqlite3.connect('db.db')
                    db.execute('insert into CATEGORIES(CATEGORY) values(?)',((category.value.upper()),))
                    db.commit()
                    column_categories.controls=[ElevatedButton(c[0],on_click=delete_category) for c in db.execute('select CATEGORY from CATEGORIES').fetchall()]
                    db.close()
                    alert.title=Text('CATEGORY CORRECTLY ADDED')
                    category.value=''
                page.open(alert)
                page.update()
            alert.title=Text('PLEASE CONFIRM CATEGORIES, NOW')
            page.open(alert)
            row.controls=[Text('CATEGORIES',color='orange')]
            db=sqlite3.connect('db.db')
            column_categories.controls=[ElevatedButton(c[0],on_click=delete_category) for c in db.execute('select CATEGORY from CATEGORIES').fetchall()]
            db.close()
            column.controls=[Row([column_categories],alignment=MainAxisAlignment.CENTER),
                                Divider(),
                                Row([Text('NEW CATEGORY',color='orange')],alignment=MainAxisAlignment.CENTER),
                                Row([category,ElevatedButton('ADD CATEGORY',on_click=add_category)],alignment=MainAxisAlignment.CENTER),
                                Divider(),
                                Row([ElevatedButton('CONFIRM ALL',on_click=lambda _:page.go('/HOME'))],alignment=MainAxisAlignment.CENTER)]
            page.update()
        def delete_area(e):
            db=sqlite3.connect('db.db')
            db.execute('delete from TABLES where AREA=?',(e.control.text[0],))
            db.commit()
            column_areas.controls=[ElevatedButton(area,on_click=delete_area) for area in db.execute('select * from TABLES').fetchall()]
            db.close()
            page.update()
        def add_area(e):
            db=sqlite3.connect('db.db')
            if area.value=='' or tables.value=='':alert.title=Text('EMPTY FIELD(S)')
            else:
                db.execute('insert into TABLES values(?,?)',((area.value).upper(),tables.value,))
                db.commit()
                area.value,tables.value='',''
                column_areas.controls=[ElevatedButton(area,on_click=delete_area) for area in db.execute('select * from TABLES').fetchall()]
                alert.title=Text('NEW AREA CORRECTLY ADDED')
            db.close()
            page.open(alert)
            page.update()
        db=sqlite3.connect('db.db')
        db.execute('update USERS set CURRENT=""')
        db.commit()
        if what=='login':
            if user.value=='' or pw.value=='':alert.title=Text('EMPTY FIELD(S)')
            elif db.execute('select * from USERS where USER=? and PASSWORD=?',((user.value.upper()),pw.value,)).fetchall()==[]:alert.title=Text('USERNAME A/O PASSWORD WRONG(S)')
            else:
                db.execute('update USERS set CURRENT="on"')
                db.commit()
                alert.title=Text('WELCOME BACK, '+(user.value.upper()+', PLEASE CONFIRM AREAS NOW'))
                row.controls=[Text('AREA,TABLES',color='orange')]
                current.value=db.execute('select USER from USERS where CURRENT="on"').fetchone()[0]
                column_areas.controls=[ElevatedButton(a,on_click=delete_area) for a in db.execute('select * from TABLES').fetchall()]
                column.controls=[Row([column_areas],alignment=MainAxisAlignment.CENTER),
                                 Divider(),
                                 Row([Text('NEW AREA',color='orange')],alignment=MainAxisAlignment.CENTER),
                                 Row([area,tables,ElevatedButton('ADD AREA',on_click=add_area)],alignment=MainAxisAlignment.CENTER),
                                 Divider(),
                                 Row([ElevatedButton('CONFIRM ALL',on_click=confirm_areas)],alignment=MainAxisAlignment.CENTER)]
                page.update()
        elif what=='register':
            if user.value=='' or pw.value=='' or re_pw.value=='':alert.title=Text('EMPTY FIELD(S)')
            elif db.execute('select * from USERS where USER=?',((user.value).upper(),)).fetchall()!=[]:alert.title=Text('USER ALREADY EXISTS')
            elif pw.value!=re_pw.value:alert.title=Text("PASSWORD AND CONFIRM DON'T MATCH")
            else:
                db.execute('insert into USERS values(?,?,"")',((user.value).upper(),pw.value,))
                db.commit()
                for r in row.controls:r.color='light-grey'
                column.controls=[]
                alert.title=Text('WELCOME, '+user.value)
        elif what=='delete':
            db.execute('delete from USERS where USER=?',(d_users.value,))
            db.commit()
            alert.title=Text('USER '+d_users.value+' CORRECTLY DELETED')
        db.close()
        page.open(alert)
        page.update()
    def update(e):
        for r in row.controls:
            if r.text==e:r.color='green'
            else:r.color='light.grey'
        user.value,pw.value,re_pw.value,d_users.value='','','',''
        page.update()
    def login(e):
        column.controls=[Row([Text('USERNAME:'),user],alignment=MainAxisAlignment.CENTER),
                         Row([Text('PASSWORD:'),pw],alignment=MainAxisAlignment.CENTER),
                         Row([ElevatedButton('LOGIN',on_click=lambda _:check('login'))],alignment=MainAxisAlignment.CENTER)]
        update('LOGIN')
    def register(e):
        column.controls=[Row([Text('USERNAME:'),user],alignment=MainAxisAlignment.CENTER),
                         Row([Text('PASSWORD:'),pw],alignment=MainAxisAlignment.CENTER),
                         Row([Text('CONFIRM PASSWORD:'),re_pw],alignment=MainAxisAlignment.CENTER),
                         Row([ElevatedButton('REGISTER',on_click=lambda _:check('register'))],alignment=MainAxisAlignment.CENTER)]
        update('REGISTER')
    def delete(e):
        db=sqlite3.connect('db.db')
        d_users.options=[dropdown.Option(u[0]) for u in db.execute('select USER from USERS').fetchall()]
        column.controls=[Row([d_users],alignment=MainAxisAlignment.CENTER),
                         Row([ElevatedButton('DELETE',on_click=lambda _:check('delete'))],alignment=MainAxisAlignment.CENTER)]
        db.close()
        update('DELETE')
    page.window.full_screen=True
    page.theme_mode='DARK'
    alert=AlertDialog(title=Text())
    row=Row([ElevatedButton('LOGIN',on_click=login),ElevatedButton('REGISTER',on_click=register),ElevatedButton('DELETE',on_click=delete)],alignment=MainAxisAlignment.CENTER)
    column=Column()
    user=TextField()
    pw=TextField(password=True)
    re_pw=TextField(password=True)
    d_users=Dropdown('USERS')
    column_areas,column_categories=Column(),Column()
    area,tables,category=TextField(label='AREA'),TextField(label='TABLES',width=100),TextField(label='CATEGORY')
    current=Text(width=100,color='green')
    title=Row(alignment=MainAxisAlignment.CENTER)
    return View('/',controls=[Row([Switch(on_change=theme),Text(width=500),current,Text(width=500),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.window.destroy())],alignment=MainAxisAlignment.END),
                              Divider(),row,column,alert])