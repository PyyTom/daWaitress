import sqlite3
from flet import *
from pages.HOME import home_view
def login_view(page: Page,theme,alert):
    def upd(how):
        db = sqlite3.connect('db.db')
        if how == 'login':
            if d_user.value is None or t_password.value is None:alert.title = Text('EMPTY FIELDS')
            elif t_password.value != db.execute('SELECT PASSWORD FROM USERS WHERE USER=?', (d_user.value,)).fetchone()[0]:alert.title = Text('PASSWORD WRONG')
            else:
                page.data={'user':d_user.value}
                alert.title = Text('WELCOME BACK, ' + d_user.value)
                page.clean()
                page.add(home_view(page))
        elif how == 'register':
            if not t_user.value or not t_password.value or not t_re_password.value:alert.title = Text('EMPTY FIELDS')
            elif t_password.value != t_re_password.value:alert.title = Text("PASSWORDS DON'T MATCH")
            else:
                db.execute('INSERT INTO USERS VALUES (?, ?)', ((t_user.value).upper(), t_password.value,))
                db.commit()
                alert.title = Text('WELCOME, ' + (t_user.value).upper())
                t_user.value = t_password.value = t_re_password.value = ''
                page.clean()
                page.add(login_view(page))
        elif how == 'unregister':
            if d_user.value is None:alert.title = Text('USER NOT SELECTED')
            else:
                db.execute('DELETE FROM USERS WHERE USER=?', (d_user.value,))
                db.commit()
                alert.title = Text(d_user.value + ' CORRECTLY UNREGISTERED')
                page.clean()
                page.add(login_view(page))
        db.close()
        page.open(alert)
        page.update()
    try:
        db = sqlite3.connect('db.db')
        d_user = Dropdown(label='USERNAME',width=200,options=[dropdown.Option(user[0]) for user in db.execute('SELECT USER FROM USERS').fetchall()])
        db.close()
    except:d_user = Dropdown(label='USERNAME', width=200)
    t_user = TextField(label='USERNAME')
    t_password = TextField(label='PASSWORD', password=True)
    t_re_password = TextField(label='CONFIRM PASSWORD', password=True)
    alert = AlertDialog(title=Text(''))
    tabs = Tabs(tabs=[Tab(text='LOGIN', content=Column([d_user, t_password, ElevatedButton('LOGIN', on_click=lambda _: upd('login'))])),
                      Tab(text='REGISTER', content=Column([t_user, t_password, t_re_password, ElevatedButton('REGISTER', on_click=lambda _: upd('register'))])),
                      Tab(text='UNREGISTER', content=Column([d_user, ElevatedButton('UNREGISTER', on_click=lambda _: upd('unregister'))]))],width=300)
    return Column([Row([Switch(on_change=theme),Text('daRestaurant', size=30, color='orange'),IconButton(icon=Icons.EXIT_TO_APP, icon_size=50, icon_color='red', on_click=lambda _: page.window.destroy())], alignment=MainAxisAlignment.CENTER, height=50),
                   Divider(height=50),
                   Row([tabs], alignment=MainAxisAlignment.CENTER, height=500),
                   alert])
