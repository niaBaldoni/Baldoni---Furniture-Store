from tracemalloc import start
from webbrowser import get
import mysql.connector
import requests

import random
import datetime

db = mysql.connector.connect(
    host="localhost",
    database = "baldonifurniturestore2",
    user="root",
    passwd="root"               
)

mycursor = db.cursor(buffered=True)

def insertDepartments(department_list):
    add_department = ("INSERT INTO Departments "
                    "(Department_Id, Deparment_Name) "
                    "VALUES (%s, %s)")

    x = len(department_list)

    for i in range(0, x):
        department_data = (i, department_list[i])
        mycursor.execute(add_department, department_data)
    db.commit()
    print("Insert of departments into DB completed.")

def generateEmployees():
    department_list = ["Sales Associate", "Cashier", "Human Resources", "Customer Service Representative", "Visual Merchandiser", "IT support", 
                        "Inventory Control", "Store Manager", "CEO"]

    add_employee = ("INSERT INTO Employees "
                        "(Employee_Id, Employee_Name, Employee_Surname, Hire_Date, Store_Id, Department_Id) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")

    insertDepartments(department_list)

    surnames_list = getSurnames()
    names_list = getFirstNames()
    range_s = datetime.date(2000, 1, 1)
    range_e = datetime.date(2021,9,9)
    employee_id = 1

    get_stores = ("SELECT Store_Id FROM Stores")
    get_random_store = ("SELECT Store_Id FROM Stores ORDER BY RAND() LIMIT 1")

    mycursor.execute(get_stores, ())
    stores = [item[0] for item in mycursor.fetchall()]

    for i in range(0,len(stores)):
        employee_data = (employee_id, random.choice(names_list), random.choice(surnames_list), 
                        "2000-01-01 00:00:00", stores[i], 8)
        employee_id = employee_id + 1
        mycursor.execute(add_employee, employee_data)
    db.commit()

    for i in range(0, len(stores)*50):
        mycursor.execute(get_random_store, ())
        store = mycursor.fetchall()[0][0]
        department = random.randint(0, len(department_list)-2)
        employee_data = (employee_id, random.choice(names_list), random.choice(surnames_list),
                        generateDate(range_s, range_e), store, department)
        employee_id = employee_id + 1
        mycursor.execute(add_employee, employee_data)
    db.commit()


def generateReceiptDetails():
    insert_details = ("INSERT INTO Fur_Tra "
                    "(Furniture_Id, Transaction_Id, Quantity) "
                    "VALUES (%s, %s, %s)")

    qty = [1, 2, 3, 4, 5, 6]
    items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for tra in range(0, 50001):
        randitems = random.choices(items, cum_weights=(10, 25, 25, 10, 10, 5, 5, 5, 3, 2), k=1)
        randfur = random.sample(range(0,999), randitems[0])
        for i in range(0,len(randfur)):
            randqty = random.choices(qty, cum_weights=(30, 25, 20, 15, 5, 5), k=1)
            details_data = (randfur[i], tra, randqty[0])
            mycursor.execute(insert_details, details_data)
            db.commit()

def generateDate(range_s, range_e):
    time_between_dates = range_e - range_s
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = range_s + datetime.timedelta(days=random_number_of_days)
    return(random_date)

def receiptNoCard(id):
    get_store = ("SELECT S.Store_Id, R.Region_Id FROM Stores S, Regions R, Provinces P, Municipalities M WHERE R.Region_Id = %s "
                "AND P.Region_Id = R.Region_Id AND M.Province_Id = M.Province_Id AND S.Municipality_Id = M.Municipality_Id ORDER BY RAND() LIMIT 1")
                
    insert_transaction_nocard = ("INSERT INTO Transactions "
                                "(Transaction_Id, Transaction_Date, Store_Id) "
                                "VALUES (%s, %s, %s)")
    
    region = random.randint(1,20)
    mycursor.execute(get_store, (region,))
    store = mycursor.fetchall()[0][0]
    date = generateDate(datetime.date(2000, 1, 1), datetime.date.today()).strftime("%Y-%m-%d %H:%M:%S")

    nocard_data = (id, date, store)
    mycursor.execute(insert_transaction_nocard, nocard_data)
    db.commit()

def receiptCard(id, card_limit):
    insert_transaction_card = ("INSERT INTO Transactions "
                                "(Transaction_Id, Transaction_Date, Store_Id, Card_Id) "
                                "VALUES (%s, %s, %s, %s)")

    get_region = ("SELECT R.Region_Id FROM Cards C, Regions R, Provinces P, Municipalities M WHERE C.Card_Id = %s "
	            "AND C.Municipality_Id = M.Municipality_Id AND M.Province_Id = P.Province_Id AND P.Region_Id = R.Region_Id AND R.Region_Id")

    get_store = ("SELECT S.Store_Id, R.Region_Id FROM Stores S, Regions R, Provinces P, Municipalities M WHERE R.Region_Id = %s "
                "AND P.Region_Id = R.Region_Id AND M.Province_Id = M.Province_Id AND S.Municipality_Id = M.Municipality_Id ORDER BY RAND() LIMIT 1")

    card = random.randint(1, card_limit)
    date = generateDate(datetime.date(2000, 1, 1), datetime.date.today()).strftime("%Y-%m-%d %H:%M:%S")

    p = random.random()
    if p <= 0.05:
        region = random.randint(1,20)
        mycursor.execute(get_store, (region,))
        store = mycursor.fetchall()[0][0]
        card_data = (id, date, store, card)
        mycursor.execute(insert_transaction_card, card_data)
    else:
        mycursor.execute(get_region, (card,))
        region = mycursor.fetchall()[0][0]
        mycursor.execute(get_store, (region,))
        store = mycursor.fetchall()[0][0]
        card_data = (id, date, store, card)
        mycursor.execute(insert_transaction_card, card_data)
    db.commit()

def generateReceipts():
    get_number_of_cards = ("SELECT count(*) FROM Cards")
    
    mycursor.execute(get_number_of_cards, ())
    card_limit = mycursor.fetchall()[0][0]

    for id in range(1, 50001):
        p = random.random()
        if p <= 0.33:
            receiptNoCard(id)
        else:
            receiptCard(id, card_limit)

def generateDiscounts():
    start_dates = ['2001-3-01', '2001-6-01', '2001-10-01', '2002-3-01', '2002-6-01', '2002-10-01', '2003-3-01', '2003-6-01', '2003-10-01', '2004-3-01', 
                    '2004-6-01', '2004-10-01', '2005-3-01', '2005-6-01', '2005-10-01', '2006-3-01', '2006-6-01', '2006-10-01', '2007-3-01', '2007-6-01', 
                    '2007-10-01', '2008-3-01', '2008-6-01', '2008-10-01', '2009-3-01', '2009-6-01', '2009-10-01', '2010-3-01', '2010-6-01', '2010-10-01', 
                    '2011-3-01', '2011-6-01', '2011-10-01', '2012-3-01', '2012-6-01', '2012-10-01', '2013-3-01', '2013-6-01', '2013-10-01', '2014-3-01', 
                    '2014-6-01', '2014-10-01', '2015-3-01', '2015-6-01', '2015-10-01', '2016-3-01', '2016-6-01', '2016-10-01', '2017-3-01', '2017-6-01', 
                    '2017-10-01', '2018-3-01', '2018-6-01', '2018-10-01', '2019-3-01', '2019-6-01', '2019-10-01', '2020-3-01', '2020-6-01', '2020-10-01']
    end_dates = ['2001-4-01', '2001-7-01', '2001-11-01', '2002-4-01', '2002-7-01', '2002-11-01', '2003-4-01', '2003-7-01', '2003-11-01', '2004-4-01', 
                '2004-7-01', '2004-11-01', '2005-4-01', '2005-7-01', '2005-11-01', '2006-4-01', '2006-7-01', '2006-11-01', '2007-4-01', '2007-7-01', 
                '2007-11-01', '2008-4-01', '2008-7-01', '2008-11-01', '2009-4-01', '2009-7-01', '2009-11-01', '2010-4-01', '2010-7-01', '2010-11-01', 
                '2011-4-01', '2011-7-01', '2011-11-01', '2012-4-01', '2012-7-01', '2012-11-01', '2013-4-01', '2013-7-01', '2013-11-01', '2014-4-01', 
                '2014-7-01', '2014-11-01', '2015-4-01', '2015-7-01', '2015-11-01', '2016-4-01', '2016-7-01', '2016-11-01', '2017-4-01', '2017-7-01', 
                '2017-11-01', '2018-4-01', '2018-7-01', '2018-11-01', '2019-4-01', '2019-7-01', '2019-11-01', '2020-4-01', '2020-7-01', '2020-11-01']

    select_randfurniture = ("SELECT F.Furniture_Id FROM Furniture F WHERE F.Discontinued = 0 ORDER BY RAND() LIMIT %s")
    
    values = [60, 70, 80, 90]

    for i in range(0,len(start_dates)):
        if i % 3 == 0:
            mycursor.execute(select_randfurniture, (10,))
            records = mycursor.fetchall()
            for element in records:
                furniture_id = element[0]
                discontinueFurniture(furniture_id, start_dates[i], 50)
        
        mycursor.execute(select_randfurniture, (50,))
        records = mycursor.fetchall()
        for element in records:
            furniture_id = element[0]
            discount = random.choices(values, cum_weights=(20, 30, 30, 20), k=1)
            createDiscount(furniture_id, start_dates[i], end_dates[i], discount[0])

def discontinueFurniture(furniture_id, date, discount):
    discontinue = ("UPDATE Furniture SET Discontinued = 1 WHERE Furniture_Id = %s")
    get_price = ("SELECT Prices.Price FROM Prices WHERE Prices.Furniture_Id = %s LIMIT 1")
    end_price = ("UPDATE Prices SET Prices.End_Date = %s WHERE Prices.Furniture_Id = %s AND (%s BETWEEN Prices.Start_Date AND Prices.End_Date)")
    start_price = ("INSERT into Prices "
                "(Furniture_Id, Start_Date, Price, Discount) "
                "VALUES (%s, %s, %s, %s)")

    sdate_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    edate_obj = sdate_obj - datetime.timedelta(seconds=1)
    sdate = sdate_obj.strftime("%Y-%m-%d %H:%M:%S")
    edate = edate_obj.strftime("%Y-%m-%d %H:%M:%S")

    mycursor.execute(get_price, (furniture_id,))
    price = mycursor.fetchall()
    mycursor.execute(discontinue, (furniture_id,))
    mycursor.execute(end_price, (edate, furniture_id, edate))
    mycursor.execute(start_price, (furniture_id, sdate, price[0][0], discount))
    db.commit()

def createDiscount(furniture_id, sdate, edate, discount):
    get_price = ("SELECT Prices.Price FROM Prices WHERE Prices.Furniture_Id = %s LIMIT 1")
    end_price = ("UPDATE Prices SET Prices.End_Date = %s WHERE Prices.Furniture_Id = %s AND (%s BETWEEN Prices.Start_Date AND Prices.End_Date)")
    start_price = ("INSERT into Prices "
                "(Furniture_Id, Start_Date, Price, Discount) "
                "VALUES (%s, %s, %s, %s)")

    ssdate_obj = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    ppdate_obj = ssdate_obj - datetime.timedelta(seconds=1)
    npdate_obj = datetime.datetime.strptime(edate, "%Y-%m-%d")
    sedate_obj = npdate_obj - datetime.timedelta(seconds=1)

    mycursor.execute(get_price, (furniture_id,))
    price = mycursor.fetchall()
    mycursor.execute(end_price, (ppdate_obj.strftime("%Y-%m-%d %H:%M:%S"), furniture_id, ppdate_obj.strftime("%Y-%m-%d %H:%M:%S")))
    mycursor.execute(start_price, (furniture_id, ssdate_obj.strftime("%Y-%m-%d %H:%M:%S"), price[0][0], discount))
    mycursor.execute(end_price, (sedate_obj.strftime("%Y-%m-%d %H:%M:%S"), furniture_id, sedate_obj.strftime("%Y-%m-%d %H:%M:%S")))
    mycursor.execute(start_price, (furniture_id, npdate_obj.strftime("%Y-%m-%d %H:%M:%S"), price[0][0], 100))
    db.commit()

################################
def getSurnames():
    file = open("surnames_list.txt", "r")

    file_lines = file.read()
    return(file_lines.split("\n"))

def getFirstNames():
    file = open("names_list.txt", "r")

    file_lines = file.read()
    return(file_lines.split("\n"))

def generateCards():
    query_municipalities = ("SELECT M.Municipality_Id FROM Regions R, Provinces P, Municipalities M "
                        "WHERE M.Province_Id = P.Province_Id AND P.Region_Id = R.Region_Id AND R.Region_Id = %s ORDER BY RAND() LIMIT 1")


    insert_cards = ("INSERT INTO Cards "
                    "(Card_Id, Card_Name, Card_Surname, Birthday, Municipality_Id) "
                    "VALUES (%s,%s,%s, %s, %s)")

    surnames_list = getSurnames()
    names_list = getFirstNames()
    range_s = datetime.date(1970, 1, 1)
    range_e = datetime.date(2003,1,1)
    card_number = 1
    #we want to generate a random number of card holders for each region
    for i in range(1, 21):
        r = random.randint(200, 1500)
        for j in range(0, r):
            mycursor.execute(query_municipalities, (i,))
            records = mycursor.fetchall()
            card_data = (card_number, random.choice(names_list), random.choice(surnames_list), 
                        generateDate(range_s, range_e).strftime("%Y-%m-%d"), records[0][0])
            card_number = card_number + 1
            mycursor.execute(insert_cards, card_data)
            db.commit()

################################

def insertCategories(categories_list):
    x = len(categories_list)

    add_category = ("INSERT INTO Categories "
                "(Category_Id, Category_Name) "
                "VALUES (%s, %s)")

    for i in range(0, x):
        category_data = (i, categories_list[i])
        mycursor.execute(add_category, category_data)

    db.commit()

    print("Insert of categories into DB completed.")

def getFurnitureNames():
    file = open("furniture_name.txt", "r")
    file_lines = file.read()
    return(file_lines.split("\n"))

def furnitureGenerator():
    add_furniture = ("INSERT INTO Furniture "
                    "(Furniture_Id, Furniture_Name, Category_Id, Furniture_Height, Furniture_Width, Furniture_Depth) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
    
    furniture_list = getFurnitureNames()
    l = len(furniture_list)

    for i in range(0, 1000):
        c = random.randint(0,11)
        x = random.randint(300,3000)
        y = random.randint(300,3000)
        z = random.randint(300,3000)
        r = random.randint(0,l)

        furniture_data = (i, furniture_list[r], c, x, y, z)
        mycursor.execute(add_furniture, furniture_data)
        db.commit()

    print("Generation and insert of furniture into DB completed.")

def generatePrices():
    add_price = ("INSERT into Prices "
                "(Furniture_Id, Start_Date, Price) "
                "VALUES (%s, %s, %s)")

    for i in range(0, 1000):
        p = (random.randint(499, 99999))/100
        d = "2000-01-01 00:00:01"
        price_data = (i, d, p)
        mycursor.execute(add_price, price_data)
        db.commit()

    print("Generation and insert of prices into DB completed.")

def furniture(headers):
    categories_list = ["Bed", "Sofa", "Bookcase", "Shelving Unit", "Table", "Desk", "Cabinet", "Media Furniture", "Drawer Unit", "Wardrobe", "Chair", "Outdoor Furniture"]
    insertCategories(categories_list)
    furnitureGenerator(headers)
    generatePrices()

################################

def insertRegions(headers):
    request = requests.get("https://raw.githubusercontent.com/napolux/italia/master/json/regioni.json", headers=headers)
    rejson = request.json()

    add_region = ("INSERT INTO Regions "
                "(Region_Id, Region_Name) "
                "VALUES (%s, %s)")

    for i in range (0, len(rejson)):
        region = rejson[i]
        region_data = (region["id"], region["nome"])
        mycursor.execute(add_region, region_data)
    db.commit()

    print("Insert of regions into DB completed.")

def insertProvinces(headers):
    request = requests.get("https://raw.githubusercontent.com/napolux/italia/master/json/province.json", headers=headers)
    projson = request.json()

    add_province = ("INSERT INTO Provinces "
                    "(Province_Id, Province_Name, Region_Id) "
                    "VALUES (%s, %s, %s)")

    for i in range(0, len(projson)):
        province = projson[i]
        province_data = (province["id"], province["nome"], province["id_regione"])
        mycursor.execute(add_province, province_data)
    db.commit()
    print("Insert of provinces into DB completed.")

def insertMunicipalities(headers):
    request = requests.get("https://raw.githubusercontent.com/napolux/italia/master/json/comuni.json", headers=headers)
    munjson = request.json()

    add_municipality = ("INSERT INTO Municipalities "
                        "(Municipality_Id, Municipality_Name, Province_Id) "
                        "VALUES (%s, %s, %s)")

    for i in range(0, len(munjson)):
        municipality = munjson[i]
        municipality_data = (municipality["id"], municipality["nome"], municipality["id_provincia"])
        mycursor.execute(add_municipality, municipality_data)
        db.commit()
    print("Insert of municipalities into DB completed.")
    
################################

def generateStores():
    query_municipalities = ("SELECT M.Municipality_Id, M.Municipality_Name FROM Regions R, Provinces P, Municipalities M "
                        "WHERE M.Province_Id = P.Province_Id AND P.Region_Id = R.Region_Id AND R.Region_Id = %s ORDER BY RAND() LIMIT 1")

    add_store = ("INSERT INTO Stores "
                "(Store_Id, Store_Name, Municipality_Id) "
                "VALUES (%s, %s, %s)")

    for r in range(1,21):
        stores = random.randint(5,15)

        for s in range(0, stores):
            id = r*100 + s
            mycursor.execute(query_municipalities, (r,))
            records = mycursor.fetchall()
            store_data = (id, "Baldoni " + records[0][1], records[0][0])
            mycursor.execute(add_store, store_data)
            db.commit()
    print("Generation and insert of stores into DB completed.")

def generateStorage():
    add_fur_in_sto = ("INSERT INTO fur_sto "
                    "(Furniture_Id, Store_Id, Quantity) "
                    "VALUES (%s, %s, %s)")
    
    query_stores = ("SELECT S.Store_Id FROM Stores S")
    mycursor.execute(query_stores, ())
    records = [item[0] for item in mycursor.fetchall()]
    for i in range(0, len(records)):
        for j in range(0, 1000):
            qty = [500, 1000, 1250, 1500, 2000, 2500]
            storage_data = (j, records[i], random.choice(qty))
            mycursor.execute(add_fur_in_sto, storage_data)
        db.commit()
    print("Generation and insert of stores inventories into DB completed.")

################################

def main():
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}

    insertRegions(headers)
    insertProvinces(headers)
    insertMunicipalities(headers)

    furniture()

    generateStores()
    generateStorage()

    generateCards()
    generateDiscounts()

    generateReceipts()
    generateReceiptDetails()

    generateEmployees()

if __name__ == "__main__":
    main()