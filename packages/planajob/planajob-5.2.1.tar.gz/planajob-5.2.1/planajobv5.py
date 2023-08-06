
# File: planajobv5.py
# Version = 5.1.2
# There was a bug in version 5.1.1





from tkinter import *
from tkinter import ttk
import sys, sqlite3
import os

root = Tk()

planajoblocn = "/home/terry/Desktop/planajobtk"

vatrate = 20

root.title("PLANAJOB")

 
    
    
def usegeditcust():
   print     ("using gedit")
   os.chdir  (planajoblocn)
   os.system ("gedit genlist.txt")
    

conn2 = sqlite3.connect('planajobsql')
conn2.isolation_level = None
c = conn2.cursor()


def setup():
    print ("setting up")
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers(custnumb INTEGER PRIMARY KEY, custname TEXT, address1 TEXT, address2 TEXT, address3 TEXT, address4 TEXT, phone TEXT)''')
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS salesorders  (ordnumb INTEGER PRIMARY KEY , custname TEXT , dateordered DATE, datereqs DATE)''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (suppnumb INTEGER PRIMARY KEY, suppname TEXT, address1 TEXT, address2 TEXT, address3 TEXT, 
address4 TEXT, phone TEXT) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS porderheader (pordernumb INTEGER PRIMARY KEY, supplier INTEGER, dateordered date, reqddate DATE, datedeliv DATE) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS partsordered (ordnumb INTEGER, linenubmb INTEGER, partnumb integer, qtyordered floating, qtyissued floating ) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS labour_details (ordnumb INTEGER, linenumb INTEGER, resource_numb INTEGER, qty_reqd float, qty_logged FLOAT) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS purchaseorders (pordernumb, linenumb INTEGER, partnumb INTEGER, qty_ordered FLOAT, qty_received FLOAT) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS resource (resource_numb INTEGER PRIMARY KEY, resource_desc TEXT, cost_per_hour FLOAT, capacity_available FLOAT, capacity_used FLOAT) ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock (partnumber INTEGER PRIMARY KEY, partdescript TEXT, uom TEXT, stockqty FLOAT, supplier_code INTEGER, cost FLOAT, price FLOAT) ''')



def listcust():
    print ("listing cust")
    kexiqu(1)

def listpurch():
    print ("Listing supps")
    kexiqu(2)

def listords():
    print ("Listing sales orders")
    kexiqu(3)

def listparts():
    print ("List parts on order")
    kexiqu(4)

def listlabbs():
    print("List labour on order")
    kexiqu(5)

def listlabor():
    print ("List labor details")
    kexiqu(8)

def liststok():
    print ("Stok list")
    kexiqu(9)


def listpurchaseorders():
    print ("list purchase orders" )
    kexiqu(6)

def listpurchasedets():
    print ("po dets")
    kexiqu(7)
   

def addcust():
        print ("adding a customer")
       
        def doit():
             print("doit")
             custnumbedt = custnumbbox.get()
             custnameedt= custnamebox.get()
             custaddredt= custaddrbox.get()
             custaddr2edt = custaddr2box.get()
             custaddr3edt = custaddr3box.get()
             custaddr4edt = custaddr4box.get()
             custphone    = custphonebox.get()

    
             c.execute ("select * from customers where custnumb = " + custnumbedt)
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no cust")
                c.execute("INSERT INTO customers (custnumb, custname, address1, address2, address3, address4, phone) VALUES(?,?,?,?,?,?,?)", (custnumbedt, custnameedt, custaddredt, custaddr2edt, custaddr3edt, custaddr4edt, custphone))
             else:
                 print ("custumer exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "CUSTOMER ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


         
         
         
        addrecframe = ttk.Frame(root)
        custnumb=  ttk.Label(addrecframe, text = "Customer Number")
        custname=  ttk.Label(addrecframe, text = "Customer Name")
        custaddr1= ttk.Label(addrecframe, text=  "Customer Address 1")
        custaddr2= ttk.Label(addrecframe, text=  "Customer Address 2")
        custaddr3= ttk.Label(addrecframe, text=  "Customer Address 3")
        custaddr4= ttk.Label(addrecframe, text=  "Customer Address4")
        custphone= ttk.Label(addrecframe, text=  "Customer Phone")

        
  
        custnamebox =  ttk.Entry  (addrecframe)
        custnumbbox =  ttk.Entry  (addrecframe)
        custaddrbox =  ttk.Entry  (addrecframe)
        custaddr2box = ttk.Entry  (addrecframe)
        custaddr3box = ttk.Entry  (addrecframe)
        custaddr4box = ttk.Entry  (addrecframe)
        custphonebox = ttk.Entry  (addrecframe)
        
        additbutton = ttk.Button (addrecframe, text ="OK",   command=doit)
        donebutton  = ttk.Button (addrecframe, text ="Done", command = addrecframe.destroy)
    
    
        addrecframe.grid(column=0, row=0)
        custnumb .grid  (column=0, row=0)
        custname .grid  (column=0, row=1)
        custaddr1.grid  (column=0, row=2)
        custaddr2.grid  (column=0, row=3)
        custaddr3.grid  (column=0, row=4)
        custaddr4.grid  (column=0, row=5)
        custphone.grid  (column=0, row=6)
        
        
        custnumbbox.grid  (column=1, row=0)
        custnamebox.grid  (column=1, row=1)
        custaddrbox.grid  (column=1, row=2)
        custaddr2box.grid (column=1, row=3)
        custaddr3box.grid (column=1, row=4)
        custaddr4box.grid (column=1, row=5)
        custphonebox.grid (column=1, row=6)
        
        additbutton.grid (column=5, row=5)
        donebutton.grid (column =4, row=5)
        

    

   

def addsupp():
    print ("adding a supplier")

    def doit():
             print("doit")
             suppnumbedt =  suppnumbbox.get()
             suppnameedt=   suppnamebox.get()
             suppaddredt=   suppaddrbox.get()
             suppaddr2edt = suppaddr2box.get()
             suppaddr3edt = suppaddr3box.get()
             suppaddr4edt = suppaddr4box.get()
             suppphone    = suppphonebox.get()

             c.execute ("select * from suppliers where suppnumb = " + repr (suppnumbedt))
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no supp")
                c.execute("INSERT INTO suppliers (suppnumb, suppname, address1, address2, address3, address4, phone) VALUES(?,?,?,?,?,?,?)", (suppnumbedt, suppnameedt, suppaddredt, suppaddr2edt, suppaddr3edt, suppaddr4edt, suppphone ))
             else:
                 print ("supplier exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "SUPPLIER ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


              

    
    addrecframe = ttk.Frame(root)
    suppnumb=  ttk.Label(addrecframe, text = "Supplier Number")
    suppname=  ttk.Label(addrecframe, text = "Supplier Name")
    suppaddr1= ttk.Label(addrecframe, text=  "Supplier Address 1")
    suppaddr2= ttk.Label(addrecframe, text=  "Supplier Address 2")
    suppaddr3= ttk.Label(addrecframe, text=  "Supplier Address 3")
    suppaddr4= ttk.Label(addrecframe, text=  "Supplier Address4")
    suppphone= ttk.Label(addrecframe, text=  "Supplier Phone")

        
  
    suppnamebox =  ttk.Entry  (addrecframe)
    suppnumbbox =  ttk.Entry  (addrecframe)
    suppaddrbox =  ttk.Entry  (addrecframe)
    suppaddr2box = ttk.Entry  (addrecframe)
    suppaddr3box = ttk.Entry  (addrecframe)
    suppaddr4box = ttk.Entry  (addrecframe)
    suppphonebox = ttk.Entry  (addrecframe)
        
    additbutton = ttk.Button (addrecframe, text ="OK", command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    
    addrecframe.grid(column=0, row=0)
    suppnumb .grid  (column=0, row=0)
    suppname .grid  (column=0, row=1)
    suppaddr1.grid  (column=0, row=2)
    suppaddr2.grid  (column=0, row=3)
    suppaddr3.grid  (column=0, row=4)
    suppaddr4.grid  (column=0, row=5)
    suppphone.grid  (column=0, row=6)
        
        
    suppnumbbox.grid  (column=1, row=0)
    suppnamebox.grid  (column=1, row=1)
    suppaddrbox.grid  (column=1, row=2)
    suppaddr2box.grid (column=1, row=3)
    suppaddr3box.grid (column=1, row=4)
    suppaddr4box.grid (column=1, row=5)
    suppphonebox.grid (column=1, row=6)
        
    additbutton.grid (column=5, row=5)
    donebutton.grid  (column = 4, row=5)

    
#  (salesorders ordnumb  , custname  , dateordered , datereqs DATE)''')
   


def addasalesorder():
    print ("adding a sales order")


    def doit():
             print("doit")
             sordnumbedt =  sordnumbbox.get()
             custnameedt=   custnamebox.get()
             dateordered=   dateorderedbox.get()
             datereqd     = datereqdbox.get()

             c.execute ("select * from salesorders  where ordnumb = " + repr (sordnumbedt))
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no supp")
                c.execute("INSERT INTO salesorders (ordnumb, custname, dateordered, datereqs) VALUES(?,?,?,?)", (sordnumbedt, custnameedt, dateordered, datereqd))
             else:
                 print ("supplier exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "ORDER ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


              

    
    addrecframe = ttk.Frame(root)
    sordnumb=     ttk.Label(addrecframe, text = "Sales order Number")
    custname=     ttk.Label(addrecframe, text = "Customer Number")
    dateordered=  ttk.Label(addrecframe, text=  "Date ordered")
    datereqd=     ttk.Label(addrecframe, text=  "Date required")

        
  
    sordnumbbox =     ttk.Entry  (addrecframe)
    custnamebox =     ttk.Entry  (addrecframe)
    dateorderedbox =  ttk.Entry  (addrecframe)
    datereqdbox =     ttk.Entry  (addrecframe)
        
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid   (column=0, row=0)
    sordnumb .grid     (column=0, row=0)
    custname .grid     (column=0, row=1)
    dateordered.grid   (column=0, row=2)
    datereqd.grid      (column=0, row=3)
        
        
    sordnumbbox.grid     (column= 1, row=0)
    custnamebox.grid     (column= 1, row=1)
    dateorderedbox.grid  (column= 1, row=2)
    datereqdbox.grid     (column= 1, row=3)
        
    additbutton.grid (column=5, row=5)
    donebutton.grid  (column =4, row=5)
    

    

   
    

    

def addpurchord():
    print ("addin a purchase order")
   

    def doit():
             print("doit")
             pordnumbedt =  pordnumbbox.get()
             suppnameedt=   suppnamebox.get()
             dateordered=   dateorderedbox.get()
             datereqd=      datereqdbox.get()
             datedeldvd=    datedeldvdbox.get()

# porderheader (pordernumb , supplier , dateordered, reqddate, datedeliv

             c.execute ("select * from porderheader  where pordernumb = " + repr (pordnumbedt))
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no order")
                c.execute("INSERT INTO porderheader (pordernumb, supplier, dateordered, reqddate, datedeliv) VALUES(?,?,?,?,?)", (pordnumbedt, suppnameedt, dateordered, datereqd, datedeldvd))
             else:
                 print ("supplier exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "ORDER ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


              

    
    addrecframe = ttk.Frame(root)
    pordnumb=     ttk.Label(addrecframe, text = "Purchase order Number")
    suppname=     ttk.Label(addrecframe, text = "Supplier Number")
    dateordered=  ttk.Label(addrecframe, text=  "Date ordered")
    datereqd=     ttk.Label(addrecframe, text=  "Date required")
    datedelvd=    ttk.Label(addrecframe, text=  "Date Delivered")

        
  
    pordnumbbox =     ttk.Entry  (addrecframe)
    suppnamebox =     ttk.Entry  (addrecframe)
    dateorderedbox =  ttk.Entry  (addrecframe)
    datereqdbox =     ttk.Entry  (addrecframe)
    datedeldvdbox=    ttk.Entry  (addrecframe)
    
        
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid   (column=0, row=0)
    pordnumb .grid     (column=0, row=0)
    suppname .grid     (column=0, row=1)
    dateordered.grid   (column=0, row=2)
    datereqd.grid      (column=0, row=3)
    datedelvd.grid     (column=0, row=4)
    
        
        
    pordnumbbox.grid     (column= 1, row=0)
    suppnamebox.grid     (column= 1, row=1)
    dateorderedbox.grid  (column= 1, row=2)
    datereqdbox.grid     (column= 1, row=3)
    datedeldvdbox.grid   (column= 1, row=4)
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)

    

   
    


def addpartstoorder():
    print ("adding parts to order")
    

# partsordered (ordnumb, linenubmb, partnumb, qtyordered, qtyissued floating


    def doit():
             print("doit")
             ordnumbedt =    ordnumbbox. get()
             linenumbedt =   linennumbbox.get()
             partnumbedt =   partnumbbox.get()
             qtyorderededt = qtyorderedbox.get()
             qtyissuededt=   qtyissuedbox.get()
             


             c.execute("INSERT INTO partsordered  (ordnumb, linenubmb, partnumb, qtyordered, qtyissued) VALUES(?,?,?,?,?)", (ordnumbedt, linenumbedt, partnumbedt, qtyorderededt, qtyissuededt))
            
    addrecframe =  ttk.Frame(root)
    ordnumb=       ttk.Label(addrecframe, text = "Sales order Number")
    linenumb=      ttk.Label(addrecframe, text = "Line number")
    partnumb=      ttk.Label(addrecframe, text=  "Part number")
    qtyordered=    ttk.Label(addrecframe, text=  "Qty ordered")
    qtyissued=     ttk.Label(addrecframe, text=  "Qty issued")
    

    ordnumbbox =         ttk.Entry  (addrecframe)
    linennumbbox =       ttk.Entry  (addrecframe)
    partnumbbox =        ttk.Entry  (addrecframe)
    qtyorderedbox  =     ttk.Entry  (addrecframe)
    qtyissuedbox=        ttk.Entry  (addrecframe)
    
        
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid    (column=0, row=0)
    ordnumb .grid       (column=0, row=0)
    linenumb.grid       (column=0, row=1)
    partnumb.grid       (column=0, row=2)
    qtyordered.grid     (column=0, row=3)
    qtyissued.grid      (column=0, row=4)
    
        
        
    ordnumbbox.grid        (column= 1, row=0)
    linennumbbox.grid       (column= 1, row=1)
    partnumbbox.grid       (column= 1, row=2)
    qtyorderedbox.grid     (column= 1, row=3)
    qtyissuedbox.grid      (column= 1, row=4)
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)

    

   
    


    

def addlabs ():
    print ("add a labour tpo sales")

# labour_details (ordnumb, linenumb, resource_numb , qty_reqd , qty_logged

    
    def doit():
             print("doit")
             ordnumbedt =        ordnumbbox. get()
             linenumbedt =       linennumbbox.get()
             resourceedt=        resourcebox.get()
             qtyreqdedt =        qtyreqdbox.get()
             qtyloggededt=       qtyloggedbox.get()
             


             c.execute("INSERT INTO labour_details  (ordnumb, linenumb, resource_numb, qty_reqd, qty_logged) VALUES(?,?,?,?,?)", (ordnumbedt, linenumbedt, resourceedt, qtyreqdedt, qtyloggededt))
            
    addrecframe =  ttk.Frame(root)
    ordnumb=       ttk.Label(addrecframe, text = "Sales order Number")
    linenumb=      ttk.Label(addrecframe, text = "Line number")
    resource=      ttk.Label(addrecframe, text=  "Resource")
    qtyreqd=       ttk.Label(addrecframe, text=  "Qty required")
    qtylogged=     ttk.Label(addrecframe, text=  "Qty logged")
    

    ordnumbbox =         ttk.Entry  (addrecframe)
    linennumbbox =       ttk.Entry  (addrecframe)
    resourcebox =        ttk.Entry  (addrecframe)
    qtyreqdbox  =     ttk.Entry  (addrecframe)
    qtyloggedbox=        ttk.Entry  (addrecframe)
    
        
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid    (column=0, row=0)
    ordnumb .grid       (column=0, row=0)
    linenumb.grid       (column=0, row=1)
    resource.grid       (column=0, row=2)
    qtyreqd.grid        (column=0, row=3)
    qtylogged.grid      (column=0, row=4)
    
        
        
    ordnumbbox.grid        (column= 1, row=0)
    linennumbbox.grid       (column= 1, row=1)
    resourcebox.grid       (column= 1, row=2)
    qtyreqdbox.grid     (column= 1, row=3)
    qtyloggedbox.grid      (column= 1, row=4)
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)

    

   
    



    

def addpurchdets():
    print ("add a new purchase order detail")
#  purchaseorders (pordernumb, linenumb, partnumb, qty_ordered, qty_received)


    def doit():
             print("doit")
             pordnumbedt =     pordnumbbox. get()
             linenumbedt =     linennumbbox.get()
             partnumbedt =     partnumbbox.get()
             qtyorderededt =   qtyorderedbox.get()
             qtyreceivededt=   qtyreceivedbox.get()
             


             c.execute("INSERT INTO purchaseorders  (pordernumb, linenumb, partnumb, qty_ordered, qty_received) VALUES(?,?,?,?,?)", (pordnumbedt, linenumbedt, partnumbedt, qtyorderededt, qtyreceivededt))
            
    addrecframe =    ttk.Frame(root)
    pordnumb=        ttk.Label(addrecframe, text = "Purchase order Number")
    linenumb=        ttk.Label(addrecframe, text = "Line number")
    partnumb=        ttk.Label(addrecframe, text=  "Part number")
    qtyordered=      ttk.Label(addrecframe, text=  "Qty ordered")
    qtyreceived=     ttk.Label(addrecframe, text=  "Qty received")
    

    pordnumbbox =          ttk.Entry  (addrecframe)
    linennumbbox =         ttk.Entry  (addrecframe)
    partnumbbox =          ttk.Entry  (addrecframe)
    qtyorderedbox  =       ttk.Entry  (addrecframe)
    qtyreceivedbox=        ttk.Entry  (addrecframe)
    
        
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
    
    
    addrecframe.grid      (column=0, row=0)
    pordnumb .grid        (column=0, row=0)
    linenumb.grid         (column=0, row=1)
    partnumb.grid         (column=0, row=2)
    qtyordered.grid       (column=0, row=3)
    qtyreceived.grid      (column=0, row=4)
    
        
        
    pordnumbbox.grid        (column= 1, row=0)
    linennumbbox.grid       (column= 1, row=1)
    partnumbbox.grid       (column= 1, row=2)
    qtyorderedbox.grid     (column= 1, row=3)
    qtyreceivedbox.grid      (column= 1, row=4)
    
        
    additbutton.grid (column=5, row=6)
    donebutton.grid  (column =4, row=6)

    
def addstok():
    print ("adding a stock record")
#   stock (partnumber, partdescript , uom, stockqty, supplier_code, cost, price
   
       
    def doit():
             print("doit")
             stoknumbedt = stoknumbbox.get()
             stokdescedt = stokdescbox.get()
             uomedt      = uombox.get()
             qtyedt      = qtybox.get()
             suppedt     = suppcodebox.get()
             costedt     = costbox.get()
             priceedt    = pricebox.get()

    
             c.execute ("select * from stock where partnumber = " + stoknumbedt)
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no stok")
                c.execute("INSERT INTO stock (partnumber, partdescript, uom, stockqty, supplier_code, cost, price) VALUES(?,?,?,?,?,?,?)", (stoknumbedt, stokdescedt, uomedt, qtyedt, suppedt, costedt, priceedt))
             else:
                 print ("stock exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "STOCK CODE  ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


         
         
         
    addrecframe = ttk.Frame(root)
    stoknumb=  ttk.Label(addrecframe, text = "StockNumber")
    stokdesc=  ttk.Label(addrecframe, text = "Stock description")
    uom      = ttk.Label(addrecframe, text=  "Unit of measure")
    qty      = ttk.Label(addrecframe, text=  "Qty in stock")
    suppcode = ttk.Label(addrecframe, text=  "Supplier code")
    cost     = ttk.Label(addrecframe, text=  "Cost")
    price    = ttk.Label(addrecframe, text=  "Price")

    
    stoknumbbox =          ttk.Entry  (addrecframe)
    stokdescbox =          ttk.Entry  (addrecframe)
    uombox =               ttk.Entry  (addrecframe)
    qtybox =               ttk.Entry  (addrecframe)
    suppcodebox  =         ttk.Entry  (addrecframe)
    costbox=               ttk.Entry  (addrecframe)
    pricebox =             ttk.Entry  (addrecframe)

           
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
 

    

        
      
    addrecframe.grid(column=0, row=0)
    stoknumb.grid  (column=0, row=0)
    stokdesc.grid  (column=0, row=1)
    uom.grid       (column=0, row=2)
    qty.grid       (column=0, row=3)
    suppcode.grid  (column=0, row=4)
    cost.grid      (column=0, row=5)
    price.grid     (column=0, row=6)
        
        
    stoknumbbox.grid   (column=1, row=0)
    stokdescbox.grid  (column=1, row=1)
    uombox.grid       (column=1, row=2)
    qtybox.grid       (column=1, row=3)
    suppcodebox.grid  (column=1, row=4)
    costbox.grid      (column=1, row=5)
    pricebox.grid     (column=1, row=6)
        
    additbutton.grid (column=5, row=5)
    donebutton.grid (column =4, row=5)
        

    

def addaresource():
    print ("Adding a resource")

     # resource (resource_numb, resource_desc, cost_per_hour, capacity_available, capacity_used

    def doit():
             print("doit")
             resonumbedt  = resonumbbox.get()
             resodescedt  = resodescbox.get()
             costedt      = costbox.get()
             avaledt      = avalbox.get()
             usededt      = usedbox.get()


    
             c.execute ("select * from resource  where resource_numb = " + resonumbedt)
             sw = c.fetchone()
             print (" sw is " ,sw)
             if sw == None:
                print ("no reso")
                c.execute("INSERT INTO resource (resource_numb, resource_desc, cost_per_hour, capacity_available, capacity_used) VALUES(?,?,?,?,?)", (resonumbedt, resodescedt, costedt, avaledt, usededt))
             else:
                 print ("resource exists")
                 warning = ttk.Frame(root)
                 warning.grid (column=0, row=20)
                 y1 = ttk.Label(warning, text= "RESOURCE CODE  ALREADY EXISTS")
                 b1 = ttk.Button(warning, text = "OK", command= warning.destroy)
                 b1.grid (column=0, row=2)
                 y1.grid (column=0, row=0)


         
         
         
    addrecframe = ttk.Frame(root)
    resonumb=     ttk.Label(addrecframe, text = "Resource Number")
    resodesc=     ttk.Label(addrecframe, text = "Resource description")
    cost     =    ttk.Label(addrecframe, text=  "Cost per hour")
    aval     =    ttk.Label(addrecframe, text=  "Capacity available")
    used =        ttk.Label(addrecframe, text=  "Capacity used")

    
    resonumbbox =           ttk.Entry  (addrecframe)
    resodescbox =           ttk.Entry  (addrecframe)
    costbox =               ttk.Entry  (addrecframe)
    avalbox =               ttk.Entry  (addrecframe)
    usedbox  =              ttk.Entry  (addrecframe)

           
    additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
    donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
 

    addrecframe.grid(column=0, row=0)
    resonumb.grid  (column=0, row=0)
    resodesc.grid  (column=0, row=1)
    cost.grid       (column=0, row=2)
    aval.grid       (column=0, row=3)
    used.grid  (column=0, row=4)
        
        
    resonumbbox.grid   (column=1, row=0)
    resodescbox.grid  (column=1, row=1)
    costbox.grid       (column=1, row=2)
    avalbox.grid       (column=1, row=3)
    usedbox.grid  (column=1, row=4)
        
    additbutton.grid (column=5, row=5)
    donebutton.grid (column =4, row=5)
        

def kexiqu(ktype):


    invfile=open (planajoblocn + "/genlist.txt", 'w')
    if ktype == 1:
        c.execute ("select * from customers ORDER BY custnumb")
        inv=""
        inv = "                        CUSTOMER LIST   \n"
        inv = inv + "_____________________________________________________________________________________________________________________________________\n"
        inv = inv + "Number                Name                  Addr1                 addr2                 addr3                 address 4            phone    \n"
        inv = inv + "_____________________________________________________________________________________________________________________________________\n"
    


    if ktype == 2:
        c.execute ("SELECT * FROM suppliers ORDER BY suppnumb")
        inv=""
        inv = "                        SUPPLIER LIST   \n"
        inv = inv + "_________________________________________________________________________________________________________________________________________\n"
        inv = inv + "Number                Name                  Addr1                 addr2                 addr3                 Addr4                 phone    \n"
        inv = inv + "__________________________________________________________________________________________________________________________________________\n"


    if ktype == 3:
        c.execute ("SELECT * FROM salesorders ORDER BY salesorders.ordnumb")
        inv=""
        inv = "                        SALES ORDER LIST   \n"
        inv = inv + "_______________________________________________________________________\n"
        inv = inv + "Order  Number       Customer name        Date Ordered        Date Reqd \n"
        inv = inv + "_______________________________________________________________________\n"
    

    if ktype == 5   :
        c.execute ("SELECT * FROM labour_details ORDER BY ordnumb")
        inv=""
        inv = "                        LABOUR ON ORDER    \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
        inv = inv + "Order  Number        Line Number        Resource Number     qTY Reqd          QTY logged       \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
   
    
    if ktype ==4 :
        c.execute ("SELECT * FROM partsordered ORDER BY ordnumb ")
        inv=""
        inv = "                        PARTS ON ORDER   \n"
        inv = inv + "________________________________________________________________________________________________________________\n"
        inv = inv + "Order Numb          Line number         Part number         Date ordered         Qty issued \n"
        inv = inv + "________________________________________________________________________________________________________________\n"
     

    if ktype == 6:
        c.execute ("SELECT * FROM porderheader")
        inv=""
        inv = "                        PURCHASE ORDER LIST   \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
        inv = inv + "Order  Number       Supplier             Date Ordered            Date Reqd            Date Deliv \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
  
    if ktype == 7:
        c.execute ("SELECT * FROM purchaseorders")
        inv=""
        inv = "                        PURCHASE ORDER DETAIL LIST   \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
        inv = inv + "Order  Number      Line number         Part Number         QTY ordered           Qty delivered  \n"
        inv = inv + "______________________________________________________________________________________________________________\n"
   

    if ktype == 8:
        c.execute ("SELECT * FROM  resource")
        inv=""
        inv = "                        RESOURCE LIST   \n"
        inv = inv + "_________________________________________________________________________________________________\n"
        inv = inv + "Resource Number     Resource Desc       Cost per hour       Capacity availabe     Capacity Used  \n"
        inv = inv + "_________________________________________________________________________________________________\n"

    if ktype == 9:
        c.execute("SELECT * FROM stock ORDER BY partnumber")
        inv=""
        inv = "                        STOCK LIST   \n"
        inv = inv + "________________________________________________________________________________________________________________________________\n"
        inv = inv + "Part number,        partdescript,       uom,                stockqty,            supplier_code,       cost,               price \n"
        inv = inv + "________________________________________________________________________________________________________________________________\n"
     


    if (ktype == 1) + (ktype == 2):
        for row in c:
            inv = inv + '%(number)-22s' %    {"number": row[0]}  
            inv = inv + '%(number)-22s' %    {"number": row[1]}
            inv = inv + '%(number)-22s' %    {"number": row[2]}
            inv = inv + '%(number)-22s' %    {"number": row[3]}
            inv = inv + '%(number)-22s' %    {"number": row[4]}
            inv = inv + '%(number)-22s' %    {"number": row[5]}
            inv = inv + '%(number)-22s' %    {"number": row[6]}  
            inv = inv + "\n"
            
        

    if (ktype == 4) + (ktype ==6) + (ktype == 5) + (ktype == 7) +(ktype == 8):
        for row in c:
            inv = inv + '%(number)-20s' %    {"number": row[0]}  
            inv = inv + '%(number)-20s' %    {"number": row[1]}
            inv = inv + '%(number)-20s' %    {"number": row[2]}
            inv = inv + '%(number)-21s' %    {"number": row[3]}
            inv = inv + '%(number)-21s' %    {"number": row[4]}

            inv = inv + "\n"

    if (ktype ==3):
       print ("sALES ORDERS")
       for row in c:
            inv = inv + '%(number)-20s' %    {"number": row[0]}  
            inv = inv + '%(number)-20s' %    {"number": row[1]}
            inv = inv + '%(number)-20s' %    {"number": row[2]}
            inv = inv + '%(number)-21s' %    {"number": row[3]}

            inv = inv + "\n"



    if (ktype == 9):
        print ("stock listing")
        print (ktype)
        for row in c:
            inv = inv + '%(number)-20s' %    {"number": row[0]}  
            inv = inv + '%(number)-20s' %    {"number": row[1]}
            inv = inv + '%(number)-20s' %    {"number": row[2]}
            inv = inv + '%(number)-21.5s' %  {"number": row[3]}
            inv = inv + '%(number)-21.5s' %  {"number": row[4]}
            inv = inv + '%(number)-21.5s' %  {"number": row[5]}
            inv = inv + '%(number)-20s' %    {"number": row[6]}  
            inv = inv + "\n"

         




    txt=Text(root, width=150)
    txt.insert(END, inv)
  
    invfile.write (inv)
    inv = ""
    invfile.close
 

# Set up window and file


    content2 = ttk.Frame(root)
    button2 = Button(content2, text = "Use gedit ??", command = usegeditcust)
    content2.grid(column=1, row=0)
    button2.grid(column=0, row=0)
    txt.grid (column=0, row=7)

 
    

def updatedblab(ordnum, linenum, qty):
   print ("Update labour")
   print ("updating db", ordnum, linenum, qty)
 
   sqlstring = "update labour_details set qty_logged  = qty_logged + " + repr(qty) +  "where ordnumb = " + repr(ordnum)+ " and linenumb = " + repr(linenum)
   print (sqlstring)
   c.execute(sqlstring)

   c.execute ("select resource_numb from labour_details  where ordnumb=" + repr (ordnum) + " and linenumb = " + repr(linenum))
   w = c.fetchone()
   print ("w is" , w)

   if w != None: 
      c.execute ("select capacity_available  from resource where resource_numb = ?", w) 
      print ("b4", c.fetchall())
      c.execute ("update resource  set capacity_available = capacity_available  - " + repr (qty) + " where resource_numb = ?", w)
      c.execute ("select capacity_available  from resource where resource_numb = ?",  w)
      print ("after", c.fetchall())

   

      
def updatesalespart (ordnum, linenum, qty):
   

   sqlstring = "update partsordered set qtyissued = qtyissued + " + repr(qty) +  "where ordnumb = " + repr(ordnum)+ " and linenubmb = " + repr(linenum)
   print (sqlstring)
   c.execute(sqlstring)

   c.execute ("select partnumb from partsordered where ordnumb=" + repr(ordnum) + "and linenubmb = " +repr(linenum))

   w = c.fetchone()
   print ("w is" , w)

   if w != None: 
      c.execute ("select stockqty from stock where partnumber = ?", w) 
      print ("b4", c.fetchall())
      c.execute ("update stock set stockqty = stockqty - " + repr (qty) + " where partnumber = ?", w)
      c.execute ("select stockqty from stock where partnumber = ?",  w)
      print ("after", c.fetchall())





def updatedbgrn(ordnum, linenum, qty):
   print ("updating db", ordnum, linenum, qty)
   sqlstring = "update purchaseorders set qty_received = qty_received  + " + repr(qty) +  "where pordernumb = " + repr(ordnum)+ " and linenumb = " + repr(linenum)
   print (sqlstring)
   c.execute(sqlstring)

   c.execute ("select partnumb from purchaseorders where pordernumb=" + repr (ordnum) + " and linenumb = " + repr(linenum))
   w = c.fetchone()
   print ("w is" , w)

   if w != None: 
      c.execute ("select stockqty from stock where partnumber = ?", w) 
      print ("b4", c.fetchall())
      c.execute ("update stock set stockqty = stockqty + " + repr (qty) + " where partnumber = ?", w)
      c.execute ("select stockqty from stock where partnumber = ?",  w)
      print ("after", c.fetchall())


 



def issstoktoorder():
    print ("Issue stock")
    getorddets(1)

def addlabourtoorder():
   print("Adding labour")
   getorddets(2)

def grn():
   print ("Goods received")
   getorddets(3)

   
   
    


def getorddets(type):
      print ("type", type)
      def doit():
         print ("doit")
         ordnum=ordnumbbox.get()
         linenum=linebox.get()
         qty=qtyissbox.get()
         print ("all entered", ordnum, linenum, qty)
         if type ==1 :
             updatesalespart(ordnum, linenum, qty)
         if type ==2:
            updatedblab(ordnum, linenum, qty)
         if type==3:
             updatedbgrn(ordnum, linenum, qty)
              
         
      addrecframe = ttk.Frame(root)
      ordnumb=      ttk.Label(addrecframe, text = "Order number")
      line =        ttk.Label(addrecframe, text = "Line number")
      qtyiss=       ttk.Label(addrecframe, text=  "Qty")


    
      ordnumbbox =        ttk.Entry  (addrecframe)
      linebox =           ttk.Entry  (addrecframe)
      qtyissbox =         ttk.Entry  (addrecframe)

           
      additbutton = ttk.Button (addrecframe, text = "OK",   command=doit)
      donebutton  = ttk.Button (addrecframe, text = "Done", command = addrecframe.destroy)
 

      addrecframe.grid   (column=0, row=0)
      ordnumb.grid       (column=0, row=0)
      line.grid          (column=0, row=1)
      qtyiss.grid        (column=0, row=2)

      ordnumbbox.grid    (column=1, row=0)
      linebox.grid       (column=1, row=1)
      qtyissbox.grid     (column=1, row=2)
      
        
      additbutton.grid (column=5, row=5)
      donebutton.grid (column =4, row=5)
   
    
# INVOICE



def printinvoice(ordnum):
   print ("printing invoice  parts", ordnum)
   txt=Text(root, width=150, height=200)

   invfile=open (planajoblocn + "/invoice.txt", 'w')
   invtot=0
   partstot=0
   labtot=0
   
# Print customer name

   c.execute ("select * from customers, salesorders where salesorders.custname = customers.custnumb and salesorders.ordnumb= " + repr(ordnum))
   inv=""
   for row in c:
      inv = "                        INVOICE    \n  \n  \n"
      inv = inv + "____________________________________________________________________________________________________\n"
      inv= inv  + "  Account number           " + '%(number)7d' %  {"number":row[0]} + "\n"
      inv = inv + "  Order number             " + '%(number)7s' %  {"number":ordnum} + "\n"
      inv = inv + "\n"
      inv = inv + '%(number)-20s' %  {"number": row[1]}
      inv = inv + "\n"
      inv = inv + '%(number)-20s' %  {"number": row[2]}
      inv = inv + "\n"
      inv = inv + '%(number)-21s' %  {"number":row[3]}
      inv = inv +"\n"
      inv = inv + '%(number)-21s' %  {"number": row[4]}
      inv = inv + "\n"
      inv = inv + "\n"
      print (inv),
      invfile.write(inv)
      txt.insert(END, inv)
      inv = ""
      
# Print out the parts

   c.execute("select p.linenubmb, p.partnumb, p.qtyissued, s.partdescript, s.price from partsordered p, stock s where p.partnumb = s.partnumber and p.ordnumb=" +  repr(ordnum))
   invfile.write ("             PARTS SUPPLIED           \n\n")
   txt.insert(END, "                   PARTS SUPPLIED        \n\n")
   partsheading="Line        Part        Qty        Part Desc                         Price         Total\n\n"
   invfile.write(partsheading)
   txt.insert(END, partsheading)
   partstot=0
   partstotr=0

   inv=""
   for row in c:
      inv= '%(number)7d' %  {"number":row[0]}
      inv = inv + '%(number)8d' %  {"number": row[1]}
      inv = inv + '%(number)13.5f' %  {"number": row[2]}
      inv = inv + '%(number)21s' %  {"number":row[3]}
      inv = inv + '                 %(number)8.2f' %  {"number": row[4]}
      inv = inv + ' %(number)13.2f' %  {"number": row[2]*row[4]}
      inv = inv + "\n"
      print (inv),
      invfile.write(inv)
      txt.insert(END, inv)
      inv = ""
      partstot =  partstot+ (row[2]*row[4])   
      partstotr = partstot


   line = "_____________".rjust(88)
   partstot = '%(number)88.2f' % {"number":partstot}
   invfile.write (line+ "\n")
   txt.insert(END, (line+"\n"))
   invfile.write (str(partstot)+"\n")
   txt.insert(END, str(partstot+"\n"))
   
# Print out labour   


   c.execute("select l.linenumb, l.resource_numb, l.qty_logged, r.resource_desc, r.cost_per_hour from labour_details l, resource r where l.resource_numb = r.resource_numb  and l.ordnumb=" +  repr(ordnum))
   invfile.write ("             BOOKED LABOUR           \n\n")
   txt.insert(END, "                   BOOKED LABOUR        \n\n")
   labourheading="Line        Labour Id        Hrs        Labour Desc         Price per hour         Total\n\n"
   invfile.write(labourheading)
   txt.insert(END, labourheading)
   labtot=0
   labtotr=0
   invtotr=0
   print ("FINDING LAB DETS")
   
   inv=""
   for row in c:
      inv= '%(number)7d' %  {"number":row[0]}
      inv = inv + '%(number)8d' %  {"number": row[1]}
      inv = inv + '%(number)17.5f' %  {"number": row[2]}
      inv = inv + '%(number)19s' %  {"number":row[3]}
      inv = inv + '%(number)23.2f' %  {"number": row[4]}
      inv = inv + '%(number)14.2f' %  {"number": row[2]*row[4]}
      inv = inv + "\n"
      print (inv), "labor dets"
      
      invfile.write(inv)
      txt.insert(END, inv)
      inv = ""
      labtot =  labtot+ (row[2]*row[4])
      labtotr = labtot
          
   line = "_____________".rjust(88)
   labtot = '%(number)88.2f' % {"number":labtot}
   invfile.write (line+ "\n")
   txt.insert(END, (line+"\n"))
   invfile.write (str(labtot)+"\n")
   txt.insert(END, str(labtot) +"\n")

#   Print invoice total

   invtotr = labtotr + partstotr
   vatr = invtotr * vatrate /100
   grandtot = invtotr+vatr
   invtotr = '%(number) 10.2f' %{"number":invtotr}
   invfile.write  ("\n\n"     + "INVOICE TOTAL = " + str(invtotr) +"\n")   
   txt.insert(END, "\n\n"     + "INVOICE TOTAL = " +str(invtotr) +"\n")
   vatr = '%(number) 10.2f' %{"number":vatr}
   txt.insert (END, "VAT =           " + str (vatr) + "\n")
   invfile.write ("VAT =           " +str(vatr) + "\n")
   invfile.write ("__________________________ \n")
   txt.insert (END, "__________________________ \n")
   grandtot  = '%(number) 10.2f' %{"number":grandtot}
   invfile.write ("GRAND TOTAL =   " +str(grandtot) + "\n\n\n")
   txt.insert(END, "GRAND TOTAL =   " + str (grandtot) + "\n\n\n")




 
   txt.insert(END, inv)
   print ("ready", inv)
  
   invfile.write (inv)
   inv = ""
   invfile.close
 
   
 

# Set up window and file


   content2 = ttk.Frame(root)
   button=    Button (content2, text= "Close", command = txt.destroy)
   button2 =  Button (content2, text = "Use gedit ??", command = usegedit2)
   content2.grid     (column=1, row=0)
   button2.grid      (column=0, row=0)
   button.grid       (column=0, row=5)
                   
   txt.grid (column=0, row=7)

 
def usegedit2():
   print ("inv gedit")
   os.chdir (planajoblocn)
   os.system ("gedit invoice.txt")


def invoice():
     def invoiceok():
         ordnum=w1.get()
         top2.destroy()
         printinvoice(ordnum)
     top2 = Toplevel()
     top2.title("INVOICE")
     l1 = Label(top2, text="Enter Order number")
     l1.pack()
     w1 = Entry(top2, width=50)
     w1.pack()
     # w1.insert(0, "Order number")
     w1.focus_set()
     b1 = Button(top2, text="OK", command=invoiceok)
     b1.pack()

   
   
   
# Now for the main window


content =    ttk.Frame (root, padding=(3,3,3,3))
salesframe = ttk.Frame (content, borderwidth=7, relief="sunken")
purchframe = ttk.Frame (content, borderwidth=7, relief="sunken")
stokframe =  ttk.Frame (content, borderwidth=7, relief="sunken")
laborframe=  ttk.Frame (content, borderwidth=7, relief="sunken")
setupframe=  ttk.Frame (content, borderwidth=7, relief="sunken")


saleslbl =    ttk.Label(salesframe, text= "SALES")
purchaselbl = ttk.Label(purchframe, text= "PURCHASING")
stoklbl=      ttk.Label(stokframe,  text= "STOCK")
laborlbl=     ttk.Label(laborframe, text= "LABOUR")
setuplbl=     ttk.Label(setupframe, text= "SETUP")

saleslbl.grid   (column=0, row=0)
purchaselbl.grid(column=0, row=0)
stoklbl.grid    (column=0, row=0)
laborlbl.grid   (column=0, row=0)
setuplbl.grid   (column=0, row=0)


salesframe.grid(column=4,  row=0)
purchframe.grid(column=8,  row=0)
stokframe. grid(column=16, row=0)
laborframe.grid(column=24, row=0)
setupframe.grid(column=32, row=0)



listcust =         ttk.Button(salesframe,  text=  "List customers",             command = listcust)
addcust =          ttk.Button(salesframe,  text=  "Add a customer",             command=addcust)
addsalesord=       ttk.Button(salesframe,  text=  "Add a sales order",          command=addasalesorder )
listords =         ttk.Button(salesframe,  text=  "List Sales orders",          command = listords)
addparts=          ttk.Button(salesframe,  text=  "Add parts to a sales order", command=addpartstoorder)
addlabtoord=            ttk.Button(salesframe,  text = "Add labour to an order",     command=addlabs)
listpart=          ttk.Button(salesframe,  text=  "List parts on order",        command= listparts)
listlaborordr=     ttk.Button(salesframe,  text=  "List labour on order",       command= listlabbs)
issstoktoorder=    ttk.Button(salesframe,  text=  "Issue stock to an order",    command= issstoktoorder)
addlabtoorder =    ttk.Button(salesframe,  text=  "Log labour to order",        command= addlabourtoorder)
invoiceprint =     ttk.Button(salesframe,  text=  "Print an invoice",           command=invoice)

listsupps =        ttk.Button (purchframe, text=  "List Suppliers",       command = listpurch)
listpurchords =    ttk.Button (purchframe, text=  "List Purchase orders", command= listpurchaseorders)
addpurchorders=    ttk.Button (purchframe, text=  "Add a purchase order", command = addpurchord)
addsupp  =         ttk.Button (purchframe, text=  "Add a supplier",       command= addsupp)
addpurchdets=      ttk.Button (purchframe, text=  "Add purchase details", command = addpurchdets)
listpurchdets=     ttk.Button (purchframe, text=  "List purchase details",command=listpurchasedets)
grn=               ttk.Button (purchframe, text=  "Goods received",       command=grn)

listlaborb =       ttk.Button (laborframe, text=   "List labour details", command= listlabor)
addlab      =      ttk.Button (laborframe, text=   "Add a resource",      command= addaresource)

liststok  =        ttk.Button (stokframe,  text=   "List stock items",    command= liststok)
addstok   =        ttk.Button (stokframe,  text=   "Add a stock item",    command= addstok)

setup =            ttk.Button (setupframe, text=   "Setup",               command= setup)



content.grid(column=0, row=10, sticky=(N, S, E, W))

listcust.grid        (column=0, row=3)
addcust.grid         (column=0, row=4)
addsalesord.grid     (column=0, row=5)
addparts.grid        (column=0, row=6)
addlabtoord.grid     (column=0, row=7)
listords.grid        (column=0, row=8)
listpart.grid        (column=0, row=9)
listlaborordr.grid   (column=0, row=10)
issstoktoorder.grid  (column=0, row=11)
addlabtoorder.grid   (column=0, row=12)
invoiceprint.grid    (column=0, row=13)

listsupps.grid       (column=0, row=3)
addsupp.grid         (column=0, row=4)
addpurchorders.grid  (column=0, row=5)
addpurchdets.grid    (column=0, row=6)
listpurchords.grid   (column=0, row=7)
listpurchdets.grid   (column=0, row=8)
grn.grid             (column=0, row=9) 

listlaborb.grid      (column=0, row=4)
addlab.grid          (column=0, row=5)


liststok.grid        (column=0, row=1)
addstok.grid         (column=0, row=2)


setup.grid (column =0, row=6)

root.mainloop()

