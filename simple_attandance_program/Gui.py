from Tkinter import *
from Tkinter import Entry
from PIL import Image, ImageTk
import mysql.connector
import tkMessageBox
import os
import datetime
import os

# Designing window for registration
users_dict={}
database = mysql.connector.connect(host='localhost', user='root', password='harun159632')
curser = database.cursor()
try:
    #curser.execute("CREATE DATABASE CS350deneme")
    curser.execute("use CS350deneme")
    curser.execute('create table courses (cid varchar(20) not null)')

    curser.execute('create table enroll (sid varchar(20) not null,cid varchar(20) not null)')

    curser.execute(
        """create table users (sid varchar(20) not null,snameuser varchar(30) not null,slastnameuser varchar(20) not null,password varchar(20) not null) """)

    curser.execute("""create table attendance (cid varchar(20) not null,start varchar(30) not null)""")
    curser.execute(
        """create table attendance2 (cid varchar(20) not null,start varchar(30) not null,sid varchar(20),attended varchar(20), sign varchar (2))""")
    database.commit()

except:
    print "all good"

def login_check(x,y):
    global login_success
    login_success = Toplevel(main_screen)
    login_success.title("Success")
    login_success.geometry("200x150")
    Label(login_success, text=x,font=("bold", 10),bg="red3").place(x=55,y=25)
    Button(login_success,width=10, height=2,bg="turquoise4", text="Keep Going",command=y).place(x=60,y=75)

def getuser():
    curser.execute("use CS350deneme")
    sql_select = "select sid,snameuser,password from users "
    curser.execute(sql_select, )
    record = curser.fetchall()
    for i in range(len(record)):
        users_dict[record[i][0]] = record[i][2]
def login():
    getuser()
    main_screen.withdraw()
    def getusername(sid):
        curser.execute("use CS350deneme")
        sql_select = """select sid,snameuser,password from users where sid = %s"""
        curser.execute(sql_select, (sid,))
        record = curser.fetchall()
        return record[0]
    def login_verify():
        global username1
        username1 = username_verify.get()
        password1 = password_verify.get()

        if username1 == "admin" and password1 == "123":
            login_check("Welcome Admin",home)
        elif username1 in users_dict.keys() and password1== users_dict[username1]:
            login_check("Welcome"+"  "+getusername(username1)[1],studenthome)
        else:

            tkMessageBox.showerror("INVALID ENTRY","Username or password is wrong")
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("385x650")
    login_screen.resizable(width=FALSE, height=FALSE)
    login_screen.configure(background="white")

    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()
    global username_login_entry
    global password_login_entry
    path = "JPG_Formatinda_SEHIR_logo_1_Ingilizce.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(login_screen, image=img)
    panel.photo = img
    panel.place(x=40, y=0)
    Label(login_screen, text="Username : ",font=("bold", 20),bg="white").place(x=50, y=490)
    def clear(x):
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END)
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.bind('<Button-1>', clear)
    username_login_entry.place(x=210, y=500,height=25,width=120)
    Label(login_screen, text="Password : ",font=("bold", 20),bg="white").place(x=50, y=540)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.place(x=210, y=550,height=25,width=120)
    loginB=Button(login_screen, text="Login", width=15, height=1,bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5', command=login_verify)
    loginB.place(x=190, y=600)
    ExitB=Button(login_screen, text="Exit", width=13, height=1, bg="turquoise4", fg="white", font="5", relief=FLAT,
           overrelief=RIDGE, borderwidth='5', command=exit)
    ExitB.place(x=40, y=600)

def home():
    global R2
    login_success.destroy()
    login_screen.destroy()
    R2 = Toplevel(main_screen)
    R2.resizable(width=FALSE, height=FALSE)
    R2.title("SELECT")
    R2.geometry("385x650")
    b1 = Button(R2, text="STUDENT REPORT", width=17, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5',command=student_report)
    b1.place(x=20, y=100)
    b5 = Button(R2, text="COURSE REPORT", width=17, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5', command=course_report)
    b5.place(x=200, y=100)
    b2 = Button(R2, text="NEW STUDENT", width=37, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE,
                borderwidth='5', command=new_student)
    b2.place(x=20, y=350)
    b3 = Button(R2, text="NEW ATTENDANCE", width=17, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5', command=new_attend)
    b3.place(x=20, y=220)
    b4 = Button(R2, text="END ATTENDANCE", width=17, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5', command=end_attendance)
    b4.place(x=200, y=220)
    b5 = Button(R2, text="CREATE NEW CLASS", width=37, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5', command=class_create)
    b5.place(x=20, y=470)

    def back():
        R2.destroy()
        login()

    b1 = Button(R2, text="logout", bg="orange red",width=5, command=back)
    b1.place(x=300, y=20)
def class_create():
    def add_class():
        try:
            curser.execute("use CS350deneme")
            curser.execute("select * from courses")
            recourses = curser.fetchall()
            for i in recourses:
                if e1.get() == str(i[0]):
                    raise NameError
            value = e1.get()
            curser.execute("INSERT INTO courses(cid) VALUES  ('%s')" % (value))

            database.commit()
            added.config(text="Class Created", fg="black",font=("bold", 20))


        except:
            added.config(text="Class already exist", fg="black",font=("bold", 20))

    R2.destroy()
    global R7
    R7 = Toplevel(main_screen)
    R7.resizable(width=FALSE, height=FALSE)
    R7.geometry("385x650")
    R7.title('MAKE NEW CLASS')
    lb1 = Label(R7, text="Class Name", font=("bold", 15))
    lb1.place(x=50, y=200)
    global e1
    e1 = Entry(R7, width=15, font=("bold", 15), highlightthickness=2)
    e1.place(x=180, y=200)

    b1 = Button(R7, text="ADD", width=32, height=2, bg="turquoise4", fg="white", font="5", relief=RAISED, overrelief=RIDGE,
                command=add_class)
    b1.place(x=50, y=300)

    def back():
        R7.destroy()
        home()

    back = Button(R7, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
    added = Label(R7, font=("bold", 15))
    added.place(x=50, y=400)
def new_student():
    def clear1(x):
        Student_no.delete(0, END)
        First_name.delete(0, END)
        Last_name.delete(0, END)
        Password.delete(0, END)

    def add_student():
        curser.execute("use CS350deneme")
        print "here"
        try:
            getuser()
            if Student_no.get() in users_dict.keys():
                added.config(text="This Student already added", fg="black")
            else:
                sid = Student_no.get()
                fname = First_name.get()
                lname = Last_name.get()
                password = Password.get()

                curser.execute("""insert into users(sid,snameuser,slastnameuser,password) values(%s,%s,%s,%s)""",
                           (sid, fname, lname, password))

                database.commit()

                added.config(text="Added", fg="black")
        except:
            added.config(text="something went wrong", fg="red")


    R2.destroy()
    global R6
    R6 = Toplevel(main_screen)
    R6.resizable(width=FALSE, height=FALSE)
    R6.geometry("385x650")
    R6.title('MAKE ATTENDENCE ENTRY')
    lb1 = Label(R6, text="Student_NO :", font=("bold", 15))
    lb1.place(x=50, y=206)
    lb2 = Label(R6, text="FirstName :", font=("bold", 15))
    lb2.place(x=50, y=280)
    lb3 = Label(R6, text="LastName :", font=("bold", 15))
    lb3.place(x=50, y=350)
    lb4 = Label(R6, text="Password :", font=("bold", 15))
    lb4.place(x=50, y=420)
    global Student_no
    global First_name
    global Last_name
    global Password
    Student_no = Entry(R6, width=15, font=("bold", 15), highlightthickness=2)
    Student_no.place(x=180, y=206)
    Student_no.bind('<Button-1>', clear1)
    First_name = Entry(R6, width=15, font=("bold", 15), highlightthickness=2)
    First_name.place(x=180, y=280)
    Last_name = Entry(R6, width=15, font=("bold", 15), highlightthickness=2)
    Last_name.place(x=180, y=350)
    Password = Entry(R6, width=15, font=("bold", 15), highlightthickness=2)
    Password.place(x=180, y=420)

    Addbutton = Button(R6, text="ADD", width=32, height=2, bg="turquoise4", fg="white", font="5", relief=RAISED,
                       overrelief=RIDGE, command=add_student)
    Addbutton.place(x=50, y=500)

    def back():
        R6.destroy()
        home()

    back = Button(R6, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
    added = Label(R6, font=("bold", 15) )
    added.place(x=50, y=600)
def new_attend():
    def create_attendance():

        curser.execute("use cs350deneme")
        sql_select = """select sid from enroll where cid = %s"""
        curser.execute(sql_select, (tkvar.get(),))
        results = curser.fetchall()
        for i in results:
            print i[0]
            print "asfasf"
            v = tkvar.get(),str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),str(i[0])
            curser.execute("INSERT INTO attendance2(cid,start,sid) VALUES  (%s,%s,%s)", (v))## 1 olacak
        values = tkvar.get(),str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        """curser.execute("INSERT INTO attendance1(cid,start,sid) VALUES  (%s,%s,%s)",(values))"""
        database.commit()
        added.config(text="Added", fg="black")


    global R8
    R2.destroy()
    R8 = Toplevel(main_screen)
    R8.resizable(width=FALSE, height=FALSE)
    R8.geometry("385x650")
    R8.title("New Attendance")

    lb1 = Label(R8, text="Select courses", font=("bold", 15))
    lb1.place(x=50, y=200)

    courses = []
    # im = 0
    curser.execute("use CS350deneme")
    curser.execute("select * from courses")
    availableclasses = curser.fetchall()
    for i in availableclasses:
        # print i[0]
        courses.append(str(i[0]))


    tkvar = StringVar()
    course_list = OptionMenu(R8, tkvar, *courses)
    course_list.config(width=15)
    course_list.place(x=200, y=200)

    def back():
        R8.destroy()
        home()

    AddButton = Button(R8, text="Create Attendance", width=32, height=2, bg="turquoise4", fg="white", font="5", relief=RAISED,
                       overrelief=RIDGE, command=create_attendance)
    AddButton.place(x=50, y=300)
    back = Button(R8, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
    added = Label(R8, font=("bold", 15))
    added.place(x=50, y=400)
def end_attendance():
    def deneme3():
        dates = []
        cd = "select distinct start,sign from attendance2 where cid = %s "
        curser.execute(cd, (var123.get(),))
        availabledates = curser.fetchall()
        print availabledates
        for i in availabledates:

            dates.append(str(i[0]))

        print dates
        global var3
        var3 = StringVar()
        droplist1 =OptionMenu(endrame, var3, *dates)
        droplist1.config(width=10)
        droplist1.place(x=180, y=250)
        lb2 = Label(endrame, text="Date", font=("bold", 15))
        lb2.place(x=50, y=250)
    def end():
        list2 = []
        deneme = """select sid from enroll where cid=%s"""
        curser.execute(deneme, (var123.get(),))
        de = curser.fetchall()
        for i in de:
            list2.append(str(i[0]))
        for a in list2:
            curser.execute("use CS350deneme")
            sql_select = """select * from attendance2 where cid = %s and start=%s and sid=%s"""
            curser.execute(sql_select, (var123.get(),var3.get(),a))
            results = curser.fetchall()
            print "asasgasgasgasgasdas"
            print results
            for i in results:
                print i[3]
                print i[4]

                if i[4] == None and i[3] != None:
                    late = int(i[3][-5:-3]) - int(i[1][-5:-3])
                    print late
                    if late < 15:

                        sql_update = """update attendance2 set sign =%s where cid=%s and start=%s and sid=%s"""  # 1
                        curser.execute(sql_update, ('1', var123.get(), var3.get(),a))
                        database.commit()
                        added.config(text="Ended", fg="black")

                    else:

                        sql_update = """update attendance2 set sign =%s where cid=%s and start=%s and sid=%s"""  # 1
                        curser.execute(sql_update, ('0', var123.get(), var3.get(),a))
                        # absent_sql = """update attendance2 set attended=%s where cid =%s"""
                        # curser.execute(absent_sql,("Absent",var.get()))
                        database.commit()
                        added.config(text="Ended", fg="black")

                else:
                    sql_update = """update attendance2 set sign =%s where cid=%s and start=%s and sid=%s"""  # 1
                    curser.execute(sql_update, ('0', var123.get(), var3.get(),a))
                    absent_sql = """update attendance2 set attended =%s  where cid =%s and start=%s  and sid=%s"""
                    curser.execute(absent_sql, ('Absent', var123.get(), var3.get(),a))
                    database.commit()
                    added.config(text="Ended", fg="black")
    R2.destroy()
    global endrame
    endrame = Toplevel(main_screen)
    endrame.resizable(width=FALSE, height=FALSE)
    endrame.geometry("385x650")
    endrame.title('END ATTENDANCE')
    courses = []
    curser.execute("use CS350deneme")


    #curser.execute("select * from attendance2 ")
    curser.execute("select distinct cid , sign from attendance2")
    result = curser.fetchall()
    available_attendance = []
    available_attendance.append("Select Course")
    print result
    for i in result:
        print i[1]
        if i[1] == None:

            available_attendance.append(str(i[0]))


    print available_attendance

    attendButton1 = Button(endrame, text="select", width=5, height=1, bg="turquoise4", fg="white",
                           font="5",
                           relief=RAISED,
                           overrelief=RIDGE, command=deneme3)

    attendButton1.place(x=300, y=200)
    var123 = StringVar()
    lb1 = Label(endrame, text="Select Class", font=("bold", 15))
    lb1.place(x=50, y=200)
    droplist = OptionMenu(endrame, var123, *available_attendance)
    droplist.config(width=10)
    droplist.place(x=180, y=200)
    attendButton = Button(endrame, text="End Attendance", width=32, height=2, bg="turquoise4", fg="white", font="5",
                          relief=RAISED,
                          overrelief=RIDGE, command=end)
    attendButton.place(x=50, y=300)
    added = Label(endrame,font=("bold", 15))
    added.place(x=50, y=400)

    def back():
        endrame.destroy()
        home()

    back = Button(endrame, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
def studenthome():
    global R2
    login_success.destroy()
    login_screen.destroy()
    R2 = Toplevel(main_screen)
    R2.title("SELECT")
    R2.resizable(width=FALSE, height=FALSE)
    R2.geometry("385x650")
    b1 = Button(R2, text="ENROLL", width=30, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5',command=enroll )
    b1.place(x=40, y=144)
    b2 = Button(R2, text="ATTEND", width=30, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE,
                borderwidth='5',command=attendforclass)
    b2.place(x=40, y=270)
    b4 = Button(R2, text="REPORT", width=30, height=5, bg="turquoise4", fg="white", font="5", relief=FLAT,
                overrelief=RIDGE, borderwidth='5',command=report_for_student)
    b4.place(x=40, y=396)

    def back():
        R2.destroy()
        login()

    b1 = Button(R2, text="logout", width=5, command=back,bg="turquoise4")
    b1.place(x=300, y=20)
def enroll():
    def enrollforclass():

        try:
            curser.execute("use CS350deneme")
            value = username1,var.get()

            sql_select = """select cid from enroll where sid = %s"""

            curser.execute(sql_select,(username1,))
            enrolled =  curser.fetchall()
            for i in enrolled:
                print i[0]
                if i[0] == var.get():
                    raise NameError

            curser.execute("INSERT INTO enroll(sid,cid) VALUES  (%s,%s)",(value))

            database.commit()
            added.config(text="Enrolled", fg="black")
        except:
            added.config(text="You already enrolled", fg="black")
    R2.destroy()
    global attendframe
    attendframe = Toplevel(main_screen)
    attendframe.resizable(width=FALSE, height=FALSE)
    attendframe.geometry("385x650")
    attendframe.title('ENROLL')
    courses = []
    curser.execute("use CS350deneme")
    curser.execute("select * from courses")
    availableclasses = curser.fetchall()
    for i in availableclasses:

        courses.append(str(i[0]))

    var = StringVar()
    lb1 = Label(attendframe, text="Select Class", font=("bold", 15))
    lb1.place(x=50, y=200)
    droplist = OptionMenu(attendframe, var, *courses)
    droplist.config(width=20)
    droplist.place(x=180,y=200)
    enrollButton = Button(attendframe, text="Enroll For Class", width=32, height=2, bg="turquoise4", fg="white", font="5", relief=RAISED,
                          overrelief=RIDGE, command=enrollforclass)
    enrollButton.place(x=50, y=300)
    added = Label(attendframe, font=("bold", 15))
    added.place(x=50, y=400)
    def back():
        attendframe.destroy()
        studenthome()

    back = Button(attendframe, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
def attendforclass():
    def attend():

        curser.execute("use CS350deneme")
        sql_select = """select * from attendance2 where sid = %s"""#1
        curser.execute(sql_select, (username1,))
        results  = curser.fetchall()

        for i in results:
            if str(i[0]) == var.get():

                if str(i[3]) == 'None' and str(i[1]) == var2.get():

                    sql_update = """update attendance2 set attended =%s where sid=%s""" # 1

                    curser.execute(sql_update,(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),username1))
                    database.commit()
                    added.config(text="Attending", fg="black")
            else:
                added.config(text="There is No Attend Session", fg="black")

    R2.destroy()
    global attendframe
    attendframe = Toplevel(main_screen)
    attendframe.resizable(width=FALSE, height=FALSE)
    attendframe.geometry("385x650")
    attendframe.title('ATTEND')
    courses = []
    courseanddate= []
    curser.execute("use CS350deneme")
    #curser.execute("select * from courses")
    cc = "select cid from enroll where sid = %s"

    curser.execute(cc , (username1,))

    availableclasses = curser.fetchall()
    for i in availableclasses:
        courses.append(str(i[0]))

    var = StringVar()

    def deneme3():
        dates = []
        cd = "select distinct start from attendance2 where cid = %s "
        curser.execute(cd, (var.get(),))
        availabledates = curser.fetchall()

        for i in availabledates:
            dates.append(str(i[0]))
        print dates
        global var2
        var2 = StringVar()
        droplist1 =OptionMenu(attendframe, var2, *dates)
        droplist1.config(width=10)
        droplist1.place(x=180, y=250)
        lb2 = Label(attendframe, text="Date", font=("bold", 15))
        lb2.place(x=50, y=250)

    lb1 = Label(attendframe, text="Select Class", font=("bold", 15))
    lb1.place(x=50, y=200)

    droplist = OptionMenu(attendframe, var, *courses)
    droplist.config(width=10)
    droplist.place(x=180, y=200)

    attendButton = Button(attendframe, text="Attend For Class", width=32, height=2, bg="turquoise4", fg="white", font="5",
                          relief=RAISED,
                          overrelief=RIDGE, command=attend)
    attendButton1 = Button(attendframe, text="select", width=5, height=1, bg="turquoise4", fg="white",
                          font="5",
                          relief=RAISED,
                          overrelief=RIDGE, command=deneme3)

    attendButton.place(x=50, y=300)
    attendButton1.place(x=300, y=200)

    added = Label(attendframe, font=("bold", 15) )
    added.place(x=50, y=400)



    def back():
        attendframe.destroy()
        studenthome()

    back = Button(attendframe, text="HOME", bg="turquoise4", fg="white", command=back)
    back.place(x=300, y=30)
def student_report():
    def report():
        curser.execute("use cs350deneme")
        sql_search = """select cid from enroll where sid =%s"""
        curser.execute(sql_search,(e1.get(),))
        results = curser.fetchall()
        course_list=[]
        for i in results:
            course_list.append(str(i[0]))

        lb2 = Label(studentreport, text="Enrolled Classes", font=("bold", 15))
        lb2.place(x=90, y=100)
        for x in range(len(course_list)):
            global compButton
            compButton = Button(studentreport, text=course_list[x], width=10, height=1, bg="turquoise4", fg="white", font="5", relief=RAISED, overrelief=RIDGE, command=lambda z=course_list[x]: listbox(z))
            compButton.place(x=200, y=x*100+150)
    def listbox(x):
        attendcelist = []
        curser.execute("use cs350deneme")
        sql_select = """select cid,start,sid,attended,sign from attendance2 where cid=%s and sid =%s"""
        curser.execute(sql_select,(x,e1.get(),))
        r= curser.fetchall()
        for i in r:
            cid = str(i[0])
            start = str(i[1])
            sid = str(i[2])
            attended = str(i[3])
            sign = str(i[4])
            tolistbox = cid + " | " + start + " | " + sid + " | " + attended + " | " + sign
            attendcelist.append(tolistbox)

        listbox=Listbox(studentreport,width=60, height=10, font=("bold", 15))
        listbox.insert(END,)
        scrollbar = Scrollbar(studentreport, orient="vertical", )
        scrollbar.config(command=listbox.yview)
        scrollbar.place(x=1150, y=150, height=242)
        listbox.config(yscrollcommand=scrollbar.set)
        for item in attendcelist:
            listbox.insert(END, item)
        st=0
        for i in range(len(attendcelist)):
            print type(attendcelist[i][-1])
            if attendcelist[i][-1]=="e":
                st=0
            else:
                st = int(attendcelist[i][-1])
            print st
            print type(st)
            if st == 0:
                listbox.itemconfig(i, {'bg': 'red'})
            else:
                listbox.itemconfig(i, {'bg': 'green'})

        # this changes the font color of the 4th item

        listbox.place(x=500,y=150,)

    R2.destroy()
    global studentreport
    studentreport = Toplevel(main_screen)
    studentreport.title("SEARCH AND REPORT")
    studentreport.geometry("1280x720")
    lb1=Label(studentreport, text="Student No :", font=("bold", 15))
    lb1.place(x=90,y=50)
    e1 = Entry(studentreport, width=10, font=("bold", 15), highlightthickness=2)
    e1.place(x=220, y=50)
    searchbutton=Button(studentreport, text="SEARCH", width=10, height=1, bg="turquoise4", fg="white", font="5", relief=RAISED, overrelief=RIDGE, command =report)
    searchbutton.place(x=350,y=50)
    def back():
        studentreport.destroy()
        home()
    b1 = Button(studentreport, text="Back", bg="turquoise4", fg="white", command=back)
    b1.place(x=1210, y=20)
def course_report():

    def listbox():
        attendcelist = []

        curser.execute("use cs350deneme")
        sql_select = """select * from attendance2 where cid=%s"""
        curser.execute(sql_select,(e2.get(),))
        r= curser.fetchall()
        for i in r:
            cid = str(i[0])
            start = str(i[1])
            sid = str(i[2])
            attended = str(i[3])
            sign = str(i[4])
            tolistbox = cid + " | " + start + " | " + sid + " | " + attended + " | " + sign
            attendcelist.append(tolistbox)
            #print attendcelist



        def deneme():
            datelist = []

            curser.execute("use cs350deneme")
            sql_select = """select * from attendance2 where cid=%s and start like %s"""
            value = e3.get() + "%"
            curser.execute(sql_select, (e2.get(),value))
            r = curser.fetchall()
            for i in r:
                cid = str(i[0])
                start = str(i[1])
                sid = str(i[2])
                attended = str(i[3])
                sign = str(i[4])
                tolistbox = cid + " | " + start + " | " + sid + " | " + attended + " | " + sign
                datelist.append(tolistbox)
                # print attendcelist
            for i in datelist:
                listbox1.insert(END, i)


        listbox=Listbox(coursereport,width=60, height=10, font=("bold", 15))
        listbox.insert(END,)
        listbox1 = Listbox(coursereport, width=60, height=10, font=("bold", 15))
        listbox1.insert(END, )
        scrollbar = Scrollbar(coursereport, orient="vertical",)
        scrollbar.config(command=listbox.yview)
        scrollbar.place(x=1150,y=150,height=242)
        scrollbar1 = Scrollbar(coursereport, orient="vertical", )
        scrollbar1.config(command=listbox1.yview)
        scrollbar1.place(x=1150, y=400, height=242)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.place(x=500,y=150,)
        listbox1.config(yscrollcommand=scrollbar1.set)
        listbox1.place(x=500, y=400, )

        lb3 = Label(coursereport, text="Date :", font=("bold", 15))
        lb3.place(x=90, y=400)
        e3 = Entry(coursereport, width=10, font=("bold", 15), highlightthickness=2)
        e3.place(x=220, y=400)
        searchbutton1 = Button(coursereport, text="SEARCH", width=10, height=1, bg="turquoise4", fg="white", font="5",
                              relief=RAISED, overrelief=RIDGE, command=deneme)
        searchbutton1.place(x=350, y=400)

        for item in attendcelist:

            listbox.insert(END, item)


        for i in range(len(attendcelist)):
            st = int(attendcelist[i][-1])
            if st == 0:
                listbox.itemconfig(i, {'bg': 'red'})
            else:
                listbox.itemconfig(i, {'bg': 'green'})

        # this changes the font color of the 4th item



    R2.destroy()
    global coursereport
    coursereport = Toplevel(main_screen)
    coursereport.title("SEARCH AND REPORT")
    coursereport.geometry("1280x720")
    lb2 = Label(coursereport, text="Course Name :", font=("bold", 15))
    lb2.place(x=90, y=150)


    e2 = Entry(coursereport, width=10, font=("bold", 15), highlightthickness=2)
    e2.place(x=220, y=150)
    searchbutton = Button(coursereport, text="SEARCH", width=10, height=1, bg="turquoise4", fg="white", font="5",
                          relief=RAISED, overrelief=RIDGE,command=listbox)
    searchbutton.place(x=350, y=150)

    def back():
        coursereport.destroy()
        home()
    b1 = Button(coursereport, text="Back", bg="turquoise4", fg="white", command=back)
    b1.place(x=1210, y=20)
def report_for_student():


    def listbox(x):
        attendcelist = []
        curser.execute("use cs350deneme")
        sql_select = """select cid,start,sid,attended,sign from attendance2 where cid=%s and sid =%s"""
        curser.execute(sql_select,(x,username1,))
        r= curser.fetchall()
        for i in r:
            cid = str(i[0])
            start = str(i[1])
            sid = str(i[2])
            attended = str(i[3])
            sign = str(i[4])
            tolistbox = cid + " | " + start + " | " + sid + " | " + attended + " | " + sign
            attendcelist.append(tolistbox)
            print attendcelist


        total = "select cid,sid,count(sid) from attendance2 where cid = %s and sid = %s group by cid,sid"
        curser.execute(total,(x,username1,))
        re = curser.fetchall()
        percent = "select cid,sid,count(sign) from attendance2 where sign = 1 and cid = %s and sid = %s group by cid,sid"
        curser.execute(percent,(x,username1,))
        fe = curser.fetchall()

        print re
        print fe
        if len(fe)==0:
            percentage = 0
        elif int(fe[0][2]) !=0  and int(re[0][2]) !=0:
            percentage = (int(fe[0][2]) /int(re[0][2]))*100

        print percentage




        percentages=Label(report,text="Percentage : %"+ str(percentage), font=("bold", 15))
        percentages.place(x=1000,y=150)
        listbox=Listbox(report,width=60, height=10, font=("bold", 15))
        listbox.insert(END,)
        scrollbar = Scrollbar(report, orient="vertical", )
        scrollbar.config(command=listbox.yview)
        scrollbar.place(x=950, y=100, height=242)
        listbox.config(yscrollcommand=scrollbar.set)
        listbox.place(x=300, y=100, )
        for item in attendcelist:
            listbox.insert(END, item)
        for i in range(len(attendcelist)):
            st = int(attendcelist[i][-1])
            if st == 0:
                listbox.itemconfig(i, {'bg': 'red'})
            else:
                listbox.itemconfig(i, {'bg': 'green'})

        # this changes the font color of the 4th item



    R2.destroy()
    global report
    report = Toplevel(main_screen)
    report.title("REPORT")
    report.geometry("1280x720")
    # lb1=Label(report, text="Student No :", font=("bold", 15))
    # lb1.place(x=90,y=50)
    # e1 = Entry(report, width=10, font=("bold", 15), highlightthickness=2)
    # e1.place(x=220, y=50)
    # searchbutton=Button(report, text="SEARCH", width=10, height=1, bg="turquoise4", fg="white", font="5", relief=RAISED, overrelief=RIDGE, command = student_report)
    # searchbutton.place(x=350,y=50)
    def back():
        report.destroy()
        studenthome()
    b1 = Button(report, text="Back", bg="turquoise4", fg="white", command=back)
    b1.place(x=1210, y=20)


    def student():
        def deneme():
            datelist = []
            listbox1 = Listbox(report, width=60, height=10, font=("bold", 15))
            listbox1.insert(END, )
            scrollbar1 = Scrollbar(report, orient="vertical", )
            scrollbar1.config(command=listbox1.yview)
            scrollbar1.place(x=950, y=450, height=242)
            listbox1.config(yscrollcommand=scrollbar1.set)
            listbox1.place(x=300, y=450, )

            curser.execute("use cs350deneme")
            sql_select = """select * from attendance2 where sid=%s and start like %s"""
            value = e3.get() + "%"
            curser.execute(sql_select, (username1, value))
            r = curser.fetchall()
            for i in r:
                cid = str(i[0])
                start = str(i[1])
                sid = str(i[2])
                attended = str(i[3])
                sign = str(i[4])
                tolistbox = cid + " | " + start + " | " + sid + " | " + attended + " | " + sign
                datelist.append(tolistbox)
                # print attendcelist
            for i in datelist:
                listbox1.insert(END, i)
        curser.execute("use cs350deneme")
        sql_search = """select cid from enroll where sid =%s"""
        curser.execute(sql_search,(username1,))
        results = curser.fetchall()
        course_list=[]
        for i in results:
            course_list.append(str(i[0]))

        lb2 = Label(report, text="Enrolled Classes", font=("bold", 15))
        lb2.place(x=90, y=50)
        for x in range(len(course_list)):
            global compButton
            compButton = Button(report, text=course_list[x], width=10, height=1, bg="turquoise4", fg="white", font="5", relief=RAISED, overrelief=RIDGE, command=lambda z=course_list[x]: listbox(z))
            compButton.place(x=x*100+300, y=50)

        lb3 = Label(report, text="Absent At :", font=("bold", 15))
        lb3.place(x=90, y=400)
        e3 = Entry(report, width=10, font=("bold", 15), highlightthickness=2)
        e3.place(x=200, y=400)
        searchbutton = Button(report, text="SEARCH", width=10, height=1, bg="turquoise4", fg="white", font="5",
                              relief=RAISED, overrelief=RIDGE, command=deneme)
        searchbutton.place(x=350, y=400)


    student()




def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("1280x720")
    main_screen.title("Account Login")
    main_screen.configure(background='gray')

    path = "Untitled.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = Label(main_screen, image=img)
    panel.photo = img
    panel.place(x=0, y=0)
    Label(text="Welcome to Sehir Attendance", bg="turquoise4", width="300", height="3", font=("bold", 15)).pack()
    Button(text="Login", height="2", width="30", bg="turquoise4", fg="white", font=("bold", 15), relief=FLAT,
           overrelief=RIDGE, borderwidth='5', command=login).place(x=470, y=100)
    Button(text="Exit", height="2", width="30", bg="turquoise4", fg="white", font=("bold", 15), relief=FLAT,
           overrelief=RIDGE, borderwidth='5', command=exit).place(x=470, y=200)

    main_screen.mainloop()


main_account_screen()
