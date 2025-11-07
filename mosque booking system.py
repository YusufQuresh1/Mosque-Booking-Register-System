import sqlite3
import datetime
from tkinter import *
from tkinter import messagebox

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db: #connects the database with the provided name
        cursor = db.cursor() #creates cursor which interacts with the database
        cursor.execute(sql)
        db.commit()
        
def create_accounts_table():
    sql="""CREATE TABLE IF NOT EXISTS Accounts
            (AccountID INTEGER,
            FirstName TEXT,
            LastName TEXT,
            EmailAddress TEXT,
            Password TEXT,
            Gender TEXT,
            Role TEXT,
            Attendance REAL,
            primary key(AccountID))"""
    create_table(db_name,"Accounts",sql)

def create_register_table():
    sql="""CREATE TABLE IF NOT EXISTS Register
            (AccountID INTEGER,
            Date TEXT,
            Gender TEXT)"""
    create_table(db_name,"Register",sql)

def create_attendance_table():
    sql="""CREATE TABLE IF NOT EXISTS Attendance
            (Date text,
            AccountID integer)"""
    create_table(db_name,"Attendance",sql)

def insert_attendance_data(records):
    sql="insert into Attendance(Date, AccountID) values(?,?)"#inserts details into table
    for record in records:
        query(sql,record)

def insert_register_data(records):
    sql="insert into Register(AccountID, Date, Gender) values(?,?,?)"#inserts details into table
    for record in records:
        query(sql,record)

def insert_gents_register_data(records):
    sql="insert into GentsRegister(AccountID, Date) values(?,?)"#inserts details into table
    for record in records:
        query(sql,record)

def insert_ladies_register_data(records):
    sql="insert into LadiesRegister(AccountID, Date) values(?,?)"#inserts details into table
    for record in records:
        query(sql,record)

def insert_accounts_data(records):
    sql="insert into Accounts(FirstName, LastName, EmailAddress, Password, Gender, Role, Attendance) values(?,?,?,?,?,?,?)"#inserts details into table
    for record in records:
        query(sql,record)
       
def query(sql,data):
    with sqlite3.connect(db_name)as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(sql,data)
        db.commit()

def calculate_attendance(accountid):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(DISTINCT Date) FROM Attendance")
        TotalDates=cursor.fetchall()[0][0]
        cursor.execute("SELECT COUNT(Date) FROM Attendance WHERE AccountID=?", [accountid])
        AttendedDates=cursor.fetchall()[0][0]
        AttendPercent= (AttendedDates / TotalDates)
        AttendPercent = (AttendPercent*100)
        AttendPercent = round(AttendPercent, 1)
        return AttendPercent


## Create Account Page ################################################################################################################################################

class Create_Account: ##Creates Account page
    def __init__(self, root):
        
        ##Creating the Window and Labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("400x210")
        self.root.resizable(False, False)
        Label(self.root, text="Create Account", font="ar 15 bold").grid(row=0, column=1)
        Label(self.root, text="First Name").grid(row=1, column=1)
        Label(self.root, text="Last Name").grid(row=2, column=1)
        Label(self.root, text="Email Address").grid(row=3, column=1)
        Label(self.root, text="Password").grid(row=4, column=1)
        Label(self.root, text="Re-enter Password").grid(row=5, column=1)
        Label(self.root, text="Gender").grid(row=6, column=1)

        
        ##Creating the Entry Fields
        self.firstname=Entry(self.root)
        self.firstname.grid(row=1, column=3)##.grid must be on a new line for Entry
        self.lastname=Entry(self.root)
        self.lastname.grid(row=2, column=3)
        self.emailaddress=Entry(self.root)
        self.emailaddress.grid(row=3, column=3)
        self.password=Entry(self.root,show="*")
        self.password.grid(row=4, column=3)
        self.passwordrepeat=Entry(self.root, show="*")
        self.passwordrepeat.grid(row=5, column=3)

        ##Creating the gender selection buttons
        self.gender=StringVar()
        Radiobutton(self.root, text="Male", variable=self.gender, value="M", cursor="hand2").grid(row=6, column=3)
        Radiobutton(self.root, text="Female", variable=self.gender, value="F", cursor="hand2").grid(row=6, column=4)

        ##Creating the Button
        Button(text="Create Account", command=self.create_account_button, cursor="hand2").grid(row=7, column=3)
        Button(text="Back", bd=0, cursor="hand2", command=self.back_button).grid(row=8, column=3)

    def back_button(self):
        self.root.destroy()
        root=Tk()
        Login(root)

    ##Button functionality
    def create_account_button(self):
        if self.firstname.get()=="" or self.lastname.get()=="" or self.emailaddress.get()=="" or self.password.get()=="" or self.passwordrepeat.get()=="" or self.gender.get()=="":
            messagebox.showerror("Error", "All fields are required.") ##Stops user from creating an account with blank fields
        elif "@" not in self.emailaddress.get():
            messagebox.showerror("Error", "Invalid Email Address.")
        elif self.password.get() != self.passwordrepeat.get():
            messagebox.showerror("Error", "Passwords do not match.") ##Displays error if passwords don't match
        else:
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                
                cursor.execute("select * from Accounts where EmailAddress=?", [self.emailaddress.get()])
                if cursor.fetchone() == None: ##If the email is not already in database
                    q=messagebox.askokcancel("Attention", "Create New Account?")
                    if q == 1:
                        accountsdata=[(self.firstname.get(), self.lastname.get(), self.emailaddress.get(), self.password.get(), self.gender.get(), "Worshipper", 0)]
                        insert_accounts_data(accountsdata)
                        messagebox.showinfo("Mosque Booking System", "Account succesfuly created")
                        self.root.destroy()##Closes the window
                        root=Tk()##must do root=Tk() again after window is destroyed
                        Login(root)##Opens Login page

                else:
                    q=messagebox.askyesno("Attention", "An account with this email already exists, are you sure you want to create a new account?")
                    if q == 1:
                        accountsdata=[(self.firstname.get(), self.lastname.get(), self.emailaddress.get(), self.password.get(), self.gender.get(), "Worshipper", 0)]
                        insert_accounts_data(accountsdata)
                        messagebox.showinfo("Mosque Booking System", "Account succesfuly created")
                        self.root.destroy()
                        root=Tk()
                        Login(root)
                    
## Login Page ###########################################################################################################################################################
        
class Login: 
    def __init__(self, root):

        ##Creating the Window and Labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("375x140")
        self.root.resizable(False, False)
        Label(self.root, text="Login", font="ar 15 bold").grid(row=0, column=1)
        Label(self.root, text="Email Address").grid(row=1, column=1)
        Label(self.root, text="Password").grid(row=2, column=1)


        ##Creating the Entry Fields
        self.emailaddress=Entry(self.root)
        self.emailaddress.grid(row=1, column=3)
        self.password=Entry(self.root, show="*")
        self.password.grid(row=2, column=3)

        ##Creating the Button
        LoginButton=Button(text="Login", cursor="hand2", command=self.login_button).grid(row=3, column=3)
        Button(text="Don't have an existing account? Create Account.", bd=0, cursor="hand2", command=self.open_create_account_button).grid(row=4, column=3)


    def open_create_account_button(self):
        self.root.destroy()
        root=Tk()
        Create_Account(root)
            
    def login_button(self):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            
            ##Makes sure the credentials are correct
            cursor.execute("select * from Accounts where EmailAddress=? and Password=?", [self.emailaddress.get(), self.password.get()])
            if cursor.fetchone() == None:
                messagebox.showerror("Error", "Incorrect Email Address or Password")
                
            else:
                ##Sends the user to the page corresponding with their role
                cursor.execute("select AccountID from Accounts where EmailAddress=?", [self.emailaddress.get()])
                AccountID=cursor.fetchall()
                cursor.execute("select FirstName from Accounts where EmailAddress=?", [self.emailaddress.get()])
                FirstName=cursor.fetchall()
                cursor.execute("select LastName from Accounts where EmailAddress=?", [self.emailaddress.get()])
                LastName=cursor.fetchall()
                cursor.execute("select EmailAddress from Accounts where EmailAddress=?", [self.emailaddress.get()])
                EmailAddress=cursor.fetchall()
                cursor.execute("select Password from Accounts where EmailAddress=?", [self.emailaddress.get()])
                Password=cursor.fetchall()
                cursor.execute("select Gender from Accounts where EmailAddress=?", [self.emailaddress.get()])
                Gender=cursor.fetchall()
                cursor.execute("select Role from Accounts where EmailAddress=?", [self.emailaddress.get()])
                if cursor.fetchall() == [('Manager',)]:
                    self.root.destroy()
                    root=Tk()
                    Manager_Menu(root)
                else:
                    self.root.destroy()
                    root=Tk()
                    Main_Menu(root, AccountID, FirstName, LastName, EmailAddress, Password, Gender)



## Main Menu Page #####################################################################################################################################################

class Main_Menu: ##Creates Main Menu page
    def __init__(self, root, AccountID, FirstName, LastName, EmailAddress, Password, Gender):

        ##Getting the data in the correct format
        self.accountid=AccountID[0][0] 
        self.firstname=FirstName[0][0]
        self.lastname=LastName[0][0]    ## As data is in a tuple, [0][0] gives the actual detail required without any brackets etc.
        self.emailaddress=EmailAddress[0][0]  
        self.password=Password[0][0]
        self.gender=Gender[0][0]

        ##Creating the Window and Buttons
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        Label(self.root, text="Main Menu", font="ar 15 bold").pack()
        Button(text="Book Place", cursor="hand2", command=self.book_place_button).pack()
        Label(self.root, text="").pack()
        Button(text="Modify Details", cursor="hand2", command=self.open_modify_details_button).pack()
        Label(self.root, text="").pack()
        Button(text="Log out", bd=0, cursor="hand2", command=self.logout_button).pack()

    def open_modify_details_button(self):
        self.root.destroy()
        root=Tk()
        Modify_Details(root, self.firstname, self.lastname, self.emailaddress, self.password, self.gender)
    
    def book_place_button(self):
        date=datetime.date.today()
        day=date.isoweekday()
        ### FOR DEMO PURPOSES ###
        day=4
        #########################
        if day == 6:
            tdelta=datetime.timedelta(days=6)
        elif day == 7:
            tdelta=datetime.timedelta(days=5)
        else:
            tdelta=datetime.timedelta(days=5-day)
        date=(date + tdelta)
        date=date.strftime("%d/%m/%Y")
        details=[(self.accountid, date, self.gender)]

        if day == 5:
            messagebox.showerror("Error", "Booking is closed. Please try again later.")
        else:
            q=messagebox.askyesno("Attention", "Are you sure you want to book a place for the upcoming Friday prayer?")
            if q == 1:
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM Register WHERE AccountID=? AND Date=?", [self.accountid, date])
                    if cursor.fetchone() == None:
                        cursor.execute('SELECT COUNT(Gender) from Register WHERE Gender=?', [self.gender])
                        numofpeople = cursor.fetchall()[0][0]

                        if self.gender == "M" and numofpeople < 100:
                            insert_register_data(details)
                            messagebox.showinfo("Mosque Booking System", f"You have successfully booked a place for {date} at 13:30.")

                        elif self.gender == "F" and numofpeople < 50:
                            insert_register_data(details)
                            messagebox.showinfo("Mosque Booking System", f"You have successfully booked a place for {date} at 13:30.")

                        else:
                            messagebox.showerror("Error", "The mosque is at maximum capacity. Apologies for any inconvenience.")
                    else:
                        messagebox.showerror("Error", "You have already booked a place.")

        
    def logout_button(self):
        self.root.destroy()
        root=Tk()
        Login(root)
    
## Modify Details Page ##################################################################################################################################################

class Modify_Details:
    def __init__(self, root, FirstName, LastName, EmailAddress, Password, Gender):

        #Creating the window and labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        FullName=(FirstName, LastName)
        Label(self.root, text="Modify Details", font="ar 20 bold").grid(row=0, column=1)
        Label(self.root, text="These are your current details:", font="ar 9 bold").grid(row=1, column=1)
        Label(self.root, text="Name:").grid(row=2, column=1)
        Label(self.root, text="Email Address:").grid(row=3, column=1)
        Label(self.root, text="Gender:").grid(row=4, column=1)
        Label(self.root, text="").grid(row=5, column=1)
        Label(self.root, text="""Enter below the modifications you would like to make. \n
If you don't wish to change something, enter the existing detail.""", font="ar 9 bold").grid(row=6, column=1)
        Label(self.root, text="").grid(row=7, column=1)
        
        ##Showing the details
        Label(self.root, text=FullName).grid(row=2, column=2)
        Label(self.root, text=EmailAddress).grid(row=3, column=2)
        Label(self.root, text=Gender).grid(row=4, column=2)

        Label(self.root, text="First Name").grid(row=8, column=1)
        Label(self.root, text="Last Name").grid(row=9, column=1)
        Label(self.root, text="Email Address").grid(row=10, column=1)
        Label(self.root, text="Password").grid(row=11, column=1)
        Label(self.root, text="Re-enter Password").grid(row=12, column=1)
        Label(self.root, text="Gender").grid(row=13, column=1)
        Label(self.root, text="").grid(row=15, column=1)
        
        ##Creating the Entry Fields
        self.newfirstname=Entry(self.root)
        self.newfirstname.grid(row=8, column=2)##.grid() must be on a new line for Entry in order to be able to do .get()
        self.newlastname=Entry(self.root)
        self.newlastname.grid(row=9, column=2)
        self.newemailaddress=Entry(self.root)
        self.newemailaddress.grid(row=10, column=2)
        self.newpassword=Entry(self.root,show="*")
        self.newpassword.grid(row=11, column=2)
        self.newpasswordrepeat=Entry(self.root, show="*")
        self.newpasswordrepeat.grid(row=12, column=2)

        ##Creating the gender selection buttons
        self.newgender=StringVar()
        Radiobutton(self.root, text="Male", variable=self.newgender, value="M", cursor="hand2").grid(row=13, column=2)
        Radiobutton(self.root, text="Female", variable=self.newgender, value="F", cursor="hand2").grid(row=13, column=3)

        ##Creating the Button
        CreateAccountButton=Button(text="Submit Changes", command=self.submit_details_button, cursor="hand2").grid(row=14, column=2)
        Button(text="Back", bd=0, cursor="hand2", font="ar 10 bold", command=self.back_button).grid(row=15, column=2)

        self.firstname=FirstName
        self.lastname=LastName
        self.gender=Gender
        self.emailaddress=EmailAddress
        self.password=Password

    ##Button functionality
    def submit_details_button(self):
        q=messagebox.askyesno("Attention", "Are you sure you want to update these details?")
        if q == 1:
            if self.newfirstname.get()=="" or self.newlastname.get()=="" or self.newemailaddress.get()=="" or self.newpassword.get()=="" or self.newpasswordrepeat.get()=="" or self.newgender.get()=="":
                messagebox.showerror("Error", "All fields are required") ##Stops user from creating an account with blank fields
            elif "@" not in self.newemailaddress.get():
                messagebox.showerror("Error", "Invalid Email Address")      
            elif self.newpassword.get() != self.newpasswordrepeat.get():
                messagebox.showerror("Error", "Passwords do not match") ##Displays error if passwords don't match
                
            else:
                with sqlite3.connect(db_name) as db:
                    c = db.cursor()
                    ## Updates the user's profile with the data entered
                    c.execute("UPDATE Accounts SET FirstName=? WHERE FirstName=?", [self.newfirstname.get(), self.firstname])
                    c.execute("UPDATE Accounts SET LastName=? WHERE LastName=?", [self.newlastname.get(), self.lastname])
                    c.execute("UPDATE Accounts SET EmailAddress=? WHERE EmailAddress=?", [self.newemailaddress.get(), self.emailaddress])
                    c.execute("UPDATE Accounts SET Password=? WHERE Password=?", [self.newpassword.get(), self.password])
                    c.execute("UPDATE Accounts SET Gender=? WHERE Gender=?", [self.newgender.get(), self.gender])
                    messagebox.showinfo("Mosque Booking System", "Account details have been updated.")
                    self.root.destroy()
                    root=Tk()
                    Login(root)
                
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Login(root)
        
## Manager Menu Page ##################################################################################################################################################

class Manager_Menu: ##Creates Manager Menu page
    def __init__(self, root):
    
        ##Creating the Window and Buttons
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        Label(self.root, text="Manager Menu", font="ar 15 bold").pack()
        Button(text="Lookup", cursor="hand2", command=self.lookup_button).pack()
        Label(self.root, text="").pack()
        Button(text="Register", cursor="hand2", command=self.register_button).pack()
        Label(self.root, text="").pack()
        Button(text="Log out", bd=0, cursor="hand2", command=self.logout_button).pack()

    def lookup_button(self):
        self.root.destroy()
        root=Tk()
        Lookup(root)
    def register_button(self):
        self.root.destroy()
        root=Tk()
        Register_Menu(root)
    def logout_button(self):
        self.root.destroy()
        root=Tk()
        Login(root)

## Lookup Pages #######################################################################################################################################################

class Lookup:
    def __init__(self, root):
    
        ##Creating the Window and Buttons
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        Label(self.root, text="Lookup", font="ar 15 bold").pack()
        Button(text="Lookup Person", cursor="hand2", command=self.lookup_person_button).pack()
        Label(self.root, text="").pack()
        Button(text="Attendance", cursor="hand2", command=self.attendance_button).pack()
        Label(self.root, text="").pack()
        Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()

    def lookup_person_button(self):
        self.root.destroy()
        root=Tk()
        Lookup_Person(root)
    def attendance_button(self):
        self.root.destroy()
        root=Tk()
        Attendance(root)
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Manager_Menu(root)
        
class Attendance:
    def __init__(self, root):
        self.root=root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        Label(self.root, text="View Attendance", font="ar 15 bold").pack()
        Button(text="Attendance By Date", cursor="hand2", command=self.attend_date_button).pack()
        Label(self.root, text="").pack()
        Button(text="Attendance By Person", cursor="hand2", command=self.attend_person_button).pack()
        Label(self.root, text="").pack()
        Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()

    def attend_date_button(self):
        self.root.destroy()
        root=Tk()
        Attendance_By_Date(root)
    def attend_person_button(self):
        self.root.destroy()
        root=Tk()
        Attendance_By_Person(root)        
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Lookup(root)

class Attendance_By_Date:
    def __init__(self, root):
        self.root=root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        Label(self.root, text="Attendance By Date", font="ar 15 bold").pack()        
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("SELECT DISTINCT Date FROM Attendance")
            dates=cursor.fetchall()
            self.var = StringVar()
            for record in dates:
                datesselection = Checkbutton(self.root, text=record, variable=self.var, onvalue=record, offvalue="").pack()
                
            Button(text="View Attendees", cursor="hand2", command=self.view_attendees_button).pack()
            Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()

    def view_attendees_button(self):
        SelectedDate=self.var.get()
        if SelectedDate != "":
            self.root.destroy()
            root=Tk()
            View_Attendees(root, SelectedDate)
        else:
            messagebox.showerror("Error", "You must select a date.")
        
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Attendance(root)

class View_Attendees:
    def __init__(self, root, SelectedDate):
        self.root=root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        Label(self.root, text="View Attendees", font="ar 15 bold").pack()        
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT Attendance.AccountID, FirstName, LastName FROM Attendance, Accounts
                                  WHERE Attendance.AccountID = Accounts.AccountID AND Attendance.Date=?""", [SelectedDate])
            records=cursor.fetchall()
            for record in records:
                Label(self.root, text=record).pack()
            Label(self.root, text="").pack()
            Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()
            
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Attendance_By_Date(root)

class Attendance_By_Person:
    def __init__(self, root):
        
        ##Creating the Window and Labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        Label(self.root, text="Attendance By Person", font="ar 15 bold").grid(row=0, column=1)
        Label(self.root, text="AccountID").grid(row=1, column=1)

        ##Creating the entry fields
        self.accountid=Entry(self.root)
        self.accountid.grid(row=1, column=2)##.grid must be on a new line for Entry    

        ##Creating the Button
        Button(text="View Attendance", cursor="hand2", command=self.view_attendance_button).grid(row=3, column=2)
        Button(text="Back", bd=0, cursor="hand2", command=self.back_button).grid(row=4, column=2)

    def view_attendance_button(self):
        AccountID=self.accountid.get()
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("select * from Attendance where AccountID=?", [AccountID])
            if cursor.fetchone() == None:##Makes sure the credentials are correct
                messagebox.showerror("Error", "No attendance information for this account ID.")
            else:    
                self.root.destroy()
                root=Tk()
                Attendance_By_Person_Output(root, AccountID)

    def back_button(self):
        self.root.destroy()
        root=Tk()
        Attendance(root)
        
class Attendance_By_Person_Output:
    def __init__(self, root, AccountID):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            ##Creating the Window and Labels
            self.root = root
            self.root.title("Mosque Booking System")
            self.root.resizable(False, False)
            Label(self.root, text="Attendance By Person", font="ar 15 bold").grid(row=0, column=1)
            cursor.execute("""SELECT Accounts.AccountID, FirstName, LastName, Attendance.Date FROM Accounts,
                                  Attendance WHERE Accounts.AccountID=? AND Attendance.AccountID=?""", [AccountID, AccountID])
            records=cursor.fetchall()
            Label(self.root, text="AccountID & Name:").grid(row=1, column=1)
            Label(self.root, text=records[0][:3]).grid(row=1, column=2)
            Label(self.root, text="Dates Attended:").grid(row=2, column=1)
            x=2
            for record in records:
                Label(self.root, text=record[3]).grid(row=x, column=2)
                x+=1
            cursor.execute("SELECT Attendance FROM Accounts WHERE AccountID=?", [AccountID])
            Attendance=(cursor.fetchall(), "%")
            cursor.execute("SELECT AVG(Attendance) FROM Accounts")
            AvgAttendance=round(cursor.fetchall()[0][0], 1)
            AvgAttendance=(AvgAttendance, "%")
            message=("This person has an attendance of", Attendance, "% and the average percentage is", AvgAttendance, "%.")
            Label(self.root, text="Attendance Percentage:").grid(row=x+1, column=1)
            Label(self.root, text=Attendance).grid(row=x+1, column=2)
            Label(self.root, text="Average Attendance Percentage:").grid(row=x+2, column=1)
            Label(self.root, text=AvgAttendance).grid(row=x+2, column=2)
            Label(self.root, text="").grid(row=x+3, column=2)
            Button(text="Back", bd=0, cursor="hand2", command=self.back_button).grid(row=x+4, column=2)

    def back_button(self):
        self.root.destroy()
        root=Tk()
        Attendance_By_Person(root)
        
class Lookup_Person:
    def __init__(self, root):
    
        ##Creating the Window and Labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        Label(self.root, text="Lookup Person", font="ar 15 bold").grid(row=0, column=1)
        Label(self.root, text="AccountID").grid(row=1, column=1)

        ##Creating the entry fields
        self.accountid=Entry(self.root)
        self.accountid.grid(row=1, column=2)##.grid must be on a new line for Entry    

        ##Creating the Button
        Button(text="Lookup", cursor="hand2", command=self.lookup_output_button).grid(row=3, column=2)
        Button(text="Back", bd=0, cursor="hand2", command=self.back_button).grid(row=4, column=2)


    def lookup_output_button(self):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            AccountID=self.accountid.get()
            cursor.execute("select * from Accounts where AccountID=?", [AccountID])
            if cursor.fetchone() == None:##Makes sure the credentials are correct
                messagebox.showerror("Error", "Invalid ID.")
            else:
                
                cursor.execute("select FirstName, LastName from Accounts where AccountID=?", [AccountID])
                FullName=(cursor.fetchall())
                cursor.execute("select EmailAddress from Accounts where AccountID=?", [AccountID])
                EmailAddress=(cursor.fetchall())
                cursor.execute("select Gender from Accounts where AccountID=?", [AccountID])
                Gender=(cursor.fetchall())
                cursor.execute("select Role from Accounts where AccountID=?", [AccountID])
                Role=(cursor.fetchall())
                cursor.execute("SELECT Attendance FROM Accounts WHERE AccountID=?", [AccountID])
                Attendance=cursor.fetchall()
                
                self.root.destroy()
                root=Tk()
                Lookup_Output(root, FullName, AccountID, EmailAddress, Gender, Role, Attendance)

    def back_button(self):
        self.root.destroy()
        root=Tk()
        Lookup(root)

class Lookup_Output:
    def __init__(self, root, FullName, AccountID, EmailAddress, Gender, Role, Attendance):

        Attendance = (Attendance, "%")
    
        ##Creating the Window and Labels
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.resizable(False, False)
        Label(self.root, text=FullName[0], font="ar 15 bold").grid(row=0, column=1)
        Label(self.root, text="Account ID:").grid(row=1, column=1)
        Label(self.root, text="Email Address:").grid(row=4, column=1)
        Label(self.root, text="Gender:").grid(row=5, column=1)
        Label(self.root, text="Role:").grid(row=6, column=1)
        Label(self.root, text="Attendance:").grid(row=7, column=1)
        Label(self.root, text="").grid(row=8, column=2)
        Label(self.root, text="").grid(row=10, column=2)
        
        ##Showing the details
        Label(self.root, text=AccountID).grid(row=1, column=2)
        Label(self.root, text=EmailAddress).grid(row=4, column=2)
        Label(self.root, text=Gender).grid(row=5, column=2)    
        Label(self.root, text=Role).grid(row=6, column=2)
        Label(self.root, text=Attendance).grid(row=7, column=2)

        self.role=Role
        self.accountid=AccountID
        
        Button(text="Change Role", cursor="hand2", command=self.change_role_button).grid(row=9, column=2)
        Button(text="Back", bd=0, cursor="hand2", font="ar 10 bold", command=self.back_button).grid(row=11, column=2)

    def change_role_button(self):
        q=messagebox.askokcancel("Attention", "Change Role?")
        if q == 1:
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                if self.role[0][0] == "Worshipper":
                    cursor.execute("UPDATE Accounts SET Role=? WHERE AccountID=?", ["Manager", self.accountid])
                    messagebox.showinfo("Mosque Booking System", "Role Succesfully Updated")
                else:
                    cursor.execute("UPDATE Accounts SET Role=? WHERE AccountID=?", ["Worshipper", self.accountid])
                    messagebox.showinfo("Mosque Booking System", "Role Succesfully Updated")
                db.commit() 
            
        
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Lookup_Person(root)

## Register Page ######################################################################################################################################################

class Register_Menu:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Mosque Booking System")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        Label(self.root, text="Register", font="ar 15 bold").pack()
        Button(text="Gents Register", cursor="hand2", command=self.gRegister_button).pack()
        Label(self.root, text="").pack()
        Button(text="Ladies Register", cursor="hand2", command=self.lRegister_button).pack()
        Label(self.root, text="").pack()
        Button(text="Back", bd=0, cursor="hand2", font="ar 8 bold", command=self.back_button).pack()


       
    def gRegister_button(self):
        Choice="M"         
        self.root.destroy()
        root=Tk()
        Register(root, Choice)

    def lRegister_button(self):
        Choice="F"
        self.root.destroy()
        root=Tk()
        Register(root, Choice)

    def back_button(self):
        self.root.destroy()
        root=Tk()
        Manager_Menu(root)

class Register:
    def __init__(self, root, Choice):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            Date=datetime.date.today()
            self.choice=Choice
            day=Date.isoweekday()
            if day == 6:
                tdelta=datetime.timedelta(days=6)
            elif day == 7:
                tdelta=datetime.timedelta(days=5)
            else:
                tdelta=datetime.timedelta(days=5-day)
            Date=(Date + tdelta)
            Date=Date.strftime("%d/%m/%Y")
            day=datetime.date.today().isoweekday()
            now=datetime.datetime.now()
            hour=now.hour
            cursor.execute("""select Register.AccountID, FirstName, LastName from Register, Accounts
                              where Register.AccountID = Accounts.AccountID and Register.Date=? and Register.Gender=?""", [Date, self.choice])
            records = cursor.fetchall()
            
            ### FOR DEMO PURPOSES ###
            hour=13
            day=5
            #########################

            self.root = root
            self.root.title("Mosque Booking System")
            if self.choice == "M":
                Label(self.root, text="Gents Register", font="ar 15 bold").pack()
            else:
                Label(self.root, text="Ladies Register", font="ar 15 bold").pack()

            if day == 5 and hour == 13:
                self.var = IntVar()
                for record in records:
                    account_id = record[0]
                    full_name = f"{record[1]} {record[2]} (ID: {account_id})" 
                    Radiobutton(self.root, text=full_name, variable=self.var, value=account_id).pack(anchor=W)
                Button(text="Submit", cursor="hand2", command=self.submit_button).pack()    
                Label(text="").pack()
                Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()

            else:
                Label(self.root, text="""Register is open to mark attendance on Fridays between 13:00 and 14:00. \n
    The following people have booked for Friday's Jummah prayer.""").pack()
                
                for record in records:
                    Label(self.root, text=record).pack()
                    Label(self.root, text="").pack()
                Button(text="Back", bd=0, cursor="hand2", command=self.back_button).pack()

                

    def submit_button(self):
            selected_id = self.var.get()
            
            if selected_id != 0:
                with sqlite3.connect(db_name) as db:
                    cursor = db.cursor()
                    date=datetime.date.today().strftime("%d/%m/%Y")

                    cursor.execute("SELECT * FROM Attendance WHERE AccountID=? AND Date=?", [selected_id, date])
                    
                    if cursor.fetchone() == None:
                        records=[(date, selected_id)]
                        insert_attendance_data(records)
                        Attendance=calculate_attendance(selected_id)
                        cursor.execute("UPDATE Accounts SET Attendance=? WHERE AccountID=?", [Attendance, selected_id])
                        cursor.execute("""SELECT COUNT(Attendance.AccountID), Accounts.AccountID FROM Attendance, Accounts WHERE
                                        Attendance.AccountID=Accounts.AccountID and Attendance.Date=? and Accounts.Gender=?""", [date, self.choice])
                        capacity=cursor.fetchone()[0]
                        
                        if self.choice == "M":
                            messagebox.showinfo("Mosque Booking System", f"Registered Succesfully. There are {100-capacity} spaces left in the Gents Room.")
                        else:
                            messagebox.showinfo("Mosque Booking System", f"Registered Succesfully. There are {50-capacity} spaces left in the Ladies Room.")

                    else:
                        messagebox.showerror("Error", "Account already registered.")
            else:
                messagebox.showerror("Error", "You must select a name.")
                
    def back_button(self):
        self.root.destroy()
        root=Tk()
        Register_Menu(root)


    
        
#######################################################################################################################################################################

if __name__ == "__main__":
    db_name = "mosque_database.db"
    create_accounts_table()
    create_attendance_table()   
    create_register_table()
    root=Tk()
    obj = Login(root)
    root.mainloop()