import sqlite3
from flet import *
from flet_route import Params,Basket
def Home(page:Page,params:Params,basket:Basket):
  def theme(e):
    if page.theme_mode=='DARK':page.theme_mode='LIGHT'
    else:page.theme_mode='DARK'
    page.update()
  def bill(e):
    db=sqlite3.connect('db.db')
    db.execute('delete from ORDERS where AREA=? and SEAT=?',(r_order.controls[0].value).split(' - TABLE '))
    db.commit()
    db.close()
    r_order.controls=c_order.controls=[]
    refresh_tables('')
  def remove(e,area,seat):
    db=sqlite3.connect('db.db')
    price=db.execute('select PRICE from PRODUCTS where PRODUCT=?',(e.control.text[1],)).fetchone()[0]
    if db.execute('select QUANTITY from ORDERS where AREA=? and SEAT=? and PRODUCT=?',(area,seat,e.control.text[1],)).fetchone()[0]==1:
      db.execute('delete from ORDERS where AREA=? and SEAT=? and PRODUCT=?',(area,seat,e.control.text[1],))
    else:db.execute('update ORDERS set QUANTITY=QUANTITY-1,PRICE=PRICE-? where AREA=? and SEAT=? and PRODUCT=?',(price,area,seat,e.control.text[1],))
    db.commit()
    total.value='TOTAL €. '+str(db.execute('select sum(PRICE) from ORDERS where AREA=? and SEAT=?',(area,seat,)).fetchone()[0])
    c_order.controls=[TextButton(p,on_click=lambda e,area=area,seat=seat:remove(e,area,seat)) for p in db.execute('select QUANTITY,PRODUCT,PRICE from ORDERS where AREA=? and SEAT=?',(area,seat,)).fetchall()]
    c_order.controls.append(Row([total,ElevatedButton('BILL',on_click=bill)],alignment=MainAxisAlignment.CENTER))
    db.close()
    refresh_tables('')
  def selected_table(e,area):
    r_order.controls=[Text(area+' - TABLE '+str(e.control.text))]
    db=sqlite3.connect('db.db')
    total.value='TOTAL €. '+str(db.execute('select sum(PRICE) from ORDERS where AREA=? and SEAT=?',(area,str(e.control.text),)).fetchone()[0])
    c_order.controls=[TextButton(p,on_click=lambda e,area=area,seat=str(e.control.text):remove(e,area,seat)) for p in db.execute('select QUANTITY,PRODUCT,PRICE from ORDERS where AREA=? and SEAT=?',(area,str(e.control.text),)).fetchall()]
    c_order.controls.append(Row([total,ElevatedButton('BILL',on_click=bill)],alignment=MainAxisAlignment.CENTER))
    db.close()
    page.update()
  def refresh_tables(e):
    db=sqlite3.connect('db.db')
    c_tables.controls=[Row([Text(a[0],color='orange',width=75)],alignment=MainAxisAlignment.CENTER,height=30) for a in db.execute('select * from TABLES').fetchall()]
    for n in range(len(c_tables.controls)):
      for t in range(1,db.execute('select TABLES from TABLES').fetchall()[n][0]+1):c_tables.controls[n].controls.append(ElevatedButton(t,width=45,on_click=lambda e,area=c_tables.controls[n].controls[0].value:selected_table(e,area)))
    for r in c_tables.controls:
      for t in r.controls[1:]:
        if db.execute('select * from ORDERS where AREA=? and SEAT=?',(r.controls[0].value,t.text,)).fetchall()==[]:t.bgcolor='green'
        else:t.bgcolor='red'
    db.close()
    page.update()
  def list_category(category):
    def show_product(e):
      db=sqlite3.connect('db.db')
      data=db.execute('select * from PRODUCTS where PRODUCT=?',((e.control.text).split('\n')[0],)).fetchone()
      d_category.value,t_product.value,t_price.value=data
      if r_order.controls!=[]:
        area,seat=(r_order.controls[0].value).split(' - TABLE ')
        if db.execute('select * from ORDERS where AREA=? and SEAT=? and PRODUCT=?',(area,seat,t_product.value,)).fetchall()==[]:
          db.execute('insert into ORDERS values(?,?,?,1,?)',(area,seat,t_product.value,t_price.value,))#AREA,SEAT,PRODUCT,QUANTITY,PRICE
        else:db.execute('update ORDERS set QUANTITY=QUANTITY+1,PRICE=PRICE+? where AREA=? and SEAT=? and PRODUCT=?',(t_price.value,area,seat,t_product.value,))
        db.commit()
        total.value='TOTAL €. '+str(db.execute('select sum(PRICE) from ORDERS where AREA=? and SEAT=?',(area,seat,)).fetchone()[0])
        c_order.controls=[TextButton(p,on_click=lambda e,area=area,seat=seat:remove(e,area,seat)) for p in db.execute('select QUANTITY,PRODUCT,PRICE from ORDERS where AREA=? and SEAT=?',(area,seat,)).fetchall()]
        c_order.controls.append(Row([total,ElevatedButton('BILL',on_click=bill)],alignment=MainAxisAlignment.CENTER))
        refresh_tables('')
      db.close()
      page.update()
    for c in r_categories.controls:
      if c.text==category:c.color='green'
      else:c.color='orange'
    t_product.value=t_price.value=''
    try:
      db=sqlite3.connect('db.db')
      c_products.controls=[GridView(controls=[ElevatedButton(p[0]+'\n'+str(p[1]),on_click=show_product) for p in db.execute('select PRODUCT,PRICE from PRODUCTS where CATEGORY=? order by PRODUCT',(category,)).fetchall()],max_extent=100)]
      db.close()
    except:pass
    page.update()
  def delete(e):
    try:
      db=sqlite3.connect('db.db')
      db.execute('delete from PRODUCTS where PRODUCT=?',(t_product.value,))
      db.commit()
      db.close()
      alert.title=Text('CORRECTLY DELETED')
    except:alert.title=Text('PRODUCT NOT IN DATABASE')
    page.open(alert)
    list_category(r_categories.controls[0].text)
  def save(e):
    def check_price(price):
      try:
        float(price)
        return(True)
      except ValueError:return(False)
    if check_price(t_price.value)==False:alert.title=Text('PRICE NOT CORRECT')
    else:
      if t_price.value=='' or t_product.value=='':alert.title=Text('PRICE A/O PRODUCT EMPTY')
      else:
        db=sqlite3.connect('db.db')
        db.execute('insert into PRODUCTS values(?,?,?)',(d_category.value,(t_product.value).upper(),float(t_price.value),))
        alert.title=Text('CORRECTLY ADDED')
        db.commit()
        db.close()
        list_category(d_category.value)
    page.open(alert)
    page.update()
  page.window.full_screen=True
  page.theme_mode='DARK'
  alert=AlertDialog(title=Text(''))
  c_tables=Column()
  db=sqlite3.connect('db.db')
  r_categories=Row([ElevatedButton(category[0],color='orange',on_click=lambda x,category=category[0]:list_category(category)) for category in db.execute('select CATEGORY from CATEGORIES order by CATEGORY').fetchall()],alignment=MainAxisAlignment.CENTER)
  c_products=Column(width=800,height=300,scroll=ScrollMode.ALWAYS)
  r_order,c_order=Row(alignment=MainAxisAlignment.CENTER,width=400),Column()
  d_category=Dropdown(label='CATEGORY',width=200,options=[dropdown.Option(category[0]) for category in db.execute('select CATEGORY from CATEGORIES').fetchall()])
  current=Text(db.execute('select USER from USERS where CURRENT="on"').fetchone()[0],width=100,color='green')
  db.close()
  t_product,t_price=TextField(label='NAME'),TextField(label='PRICE',width=150)
  r_product=Row([d_category,t_product,t_price,Column([ElevatedButton('SAVE',on_click=save),ElevatedButton('DELETE',on_click=delete)])])
  total=Text()
  refresh_tables('')
  return View('/',controls=[Row([Switch(on_change=theme),Text(width=500),current,Text(width=500),IconButton(icon=Icons.EXIT_TO_APP,icon_color='red',icon_size=50,on_click=lambda _:page.go('/'))],height=40),
                            Divider(),
                            Row([c_tables]),
                            Divider(),
                            Row([Column([r_categories,c_products,Divider(),Row([Text('NEW PRODUCT',color='orange',height=15)],alignment=MainAxisAlignment.CENTER),r_product],width=800),VerticalDivider(),
                                 Column([r_order,Divider(),c_order])],height=600)])