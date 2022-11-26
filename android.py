from flask import *


from dbconnection import *

app=Flask(__name__)
app. secret_key ="89"


@app.route('/login',methods=['post'])
def login():
    username=request.form['username']
    password=request.form['password']
    query = "select * from login where USERNAME=%s and PASSWORD=%s"
    value = (username, password)
    res = selectone(query, value)
    print(res)
    if res is None:
        return jsonify({'task':'invalid'})
    else:
        print({'task':'valid','id':res[0],'type':res[2]})
        return jsonify({'task':'valid','id':res[0],'type':res[3]})

@app.route('/registration',methods=['post'])
def registration():
    fname=request.form['fname']
    lname = request.form['lname']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    phone = request.form['phone']
    username=request.form['username']
    password = request.form['password']
    query1="INSERT INTO `login` VALUES(NULL,%s,%s,'user')"
    value=(username,password)
    id=iud(query1,value)
    query='INSERT INTO `registration` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s)'
    value1=(id,fname,lname,place,post,pin,phone)
    id1=iud(query,value1)

    return jsonify({'task':'succes'})

@app.route('/viewProfile',methods=['post'])
def viewProfile():
    id=request.form['id']
    print(id)
    query="SELECT * FROM `registration` WHERE`LID`=%s"
    value=(id)
    res=androidselectall(query,value)
    print(res)
    return jsonify(res)

@app.route('/editProfile',methods=['post'])
def editProfile():
    id=request.form['id']
    fname = request.form['fname']
    lname = request.form['lname']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    phone = request.form['phone']
    print("id"+id)
    query="UPDATE `registration` SET `FNAME`=%s,`LNAME`=%s,`PLACE`=%s,`POST`=%s,`PIN`=%s,`PHONE`=%s WHERE LID=%s"
    value=(fname,lname,place,post,pin,phone,id)
    id=iud(query,value)
    return jsonify({'task': 'succes'})

@app.route('/viewNews',methods=['post'])
def viewNews():
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
        if len(stri)>30:
            string.append(stri)
            links.append(link)

    ress = res.split('<div class="blog-list-blog">')
    for i in range(1, len(ress) - 1):
        lin = ress[i].split('<p><a href="')[1].split('</a>')
        lin = lin[0].split('">')
        if len(lin[1])>30:

            string.append(lin[1])
            links.append('https://malayalam.news18.com/' + lin[0])
        print(lin)

    print(string)
    print(links)
    json_data = []
    row_headers = ['news', 'link']
    for i in range(0, len(string)):
        result = [string[i], links[i]]
        json_data.append(dict(zip(row_headers, result)))
    con.commit()
    print(json_data)
    return jsonify(json_data)

@app.route('/viewHospitals',methods=['post'])
def viewHospital():
    print(request.form)
    lati=request.form['lati']
    longi=request.form['longi']
    print(lati)
    query = "SELECT `hospital`.*, (3959 * ACOS ( COS ( RADIANS(%s) ) * COS( RADIANS( latitude) ) * COS( RADIANS( longitude ) - RADIANS(%s) ) + SIN ( RADIANS(%s) ) * SIN( RADIANS( latitude ) ))) AS user_distance FROM `hospital` HAVING user_distance  < 31.068"
    val=(lati,longi,lati)
    res =androidselectall(query,val)
    print(res)
    return jsonify(res)

@app.route('/viewEmergency',methods=['post'])
def viewEmergency():
    query="SELECT `accident_info`.*, (3959 * ACOS ( COS ( RADIANS(%s) ) * COS( RADIANS( `LATITUDE`) ) * COS( RADIANS( `LONGITUDE` ) - RADIANS(%s) ) + SIN ( RADIANS(%s) ) * SIN( RADIANS( `LATITUDE` ) ))) AS user_distance FROM `accident_info` HAVING user_distance  < 31.068 AND `status`='pending'"
    print(request.form)
    lati=request.form['lati']
    longi=request.form['longi']
    val = (lati, longi, lati)
    print(val,"====================================")
    res = androidselectall(query, val)
    print(res,"*****************")
    return jsonify(res)

@app.route('/viewAccidentInfo',methods=['post'])
def viewAccidentInfo():
    query = "SELECT `registration`.`FNAMe`,`LNAME` ,`accident_info`.* FROM `registration` JOIN `accident_info` ON `registration`.`LID`=`accident_info`.`LID`"
    res = select(query)
    print(res)
    return jsonify(res)

@app.route('/setEmergencyNumber',methods=['post'])
def setEmergencyNumber():
        name=request.form['name']
        phone=request.form['number']
        uid=request.form['id']
        query="INSERT INTO `contact_list` values(null,%s,%s,%s)"
        value = (name, phone, uid)
        iud(query,value)
        return jsonify({'task': 'valid'})

@app.route('/update_stat',methods=['post'])
def update_stat():
    aid=request.form['aid']
    status=request.form['status'];
    print(aid,"id===")
    query="update `accident_info` set status=%s where AID=%s"
    value=(status,aid)
    iud(query,value)
    return jsonify({'task':'valid'})

@app.route('/sendFeedback',methods=['post'])
def sendFeedback():
    feedback=request.form['feedback']
    uid=request.form['id']
    value=(uid,feedback)
    query="INSERT INTO `feedback` VALUES(null,%s,%s,curdate())"
    iud(query, value)
    return jsonify({'task': 'succes'})


@app.route('/manuallyAddAccident',methods=['post'])
def manuallyAddAccident():
    date=request.form['data']
    latitude=request.form['latitude']
    longitude=request.form['longitude']
    uid=request.form['id']
    value=(uid,date,latitude,longitude)
    query="INSERT INTO `accident_info` VALUES(%s,%s,%s,%s)"
    iud(query, value)
    return jsonify({'task': 'succes'})

@app.route('/view_rootmap1',methods=['post'])
def view_rootmap1():
    date=request.form['date']
    uid=request.form['uid']
    if date=="na":
        query="SELECT * FROM `accident_info` GROUP BY `DATE`"
        res=androidselectallnew(query)
        print(res,"=====================")
        return jsonify(res)
    else:
        query = "SELECT * FROM `accident_info` WHERE DATE=%s GROUP BY `DATE`"
        value = (str(date))
        res = androidselectall(query, value)
        return jsonify(res)

@app.route('/emergency',methods=['post'])
def emergency():
    latitude=request.form['lati']
    longitude=request.form['longi']
    uid=request.form['uid']
    query="INSERT INTO `accident_info` VALUES(null,%s,curdate(),%s,%s,'pending',curtime())"
    value=(uid,latitude,longitude)
    iud(query, value)
    qry="SELECT phn_no FROM `contact_list` WHERE `id`=%s"
    res=androidselectall(qry,uid)
    print(res)
    return jsonify(res)
# @app.route('/service',methods=['post'])
# def emergency():
#     q=""


app.run(port=5000,host="0.0.0.0")


