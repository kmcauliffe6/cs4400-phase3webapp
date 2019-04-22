import pymysql
from flask import Flask, request, render_template, redirect, url_for, flash, session
import random
app = Flask(__name__)
connection = pymysql.connect(host='localhost',
                             user='root',
                             passwd='13',
                             db='phase3',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@app.route("/")
def setup():
    return render_template('home.html')

#registration methods
@app.route('/registernavigation')
def registernavigation():
    return render_template('register_navigation.html')

@app.route('/back')
def back_to_home():
    return render_template('home.html')

@app.route('/register_user')
def register_user():
    return render_template('register.html')

@app.route('/register_visitor')
def register_visitor():
    return render_template('register_visitor.html')

@app.route('/register_employee')
def register_employee():
    return render_template('register_employee.html')

@app.route('/register_employee_visitor')
def register_employee_visitor():
    return render_template('register_employee_visitor.html')

@app.route('/manager_manage_staff')
def manager_manage_staff():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    return render_template('manager_manage_staff.html', sites = sites)

@app.route('/manager_site_report')
def manager_site_report():
    return render_template('manager_site_report.html')

@app.route('/staff_view_schedule')
def staff_view_schedule():
    return render_template('staff_view_schedule.html')

@app.route('/visitor_explore_event')
def visitor_explore_event():
    return render_template('visitor_explore_event.html')

@app.route('/visitor_explore_site')
def visitor_explore_site():
    return render_template('visitor_explore_site.html')

@app.route('/visitor_visit_history')
def visitor_visit_history():
    return render_template('visitor_visit_history.html')

@app.route('/manager_manage_event')
def manager_manage_event():
    return render_template('manager_manage_event.html')

@app.route('/manager_manage_event_buttonClick')
def manager_manage_event_buttonClick():
    #manage_event = "SELECT SiteName, COUNT(Username) as Staff Count, Count(VisitorUsername) as Total Visits, "
    #confused about this sql statement
    return render_template('manager_manage_event.html')

@app.route('/employee_manage_profile', methods=['GET','POST'])
def employee_manage_profile():
    sql = "SELECT Firstname, Lastname, Username FROM User WHERE Username = '{username}'".format(username = session['username'])
    cursor.execute(sql);
    for row in cursor:
        first_name = row['Firstname']
        last_name = row['Lastname']
        username = row['Username']
    get_site_name = "SELECT SiteName FROM Site WHERE ManagerUsername = '{username}'".format(username = username)
    cursor.execute(get_site_name)
    sitename = ""
    for row in cursor:
        sitename = row['SiteName']
    get_employee_id = "SELECT EmployeeID, EmployeeAddress, Phone FROM Employee WHERE Username = '{username}'".format(username = username)
    cursor.execute(get_employee_id)
    emp_id = 0
    address = ""
    phone = 0
    for row in cursor:
        emp_id = row['EmployeeID']
        address = row['EmployeeAddress']
        phone = row['Phone']
    get_emails = "SELECT Email FROM UserEmail WHERE Username = '{username}'".format(username = username)
    cursor.execute(get_emails)
    emails = cursor.fetchall()
    #site name
    #employee ID
    #phone
    #address
    #emails
    data = [first_name, last_name, username, phone, sitename, emp_id, address]
    return render_template('manage_profile.html', data=data, emails = emails)

@app.route('/update_profile', methods=['GET','POST'])
def update_profile():
    if not request.form['phone'] == '':
        sql = "UPDATE Employee SET Phone = '{phone}' WHERE Username = '{username}'".format(phone = request.form['phone'], username = session['username'])
        cursor.execute(sql)
    if not request.form['first_name'] == '':
        sql = "UPDATE User SET Firstname = '{name}' WHERE Username = '{username}'".format(name = request.form['first_name'], username = session['username'])
        cursor.execute(sql)
    if not request.form['last_name'] == '':
        sql = "UPDATE User SET Lastname = '{name}' WHERE Username = '{username}'".format(name = request.form['last_name'], username = session['username'])
        cursor.execute(sql)
    if not request.form['email_to_delete'] == "none":
        sql = "DELETE FROM UserEmail WHERE Username = '{username}' AND Email = '{email}'".format(username = session['username'], email = request.form['email_to_delete'])
        cursor.execute(sql)
    if not request.form['new_email'] == '':
        sql = "INSERT INTO UserEmail(Username, Email) VALUES ('{username}', '{email}')".format(username = session['username'], email = request.form['new_email'])
        cursor.execute(sql)
    if request.form.get('isVisitor'):
        sql = "SELECT * FROM Visitor WHERE Username = '{username}'".format(username = session['username'])
        result = cursor.execute(sql)
        if not result:
            print("adding to visitor")
            sql = "INSERT INTO Visitor(Username) Values ('{username}'".format(username = session['username'])
    if not request.form.get('isVisitor'):
        sql = "SELECT * FROM Visitor WHERE Username = '{username}'".format(username = session['username'])
        result = cursor.execute(sql)
        if result:
            print("not visitor anymore")
            sql = "DELETE FROM Visitor WHERE Username = '{username}'".format(username = session['username'])

    #reset values on screen
    sql = "SELECT Firstname, Lastname, Username FROM User WHERE Username = '{username}'".format(username = session['username'])
    cursor.execute(sql);
    userdetails = cursor.fetchone()
    print(userdetails)
    first_name = userdetails['Firstname']
    last_name = userdetails['Lastname']
    username = userdetails['Username']
    get_site_name = "SELECT SiteName FROM Site WHERE ManagerUsername = '{username}'".format(username = username)
    cursor.execute(get_site_name)
    sitename = ""
    for row in cursor:
        sitename = row['SiteName']
    get_employee_id = "SELECT EmployeeID, EmployeeAddress, Phone FROM Employee WHERE Username = '{username}'".format(username = username)
    cursor.execute(get_employee_id)
    emp_id = 0
    address = ""
    phone = 0
    for row in cursor:
        emp_id = row['EmployeeID']
        address = row['EmployeeAddress']
        phone = row['Phone']
    get_emails = "SELECT Email FROM UserEmail WHERE Username = '{username}'".format(username = username)
    cursor.execute(get_emails)
    emails = []
    for row in cursor:
        emails.append(row['Email'])
    data = [first_name, last_name, username, phone, sitename, emp_id, address, emails]
    return render_template('manage_profile.html', data= data)


#NOTE: should probably add hashing for passwords
@app.route('/register', methods=['GET','POST'])
def register():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            emails = request.form['email'].split(',')
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
                return render_template('register.html')
            try:
                for eemail in emails:
                    sql2 = "INSERT INTO UserEmail(Email, Username) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                    cursor.execute(sql2)
                connection.commit()
                session['username'] = request.form['username']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("One of your emails is already being used. Please try again", 'alert-error')
    return render_template('register.html')


@app.route('/register_visitor_buttonclick', methods=['GET','POST'])
def register_visitor_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                    sql2 = "INSERT INTO UserEmail(Email, Username) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                    cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("One of your emails is already being used. Please try again", 'alert-error')
            sql3 = "INSERT INTO Visitor(Username) VALUES ('{username}')".format(username = request.form['username'])
            try:
                cursor.execute(sql3)
                connection.commit()
                session['email'] = request.form['email']
                session['username'] = request.form['username']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong.", 'alert-error')
        return render_template('register_visitor.html')

@app.route('/register_employee_buttonclick', methods=['GET','POST'])
def register_employee_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                        sql2 = "INSERT INTO UserEmail(Email, Username) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                        cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("That email already exists. Please try again.", 'alert-error')
            sql3 = "INSERT INTO Employee(Username, Phone, EmployeeID, EmployeeAddress, EmployeeCity, EmployeeState, EmployeeZipcode) VALUES ('{username}', '{phone}', '{id}', '{address}', '{city}', '{state}', '{zipcode}');".format(username = request.form['username'], phone = request.form['phone'], id = random.randint(1, 999999999), address = request.form['address'], city = request.form['city'], state = request.form['state'], zipcode = request.form['zipcode'])
            if request.form['User Type'] == "Manager":
                sql4 = "INSERT INTO Manager(Username) VALUES ('{username}')".format(username = request.form['username'])
            else:
                sql4 = "INSERT INTO Staff(Username) VALUES ('{username}')".format(username = request.form['username'])
            #need to get employee ID??
            try:
                cursor.execute(sql3)
                cursor.execute(sql4)
                connection.commit()
                session['email'] = request.form['email']
                session['username'] = request.form['username']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong", 'alert-error')
    return render_template('register.html')

@app.route('/register_employee_visitor_buttonclick', methods=['GET','POST'])
def register_employee_visitor_buttonclick():
    if (request.method == 'POST'):
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords need to match", 'alert-error')
        else:
            sql = "INSERT INTO User(Username, Lastname, Firstname, Password, Status) VALUES('{username}', '{last_name}', '{first_name}', '{password}', '{status}');".format(username = request.form['username'],
                last_name = request.form['last_name'], first_name = request.form['first_name'], usertype = request.form['User Type'],
                password = request.form['password'], status = "Not Approved")
            try:
                cursor.execute(sql)
            except pymysql.err.IntegrityError:
                flash("That username already exists. Please try again.", 'alert-error')
            try:
                emails = request.form['email'].split(',')
                for eemail in emails:
                        sql2 = "INSERT INTO UserEmail(Email, Username) VALUES ('{email}', '{username}')".format(email = eemail, username = request.form['username'])
                        cursor.execute(sql2)
            except pymysql.err.IntegrityError:
                flash("That email already exists. Please try again.", 'alert-error')
            sql3 = "INSERT INTO Employee(Username, Phone, EmployeeID, EmployeeAddress, EmployeeCity, EmployeeState, EmployeeZipcode) VALUES ('{username}', '{phone}', '{id}', '{address}', '{city}', '{state}', '{zipcode}');".format(username = request.form['username'], phone = request.form['phone'], id = 111, address = request.form['address'], city = request.form['city'], state = request.form['state'], zipcode = request.form['zipcode'])
            if request.form['User Type'] == "Manager":
                sql4 = "INSERT INTO Manager(Username) VALUES ('{username}')".format(username = request.form['username'])
            else:
                sql4 = "INSERT INTO Staff(Username) VALUES ('{username}')".format(username = request.form['username'])
            sql5 = "INSERT INTO Visitor(Username) VALUES ('{username}')".format(username = request.form['username'])
            #need to get employee ID
            try:
                cursor.execute(sql3)
                cursor.execute(sql4)
                cursor.execute(sql5)
                connection.commit()
                session['email'] = request.form['email']
                session['username'] = request.form['username']
                getUserType(request.form['username'])
                correctpage = goToCorrectFunctionalityPage()
                return render_template('{page}'.format(page = correctpage))
            except pymysql.err.IntegrityError:
                flash("Something went wrong. Please try again.", 'alert-error')
    return render_template('register_employee_visitor.html')

#login methods
@app.route('/login', methods=['GET','POST'])
def login():
    #currently checking username and password, need to write queries to check
    #email and password
    if (request.method == 'POST'):
        sql1 = "SELECT Username FROM UserEmail WHERE Email = '{email}'".format(email = request.form['email'])
        result = cursor.execute(sql1);
        username = ""
        for row in cursor:
            username = row['Username']
        sql2 = "SELECT * FROM  User WHERE Username = '{username1}' AND Password = '{password}'".format(username1 = username, password = request.form['password'])
        result = cursor.execute(sql2);
        if result: #if any rows returned aka username was found
            row = cursor.fetchone()
            session['email'] = row.get('email') #keep track of current user
            getUserType(username)
            correctpage = goToCorrectFunctionalityPage()
            session['username'] = username
            session['email'] = request.form['email']
            print(username)
            print(session['user_type'])
            return render_template('{page}'.format(page = correctpage))
        else:
            flash("Incorrect Credentials. Please Try Again.", 'alert-error')
    return render_template('home.html')

#user function methods
@app.route('/take_transit')
def take_transit():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    print(sites)
    return render_template('user_take_transit.html', sites = sites)
@app.route('/view_transit_history')
def view_transit_history():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    return render_template('user_view_transit_history.html', sites = sites)
#navigation methods
@app.route('/go_to_user_functionality')
def go_to_user_functionality():
    return render_template("user_functionality.html")

@app.route('/go_to_user_type_functionality')
def go_to_user_type_functionality():
    correctpage = goToCorrectFunctionalityPage()
    return render_template('{page}'.format(page = correctpage))


@app.route('/go_to_admin_manage_transit')
def go_to_admin_manage_transit():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    return render_template('admin_manage_transit.html', sites = sites)

#transit methods
@app.route('/filter_transit_buttonClick',methods=['GET','POST'])
def filter_transit_buttonClick():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    siteFilter = request.form['contain_site']
    transportTypeFilter = request.form['transport_type']
    lowerPriceFilter = request.form['lower']
    upperPriceFilter = request.form['upper']
    load_sites = "SELECT TransitRoute, TransitType, TransitPrice, NumSites as '# Connected Sites' FROM transitconnectview WHERE 1=1"
    if not (transportTypeFilter == "ALL" or transportTypeFilter == ''):
        load_sites += " AND TransitType = '{type}'".format(type = transportTypeFilter)
    if not (siteFilter == "ALL" or siteFilter == ''):
        load_sites += " AND SiteName = '{site}'".format(site = siteFilter)
    if (not lowerPriceFilter == ''):
        load_sites += " AND TransitPrice >= '{lower}'".format(lower = lowerPriceFilter)
    if (not upperPriceFilter == ''):
        load_sites += " AND TransitPrice <= '{upper}'".format(upper = upperPriceFilter)
    #not working rn, come back
    print(load_sites)
    cursor.execute(load_sites)
    data = cursor.fetchall()
    return render_template('user_take_transit.html', data = data, sites = sites)

@app.route('/filter_transit_history_buttonClick',methods=['GET','POST'])
def filter_transit__history_buttonClick():
    sites = "SELECT SiteName FROM Site"
    cursor.execute(sites)
    sites = cursor.fetchall()
    #cursor.execute(contain_site)
    transportTypeFilter = request.form['transport_type']
    siteFilter = request.form['contain_site']
    routeFilter = request.form['route']
    sql = "SELECT TransitDate, TransitRoute, TransitType, TransitPrice FROM transitconnectview NATURAL JOIN TakeTransit WHERE Username = '{username}'".format(username = session['username'])
    if not (transportTypeFilter == '' or transportTypeFilter ==  "ALL"):
        sql += " AND TransitType = '{type}'".format(type = transportTypeFilter)
    if not (siteFilter == "ALL" or siteFilter == ''):
        sql += " AND SiteName = '{site}'".format(site = siteFilter)
    if not routeFilter == '':
        sql += " AND TransitRoute = '{route}'".format(route = routeFilter)
    startDateFilter = request.form['start_date']
    endDateFilter = request.form['end_date']
    if not startDateFilter == '':
        sql += " AND TransitDate >= '{lower}'".format(lower = startDateFilter)
    if not endDateFilter == '':
        sql += " AND TransitDate <= '{upper}'".format(upper = endDateFilter)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('user_view_transit_history.html', data=data, sites = sites)


@app.route('/log_transit_buttonClick',methods=['GET','POST'])
def log_transit_buttonClick():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    tablerow = request.form['selected_transit']
    print(tablerow)
    row = tablerow.split(',')
    route = row[0]
    type = row[1]
    sql = "INSERT INTO TakeTransit(Username, TransitType, TransitRoute, TransitDate) VALUES ('{username}', '{type}', '{route}', '{date}')".format(username = session['username'], type = type, route = route, date = request.form['transit_date'])
    result = cursor.execute(sql)
    print(result)
    return render_template('user_take_transit.html', sites =  sites)

#manager methods
@app.route('/manager_site_report_buttonClick',methods=['GET','POST'])
def manager_site_report_buttonClick():
    render_template('manager_site_report.html')
    #if request.form['Daily Detail']:
        #render_template('manager_daily_detail.html')

#admin methods
@app.route('/admin_manage_user',methods=['GET','POST'])
def admin_manage_user():
    #initial load of table
    sql = "SELECT Username, COUNT(Email) AS 'Email Count', Status, UserType FROM User NATURAL JOIN UserEmail NATURAL JOIN usertypeview GROUP BY Username"
    cursor.execute(sql)
    data = cursor.fetchall()

    return render_template('admin_manage_user.html', data = data)

@app.route('/admin_manage_user_filter_buttonClick',methods=['GET','POST'])
def admin_manage_user_filter_buttonClick():
    sql = "SELECT Username, COUNT(Email) AS 'Email Count', Status, UserType FROM User NATURAL JOIN UserEmail NATURAL JOIN usertypeview WHERE 1=1"
    if not request.form['username'] == '':
        sql += " AND Username = '{username}'".format(username = request.form['username'])
    if not (request.form["user_type"] == "ALL" or request.form["user_type"] == ''):
        sql += " AND UserType = '{usertype}'".format(usertype = request.form["user_type"])
    if not (request.form["status"] == "ALL" or request.form["status"] == ''):
        sql += " AND Status = '{status}'".format(status = request.form["status"])
    sql += " GROUP BY Username"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('admin_manage_user.html', data = data)

@app.route('/admin_manage_user_approve_or_decline',methods=['GET','POST'])
def admin_manage_user_approve_or_decline():
    tablerow = request.form['selected_user']
    row = tablerow.split(',')
    if request.form['action'] == 'Approve':
        status = 'Approved'
        print("approve button pressed")
    else:
        status = 'Declined'
    sql = "UPDATE user SET Status = '{status}' WHERE Username = '{username}'".format(status = status, username = row[0])
    result = cursor.execute(sql)
    print(result)
    return render_template('admin_manage_user.html')

@app.route('/admin_manage_site',methods=['GET','POST'])
def admin_manage_site():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()

    sql2 = "SELECT CONCAT(Firstname, ' ', Lastname) as Manager FROM Site Join User On Site.ManagerUsername = User.Username"
    cursor.execute(sql2)
    managers = cursor.fetchall()
    #initial load of table
    sql = "SELECT SiteName, CONCAT(Firstname, ' ', Lastname) as Manager, OpenEveryday FROM Site JOIN User ON Site.ManagerUsername = User.Username;"
    cursor.execute(sql)
    data = cursor.fetchall()
    session['current_data'] = data
    return render_template('admin_manage_site.html', data = data, sites = sites, mans = managers)

@app.route('/admin_manage_site_filter_buttonClick',methods=['GET','POST'])
def admin_manage_site_filter_buttonClick():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    sql2 = "SELECT CONCAT(Firstname, ' ', Lastname) as Manager FROM Site Join User On Site.ManagerUsername = User.Username"
    cursor.execute(sql2)
    managers = cursor.fetchall()

    sql = "SELECT SiteName, CONCAT(Firstname, ' ', Lastname) as Manager, OpenEveryday FROM Site JOIN User ON Site.ManagerUsername = User.Username WHERE 1=1"
    if not (request.form['site'] == '' or request.form['site'] == "ALL"):
        sql += " AND SiteName = '{site}'".format(site = request.form['site'])
    if not (request.form['manager'] == '' or request.form['manager'] == "ALL"):
        name = request.form['manager']
        names = name.split(' ')
        sql += " AND Firstname = '{fname}' AND Lastname = '{lname}'".format(fname = names[0], lname = names[1])
    if not (request.form['open_everyday'] == ''):
        if request.form['open_everyday'] == "Yes":
            value = 1
        else:
            value = 0
        sql += " AND OpenEveryday = '{value}'".format(value = value)
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('admin_manage_site.html', data = data, sites = sites, mans = managers)


@app.route('/admin_manage_site_buttonClick',methods=['GET','POST'])
def admin_manage_site_buttonClick():
    selected_site = request.form['selected_site']
    site_info = selected_site.split(',')
    if request.form['action'] == 'Create':
        get_available_managers = "SELECT DISTINCT CONCAT(Firstname, ' ', Lastname) as Manager FROM Manager JOIN User on Manager.Username = User.Username WHERE User.Username NOT IN (SELECT ManagerUsername FROM Site)"
        cursor.execute(get_available_managers)
        managers = cursor.fetchall()
        return render_template('admin_create_site.html', managers = managers)
    if request.form['action'] == 'Edit':
        get_available_managers = "SELECT DISTINCT CONCAT(Firstname, ' ', Lastname) as Manager FROM Manager JOIN User on Manager.Username = User.Username WHERE User.Username NOT IN (SELECT ManagerUsername FROM Site WHERE not SiteName = '{site}')".format(site = site_info[0])
        cursor.execute(get_available_managers)
        managers = cursor.fetchall()
        data = []
        print(selected_site)
        data.append(site_info[0]) #sitename
        data.append(site_info[1]) #manager
        data.append(site_info[2]) #open everyday
        sql = "SELECT SiteZipcode, SiteAddress FROM Site WHERE SiteName = '{name}'".format(name = site_info[0])
        cursor.execute(sql)
        zipcode = 0
        address = ""
        for row in cursor:
            address = row['SiteAddress']
            zipcode = row['SiteZipcode']
        data.append(zipcode)
        data.append(address)
        session['current_site'] = data[0]
        return render_template('admin_edit_site.html', data = data, managers = managers)
    else:
        sql = "DELETE FROM Site WHERE SiteName = '{name}'".format(name = site_info[0])
        result = cursor.execute(sql)
        print(result)
        return render_template('admin_manage_site.html')

@app.route('/admin_create_site_buttonClicked',methods=['GET','POST'])
def admin_create_site_buttonClicked():
    name = request.form['site_name']
    manager = request.form['manager'] #need to get username
    zipcode = request.form['zipcode']
    address = request.form['address']
    open_everyday = request.form['open_everyday']
    if open_everyday == "Yes":
        oed = 1
    else:
        oed = 0
    splitm = manager.split(' ')
    get_manager_username = "SELECT Username FROM User WHERE Firstname = '{fname}' and Lastname = '{lname}'".format(fname = splitm[0], lname = splitm[1])
    cursor.execute(get_manager_username)
    username = ""
    for row in cursor:
        username = row['Username']
    print(username)
    sql = "INSERT INTO Site(SiteName, ManagerUsername, SiteAddress, SiteZipcode, OpenEveryday) VALUES ('{name}', '{username}', '{address}', '{zipcode}', '{open}')".format(name = name, username = username, address = address, zipcode = zipcode, open = oed)
    cursor.execute(sql)
    return render_template('admin_manage_site.html')

@app.route('/admin_edit_site_updateClicked',methods=['GET','POST'])
def admin_edit_site_updateClicked():
    if not request.form['update_address'] == '':
        sql = "UPDATE Site SET SiteAddress = '{address}' WHERE SiteName = '{name}'".format(address = request.form['update_address'], name = session['current_site'])
        result = cursor.execute(sql)
    if not request.form['update_zipcode'] == '':
        sql = "UPDATE Site SET SiteZipcode = '{zip}' WHERE SiteName = '{name}'".format(zip = request.form['update_zipcode'], name = session['current_site'])
        cursor.execute(sql)
    if not request.form['manager'] == '':
        sql = "UPDATE Site SET ManagerUsername = '{mng}' WHERE SiteName = '{name}'".format(mng = request.form['manager'], name = session['current_site'])
    if request.form['open_everyday'] == "Yes":
        oed = 1
    else:
        oed = 0
    #open everyday not working yet
    sql = "UPDATE Site SET OpenEveryday = '{oed}' WHERE SiteName = '{name}'".format(oed = oed, name = session['current_site'])
    return render_template('admin_manage_site.html')

@app.route('/admin_manage_transit_filterClick',methods=['GET','POST'])
def admin_manage_transit_filterClick():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    sql = "SELECT TransitRoute, TransitType, TransitPrice, NumSites, NumTaken FROM transitconnectview NATURAL JOIN (SELECT TransitType, TransitRoute, COUNT(*) as NumTaken FROM TakeTransit GROUP BY TransitType, TransitRoute) as T WHERE 1=1"
    if not (request.form['transit_type'] == '' or request.form['transit_type'] == "ALL"):
        sql += " AND TransitType = '{type}'".format(type = request.form['transit_type'])
    if not (request.form['contain_site'] == '' or request.form['contain_site'] == "ALL"):
        sql += " AND SiteName = '{name}'".format(name = request.form['contain_site'])
    if not request.form['route'] == '':
        sql += " AND TransitRoute = '{route}'".format(route = request.form['route'])
    if not request.form['lower'] == '':
        sql += " AND TransitPrice >= '{low}'".format(low = request.form['lower'])
    if not request.form['upper'] == '':
        sql += " AND TransitPrice <= '{upper}'".format(upper = request.form['upper'])
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('admin_manage_transit.html', sites = sites, data = data)

@app.route('/admin_manage_transit_create_edit_delete',methods=['GET','POST'])
def admin_manage_transit_create_edit_delete():
    if request.form['action'] == 'Create':
        get_connected_sites = "SELECT SiteName FROM Site"
        cursor.execute(get_connected_sites)
        sites = cursor.fetchall()
        return render_template('admin_create_transit.html', sites = sites)
    if request.form['action'] == 'Edit':
        #edit event stuff here
        variable = 1
    else:
        #not working yet
        details = request.form['selected_transit'];
        #delete button pressed
        sql = "DELETE FROM Transit WHERE TransitType = '{type}' AND TransitRoute = '{route}'".format(type = details[1], route = details[0])
        sql2 = "DELETE FROM CONNECT WHERE TransitType = '{type}' AND TransitRoute = '{route}'".format(type = details[1], route = details[0])
        result = cursor.execute(sql)
        cursor.execute(sql2)
        print(result)
        return render_template('admin_manage_transit.html')

#not currently working, can't figure out why
@app.route('/admin_create_transit_buttonClick',methods=['GET','POST'])
def admin_create_transit_buttonClick():
    sites = request.form['sites'].split(',')
    if len(sites) < 2:
        get_connected_sites = "SELECT SiteName FROM Site"
        cursor.execute(get_connected_sites)
        sites = cursor.fetchall()
        flash("Must Select As Least 2 Connecting Sites.", 'alert-error')
        return render_template('admin_create_transit.html', sites = sites)
    try:
        sql = "INSERT INTO Transit(TransitType, TransitRoute, TransitPrice) VALUES ('{type}', '{route}', '{price}')".format(type = request.form['transport_type'], route = request.form['route'], price = request.form['price'])
        cursor.execute(sql)
        for site in sites:
            print(site)
            sql = "INSERT INTO CONNECT(SiteName, TransitType, TransitRoute) VALUES ('{name}', '{type}', '{route}')".format(name = site, type = request.form['transport_type'], route = request.form['route'])
            cursor.execute(sql)
    except pymysql.err.IntegrityError:
        get_connected_sites = "SELECT SiteName FROM Site"
        cursor.execute(get_connected_sites)
        sites = cursor.fetchall()
        flash("Route and Transport Type Combo Must Be Unique", 'alert-error')
        return render_template('admin_create_transit.html', sites = sites)
    return render_template("admin_manage_transit.html")

#saying method not allowed??
@app.route('/manage_staff_buttonClick',methods=['GET','POST'])
def manage_staff_buttonClick():
    sql = "SELECT SiteName FROM Site"
    cursor.execute(sql)
    sites = cursor.fetchall()
    sql = "SELECT CONCAT(Firstname, ' ', Lastname) as Staff Name, COUNT(EventName) AS NumShifts FROM User JOIN Staff on User.Username = Staff.Username"
    data = cursor.execute(sql).fetchall()
    return render_template('manager_manage_staff.html', sites = sites, data = data)

#staff methods
@app.route('/staff_view_schedule_buttonClick',methods=['GET','POST'])
def staff_view_schedule_buttonClick():
    print(session['username'])
    sql = "SELECT EventName, SiteName, StartDate, EndDate, COUNT(StaffUsername) AS StaffCount FROM Event NATURAL JOIN Assign_To WHERE StaffUsername = '{name}'".format(name = session['username'])
    if not request.form['event_name'] == '':
        sql += " AND EventName = '{ename}'".format(ename = request.form['event_name'])
    if not request.form['description_keyword'] == '':
        sql += " AND Description LIKE '%{key}%'".format(key = request.form['description_keyword'])
    if not request.form['start_date'] == '':
        sql += " AND EndDate >= '{startdate}'".format(startdate = request.form['start_date'])
    if not request.form['end_date'] == '':
        sql += " AND StartDate <= '{enddate}'".format(enddate = request.form['end_date'])
    sql += "GROUP BY EventName, SiteName, StartDate"
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('staff_view_schedule.html', data = data)

@app.route('/staff_view_event_buttonClick',methods=['GET','POST'])
def staff_view_event_buttonClick():
    details = request.form['selection']
    details = details.split(',')
    sql = "SELECT EventName, SiteName, EndDate, (DateDiff(EndDate, StartDate) + 1) AS Duration, Capacity, EventPrice, Description FROM Event WHERE EventName = '{ename}' AND SiteName = '{sname}' AND StartDate = '{start_date}'".format(ename = details[0], sname = details[1], start_date = details[2])
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template('staff_event_detail.html', data = data)

#helper methods
def getUserType(username):
    print(username)
    #need to add visitor/user case
    sql1 = "SELECT * FROM Manager WHERE Username = '{username1}'".format(username1 = username)
    sql2 = "SELECT * FROM Visitor WHERE Username = '{username1}'".format(username1 = username)
    sql3 = "SELECT * FROM Staff WHERE Username = '{username1}'".format(username1 = username)
    sql4 = "SELECT * FROM Administrator WHERE Username = '{username1}'".format(username1 = username)
    sql5 = "SELECT * FROM User WHERE Username = '{username1}'".format(username1 = username)
    isUser = cursor.execute(sql5)
    isManager = cursor.execute(sql1)
    isVisitor = cursor.execute(sql2)
    isStaff = cursor.execute(sql3)
    isAdmin = cursor.execute(sql4)
    if isManager and isVisitor:
        session['user_type'] = "manager-visitor"
        return;
    if isManager:
        session['user_type'] = "manager"
        return;
    if isStaff and isVisitor:
        session['user_type'] = "staff-visitor"
        return;
    elif isStaff:
        session['user_type'] = "staff"
        return;
    if isAdmin and isVisitor:
        session['user_type'] = "admin-visitor"
        return;
    elif isAdmin:
        session['user_type'] = "admin"
        return;
    if isVisitor:
        session['user_type'] = "visitor"
        return;
    if isUser:
        session['user_type'] = "user"
        return;

def goToCorrectFunctionalityPage():
    if session['user_type'] == 'user':
       return 'user_functionality.html'
    if session['user_type'] == "visitor":
        return 'visitor_functionality.html'
    if session['user_type'] == "manager":
        return 'manager_functionality.html'
    if session['user_type'] == "manager-visitor":
        return "manager_visitor_functionality.html"
    if session['user_type'] == "staff-visitor":
        return "staff_visitor_functionality.html"
    if session['user_type'] == "staff":
        return "staff_functionality.html"
    if session['user_type'] == "admin":
        return "administrator_functionality.html"
    if session['user_type'] == "admin-visitor":
        return "admin_visitor_functionality.html"






if __name__ == "__main__":
    app.secret_key = 'supersecretkey'
    app.run(debug=True)
