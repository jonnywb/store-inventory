from types import SimpleNamespace
from models import (Base, session,
                    Product, engine)

import csv
import datetime
import time

def clean_price(price_str):
    try:
        price_str = price_str.strip('$')
        price_float = float(price_str)
        if price_float < 0:
            raise ValueError

    except ValueError:
        input(''' 
        \n****************** PRICE ERROR ******************
        \rOnly numbers including the dollar sign are valid.
        \rEx: $10.99 or 10.99
        \rPress Enter to try again.
        \r*************************************************''')
        return
    else:
        return int(price_float * 100)

def clean_date(date_str):
    split_date = date_str.split('/')

    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        
        cleaned_date = datetime.date(year, month, day)

    except ValueError:
        input(''' 
        \n*********** DATE ERROR ***********
        \rThe date format be Month/Day/Year.
        \rFor example: 6/12/1990
        \rPress enter to try again.
        \r**********************************''')
        return
    else:
        return cleaned_date

def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)

        for count, row in enumerate(data):
            if count == 0:
                continue
            else:
                product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()

                if product_in_db == None:
                    name = row[0]
                    price = clean_price(row[1])
                    quantity = int(row[2])
                    date = clean_date(row[3])
                    new_product = Product(product_name = name, product_price = price, product_quantity = quantity, date_updated = date)
                    session.add(new_product)
                elif clean_date(row[3]) > product_in_db.date_updated:
                    product_in_db.product_price = clean_price(row[1])
                    product_in_db.product_quantity = int(row[2])
                    product_in_db.date_updated = clean_date(row[3])
        session.commit()

def backup_csv():
    with open('backup.csv', 'w', newline='') as csvfile:
        headers = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        newdata = csv.DictWriter(csvfile, fieldnames=headers)
        newdata.writeheader()
        for product in session.query(Product).order_by(Product.product_id).all():
            new_date = product.date_updated
            new_date = new_date.strftime('%m/%d/%Y')
            str_price = '$' + str(product.product_price / 100)
            newdata.writerow({'product_name': product.product_name, 'product_price': str_price, 'product_quantity': product.product_quantity,'date_updated': new_date})

def add_product():
    name = input('Product Name:\n>  ')
            
    quantity_error = True
    while quantity_error:
        try:
            quantity = int(input('Quantity:\n>  '))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            input('''
            \n************* ERROR *************
            \rPlease enter a number above zero
            \r  Press enter to continue
            \r*********************************''')
            continue
        else:
            quantity_error = False

    price_error = True
    while price_error:
        price = input('Price (Example: 99.99):\n>  ')
        price = clean_price(price)
        if type(price) == int:
            price_error = False

    date_added = datetime.date.today()

    if session.query(Product).filter(Product.product_name==name).first():
        upd_product = session.query(Product).filter(Product.product_name==name).first()
        upd_product.product_quantity = quantity
        upd_product.date_updated = date_added
        upd_product.product_price = price
        print('*** Product updated! ***')

    else:
        new_product = Product(product_name=name, product_quantity = quantity, date_updated=date_added, product_price=price)
        session.add(new_product) 
        print('*** Product added! ***')
    
    session.commit()
    time.sleep(1.5)

def find_id():
    id_error = True

    while id_error:
        try:
            search_id = int(input(\
                '\nPlease enter the product_id of the item you are looking for.\n> '))

            the_product = session.query(Product).filter(Product.product_id==search_id).first()

            print(f'''
                \n*****************************************
                \rProduct Name: {the_product.product_name}
                \rPrice: ${the_product.product_price / 100}
                \rQuantity: {the_product.product_quantity}
                \rDate: {the_product.date_updated}
                \r*****************************************''')

            id_error = False

            input('''
            \nPress enter when you are ready to continue
            \r*******************************************''')

        except ValueError:
            input(''' 
            \n******* ID ERROR *******
            \rThe ID should be a number.
            \rPress enter to try again.
            \r**********************''')

        except AttributeError:
            input('''
            \n**** PRODUCT NOT FOUND ****
            \r Press enter to try again.
            \r**************************''')

def menu():
    while True:
        print('''
            \n*********** STORE INVENTORY **********
            \r- Press 'a' to add product
            \r- Press 'v' to view product using product_ID
            \r- Press 'b' to backup all existing data
            \r- Type 'exit' to exit application.
            \r**************************************''')
        
        choice = input('\nPlease make a selection.\n> ').lower()

        if choice in ['a', 'v', 'b', 'exit']:
            return choice
        else:
            input('''
                \n*************** ERROR ****************
                \nPlease choose one of the options above.
                \rPress enter to try again.
                \n**************************************''')

def app():
    app_running = True

    while app_running:
        choice = menu()

        if choice == 'a':
            add_product()

        elif choice == 'v':
            find_id()

        elif choice == 'b':
            backup_csv()

        else:
            print('*** Goodbye! ***')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()