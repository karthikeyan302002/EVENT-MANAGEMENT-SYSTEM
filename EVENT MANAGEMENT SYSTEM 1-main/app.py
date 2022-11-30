from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import re
import datetime as dt

# global length
app = Flask(__name__,template_folder='template')

app.secret_key = 'k'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'function_system'

mysql = MySQL(app)


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template('index.html', data = fetchdata)




@app.route('/login', methods =['GET','POST'])
def login():
    global dept_id
    msg = ''
    
    
    #Data in drop down menu
    cur = mysql.connection.cursor()
    cur.execute("SELECT department_name FROM admin")
    login_data = cur.fetchall()
    print(login_data)
    cur.close()
    
    #login user and create session
    if request.method == 'POST':
        department = request.form['department']
        password = request.form['password']
        
        
        print(department , password)
        
        # checking for existing account using cursor
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admin WHERE department_name = %s AND password = %s" , (department,password,))
        account = cursor.fetchone()
        print("account")
        print(account)
        cursor.close()
        
       
        # if account exists crate a session data
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            dept_id = account[0]
            msg = 'Logged in successfully !'
            
            #cursor for checking user data availablity
            user_id = session['id']
            # events_account=''
            events_cursor = mysql.connection.cursor()
            events_cursor.execute("SELECT * FROM events WHERE dept_id = {}".format(user_id))
            events_account = events_cursor.fetchall()
            events_length = len(events_account)
            print("user account")
            print(events_account)
            print(events_length)
            events_cursor.close()
            
            return render_template('dashboard.html', length = events_length, event_data = events_account, account = account)
        
        else:
            msg = 'Incorrect password !'
        
    return render_template('login.html', msg = msg, data = login_data)
    
    # return render_template('login.html', data = login_data)
    
    
    
    
@app.route('/dashboard')
def dashboard():
    user_id = session['id']

    events_cursor = mysql.connection.cursor()
    events_cursor.execute("SELECT * FROM events WHERE dept_id = {}".format(user_id))
    events_account = events_cursor.fetchall()
    # events_display = events_cursor.
    events_length = len(events_account)
    print("user account")
    print(events_account)
    print(events_length)
    events_cursor.close()
    # events = []
    # while events_account != False:
    #     events.append(events_account)
    #     events_account = events_cursor.fetch
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin")
    account = cursor.fetchone()
    
    #cursor for selecting the upcomming event
    return render_template('dashboard.html', length=events_length, event_data = events_account,account=account)





@app.route('/view_events/<int:id>')
def view_event(id):
    uid = id
    
    #cursor for selecting department name
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin")
    des_dept_account = cursor.fetchone()
    
    #cursor for selecting specific item
    des_cursor = mysql.connection.cursor()
    des_cursor.execute("SELECT * FROM events WHERE id = {} AND dept_id = {}".format(uid,session['id']))
    des_account = des_cursor.fetchone()
    print(des_account)
    
    return render_template('event_des.html',d_msg = uid, d_account = des_account, admin_acc = des_dept_account)
  
  
  
  
    

@app.route('/event')
def event():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin")
    account = cursor.fetchone()
    
    return render_template('event_details.html', account = account)






@app.route('/create_event', methods = ['GET','POST'])
def add_events():
    msg = ''
    dep_id = session['id']
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        org_dept = request.form['org_dept']
        hod_name = request.form['hod_name']
        part_dept = request.form['part_dept']
        part_clg = request.form['part_clg']
        event_mode = request.form['event_mode']
        guest_details = request.form['guest_details']
        al_batch_yrs = request.form['al_batch_yrs']
        al_clg_name = request.form['al_clg_name']
        staff_cord = request.form['staff_cord']
        student_cord = request.form['student_cord']
        staff_rapp = request.form['staff_rapp']
        studnet_rapp = request.form['studnet_rapp']
        fun_level = request.form['fun_level']
        partici_type = request.form['partici_type']
        partici_no = request.form['no_partici'] 
        no_days = request.form['no_days']
        
        #date and time
        date = request.form['event_date']
        time = request.form['event_time']
        
        print("dfds",type(date))
        
        
        
        #cursor for inserting a data
        ins_cursor = mysql.connection.cursor()
        # ins_cursor.execute("INSERT INTO events (dept_id,event_name,event_type,organizing_dept,hod_name,participating_clg,participating_dept,event_mode,guest_details,alumni_batch_yr,alumni_clg_name,staff_coordinator,student_coordinator,staff_rapportuer,student_rapportuer,function_level,participation_type,no_participants,no_days,event_time,event_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s)",
        #                    [dep_id,event_name,event_type,org_dept,hod_name,part_dept,part_clg,event_mode,guest_details,al_batch_yrs,al_clg_name,staff_cord,
        #                     student_cord,staff_rapp,studnet_rapp,fun_level,partici_type,partici_no,no_days,date,time])
        
        
        ins_cursor.execute("INSERT INTO events (dept_id,event_name,event_type,organizing_dept,hod_name, participating_dept,participating_clg,event_mode,guest_details,alumni_batch_yr,alumni_clg_name,staff_coordinator,student_coordinator,staff_rapportuer,student_rapportuer,function_level,participation_type,no_participants,no_days,event_time,event_date) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}', {20})"
                           .format(dep_id,event_name,event_type,org_dept,hod_name,part_dept,part_clg,event_mode,guest_details,al_batch_yrs,al_clg_name,staff_cord,
                            student_cord,staff_rapp,studnet_rapp,fun_level,partici_type,partici_no,no_days,time,date))
        mysql.connection.commit()
        ins_cursor.close()
        
        msg = 'registered successfully'
        session['loggedin'] = True
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    
    return render_template('add_event.html',msg = msg)





@app.route('/add_event_close')
def add_eve_close():
    user_id = session['id']

    events_cursor = mysql.connection.cursor()
    events_cursor.execute("SELECT * FROM events WHERE dept_id = {}".format(user_id))
    events_account = events_cursor.fetchall()
    # events_display = events_cursor.
    events_length = len(events_account)
    print("user account")
    print(events_account)
    print(events_length)
    events_cursor.close()
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM admin")
    account = cursor.fetchone()
    
    return render_template('dashboard.html',length=events_length, event_data = events_account,account=account)




@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id',None)
    return render_template('index.html')



if __name__ == '__main__':
   app.run(host='0.0.0.0')