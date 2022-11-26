from flask import *


from dbconnection import *



app=Flask(__name__)
app. secret_key ="89"
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/')
def adminHome():
    return render_template("login.html")
@app.route('/authenticate',methods=['post'])
def authenticate():
    uname=request.form['username']
    password=request.form['password']
    query="select * from login where USERNAME=%s and PASSWORD=%s"
    value=(uname,password)
    print(value)
    res=selectone(query,value)
    print(res)
    if res is None:
        return '''<script>alert("Invalid username/password");
        window.location="/"</script>
        '''
    elif res[3]=='admin':
        return '''<script>alert("login succesful");
        window.location="/adminhome"</script>'''
    else:
        return '''<script>alert("Invalid username/password");
                window.location="/"</script>
                '''


@app.route('/adminhome')
def login():
    return render_template("adminhome.html")
@app.route('/users')
def viewUser():
    query="select * from registration "
    res=select(query)
    return render_template("view_users.html",val=res)

@app.route('/view&manage_hospitals')
def viewAndManageHospital():
    query="select * from hospital"
    res=select(query)
    print(res);
    return render_template("add&manage_hospital.html",val=res)
@app.route('/feedback')
def viewFeedback():
    query = "SELECT `registration`.`FNAME`,`LNAME`,`feedback`.* FROM `registration` JOIN `feedback` ON `registration`.`LID`=`feedback`.`LID`"
    res = select(query)
    return render_template("feedback.html",val=res)
@app.route('/accident_info')
def accidenrInfo():
    query="SELECT `registration`.`FNAME`,`LNAME` ,`accident_info`.* FROM `registration` JOIN `accident_info` ON `registration`.`LID`=`accident_info`.`LID`"
    res=select(query)
    print(res)
    return render_template("accident_information.html",val=res)
@app.route('/view&manage_vehicle')
def addAndManageVehicle():
    query = "select * from vehicle"
    res = select(query)
    print(res);

    return render_template("add&manageveh.html",val=res)

@app.route('/edit_vehicle')
def geteditVehicle():
    id=request.args.get('id')
    session['vid']=id
    print(id)
    query="select * from vehicle where vid=%s"
    val=selectone(query,id)
    print(val)
    return render_template("editVehicle.html",v=val)

@app.route('/editVehicle',methods=['post'])
def editVehicle():
    vehicleNo=request.form['vehicleNo']
    driverName = request.form['driverName']
    driverPhone = request.form['driverPhone']
    address = request.form['address']
    value=(vehicleNo,driverName,driverPhone,address,session['vid'])
    query='update vehicle set vehicle_no=%s,driver_name=%s,driver_phn=%s,address=%s where vid=%s'
    id=iud(query,value)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Vehicle Edited");
                window.location="/add_hospital"</script>
                '''

@app.route('/deleteVehicle',)
def deleteVehicle():
    id = request.args.get('id')
    query='DELETE FROM vehicle WHERE vid=%s'
    id=iud(query,id)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Vehicle Deleted");
                window.location="/view&manage_vehicle"</script>
                '''





@app.route('/add_hospital')
def getHospital():
            return render_template("Hospital.html")

@app.route('/addHospital',methods=['post'])
def addHospital():
    name=request.form['hname']
    place = request.form['hplace']
    description = request.form['description']
    contactNo = request.form['hcontact']
    latitude = request.form['hlatitude']
    longitude = request.form['hlongitude']
    value = (name, place,description,contactNo,latitude,longitude)
    print(value)
    query="INSERT INTO `hospital` VALUES(NULL,%s,%s,%s,%s,%s,%s)"
    id=iud(query,value)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Hospital added");
                window.location="/add_hospital"</script>
                '''




@app.route('/view_news')
def viewNews():
    return render_template("news.html")


@app.route('/edit_hospital')
def geteditHospital():
    id=request.args.get('id')
    session['hid']=id
    print(id)
    query="select * from hospital where HID=%s"
    val=selectone(query,id)
    print(val)
    return render_template("edit_hospital.html",val=val)

@app.route('/editHospital',methods=['post'])
def editHospital():
    name=request.form['hname']
    place = request.form['hplace']
    description = request.form['description']
    contact = request.form['hcontact']
    latitude = request.form['hlatitude']
    longitude = request.form['hlongitude']

    value=(name,place,description,contact,latitude,longitude,session['hid'])
    query='update hospital set NAME=%s,PLACE=%s,DISCRIPTION=%s,`CONTACT NUMBER`=%s,LATITUDE=%s,LONGITUDE=%s where HID=%s'
    id=iud(query,value)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Hospital Edited");
                window.location="/add_hospital"</script>
                '''

@app.route('/deleteHospital',)
def deleteHospital():
    id = request.args.get('id')
    query='DELETE FROM hospital WHERE hid=%s'
    id=iud(query,id)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Hospital Deleted");
                window.location="/view&manage_hospitals"</script>
                '''



@app.route('/add_vehicle',)
def getVehicle():
    return render_template("addVehicle.html")


@app.route('/addVehicle',methods=['post'])
def addVehicle():
    vehicleNo=request.form['vehicleNo']
    driverName = request.form['driverName']
    driverPhone = request.form['driverPhone']
    address = request.form['address']
    username = request.form['username'];
    password = request.form['password'];
    query1 = "INSERT INTO `login` VALUES(NULL,%s,%s,'emergency')"
    value = (username, password)
    id1 = iud(query1, value)

    query="INSERT INTO `vehicle` VALUES(NULL,%s,%s,%s,%s)"
    value = (vehicleNo, driverName, driverPhone, address)
    id=iud(query,value)
    if id is None:
        return '''<script>alert("Error");
        window.location="/"</script>
        '''
    else:
        return '''<script>alert("Vehicle added");
                window.location="/add_vehicle"</script>
                '''




@app.route('/news',methods=['get'])
def news():
    con = pymysql.connect(host="localhost", user="root", password="", port=3306, database="accident detection")
    cmd = con.cursor()
    import requests

    res = requests.get("https://malayalam.news18.com/kerala/").text

    ress = res.split('<div class="section-blog-left-img-list">')[1]
    ress = ress.split('</ul>')[0]
    ress = ress.split('<li>')
    string = []
    links = []
    for i in range(1, len(ress) - 1):
        # print(ress[i])

        lin = ress[i].replace('</a></li>', '')
        lin = lin.replace('<span class="photo_icon_ss"></span>', '')
        lines = lin.split('">')
        link = 'https://malayalam.news18.com/' + lines[0].split('href="')[1]
        stri = lines[1]
        string.append(stri)
        links.append(link)

    ress = res.split('<div class="blog-list-blog">')
    for i in range(1, len(ress) - 1):
        lin = ress[i].split('<p><a href="')[1].split('</a>')
        lin = lin[0].split('">')
        string.append(lin[1])
        links.append('https://malayalam.news18.com/' + lin[0])

    json_data = []
    row_headers=['string','links']
    for i in range(0,len(string)):
        result=[string[i],links[i]]
        # if result[0].startswith("Accident"):
        json_data.append(dict(zip(row_headers, result)))
    con.commit()



    return render_template("news.html",val=json_data)





app.run(debug=True)