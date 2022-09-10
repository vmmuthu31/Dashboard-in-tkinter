from ctypes import alignment
import sys
from tkinter import *
from tkinter import ttk
import webbrowser
import sqlite3
import threading
import jwt

global root;
root = Tk()
root.geometry('500x350')
root.title("Login Form")
nameVar=StringVar()
emailVar=StringVar()
passVar=StringVar()
OrganizVar = StringVar()

#link for generating pdf
def link():
    webbrowser.open_new("https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwil27f4w_j5AhVnR2wGHUT-CWUQFnoECAgQAQ&url=https%3A%2F%2Fwww.dsengg.ac.in%2Feee%2F07%2520COMMUNICATION%2520ENGINEERING%2520.pdf&usg=AOvVaw2yeloZyHPaGHGLs1n_wGs0")

# method to connect to database
def connection():
    email=emailVar.get()
    password=passVar.get()
    encpassword=jwt.encode({"some": "payload"}, password, algorithm="HS256")
    conn = sqlite3.connect('Users.db')
    with conn:
        cursor = conn.cursor()
    cursor.execute('Select * from User Where Email=? AND Password=? and activeflag= true',(email,encpassword))
    conn.commit()
    conn.close()
    
#method to add user register data in database    
def addNew():
    name=nameVar.get()
    email=emailVar.get()
    password=passVar.get()
    organiz=OrganizVar.get()
    encname=jwt.encode({"some": "payload"}, name, algorithm="HS256")
    encemail=jwt.encode({"some": "payload",}, email, algorithm="HS256")
    encpassword=jwt.encode({"some": "payload"}, password, algorithm="HS256")
    encorganiz=jwt.encode({"some": "payload"}, organiz, algorithm="HS256")
    conn = sqlite3.connect('Users.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS User (Name TEXT NOT NULL,Email TEXT UNIQUE,Password Text NOT NULL,organiz TEXT NOT NULL,ActiveFlag bool)')
    count=cursor.execute('INSERT INTO User (Name,Email,Password,organiz,ActiveFlag) VALUES(?,?,?,?,true)',(name,email,encpassword,organiz))
    if(cursor.rowcount>0):
        print ("Registration Successfully")
    else:
        print ("Signup Error")
    conn.commit()
    conn.close()

#Dashboard    
def dashboard(): 
    dashboardScreen=Tk()
    dashboardScreen.title("Futaucon")
    dashboardScreen.geometry('500x500')
    label = Label(dashboardScreen, text="Welcome To Futaucon",width=20,fg="blue",font=("bold", 20))
    label.place(x=120,y=53)
    Button(dashboardScreen, text='Download PDF',width=20,bg='green',fg='white',pady=5,command=link).place(x=170,y=110)
    Button(dashboardScreen, text='Quit',width=20,bg='blue',fg='white',pady=5,command=dashboardScreen.destroy).place(x=170,y=150)   

#method to perform login    
def loginNow():
    email=emailVar.get()
    password=passVar.get()
    encpassword=jwt.encode({"some": "payload"}, password, algorithm="HS256")
    conn = sqlite3.connect('Users.db')
    with conn:
        cursor=conn.cursor()
    # cursor.execute('CREATE TABLE IF NOT EXISTS User (Name TEXT NOT NULL,Email TEXT NOT NULL UNIQUE,Password Text NOT NULL,organiz TEXT NOT NULL,ActiveFlag bool)')
    cursor.execute('Select * from User Where Email=? AND Password=? and activeflag= true',(email,encpassword))
    if cursor.fetchone() is not None:
        dashboard()
    else:
        print ("Check the username and password")
    conn.commit()
    conn.close()

#Session Expiration
def set_interval(loginNow, time):
    def func_wrapper():
        set_interval(loginNow, time)
        root.destroy() 
        sys.exit()
    t = threading.Timer(360000, func_wrapper)
    t.start()
    return t
set_interval(loginNow,1)

def close():
    root.destroy() #Removes  root window
    sys.exit()

#method to design register window
def registerWindow(): 
    registerScreen=Toplevel(root)
    registerScreen.title("Registration Here")
    registerScreen.geometry('500x500')
    label = Label(registerScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    label.place(x=90,y=53)
    nameLabel = Label(registerScreen, text="FullName:",width=20,font=("bold", 10))
    nameLabel.place(x=80,y=130)
    nameEntry = Entry(registerScreen,textvar=nameVar)
    nameEntry.place(x=240,y=130)
    emailLabel = Label(registerScreen, text="Email:",width=20,font=("bold", 10))
    emailLabel.place(x=68,y=180)
    emailEntry = Entry(registerScreen,textvar=emailVar)
    emailEntry.place(x=240,y=180)
    passLabel = Label(registerScreen, text="Password:",width=20,font=("bold", 10))
    passLabel.place(x=78,y=230)
    passEntry = Entry(registerScreen,textvar=passVar,show='*')
    passEntry.place(x=240,y=230)
    organizLabel = Label(registerScreen, text="Organization Name:",width=20,font=("bold", 10))
    organizLabel.place(x=70,y=280)
    OrganizEntry = Entry(registerScreen,textvar=OrganizVar)
    OrganizEntry.place(x=240,y=280)
    Button(registerScreen, text='Submit',width=20,bg='blue',fg='white',pady=5,command=addNew).place(x=180,y=380)

label = Label(root, text="Login Here",width=20,fg="blue",font=("bold", 20))
label.place(x=90,y=53)
emailLabel = Label(root, text="Email",width=20,font=("bold", 10))
emailLabel.place(x=68,y=130)
emailEntry = Entry(root,textvar=emailVar)
emailEntry.place(x=240,y=130)
passwordLabel = Label(root, text="Password",width=20,font=("bold", 10))
passwordLabel.place(x=68,y=180)
passwordEntry = Entry(root,textvar=passVar,show='*')
passwordEntry.place(x=240,y=180)
Button(root, text='Login Now',width=20,bg='blue',fg='white',pady=5,command=loginNow).place(x=180,y=230)
Button(root,text="Have no Account! Create one",bg="red",fg="white",font=("bold",10),command=registerWindow).place(x=170,y=280)
root.mainloop()

