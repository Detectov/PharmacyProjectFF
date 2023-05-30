import sys 
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from datetime import date
from PyQt5.QtWidgets import QMainWindow
import sqlite3

products = []
sales = []
conn = sqlite3.connect('sanpablo.db')

c = conn.cursor()

c.execute ("""CREATE TABLE if not exists users(
            id integer primary key autoincrement,
            username text,
            password text
)""")


c.execute("""CREATE TABLE if not exists products(
            id integer primary key autoincrement,
            sku text,
            name text,
            stock integer,
            tax text,
            presentation text,
            costvalue real,
            salevalue real,
            laboratory text,
            expdate text
)""")
c.execute("""CREATE TABLE if not exists sales(
            id integer primary key autoincrement,
            date text,
            soldprod text,
            amount integer,
            billed text,
            method text,
            subtotal real,
            total real
)""")
conn.commit()
conn.close()

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        
        self.createbutton.clicked.connect(self.signup)
        self.loginbutton.clicked.connect(self.login)
        

    def login(self):
        conn = sqlite3.connect('sanpablo.db')
        c = conn.cursor()
        query = "SELECT username, password FROM users WHERE username = ? AND password = ? "
        c.execute(query, (self.username_input.text(), self.password_input.text()))
        f = c.fetchall()
        print(f)
        if len(f) > 0:
            QtWidgets.QMessageBox.information(self, 'Login succesful!', 'Welcome, {}!'.format(self.username_input.text()))
            menu=Menu()
            widget.addWidget(menu)
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            QtWidgets.QMessageBox.warning(self, 'Login failed', 'Username or password not valid')
        conn.commit()
        conn.close()
        return
        
        
    def signup(self):
        conn = sqlite3.connect('sanpablo.db')
        c = conn.cursor()
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QtWidgets.QMessageBox.warning(self, 'Error', 'You need to enter a username and a password')
            return
        
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        c.execute(query, (username, password))
        QtWidgets.QMessageBox.information(self, 'Account created', 'The account has been created!')

        conn.commit()
        conn.close()


    

class Menu(QDialog):
    def __init__(self):
        super(Menu, self).__init__()
        loadUi("menu.ui", self)
        widget.setFixedWidth(620)
        widget.setFixedHeight(480)
        self.addbutton.clicked.connect(self.gotoaddprod)
        self.reportbutton.clicked.connect(self.gotoreports)
        self.addsalebutton.clicked.connect(self.gotoaddsale)

    def gotoaddprod(self):
        addprod = AddProduct()
        widget.addWidget(addprod)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoreports(self):
        reports = Reports()
        widget.addWidget(reports)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoaddsale(self):
        addsale = AddSale()
        widget.addWidget(addsale)
        widget.setCurrentIndex(widget.currentIndex()+1)

class AddProduct(QDialog):
    
    def __init__(self):
        super(AddProduct, self).__init__()
        loadUi("addprod.ui", self)
        widget.setFixedWidth(620)
        widget.setFixedHeight(480)
        self.backbutton.clicked.connect(self.backtomenu)
        self.donebutton.clicked.connect(self.backtomenu)
        self.donebutton.clicked.connect(self.savedata)
    def savedata(self):
        conn = sqlite3.connect('sanpablo.db')
        c = conn.cursor() 
        proddict = {
            "sku" : self.nameinput.text()[0:3],
            "name" : self.nameinput.text(),
            "stock" : int(self.stockinput.text()),
            "tax" : self.taxinput.text(),
            "presentation" : self.presinput.text(),
            "costvalue" : float(self.costinput.text()),
            "salevalue" : float(self.saleinput.text()),
            "laboratory" : self.labinput.text(),
            "expdate" : self.expdate.text()
        }
        if not proddict["sku"] or not proddict["name"] or not proddict["stock"] or not proddict["tax"] or not proddict["presentation"] or not proddict["costvalue"] or not proddict["salevalue"] or not proddict["laboratory"] or not proddict["expdate"]:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter all values')
                return
        for product in products:
            if product["sku"] == proddict["sku"]:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Product already exists')
                return
        query = "INSERT INTO products (sku, name, stock, tax, presentation, costvalue, salevalue, laboratory, expdate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(query, (proddict["sku"], proddict["name"], proddict["stock"], proddict["tax"], proddict["presentation"], proddict["costvalue"], proddict["salevalue"], proddict["laboratory"], proddict["expdate"]))
        QtWidgets.QMessageBox.information(self, 'Product added', 'The product has been added!')
        
        conn.commit()
        conn.close()
            
         
    def backtomenu(self):
        menu=Menu()

        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class AddSale(QDialog):
    def __init__(self):
        self.products = []
        super(AddSale, self).__init__()
        loadUi("createsale.ui", self)
        widget.setFixedHeight(480)
        widget.setFixedWidth(772)
        self.backbutton.clicked.connect(self.backtomenu)
        self.addbutton.clicked.connect(self.storedata)
        self.donebutton.clicked.connect(self.savedata)
        
        
    def reset(self):
        self.soldinput.setText("")
        self.amountinput.setText("")
        self.billedinput.setText("")
        self.methodinput.setText("")

        
    def storedata(self):
        product = {
            "date" : date.today(),
            "soldprod" : self.soldinput.text(),
            "amount" : int(self.amountinput.text()),
            "billed": self.billedinput.text(),
            "method":self.methodinput.text(),
            "subtotal" : 0,
            "total" : 0
        }
        if not "soldprod" or not "amount" or not "billed" or not "method":
                QtWidgets.QMessageBox.warning(self, 'Error', 'Please enter all values')
        else:
            QtWidgets.QMessageBox.information(self, 'Product added', 'The product has been added!')
            self.products.append(product)
        self.reset()
        

    def savedata(self):
        conn = sqlite3.connect('sanpablo.db')
        c = conn.cursor()
        for i in self.products:
            saledict = i
            product = saledict["soldprod"].strip()
            query = "SELECT * FROM products WHERE name = ?"
            c.execute(query, (product,))
            f = c.fetchall()
            if len(f) > 0:
                for row in f:
                    row = list(row)
                    if row[3] >= saledict["amount"]:
                        saledict["subtotal"] = row[7] * saledict["amount"]
                        if row[4] == "Y":
                            saledict["total"] = saledict["subtotal"] * 1.16
                        else:
                            saledict["total"] = saledict["subtotal"]
                        row[3] -= saledict["amount"]
                        query = "INSERT INTO sales (date, soldprod, amount, billed, method, subtotal, total) VALUES (?, ?, ?, ?, ?, ?, ?)"                            
                        c.execute(query, (saledict["date"], saledict["soldprod"], saledict["amount"], saledict["billed"], saledict["method"], saledict["subtotal"], saledict["total"]))
                        conn.commit()
                        QtWidgets.QMessageBox.information(self, 'Sale added', 'The sale has been added!')
                        query = "UPDATE products SET stock = ? WHERE name = ?"
                        c.execute(query, (row[3], product))
                        conn.commit()
                    else:
                        QtWidgets.QMessageBox.warning(self, 'Error', "There's not enough stock for that sale")
            else:
                QtWidgets.QMessageBox.warning(self, 'Error', 'Product not found')
        conn.commit()
        conn.close()
        self.products = []
        self.backtomenu()

    def backtomenu(self):
        menu=Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
     
        
class Reports(QDialog):
    def __init__(self):
        super(Reports, self).__init__()
        loadUi("report.ui", self)
        widget.setFixedWidth(620)
        widget.setFixedHeight(480)
        self.prodbutton.clicked.connect(self.gotoprodtab)
        self.salesbutton.clicked.connect(self.gotosalestab)
        self.backbutton.clicked.connect(self.backtomenu)
        self.salesmenubutton.clicked.connect(self.gotosalesmenu)
        self.labbutton.clicked.connect(self.gotolab)
        self.billbutton.clicked.connect(self.gotobill)
        
        
        
    def backtomenu(self):
        menu=Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def gotoprodtab(self):
        prodtable = ProdTable()
        widget.addWidget(prodtable)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotosalestab(self):
        salestable = SalesTable()
        widget.addWidget(salestable)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosalesmenu(self):
        salesmenu = SalesMenu()
        widget.addWidget(salesmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotolab(self):
        lab= viewProd()
        widget.addWidget(lab)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotobill(self):
        bill= Billmenu()
        widget.addWidget(bill)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    
        
class ProdTable(QDialog):
    def __init__(self):
        super(ProdTable, self).__init__()
        loadUi("prodtable.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        self.tableWidget.setColumnWidth(7,250)
        self.tableWidget.setColumnWidth(7,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtoreports)
        self.loaddata()
        
    def loaddata(self):
        conn = sqlite3.connect('sanpablo.db')
        c = conn.cursor()
        products = []
        with open('products.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                product = {
                    "sku": values[0],
                    "name": values[1],
                    "stock": values[2],
                    "tax": values[3],
                    "presentation": (values[4]),
                    "costvalue": float(values[5]),
                    "salevalue": float(values[6]),
                    "laboratory": values[7],
                    "expdate": values[8]
                }
                products.append(product)
        row = 0
        self.tableWidget.setRowCount(len(products))
        for product in products:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(product["sku"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(product["name"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(product["stock"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(product["tax"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(product["presentation"])))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(product["costvalue"])))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(product["salevalue"])))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(product["laboratory"]))
            self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(product["expdate"])))
            row += 1 
    
    def backtoreports(self):
        reports=Reports()
        widget.addWidget(reports)
        widget.setCurrentIndex(widget.currentIndex()+1)


class SalesTable(QDialog):
    def __init__(self):
        super(SalesTable, self).__init__()
        loadUi("saletable.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtoreports)
        self.loaddata()
        
    def loaddata(self):
        sales = []
        with open('sales.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                sale = {
                    "date": values[0],
                    "soldprod": values[1],
                    "amount": values[2],
                    "subtotal": values[3],
                    "total": values[4],
                    "method": values[5],
                    "billed": values[6]
                }
                sales.append(sale)
        row = 0
        self.tableWidget.setRowCount(len(sales))
        for sale in sales:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(sale["date"])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(sale["soldprod"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(sale["amount"])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(sale["subtotal"])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(sale["total"])))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(sale["method"]))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(sale["billed"]))
            row += 1
    
    def backtoreports(self):
        reports=Reports()
        widget.addWidget(reports)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SalesMenu(QDialog):
    def __init__(self):
        super(SalesMenu, self).__init__()
        loadUi("salesmenu.ui", self)
        widget.setFixedWidth(620)
        widget.setFixedHeight(480)
        self.cardbutton.clicked.connect(self.gotocards)
        self.cashbutton.clicked.connect(self.gotocash)
        self.backbutton.clicked.connect(self.backtoreports)


    def gotocards(self):
        cards = SalesByCard()
        widget.addWidget(cards)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocash(self):
        cash = SalesByCash()
        widget.addWidget(cash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def backtoreports(self):
        reports=Reports()
        widget.addWidget(reports)
        widget.setCurrentIndex(widget.currentIndex()+1)

    

   


class SalesByCard(QDialog):
    def __init__(self):
        super(SalesByCard, self).__init__()
        loadUi("salesbycard.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtosalesmenu)
        self.loaddata()

    def loaddata(self):
        sales = []
        with open('sales.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                sale = {
                    "date": values[0],
                    "soldprod": values[1],
                    "amount": values[2],
                    "subtotal": values[3],
                    "total": values[4],
                    "method": values[5],
                    "billed": values[6]
                }
                sales.append(sale)
        row = 0
        for sale in sales:
            if sale["method"] == "Card":
                self.tableWidget.setRowCount(len(sales))
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(sale["date"])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(sale["soldprod"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(sale["amount"])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(sale["subtotal"])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(sale["total"])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(sale["method"]))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(sale["billed"]))
                row += 1
            
    
    def backtosalesmenu(self):
        salesmenu=SalesMenu()
        widget.addWidget(salesmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class SalesByCash(QDialog):
    def __init__(self):
        super(SalesByCash, self).__init__()
        loadUi("salesbycash.ui",self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtosalesmenu)
        self.loaddata()

    def loaddata(self):
        sales = []
        with open('sales.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                sale = {
                    "date": values[0],
                    "soldprod": values[1],
                    "amount": values[2],
                    "subtotal": values[3],
                    "total": values[4],
                    "method": values[5],
                    "billed": values[6]
                }
                sales.append(sale)
        row = 0
        for i in sales:
            if i["method"] == "Cash":
                self.tableWidget.setRowCount(len(sales))
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i["date"])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i["soldprod"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i["amount"])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i["subtotal"])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i["total"])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i["method"]))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(i["billed"]))
                row += 1
            

    def backtosalesmenu(self):
        salesmenu = SalesMenu()
        widget.addWidget(salesmenu)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Billmenu(QDialog):
    def __init__(self):
        super(Billmenu, self).__init__()
        loadUi("billmenu.ui", self)
        widget.setFixedWidth(620)
        widget.setFixedHeight(480)
        self.yesbill.clicked.connect(self.yesbills)
        self.nobill.clicked.connect(self.nobills)
        self.backbutton.clicked.connect(self.backtoreports)

    def yesbills(self):
        bill = BILLED()
        widget.addWidget(bill)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def nobills(self):
        notbill=NOTBILLED()
        widget.addWidget(notbill)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def backtoreports(self):
        report=Reports()
        widget.addWidget(report)
        widget.setCurrentIndex(widget.currentIndex()+1)
        

    
class BILLED(QDialog):
    def __init__(self):
        super(BILLED, self).__init__()
        loadUi("yesbilltable.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtobillmenu)
        self.loaddata()

    def loaddata(self):
        sales = []
        with open('sales.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                sale = {
                    "date": values[0],
                    "soldprod": values[1],
                    "amount": values[2],
                    "subtotal": values[3],
                    "total": values[4],
                    "method": values[5],
                    "billed": values[6]
                }
                sales.append(sale)
        row = 0
        for i in sales:
            if i["billed"] == "Y":
                self.tableWidget.setRowCount(len(sales))
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i["date"])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i["soldprod"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i["amount"])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i["subtotal"])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i["total"])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i["method"]))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(i["billed"]))
                row += 1
            
    
    def backtobillmenu(self):
        bill=Billmenu()
        widget.addWidget(bill)
        widget.setCurrentIndex(widget.currentIndex()+1)

class NOTBILLED(QDialog):
    def __init__(self):
        super(NOTBILLED, self).__init__()
        loadUi("notbilltable.ui", self)
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,250)
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,250)
        self.tableWidget.setColumnWidth(5,250)
        self.tableWidget.setColumnWidth(6,250)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.backbutton.clicked.connect(self.backtobillmenu)
        self.loaddata()

    def loaddata(self):
        sales = []
        with open('sales.txt', 'r') as f:
            for line in f:
                values = line.strip().split(',')
                sale = {
                    "date": values[0],
                    "soldprod": values[1],
                    "amount": values[2],
                    "subtotal": values[3],
                    "total": values[4],
                    "method": values[5],
                    "billed": values[6]
                }
                sales.append(sale)
        row = 0
        for i in sales:
            if i["billed"] == "N":
                self.tableWidget.setRowCount(len(sales))
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i["date"])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(i["soldprod"]))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i["amount"])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i["subtotal"])))
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i["total"])))
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(i["method"]))
                self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(i["billed"]))
                row += 1
            
    
    def backtobillmenu(self):
        bill=Billmenu()
        widget.addWidget(bill)
        widget.setCurrentIndex(widget.currentIndex()+1)

    
            

class viewProd(QDialog):
    def __init__(self):
        super(viewProd, self).__init__()
        loadUi("viewbylab.ui",self)
        widget.setFixedWidth(1067)
        widget.setFixedHeight(735)
        self.donebutton.clicked.connect(self.loaddata)
        self.backbutton.clicked.connect(self.backtoreports)
    def loaddata(self):
        products = []
        with open("products.txt", "r") as f:
            for line in f:
                values = line.strip().split(",")
                product = {
                    "sku": values[0],
                    "name": values[1],
                    "stock": int(values[2]),
                    "tax": values[3],
                    "presentation": values[4],
                    "costvalue": float(values[5]),
                    "salevalue": float(values[6]),
                    "laboratory": values[7],
                    "expdate": values[8]
                }
                products.append(product)

        row = 0
        self.tableWidget.setRowCount(len(products))
        for product in products:
                if product["laboratory"] == self.labinput.text():
                    self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(product["sku"]))
                    self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(product["name"]))
                    self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(product["presentation"]))
                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(product["laboratory"]))
                    self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(product["stock"])))
                    self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(product["costvalue"])))
                    self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(product["salevalue"])))
                    self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(product["tax"]))
                    self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(product["expdate"])))
                    row += 1
    def backtoreports(self):
        reports=Reports()
        widget.addWidget(reports)
        widget.setCurrentIndex(widget.currentIndex()+1)


            
app=QApplication(sys.argv)
mainwindow = Login()
widget=QtWidgets.QStackedWidget()
widget.setFixedWidth(620)
widget.setFixedHeight(480)
widget.addWidget(mainwindow)
widget.show()
app.exec_()