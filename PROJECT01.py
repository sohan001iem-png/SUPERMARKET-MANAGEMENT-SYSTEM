import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter import messagebox
from tkinter import ttk
import smtplib#to connect the program to Gmail server
import random#to generate otp, order id, customer id
import datetime#to input current date and time on system
import csv
import os
if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MARKET_FILE=os.path.join(BASE_DIR,"market.csv")
CUSTOMER_FILE=os.path.join(BASE_DIR,"customers.csv")
def gui_message(title,msg):
        if title=="Info":
                messagebox.showinfo(title,msg)
        elif title=="Error":
                messagebox.showerror(title,msg)
        elif title=="Warning":
                messagebox.showwarning(title,msg)
def gui_input(prompt):
        value=askstring("Input Required",prompt)
        if value is None:
                return None
        return value.strip()
def gui_num_input(prompt,*,num_type=int,min_val=0,max_val=None,length=None,allow_zero=True,round_to=None):# return valid number as per corresponding format
        while True:
                val=gui_input(prompt)
                if val is None:
                        return None
                try:
                        num=num_type(val)
                        if not allow_zero and num == 0:
                                raise ValueError
                        if num < min_val:
                                raise ValueError
                        if max_val is not None and num > max_val:
                                raise ValueError
                        if length is not None and len(val) != length:
                                raise ValueError
                        if round_to is not None and num_type is float:
                                num=round(num, round_to)
                        return num
                except ValueError:
                        messagebox.showerror("Invalid Input",f"Please enter a valid {num_type.__name__}")
def gui_choice(prompt,options,title="Select Option"):
        result={"value":None}
        win=tk.Toplevel()
        win.title(title)
        win.resizable(False,False)
        win.grab_set()
        tk.Label(win,text=prompt,font=("Arial",11)).pack(pady=10)
        btn_frame=tk.Frame(win)
        btn_frame.pack(pady=5)
        def select(val):
                result["value"]=val
                win.destroy()
        for val,text in options:
                tk.Button(btn_frame,text=text,width=20,command=lambda v=val: select(v)).pack(pady=3)
        win.wait_window()
        return result["value"]
def show_table(title, columns, rows, widths=None):
        win=tk.Toplevel()
        win.title(title)
        win.geometry("900x400")
        frame=tk.Frame(win)
        frame.pack(fill="both",expand=True)
        tree=ttk.Treeview(frame,columns=columns,show="headings")
        tree.pack(side="left",fill="both", expand=True)
        scrollbar=ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        for col in columns:
                tree.heading(col,text=col)
                tree.column(col,anchor="center",width=widths[col] if widths else 150)
        for row in rows:
                tree.insert("","end",values=row)
def show_bill_gui(bill):
        win=tk.Toplevel()
        win.title("Bill Receipt")
        win.geometry("900x600")
        tk.Label(win,text="SUPERMARKET",font=("Arial",18,"bold")).pack()#HEADER
        tk.Label(win,text="CASH RECEIPT",font=("Arial",14,"bold")).pack()
        now=bill["datetime"]
        tk.Label(win,text=f"Order ID: {bill['order_id']} | Date: {now.strftime('%d-%m-%Y %H:%M:%S')}",font=("Arial",10)).pack(pady=5)
        frame=tk.Frame(win)#TABLE
        frame.pack(fill="both",expand=True,padx=10)
        columns=("Item","Quantity","Unit Price","GST","Total")
        tree=ttk.Treeview(frame,columns=columns,show="headings")
        tree.pack(side="left",fill="both",expand=True)
        scrollbar=ttk.Scrollbar(frame, orient="vertical",command=tree.yview)
        scrollbar.pack(side="right",fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        for col in columns:
                tree.heading(col,text=col)
                tree.column(col,anchor="center",width=150)
        for item in bill["items"]:
                tree.insert("","end",values=(item["name"],item["qty"],item["rate"],item["gst"],round(item["cost"],2)))
        summary=tk.Frame(win)#SUMMARY
        summary.pack(fill="x",pady=10)
        tk.Label(win,text=f"TOTAL: ₹{round(bill['total'])}",font=("Arial",12,"bold")).pack(anchor="w",padx=20)
        tk.Label(win,text=f"PAID: ₹{round(bill['paid'])}").pack(anchor="w",padx=20)
        tk.Label(win,text=f"DUE: ₹{round(bill['due'])}").pack(anchor="w",padx=20)
        tk.Label(win,text=f"PAYMENT MODE: {bill['payment'][0]}").pack(anchor="w",padx=20)
        tk.Label(win,text=f"Rupees {num_to_words(round(bill['total']))} only",font=("Arial",10,"italic")).pack(pady=5)      
        tk.Label(win,text="THANK YOU, PLEASE VISIT AGAIN!",font=("Arial",12,"bold")).pack(pady=10)
def create_bill_pdf(bill,filename):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        c=canvas.Canvas(filename,pagesize=A4)
        width,height=A4
        y=height-50
        c.setFont("Helvetica-Bold",14)
        c.drawCentredString(width/2,y,"SUPERMARKET BILL")
        y-=40
        c.setFont("Helvetica", 10)
        c.drawString(40,y,f"Customer:{bill['customer']}")
        y-=15
        c.drawString(40,y,f"Mobile:{bill['mobile']}")
        y-=15
        c.drawString(40,y,f"Order ID:{bill['order_id']}")
        y-=30
        c.drawString(40,y,"Item")
        c.drawString(200,y,"Qty")
        c.drawString(250,y,"Rate")
        c.drawString(320,y,"GST")
        c.drawString(380,y,"Amount")
        y-=15
        c.line(40,y,width-40,y)
        for item in bill["items"]:
                y-=15
                c.drawString(40,y,item["name"])
                c.drawString(200,y,str(item["qty"]))
                c.drawString(250,y,str(item["rate"]))
                c.drawString(320,y,str(item["gst"]))
                c.drawString(380,y,str(round(item["cost"],2)))
        y-=30
        c.drawString(40,y,f"TOTAL: ₹{round(bill['total'],2)}")
        y-=15
        c.drawString(40,y,f"PAID: ₹{round(bill['paid'],2)}")
        y-=30
        payment_mode=bill["payment"][0]#Payment details
        c.drawString(40,y,f"PAYMENT MODE: {payment_mode}")
        y-=20
        if payment_mode == "DEBIT CARD":
                c.drawString(40,y-15,f"Card ending with: {str(bill['payment'][1])[-4:]}")
        amount_words=num_to_words(round(bill["total"]))#Amount in words
        c.drawString(40,y,f"Rupees {amount_words} only")
        y-=40
        c.setFont("Helvetica-Bold",11)
        c.drawCentredString(width/2,y,"THANK YOU,PLEASE VISIT AGAIN!")
        c.save()
def generate_bill_data(litem,lqty,lrate,lgst,lcost,total_cost,amt,name,mob,payment_info,oid):
        items=[]
        for i in range(len(litem)):
                items.append({"name":litem[i],"qty":lqty[i],"rate":lrate[i],"gst":lgst[i],"cost":lcost[i]})
        bill={"items":items,"total":total_cost,"paid":amt,"due":total_cost-amt,"customer":name,"mobile":mob,"payment":payment_info,"order_id":oid,"datetime":datetime.datetime.now()}
        return bill
def print_bill_physical(bill):
        lines=[]
        lines.append("SUPERMARKET")
        lines.append("CASH RECEIPT")
        lines.append("-"*40)
        for i, item in enumerate(bill["items"],start=1):
                lines.append(f"{i}. {item['name']}  {item['qty']}  ₹{item['cost']}")
        lines.append("-"*40)
        lines.append(f"TOTAL: ₹{round(bill['total'])}")
        lines.append(f"PAID: ₹{round(bill['paid'])}")
        lines.append(f"DUE: ₹{round(bill['due'])}")
        lines.append(f"ORDER ID: {bill['order_id']}")
        text = "\n".join(lines)
        with open("temp_bill.txt","w",encoding="utf-8") as f:
                f.write(text)
        os.startfile("temp_bill.txt","print")
def AcptId(x,s):# accept valid item id based on operation
        while True:
                if s=="REPLACE":
                        r=gui_input("ENTER ITEM NAME:")
                elif s=="OID":
                        r=gui_input("ENTER ORDER ID:")
                else:
                        r=gui_input("ENTER ITEM ID:")
                if r is None:#input cancelled
                        return None
                if r=='0' or r in x:#Valid input or exit loop
                        return r
                if s=="RETURN":#messagebox.showerror(title,message)
                        messagebox.showerror("INVALID ITEM","ITEM ID NOT TAKEN BY CUSTOMER:")
                elif s in ("BUY","EDIT"):
                        messagebox.showerror("INVALID ITEM","ITEM ID NOT AVAILABLE IN MARKET:")
                elif s=="OID":
                        messagebox.showerror("INVALID ID","ORDER ID NOT FOUND:")
                elif s=="REPLACE":
                        messagebox.showerror("INVALID ITEM","ITEM NOT BOUGHT BY CUSTOMER")
def otp_verification(xotp):#function for otp verification
        ootp=gui_num_input("otp")
        if ootp is None or ootp!=xotp:# xotp is system generated
                return "UNSUCCESSFUL"
        else:
                return "SUCCESSFUL"
def num_to_words(n):#print a number in words
        s=str(n)
        l=len(s)#stores number of digits in the number
        wd=""
        unit=('','ONE ','TWO ','THREE ','FOUR ','FIVE ','SIX ','SEVEN ','EIGHT ','NINE ')
        ttns=('TEN ','ELEVEN ','TWELVE ','THIRTEEN ','FOURTEEN ','FIFTEEN ','SIXTEEN ','SEVENTEEN ','EIGHTEEN ','NINETEEN ')
        tens=('','','TWENTY ','THIRTY ','FORTY ','FIFTY ','SIXTY ','SEVENTY ','EIGHTY ','NINETY ')
        listplcvalue={}#stores place value of the digits as key and digit as value
        m=n
        for x in range(l,0,-1):
                p=n//10**(x-1)
                listplcvalue[x]=p
                n=n%10**(x-1)
        def concatC(y):
                wr=""
                if y==6 or y==4 or y==3 or y==1:
                        k=listplcvalue[y]
                        wr=wr+unit[k]
                else:
                        wr=""
                if  y==7 or y==6:
                        wr=wr+"LAKHS "
                elif y==5 or y==4:
                        wr=wr+"THOUSAND "
                elif y==3:
                        wr=wr+"HUNDRED "
                elif y==2 or y==1:
                        wr=wr+""
                return(wr)
        def concatA(x):#for concatenation of words for digits  in 10lakhs, 10thousands and tens place
                w=""
                q=listplcvalue[x]
                r=listplcvalue[x-1]
                m=q*10+r
                if m>=10 and m<=19:
                        w=w+ttns[r]
                elif m>=20 and m<=99:
                        w=w+tens[q]+unit[r]
                if listplcvalue[j]==0:
                        w=""
                else:
                        w=w+concatC(x)
                return(w)
        def concatB(x):#for concatenation of words for digits  in 1 lakhs, 1 thousands and ones place
                w=""
                if (x+1) in list(listplcvalue.keys()):
                        if listplcvalue[x]==0 or listplcvalue[x+1]!=0:
                                w=w+""
                        else:
                                w=w+concatC(x)
                else:
                        w=w+concatC(x)
                return(w)
        if m==0:
                wd="ZERO"
        for j in range(l,0,-1):
                if j==7:
                        add=concatA(j)
                elif j==6:
                        add=concatB(j)
                elif j==5:
                        add=concatA(j)
                elif j==4:
                        add=concatB(j)
                elif j==3:
                        if listplcvalue[j]==0:
                                add=""
                        else:
                                add=concatC(j)
                elif j==2:
                        add=concatA(j)
                elif j==1:
                        add=concatB(j)
                wd=wd+add
        return(wd)
def mail_validity():#return valid email id
        while True:
                mail=gui_input("Enter customer mail id:")
                if mail is None:
                        return None
                while  mail.endswith('@gmail.com')==False:
                        mail=gui_input("Enter valid customer mail id:")
                        if mail is None:
                                return None
                l=mail.split('@gmail.com')
                c=0
                for i in l[0]:#gmail id can contain only lowercase letters, digits and '.'
                        if i.islower()==True or i=='.' or i.isdigit()==True:
                                c+=1
                if c!=len(l[0]):
                        gui_message("Warning","Invalid Email")
                else:
                        return(mail)
def send_mail(mail,x,s):#function to send mail to customer
        sender_email='sohan.project29@gmail.com'
        sender_password=os.getenv("MAIL_PASSWORD")
        if s in("OTP","USER ID"):
                if s=="OTP":#mail sent as otp to customer
                        subject='SUPERMARKET OTP'
                        body=f'Your OTP is: {x}.Thank you for visiting our shopping facility!'
                elif s=="USER ID":#mail sent as user id to customer
                        subject='SUPERMARKET USER ID'
                        body=f'Your USER ID is: {x}.Thank you for visiting our shopping facility!'
                message=f'Subject: {subject}\n\n{body}'
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email,sender_password)
                        server.sendmail(sender_email,mail,message)
        elif s=="BILL":#copy of bill sent to customer via mail
                from email.message import EmailMessage
                msg=EmailMessage()
                msg["Subject"]="Your Supermarket Bill"
                msg["From"]=sender_email
                msg["To"]=mail
                msg.set_content("Thank you for shopping with us.\n""Please find your bill attached.\n\n""Regards,\nSupermarket Team")
                with open(x,"rb") as f:
                        msg.add_attachment(f.read(),maintype="application",subtype="pdf",filename=os.path.basename(x))
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
def date_validity(x,cd):
        import datetime
        while True:
                crnt_date=datetime.datetime.now().date()
                try:
                        if x=="N":
                                exp_date=gui_input("Enter card expiry date (MM/YY):")
                                if exp_date is None:
                                        return "INVALID"
                                expiry_date=datetime.datetime.strptime(exp_date, "%m/%y") # Get the current date
                                if crnt_date<expiry_date:
                                        return "VALID"
                                else:
                                        return "INVALID"
                except ValueError:
                                gui_message("Warning","INVALID DATE. PLEASE TRY AGAIN")
                                continue
                except Exception as e:
                                print(e)
                                break
                else:
                                break
def PayProcess(mail,at,cd):#function for processing payment
        attempts=0
        br=''
        while attempts<3:   
                n=gui_choice("Select operation",[(1,"CASH"),(2,"DEBIT CARD"),(3,"UPI")])
                if n is None:
                        return None
                iotp=random.randint(100000,999999)
                if n==2:
                        dno=gui_num_input("Enter card number",length=16)
                        if dno is None:
                                continue
                        pr=date_validity("N",cd)#check and return whether card being used is valid or not
                        while pr=="INVALID":
                                gui_message("Warning","CARD NOT VALID")
                                pr=date_validity("N",cd)
                        cvv=gui_num_input("Enter CVV",length=3)
                        if cvv is None:
                                continue
                        send_mail(mail,iotp,"OTP")
                        gui_message("Info",f"Processing payment of Rs. {at} using debit card ending with {str(dno)[-4:]}...")
                elif n in [1,3]:
                        send_mail(mail,iotp,"OTP")
                        gui_message("Info","OTP sent successfully!")
                br=otp_verification(iotp)
                if br=="SUCCESSFUL":
                        gui_message("Info","PAYMENT SUCCESSFUL")
                        if n==2:
                                return ("DEBIT CARD",dno)
                        elif n==1:
                                return ("CASH",)
                        elif n==3:
                                return ("UPI",)
                attempts+=1
                gui_message("Warning","OTP verification failed. Try again.")
        gui_message("Error","Maximum OTP attempts exceeded")
        return None
def AddCustomerDetails():
        name=gui_input("Enter Customer name:")
        if name is None:
                return
        name=name.upper()
        mob=gui_input("phone number")
        if mob is None:
                return
        with open(CUSTOMER_FILE,"r",newline="",encoding="utf-8") as f:
                reader=csv.DictReader(f)
                for row in reader:#check if customer already exists
                        if name ==row["CUSTOMER_NAME"] and str(mob)==row["MOBILE"]:
                                gui_message("Info","CUSTOMER DETAILS ALREADY SAVED")
                                return None
        customer_mail=mail_validity()
        if customer_mail is None:
                gui_message("Warning","Customer registration cancelled")
                return
        uid=chr(random.randint(65,90))+chr(random.randint(65,90))+str(random.randint(100000,999999))
        send_mail(customer_mail,uid,"USER ID")#creating unique user id
        gui_message("Info","User ID sent to customer")
        with open(CUSTOMER_FILE,"a",newline="",encoding="utf-8") as f:
                writer=csv.DictWriter(f,fieldnames=["USER_ID","CUSTOMER_NAME","MOBILE","MAIL"])
                writer.writerow({"USER_ID":uid,"CUSTOMER_NAME":name,"MOBILE":str(mob),"MAIL":customer_mail})
def ViewCustomerDetails():
        with open(CUSTOMER_FILE,"r",newline="",encoding="utf-8") as f:
                customers=list(csv.DictReader(f))
        if not customers:
                gui_message("Info","NO CUSTOMER RECORDS FOUND")
                return
        columns=["USER_ID","CUSTOMER_NAME","MOBILE","MAIL"]
        rows=[]
        for c in customers:
                rows.append((c["USER_ID"],c["CUSTOMER_NAME"],c["MOBILE"],c["MAIL"]))
        show_table(title="Customer Details",columns=columns,rows=rows,widths={"USER_ID":120,"CUSTOMER_NAME":220,"MOBILE":140,"MAIL":260})
def ViewMarketDetails():
        with open(MARKET_FILE,"r",newline="",encoding="utf-8") as f:
                items=list(csv.DictReader(f))#list of dictionaries as(item id: item name, quantity,unit price, gst) format
        if not items:
                gui_message("Info","NO ITEMS AVAILABLE IN MARKET")
                return
        columns=["SNO","ITEM_NAME","STOCK","UNIT_PRICE","GST"]
        rows=[]
        for item in items:
                rows.append((item["SNO"],item["ITEM_NAME"],item["STOCK"],item["UNIT_PRICE"],item["GST"]))
        show_table(title="Market Inventory",columns=columns,rows=rows,widths={"SNO": 100,"ITEM_NAME": 260,"STOCK": 100,"UNIT_PRICE": 160,"GST": 100})
def EditStock():
        a=gui_choice("Select operation",[(1,"Add Item"),(2,"Remove Item"),(3,"Renew stock")])
        if a is None:
                return
        gui_message("Info","Enter 0 to finish list")
        with open(MARKET_FILE,"r",newline="",encoding="utf-8") as f:
                items=list(csv.DictReader(f))
        idlist=[]
        for item in items:
                idlist.append(item["SNO"])
        if a==1:#addition of items to stock in database
                while True:
                        idd=gui_input("Enter item id to be added:")
                        if  idd=='0':
                                break
                        if idd in idlist:
                                gui_message("Info","Item id exists in market")
                                continue
                        qty=gui_num_input("quantity")
                        cost=gui_num_input("price per unit:Rs.")
                        gst=0.18*cost
                        name=gui_input("Enter item name:")
                        with open(MARKET_FILE,"a",newline="",encoding="utf-8") as f:
                                writer=csv.DictWriter(f,fieldnames=["SNO","ITEM_NAME","STOCK","UNIT_PRICE","GST"])
                                writer.writerow({"SNO":idd,"ITEM_NAME":name,"STOCK":qty,"UNIT_PRICE":cost,"GST":gst})
        elif a==2 or a==3:#REMOVE/RENEW
                while True:
                        idd=AcptId(idlist,"EDIT")
                        if idd=='0':
                                break
                        if a==2:
                                for item in items:
                                        if item["SNO"]==idd:
                                                items.remove(item)
                                                gui_message("Info","ITEM REMOVED")
                                                break
                        elif a==3:
                                qty=gui_num_input("Enter quantity",min_val=1)
                                for item in items:
                                        if item["SNO"]==idd:
                                                item["STOCK"]=str(int(item["STOCK"])+qty)
                                                gui_message("Info","STOCK RENEWED")
                                                break
                        with open(MARKET_FILE,"w",newline="",encoding="utf-8") as f:
                                writer=csv.DictWriter(f,fieldnames=["SNO","ITEM_NAME","STOCK","UNIT_PRICE","GST"])
                                writer.writeheader()
                                writer.writerows(items)
def CheckStock():
        with open(MARKET_FILE,"r",newline="",encoding="utf-8") as f:
                items=list(csv.DictReader(f))
        if not items:
                return
        out_of_stock=[]
        for item in items:
                if int(item["STOCK"]) == 0:
                        out_of_stock.append((item["SNO"],item["ITEM_NAME"]))
        if not out_of_stock:# everything fine
                return
        show_table(title="Out of Stock Items",columns=["ITEM ID", "ITEM NAME"],rows=out_of_stock,widths={"ITEM ID": 120, "ITEM NAME": 300})#Show table
        choice=gui_choice("Some items are out of stock. What would you like to do?",[(1, "Edit Inventory"), (2, "Ignore")])# 2Ask what to do
        if choice==1:
                EditStock()
def NewBill_Generation():
        from copy import deepcopy
        import datetime
        marketid=[]
        lid=[]# lid stores item id
        litem=[]#litem stores item names
        llength=[]#llength stores length of item names
        lqty=[]#lqty stores quantity of items
        lrate=[]#lrate stores unit price of items
        lgst=[]#lgst stores gst amount
        lcost=[]#lcost stores total cost of individual items
        gui_message("Info","Enter 0 to finish list")
        with open(MARKET_FILE,"r",newline="",encoding="utf-8") as f:
                market_items=list(csv.DictReader(f))
                working_items=deepcopy(market_items)
        if not working_items:
                gui_message("Warning","NO ITEMS AVAILABLE IN MARKET")
                return
        for m in working_items:
                marketid.append(m["SNO"])
        while True:#input item details being bought
                item=AcptId(marketid,"BUY")
                if item=="0":
                        break
                lid.append(item)
                found=False
                for m in working_items:
                        if m["SNO"]==item:
                                found=True
                                stock=int(m["STOCK"])
                                name=m["ITEM_NAME"]
                                price=float(m["UNIT_PRICE"])
                                gst=float(m["GST"])
                                break
                if not found:
                        gui_message("Warning","ITEM NOT FOUND")
                        continue
                qty=gui_num_input("Enter quantity",min_val=1)
                if qty>stock:
                        gui_message("Warning","STOCK NOT SUFFICIENT TO FULFILL ORDER")
                        continue
                m["STOCK"]=str(stock-qty)#update stock in memory
                litem.append(name)
                llength.append(len(name))
                lrate.append(price)
                lgst.append(gst)
                lqty.append(qty)
                cost=qty*(price+gst)#store total cost of similar items bought
                lcost.append(cost)
        total_cost=sum(lcost)
        gui_message("Info",f"Total amount= Rs.{round(total_cost)}\n{num_to_words(round(total_cost))}")
        ask=gui_choice("Do you want to return any item(s) ?",[("yes", "Yes"), ("no", "No")],title="Confirmation")
        if ask=='yes':
                gui_message("Info","Enter 0 to finish list")
                while True:
                        item=AcptId(lid,"RETURN")
                        if item=="0":
                                break
                        qty=gui_num_input("Enter quantity",min_val=1)
                        while qty >lqty[lid.index(item)]:
                                gui_message("Warning","Number of items to be returned is greater than number of items bought")
                                qty=gui_num_input("Enter quantity",min_val=1)
                        idx=lid.index(item)
                        rate=lrate[lid.index(item)]
                        gst=lgst[lid.index(item)]
                        cost=lcost[lid.index(item)]
                        refund=qty*(rate+gst)
                        lcost[lid.index(item)]=cost-refund
                        lqty[idx]-=qty
                        for m in working_items:
                                if m["SNO"]==item:
                                        m["STOCK"]=str(int(m["STOCK"])+qty)
        total_cost=sum(lcost)
        oid=random.randint(100000,999999)
        gui_message("Info",f"Amount to be paid: ₹{round(total_cost)}\n"f"(inclusive of all taxes)\n"f"{num_to_words(round(total_cost))}")
        ask=gui_choice("Is the customer already registered?",[("yes","Yes"),("no","No")],title="Confirmation")
        if ask=='no':
                sk=gui_choice("Do you want to save your details?",[("yes","Yes"),("no","No")],title="Confirmation")
                if sk=='yes':
                        AddCustomerDetails()
                        name=gui_input("Enter customer name:")
                        mob=gui_num_input("phone number")
                        customer_mail=mail_validity()
        else:#accept user id from customer and obtain necessary details from database
                uid=gui_input("Enter user id:")
                with open(CUSTOMER_FILE,"r",newline="",encoding="utf-8") as f:
                        customers=list(csv.DictReader(f))
                user=None
                for row in customers:
                        if row["USER_ID"]==uid:
                                user=row
                                break
                while user is None:
                        uid=gui_input("Id not found. Enter valid user id:")
                        for row in customers:
                                if row["USER_ID"]==uid:
                                        user=row
                                        break
                name=user["CUSTOMER_NAME"]
                mob=user["MOBILE"]
                customer_mail=user["MAIL"]
        amt=total_cost
        if amt==0.0:
                gui_message("Info","NO ITEMS PURCHASED")
                return
        t=PayProcess(customer_mail,round(amt),oid)
        if t is None:
                gui_message("Error","PAYMENT CANCELLED")
                return
        with open(MARKET_FILE,"w",newline="",encoding="utf-8") as f:
                writer=csv.DictWriter(f,fieldnames=["SNO","ITEM_NAME","STOCK","UNIT_PRICE","GST"])
                writer.writeheader()
                writer.writerows(working_items)
        bill=generate_bill_data(litem=litem,lqty=lqty,lrate=lrate,lgst=lgst,lcost=lcost,total_cost=total_cost,amt=amt,name=name,mob=mob,payment_info=t,oid=oid)
        show_bill_gui(bill)
        print_bill_physical(bill)
        pdf_path = f"bill_{bill['order_id']}.pdf"
        create_bill_pdf(bill,pdf_path)
        send_mail(customer_mail,pdf_path,"BILL")
def close_app():#Function to close the application
        choice=gui_choice("Do you really want to exit?",[(1, "Yes"), (2, "No")],title="Exit Confirmation")
        if choice==1:
                root.quit()#stop Tkinter event loop
                root.destroy()#destroy all windows
root=tk.Tk()
root.title("Supermarket Management System")#Add a label
root.protocol("WM_DELETE_WINDOW",close_app)
label=tk.Label(root,text="Choose an option:")#Create buttons for each option
label.pack(pady=10)
button_1=tk.Button(root,text="NEW BILL",command=NewBill_Generation)
button_1.pack(pady=5)
button_2=tk.Button(root,text="VIEW STORE DETAILS",command=ViewMarketDetails)
button_2.pack(pady=5)
button_3=tk.Button(root,text="VIEW CUSTOMER DETAILS",command=ViewCustomerDetails)
button_3.pack(pady=5)
button_4=tk.Button(root,text="MODIFY STORE ITEMS",command=EditStock)
button_4.pack(pady=5)
button_5=tk.Button(root,text="CHECK INVENTORY",command=CheckStock)
button_5.pack(pady=5)
close_button=tk.Button(root, text="Close",command=close_app)# Create a close button
close_button.pack(pady=20)
def Market_Management():
        try:
                root.mainloop()# Run the application until the user clicks the close button
        except Exception as E:
                messagebox.showerror("Application Error",str(E))
Market_Management()
