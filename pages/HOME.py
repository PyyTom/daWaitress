import sqlite3
from flet import *
def home_view(page: Page,theme,alert):
    def bill(e):
        db=sqlite3.connect('db.db')
        db.execute('delete from WORKING where AREA=? and TABLE_=?',(r_order.controls[0].value,r_order.controls[1].value,))
        db.commit()
        db.close()
        r_order.controls[0].value=r_order.controls[1].value=''
        upd_tables('')
    def upd_tables(e):
        def table_selected(e):
            r_order.controls=[TextField(label='AREA',value=e.control.parent.controls[0].value,read_only=True,width=200),TextField(label='TABLE',value=e.control.text,read_only=True,width=100),TextField(label='TOTAL',read_only=True,width=100),ElevatedButton('BILL',on_click=bill)]
            try:
                db = sqlite3.connect('db.db')
                c_order.controls = [TextButton(w[2:], on_click=from_order) for w in db.execute('select * from WORKING where AREA=? and TABLE_=?',(r_order.controls[0].value, r_order.controls[1].value,)).fetchall()]
                r_order.controls[2].value=db.execute('select sum(PARTIAL) from WORKING where AREA=? and TABLE_=?',(r_order.controls[0].value,r_order.controls[1].value,)).fetchone()[0]
                db.close()
            except:pass
            page.update()
        def from_order(e):
            db=sqlite3.connect('db.db')
            if e.control.text[0]==1:db.execute('delete from WORKING where AREA=? and TABLE_=? and PRODUCT=?',(r_order.controls[0].value,r_order.controls[1].value,e.control.text[1],))
            else:
                price=db.execute('select PRICE from PRODUCTS where PRODUCT=?',(e.control.text[1],)).fetchone()[0]
                db.execute('update WORKING set QUANTITY=QUANTITY-1,PARTIAL=PARTIAL-? where AREA=? and TABLE_=? and PRODUCT=?',(price,r_order.controls[0].value,r_order.controls[1].value,e.control.text[1],))
            db.commit()
            db.close()
            upd_tables('')
        db=sqlite3.connect('db.db')
        if db.execute('select * from TABLES').fetchall()!=[]:
            c_tables.controls=[Row([Text(area[0],width=100)]) for area in db.execute('select AREA from TABLES order by AREA').fetchall()]
            for n in range(len(c_tables.controls)):
                for t in range(1,int(db.execute('select TABLES from TABLES where AREA=?',(c_tables.controls[n].controls[0].value,)).fetchone()[0])+1):
                    if db.execute('select * from WORKING where AREA=? and TABLE_=?',(c_tables.controls[n].controls[0].value,t,)).fetchall()==[]:color='green'
                    else:color='red'
                    c_tables.controls[n].controls.append(ElevatedButton(t,width=50,color=color,on_click=table_selected))
        try:
            c_order.controls = [TextButton(w[2:], on_click=from_order) for w in db.execute('select * from WORKING where AREA=? and TABLE_=?', (r_order.controls[0].value,r_order.controls[1].value,)).fetchall()]
            r_order.controls[2].value = db.execute('select sum(PARTIAL) from WORKING where AREA=? and TABLE_=?',(r_order.controls[0].value, r_order.controls[1].value,)).fetchone()[0]
        except:pass
        db.close()
        page.update()
    def show_category(e):
        def to_order(product,price):
            if r_order.controls==[]:
                alert.title=Text('NO TABLE SELECTED')
                page.open(alert)
            else:
                db=sqlite3.connect('db.db')
                if c_order.controls==[]:db.execute('insert into WORKING values(?,?,?,?,?)',(r_order.controls[0].value,r_order.controls[1].value,1,product,price,))
                else:
                    if db.execute('select * from WORKING where PRODUCT=?',(product,)).fetchall()==[]:db.execute('insert into WORKING values(?,?,?,?,?)',(r_order.controls[0].value,r_order.controls[1].value,1,product,price,))
                    else:db.execute('update WORKING set QUANTITY=QUANTITY+1,PARTIAL=PARTIAL+? where PRODUCT=?',(price,product,))
                db.commit()
                db.close()
                upd_tables('')
        for c in r_categories.controls:c.color='grey'
        e.control.color='green'
        db=sqlite3.connect('db.db')
        if db.execute('select * from PRODUCTS where CATEGORY=?',(e.control.text,)).fetchall()!=[]:
            c_category.controls=[GridView([Container(tooltip='CLICK FOR ADDING IT TO ORDER',content=Column([Text(item[1]+' $.'+str(item[2]))]),image=DecorationImage(src=item[4]),width=200,height=200,on_click=lambda e,product=item[1],price=item[2]:to_order(product,price)) for item in db.execute('select * from PRODUCTS where CATEGORY=?',(e.control.text,)).fetchall()],expand=1,runs_count=3,auto_scroll=True)]
        db.close()
        page.update()
    user=page.data.get('user')
    c_tables = Column()
    db = sqlite3.connect('db.db')
    if db.execute('select * from PRODUCTS').fetchall()!=[]:r_categories=Row([ElevatedButton(category[0],on_click=show_category,tooltip='IT SHOWS '+category[0]) for category in db.execute('select CATEGORY from PRODUCTS group by CATEGORY order by CATEGORY').fetchall()],width=600,alignment=MainAxisAlignment.CENTER)
    else:r_categories=Row(width=600,alignment=MainAxisAlignment.CENTER)
    db.close()
    c_category = Column(width=600,height=500,scroll=ScrollMode.ALWAYS)
    r_order=Row(alignment=MainAxisAlignment.CENTER)
    c_order=Column(width=600,height=500,scroll=ScrollMode.ALWAYS)
    upd_tables(None)
    return Column([Row([Switch(on_change=theme,tooltip='CHANGE THEME-MODE (DARK/LIGHT)'),
                        Text('daRestaurant, user '+user, size=30, color='orange'),
                        ElevatedButton('EDITOR', on_click=lambda _: page.go('/EDITOR'),tooltip='TO ADDING,EDITING AND DELETING AREAS,TABLES AND PRODUCTS'),
                        IconButton(icon=Icons.EXIT_TO_APP, icon_size=50, icon_color='red', on_click=lambda _:page.go('/'),tooltip='EXIT')], alignment=MainAxisAlignment.CENTER, height=50),
                   Divider(),
                   Row([c_tables], alignment=MainAxisAlignment.CENTER),
                   Divider(),
                   Row([Row([Text('PRODUCTS',color='orange',size=20)],alignment=MainAxisAlignment.CENTER,width=600), VerticalDivider(),Row([Text('ORDER',color='orange',size=20)],alignment=MainAxisAlignment.CENTER,width=600)], height=50),
                   Row([r_categories, VerticalDivider(),r_order], height=50),
                   Row([c_category, VerticalDivider(),c_order], height=500),
                   alert])
