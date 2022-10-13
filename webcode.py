from flask import *
from src.dbconnectionnew import *
import os
from werkzeug.utils import secure_filename
import functools

app = Flask(__name__)

app.secret_key="74745"

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('login_index.html')
        return func()

    return secure_function


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def login():
    return render_template("login_index.html")


@app.route('/login_code',methods=['post'])
def login_code():
    print(request.form)
    uname=request.form['textfield']
    pswd=request.form['textfield2']
    qry="select * from login where username=%s and password=%s"
    val=(uname,pswd)
    res=selectone(qry,val)

    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type']=="admin":
        session['lid']=res['lid']
        return '''<script>alert("Welcome admin");window.location="/admin_home"</script>'''
    elif res['type'] == "staff":
        session['lid'] = res['lid']
        return '''<script>alert("Welcome");window.location="/staff_home"</script>'''

    else:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''





@app.route('/admin_home')
@login_required
def admin_home():
    return render_template("admin home.html")


@app.route('/staff_home')
@login_required
def staff_home():
    return render_template("staff home.html")


@app.route('/add_club',methods=['post'])
@login_required
def add_club():
    return render_template("addclub.html")


@app.route('/add_course',methods=['post'])
@login_required
def add_course():

    qry = "select * from department"
    res = selectall(qry)

    return render_template("addcourse.html",val = res)


@app.route('/insert_course',methods=['post'])
@login_required
def insert_course():
    dep = request.form['select']
    course = request.form['textfield']

    qry = "insert into course values(null,%s,%s)"
    val = (dep,course)
    iud(qry,val)
    return '''<script>alert("successfully added");window.location="manage_course#about"</script>'''


@app.route('/add_dataset',methods=['post'])
@login_required
def add_dataset():
    return render_template("adddataset.html")


@app.route('/add_staff',methods=['post'])
@login_required
def add_staff():
    return render_template("addstaff.html")


@app.route('/add_student',methods=['post'])
@login_required
def add_student():

    qry = "select * from course"
    res = selectall(qry)

    return render_template("addstudent.html",val=res)

@app.route('/insert_student',methods=['post'])
@login_required
def insert_student():
    print(request.form)
    name = request.form['textfield']
    sem = request.form['select']
    cid = request.form['select2']
    qual = request.form['textfield2']
    gender = request.form['radio']
    dob = request.form['textfield4']
    phone = request.form['textfield5']
    email = request.form['textfield6']
    address = request.form['textfield7']
    uname = request.form['textfield8']
    pswd = request.form['textfield9']

    qry = "insert into login values(null,%s,%s,'student')"
    val = (uname,pswd)
    id = iud(qry,val)

    qry = "insert into student values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (id,cid,name,qual,gender,dob,phone,sem,email,address)
    iud(qry,val)

    return '''<script>alert("successfully added");window.location="studentreg#about"</script>'''

@app.route('/add_subject',methods=['post'])
@login_required
def add_subject():

    qry = "select * from course"
    res = selectall(qry)

    return render_template("addsubject.html",val=res)

@app.route('/complaint')
@login_required
def complaint():

    qry = "SELECT `student`.`stname`,`complaint`.* FROM `student` JOIN `complaint` ON `student`.`lid`=`complaint`.lid WHERE `complaint`.reply='pending'"
    res = selectall(qry)

    return render_template("complaint.html",val=res)

@app.route('/reply')
@login_required
def reply():
    id = request.args.get("id")
    session['cid']=id
    return render_template("reply.html")

@app.route('/send_reply',methods=['post'])
@login_required
def send_reply():
    reply=request.form['textfield']
    qry = "update complaint set reply=%s where coid=%s"
    val = (reply,session['cid'])
    iud(qry,val)
    return '''<script>alert("Reply sent successfully");window.location="complaint#about"</script>'''


@app.route('/manage_dataset')
@login_required
def manage_dataset():

    qry = "select * from dataset"
    res = selectall(qry)

    return render_template("datasetmanagement.html",val=res)

@app.route('/delete_dataset')
@login_required
def delete_dataset():
    id = request.args.get("id")
    qry = "delete from dataset where did=%s"
    iud(qry,id)

    return '''<script>alert("Deleted");window.location="manage_dataset#about"</script>'''


@app.route('/insert_dataset', methods=['post'])
@login_required
def insert_dataset():
    qstn = request.form['textfield']
    answer = request.form['textfield2']

    qry = "insert into dataset values(null,%s,%s)"
    val = (qstn,answer)

    iud(qry, val)

    return '''<script>alert("Added successfully");window.location="manage_dataset#about"</script>'''


@app.route('/internal')
@login_required
def internal():

    qry = "SELECT * FROM SUBJECT JOIN `assign` ON `subject`.`subid`=`assign`.`sid` WHERE `assign`.`lid`=%s"
    res = selectall2(qry,session['lid'])

    qry = "SELECT `student`.* FROM `student` JOIN `subject` ON `student`.cid=`subject`.`cid` JOIN `assign` ON `subject`.`subid`=`assign`.`sid` WHERE `assign`.`lid`=%s"
    res2 = selectall2(qry,session['lid'])

    return render_template("internal.html",val=res2,val2=res)

@app.route('/insert_internal',methods=['post'])
@login_required
def insert_internal():
    stnm = request.form['select']
    sub = request.form['select2']
    mark = request.form['textfield']

    qry = "select * from internalmark where sid=%s and stid=%s"
    val = (sub,stnm)
    res = selectone(qry,val)
    print(res)

    if res is None:

        qry = "INSERT INTO `internalmark` VALUES(NULL,%s,%s,%s)"
        val = (sub,stnm,mark)
        iud(qry,val)

        return '''<script>alert("Added successfully");window.location="staff_home"</script>'''
    else:
        return '''<script>alert("Already added");window.location="staff_home"</script>'''



@app.route('/manage_club')
@login_required
def manage_club():

    qry = "select * from club"
    res = selectall(qry)
    return render_template("manageclub.html", val=res)

@app.route('/delete_club')
@login_required
def delete_club():
    id = request.args.get("id")

    qry = "delete from club where clubid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_club#about"</script>'''

@app.route('/insert_club',methods=['post'])
@login_required
def insert_club():

    club = request.form['textfield']
    qry = "insert into club values(null,%s)"
    iud(qry,club)
    return '''<script>alert("Successfully added");window.location="manage_club#about"</script>'''

@app.route('/manage_course')
@login_required
def manage_course():

    qry= "SELECT `department`.`deptname`,`course`.* FROM `course` JOIN `department` ON `course`.`deptid`=`department`.`deptid`"
    res = selectall(qry)

    return render_template("managecourse.html", val=res)

@app.route('/delete_course')
@login_required
def delete_course():
    id = request.args.get("id")
    qry = "delete from course where cid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_course#about"</script>'''


@app.route('/manage_staff')
@login_required
def manage_staff():

    qry = "SELECT * FROM `staff`"
    res = selectall(qry)

    return render_template("managestaff.html", val=res)

@app.route('/insert_staff', methods=['post'])
@login_required
def insert_staff():

    fname = request.form['textfield']
    lname = request.form['textfield2']
    phone = request.form['textfield3']
    email = request.form['textfield4']
    qual = request.form['textfield5']
    place = request.form['textfield6']
    post = request.form['textfield7']
    pin = request.form['textfield8']
    uname = request.form['textfield9']
    pswd = request.form['textfield10']

    qry = "INSERT INTO login VALUES(NULL,%s,%s,'staff')"
    val = (uname, pswd)
    id = iud(qry, val)

    qry = "INSERT INTO `staff` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (id,fname,lname,phone,email,qual,place,post,pin)

    iud(qry,val)

    return '''<script>alert("Added successfully");window.location="manage_staff#about"</script>'''

@app.route('/delete_staff')
@login_required
def delete_staff():
    id = request.args.get("id")

    qry = "delete from login where lid = %s"
    val = (id)
    iud(qry,val)

    qry = "delete from staff where lid=%s"
    iud(qry,val)
    return '''<script>alert("Deleted");window.location="manage_staff#about"</script>'''

@app.route('/edit_staff')
@login_required
def edit_staff():
    id = request.args.get("id")
    session['sid']=id

    qry = "select * from staff where lid=%s"
    res = selectone(qry,id)

    return render_template("editstaff.html",val=res)

@app.route('/update_staff',methods=['post'])
@login_required
def update_staff():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    phone = request.form['textfield3']
    email = request.form['textfield4']
    qual = request.form['textfield5']
    place = request.form['textfield6']
    post = request.form['textfield7']
    pin = request.form['textfield8']

    qry = "UPDATE `staff` SET `fname`=%s,`lname`=%s,`phone`=%s,`email`=%s,`qualification`=%s,`place`=%s,`post`=%s,`pin`=%s WHERE lid=%s"

    val=(fname,lname,phone,email,qual,place,post,pin,session['sid'])
    iud(qry,val)
    return '''<script>alert("Updated successfully");window.location="manage_staff#about"</script>'''





@app.route('/studentreg')
@login_required
def studentreg():

    qry = "SELECT `student`.*,`course`.`coursename` FROM `student` JOIN `course` ON `student`.cid=`course`.`cid`"
    res = selectall(qry)

    return render_template("studentreg.html",val=res)

@app.route('/delete_student')
@login_required
def delete_student():
    id = request.args.get("id")
    qry = "delete from student where lid=%s"
    iud(qry,id)

    qry = "delete from login where lid=%s"
    iud(qry,id)

    return '''<script>alert("Deleted");window.location="studentreg#about"</script>'''

@app.route('/edit_student')
@login_required
def edit_student():
    id = request.args.get("id")

    session['stid'] = id

    qry = "select * from student where lid=%s"
    res = selectone(qry,id)

    qry = "select * from course"

    res2 = selectall(qry)

    return render_template("editstudent.html",val2=res,val=res2)

@app.route('/update_student',methods=['post'])
@login_required
def update_student():
    name = request.form['textfield']
    sem = request.form['select']
    cid = request.form['select2']
    qual = request.form['textfield2']
    gender = request.form['radio']
    dob = request.form['textfield4']
    phone = request.form['textfield5']
    email = request.form['textfield6']
    address = request.form['textfield7']

    qry = "UPDATE `student` SET `cid`=%s,`stname`=%s,`qualification`=%s,`gender`=%s,`dob`=%s,`phno`=%s,`semester`=%s,`email`=%s,`address`=%s WHERE lid=%s"
    val = (cid,name,qual,gender,dob,phone,sem,email,address,session['stid'])
    iud(qry,val)

    return '''<script>alert("Updated");window.location="studentreg#about"</script>'''



@app.route('/syllabus')
@login_required
def syllabus():
    return render_template("syllabus.html")

@app.route('/manage_notification')
@login_required
def manage_notification():

    qry = "select * from notification"
    res = selectall(qry)

    return render_template("manage notification.html",val=res)

@app.route('/delete_notification')
@login_required
def delete_notification():

    id = request.args.get("id")
    qry = "delete from notification where nid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_notification#about"</script>'''

@app.route('/insert_notification',methods=['post'])
@login_required
def insert_notification():
    notification = request.form['textfield']
    qry = "insert into notification values(null,%s,curdate())"
    iud(qry,notification)
    return '''<script>alert("Successfully added");window.location="manage_notification#about"</script>'''


@app.route('/send_notification',methods=['post'])
@login_required
def send_notification():
    return render_template("/send notificatio.html")

@app.route('/manage_department')
@login_required
def manage_department():

    qry = "select * from department"
    res = selectall(qry)

    return render_template("manage department.html",val=res)

@app.route('/add_department',methods=['post'])
@login_required
def add_department():
    return render_template("add department.html")

@app.route('/insert_department',methods=['post'])
@login_required

def insert_department():
    dep = request.form['textfield']
    qry = "insert into department values(null,%s)"
    iud(qry,dep)
    return '''<script>alert("Successfully added");window.location="manage_department#about"</script>'''

@app.route('/delete_department')
@login_required
def delete_department():
    id = request.args.get("id")
    qry = "delete from department where deptid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_department#about"</script>'''

@app.route('/manage_subject')
@login_required
def manage_subject():
    qry = "SELECT `course`.`coursename`,`subject`.* FROM `course` JOIN `subject` ON `course`.`cid`=`subject`.cid"
    res = selectall(qry)
    return render_template("manage subject.html", val=res)

@app.route('/delete_subject')
@login_required
def delete_subject():
    id = request.args.get("id")
    qry = "delete from subject where subid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_subject#about"</script>'''

@app.route('/insert_subject',methods=['post'])
@login_required
def insert_subject():
    sem = request.form['select2']
    cid = request.form['select']
    sub = request.form['textfield']

    qry = "insert into subject values(null,%s,%s,%s)"
    val = (cid,sub,sem)
    iud(qry,val)
    return '''<script>alert("Successflly added");window.location="manage_subject#about"</script>'''

@app.route('/view_notification')
@login_required
def view_notification():
    qry = "select * from notification"
    res = selectall(qry)
    return render_template("view notification.html",val=res)

@app.route('/manage_assign')
@login_required
def manage_assign():
    qry ="SELECT `staff`.`fname`,`lname`,`subject`.`subjectname`,assign.* FROM `staff` JOIN `assign` ON `staff`.`lid` = `assign`.`lid` JOIN `subject` ON `assign`.`sid`=`subject`.`subid`"
    res = selectall(qry)
    return render_template("assign subject.html",val=res)

@app.route('/delete_assign')
@login_required
def delete_assign():
    id = request.args.get("id")

    qry = "delete from assign where id=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_assign#about"</script>'''

@app.route('/assign',methods=['post'])
@login_required
def assign():
    qry = "select * from staff"
    res = selectall(qry)

    qry = "select * from subject"
    res2 = selectall(qry)

    return render_template("assign.html",val=res,val2=res2)

@app.route('/assign_insert',methods=['post'])
@login_required
def assign_insert():
    stf = request.form['select']
    sub = request.form['select2']

    qry ="select * from assign where lid=%s and sid=%s"
    val=(stf,sub)
    res = selectone(qry,val)

    if res is None:

        qry = "insert into assign values(null,%s,%s)"
        val = (stf,sub)
        iud(qry,val)

        return '''<script>alert("Successfully added");window.location="manage_assign#about"</script>'''

    else:
        return '''<script>alert("Already assigned");window.location="manage_assign#about"</script>'''

@app.route('/manage_syllabus')
@login_required
def manage_syllabus():
    qry = "SELECT `course`.`coursename`,`syllabus`.* FROM `course` JOIN `syllabus` ON `course`.cid=`syllabus`.cid"
    res = selectall(qry)
    return render_template("manage syllabus.html",val = res)


@app.route('/add_syllabus',methods=['post'])
@login_required
def add_syllabus():
    qry = "select * from course"
    res = selectall(qry)
    return render_template("add syllabus.html",val=res)

@app.route('/insert_syllabus',methods=['post'])
@login_required
def insert_syllabus():
    cid = request.form['select']
    file = request.files['textfield']
    fname = secure_filename(file.filename)
    file.save(os.path.join('static/uploads',fname))

    qry="select * from syllabus where cid=%s"
    res = selectone(qry,cid)

    if res is None:
        qry = "insert into syllabus values(null,%s,%s)"
        val = (cid,fname)
        iud(qry,val)
        return '''<script>alert("Added successfully");window.location="manage_syllabus"</script>'''
    else:
        return '''<script>alert("Already Exist");window.location="manage_syllabus"</script>'''

@app.route('/delete_syllabus')
@login_required
def delete_syllabus():
    id = request.args.get("id")
    qry ="delete from syllabus where syid=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_syllabus"</script>'''


@app.route('/manage_result')
@login_required
def manage_result():
    qry ="SELECT `subject`.`subjectname`,`result`.* FROM `subject` JOIN `result` ON `subject`.subid=`result`.sid"
    res = selectall(qry)
    return render_template("manage result.html",val=res)

@app.route("/add_result",methods=['post'])
@login_required
@login_required
def add_result():
    qry = "SELECT * FROM SUBJECT JOIN `assign` ON `subject`.`subid`=`assign`.`sid` WHERE `assign`.`lid`=%s"
    res = selectall2(qry,session['lid'])
    return render_template("add result.html",val=res)

@app.route('/insert_result',methods=['post'])
@login_required
def insert_result():
    sub = request.form['select']
    file = request.files['textfield2']
    fname = secure_filename(file.filename)
    file.save(os.path.join('static/uploads',fname))
    qry = "insert into result values(null,%s,%s)"
    val = (sub,fname)
    iud(qry,val)
    return '''<script>alert("Successfully added");window.location="manage_result#about"</script>'''


@app.route('/delete_result')
@login_required
def delete_result():
    id=request.args.get("id")
    qry = "delete from result where id=%s"
    iud(qry,id)
    return '''<script>alert("Deleted");window.location="manage_result#about"</script>'''

@app.route('/search_attendance')
@login_required
def search_attendance():
    qry ="SELECT * FROM SUBJECT JOIN `assign` ON `subject`.`subid`=`assign`.`sid` WHERE `assign`.`lid`=%s"
    res = selectall2(qry,session['lid'])

    return render_template("searchattendence.html", val=res)

@app.route('/attendance',methods=['post'])
@login_required
def attendance():

    sub = request.form['select']
    date = request.form['textfield']

    session['sub_id'] = sub

    session['date'] = date

    qry = "SELECT `student`.* FROM `student` WHERE `cid` IN(SELECT `cid` FROM `subject` WHERE `subid`=%s) AND `semester` IN(SELECT `semester` FROM `subject` WHERE `subid`=%s)"
    res = selectall2(qry,(sub,sub))

    return render_template("save attendance.html",val=res)



@app.route('/attendance1',methods=['post'])
@login_required
def attendance1():
    ch=request.form.getlist('check')


    sub = session['sub_id']

    date = session['date']

    qry = "SELECT `student`.* FROM `student` WHERE `cid` IN(SELECT `cid` FROM `subject` WHERE `subid`=%s) AND `semester` IN(SELECT `semester` FROM `subject` WHERE `subid`=%s)"
    res = selectall2(qry,(sub,sub))

    for i in res:
        if str(i['lid']) in ch:
            qry="INSERT INTO `attendence` VALUES(NULL,%s,%s,1,%s)"
            iud(qry,(i['lid'],sub,date))
        else:
            qry = "INSERT INTO `attendence` VALUES(NULL,%s,%s,0,%s)"
            iud(qry, (i['lid'], sub, date))

    return '''<script>alert("Attendance added");window.location="search_attendance#about"</script>'''



app.run(debug=True)