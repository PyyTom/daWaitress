import sqlite3,os
from flet import *
def editor_view(page: Page,picker:FilePicker):
    user=page.data.get('user')
    def theme(e):
        page.theme_mode = 'LIGHT' if page.theme_mode == 'DARK' else 'DARK'
        page.update()
    def upd_textfield(which):
        db=sqlite3.connect('db.db')
        if which=='area':
            if d_areas.value=='NEW':
                t_area.disabled=False
                t_area.value=''
                t_tables.value=0
            else:
                t_area.disabled=True
                t_area.value=d_areas.value
                t_tables.value=db.execute('select TABLES from TABLES where AREA=?',(d_areas.value,)).fetchone()[0]
        elif which=='category':
            if d_categories.value=='NEW':
                t_category.disabled=False
                t_category.value=''
                t_product.value=''
                t_price.value=0.0
                t_info.value=''
                i_image.src=''
            else:
                t_category.disabled=True
                t_category.value=d_categories.value
                for c in db.execute('select PRODUCT from PRODUCTS where CATEGORY=?',(t_category.value,)).fetchall():d_products.options.append(dropdown.Option(c[0]))
        elif which=='product':
            if d_products.value=='NEW':
                t_product.disabled=False
                t_product.value=d_products.value
                t_price.value=0.0
                t_info.value=''
                i_image.src=''
            else:
                data=[d for d in db.execute('select * from PRODUCTS where CATEGORY=? and PRODUCT=?',(t_category.value,d_products.value)).fetchall()[0]]
                t_product.value,t_price.value,t_info.value,i_image.src=data[1:]
        db.close()
        page.update()
    def pick_image(e: FilePickerResultEvent):
        i_image.src=e.files[0].path
        page.update()
    def check_empty():
        missing = False
        for c in tabs.tabs[tabs.selected_index].content.controls:
            if c._get_control_name() == 'dropdown' or c._get_control_name() == 'textfield':
                if c.value == '':
                    missing = True
                    break
        return missing
    def save(what):
        if check_empty()==True:
            alert.title=Text('EMPTY FIELDS')
            page.open(alert)
        else:
            db=sqlite3.connect('db.db')
            if what=='area':
                if d_areas.value=='NEW':db.execute('insert into TABLES values(?,?)',((t_area.value).upper(),t_tables.value,))
                else:db.execute('update TABLES set TABLES=? where AREA=?',(t_tables.value,t_area.value))
            elif what=='product':
                if d_categories.value=='NEW':os.mkdir('images/'+(t_category.value).upper())
                if d_products.value=='NEW':
                    db.execute('insert into PRODUCTS values(?,?,?,?,?)',((t_category.value).upper(),(t_product.value).upper(),t_price.value,(t_info.value).upper(),i_image.src,))
                else:db.execute('update PRODUCTS set PRICE=?,INFO=?,IMAGE=? where CATEGORY=? and PRODUCT=?',(t_price.value,(t_info.value).upper(),i_image.src,t_category.value,t_product.value,))
            db.commit()
            db.close()
            alert.title=Text('CORRECTLY SAVED')
            page.open(alert)
            page.clean()
            page.add(editor_view(page,picker))
    def delete(what):
        if check_empty()==True:
            alert.title=Text('EMPTY FIELDS')
            page.open(alert)
        else:pass
    alert = AlertDialog(title=Text(''))
    d_areas = Dropdown(label='AREAS',options=[dropdown.Option('NEW')],on_change=lambda _:upd_textfield('area'))
    t_area = TextField(label='AREA')
    t_tables = TextField(label='TABLES', keyboard_type=KeyboardType.NUMBER)
    d_categories = Dropdown(label='CATEGORIES',options=[dropdown.Option('NEW')],on_change=lambda _:upd_textfield('category'))
    t_category = TextField(label='CATEGORY')
    d_products=Dropdown(label='PRODUCTS',options=[dropdown.Option('NEW')],on_change=lambda _:upd_textfield('product'))
    t_product = TextField(label='PRODUCT')
    t_price = TextField(label='PRICE', keyboard_type=KeyboardType.NUMBER)
    t_info = TextField(label='INFO')
    i_image=Image(src='',width=200, height=200)
    picker.on_result=pick_image
    b_image = ElevatedButton('IMAGE', on_click=picker.pick_files)
    db=sqlite3.connect('db.db')
    try:
        for area in db.execute('select AREA from TABLES').fetchall():d_areas.options.append(dropdown.Option(area[0]))
    except:pass
    try:
        for category in db.execute('select CATEGORY from PRODUCTS group by CATEGORY').fetchall():d_categories.options.append(dropdown.Option(category[0]))
    except:pass
    db.close()
    tabs = Tabs(tabs=[Tab(text='AREAS',content=Column([Row([ElevatedButton('SAVE', color='green', on_click=lambda _: save('area')),
                                                       ElevatedButton('DELETE', color='red', on_click=lambda _: delete('area'))], alignment=MainAxisAlignment.CENTER),
                                                       d_areas, t_area,t_tables])),
                      Tab(text='PRODUCTS',content=Column([Row([ElevatedButton('SAVE', color='green', on_click=lambda _: save('product')),
                                                               ElevatedButton('DELETE', color='red', on_click=lambda _: delete('product'))], alignment=MainAxisAlignment.CENTER),
                                                          d_categories,t_category,d_products, t_product, t_price, t_info,Row([b_image,i_image])]))],width=500)
    return Column([Row([Switch(on_change=theme),
                        Text('daRestaurant, user '+user, size=30, color='orange'),
                        IconButton(icon=Icons.EXIT_TO_APP, icon_size=50, icon_color='red', on_click=lambda _: page.go('/HOME'))], alignment=MainAxisAlignment.CENTER, height=50),
                   Divider(),
                   Row([tabs], alignment=MainAxisAlignment.CENTER, height=700),
                   alert])