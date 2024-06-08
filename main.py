# main.py
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import os
import base64
import mysql.connector
import hashlib
import datetime
from datetime import date
import time
from random import seed
from random import randint
from PIL import Image
import stepic
import urllib.request
import urllib.parse
from urllib.request import urlopen

from math import sin, cos, sqrt, atan2, radians
import webbrowser
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  charset="utf8",
  database="ev_charging"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'


@app.route('/')
def index():
    cursor = mydb.cursor()
    '''rdate=""
    sid="3"
    i=2
    cursor.execute("SELECT count(*) FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(i,sid,rdate))
    cn= cursor.fetchone()[0]
    print(cn)'''

    #t = time.localtime()
    #rtime = time.strftime("%H:%M:%S", t)
    #print(rtime)
    
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        lat=request.form['lat']
        lon=request.form['lon']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ev_register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            cursor.execute("update ev_register set latitude=%s,longitude=%s where uname=%s",(lat,lon,uname))
            mydb.commit()
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login2', methods=['GET', 'POST'])
def login2():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ev_station WHERE uname = %s AND pass = %s && status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password! or Not Approved'
    return render_template('login2.html',msg=msg)

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ev_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_admin.html',msg=msg)



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ev_register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        address=request.form['address']
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        account=request.form['account']
        card=request.form['card']
        bank=request.form['bank']
        uname=request.form['uname']
        pass1=request.form['pass']

        cursor = mydb.cursor()
        sql = "INSERT INTO ev_register(id,name,address,mobile,email,account,card,bank,amount,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        val = (maxid,name,address,mobile,email,account,card,bank,'10000',uname,pass1)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="sucess"
        return redirect(url_for('login'))

    return render_template('register.html',msg=msg)

@app.route('/reg_station', methods=['GET', 'POST'])
def reg_station():
    msg=""
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ev_station")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        stype=request.form['stype']
        name=request.form['name']
        num_charger=request.form['num_charger']
        area=request.form['area']
        city=request.form['city']
        lat=request.form['lat']
        lon=request.form['lon']
        uname=request.form['uname']
        pass1=request.form['pass']
        landmark=request.form['landmark']
        mobile=request.form['mobile']
        email=request.form['email']

        
        sql = "INSERT INTO ev_station(id,name,stype,num_charger,area,city,lat,lon,uname,pass,landmark,mobile,email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        val = (maxid,name,stype,num_charger,area,city,lat,lon,uname,pass1,landmark,mobile,email)
        mycursor.execute(sql, val)
        mydb.commit()

        num=int(num_charger)
        i=1
        while i<=num:
            mycursor.execute("SELECT max(id)+1 FROM ev_slot")
            maxid2 = mycursor.fetchone()[0]
            if maxid2 is None:
                maxid2=1
            sql = "INSERT INTO ev_slot(id,station,slot) VALUES (%s, %s, %s)"
        
            val = (maxid2,str(maxid),str(i))
            mycursor.execute(sql, val)
            mydb.commit()
            i+=1

        msg="success"
        #return redirect(url_for('login2'))

    return render_template('reg_station.html',msg=msg)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    email=""
    mess=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station")
    data= cursor.fetchall()

    
    if act=="yes":
        sid=request.args.get("sid")

        cursor.execute("SELECT * FROM ev_station where id=%s",(sid,))
        dd = cursor.fetchone()
        email=dd[13]
        mess="EV Station Approved, Username: "+dd[8]+", Password:"+dd[9]
            
        cursor.execute("update ev_station set status=1 where id=%s",(sid,))
        mydb.commit()
        msg="ok"

    
    return render_template('admin.html',msg=msg, data=data,mess=mess,email=email)

@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('userhome.html',msg=msg, data=data, uname=uname)

@app.route('/station', methods=['GET', 'POST'])
def station():
    msg=""
    st=""
    rdx=""
    sdata=[]
    data=[]
    # approximate radius of earth in km
    R = 6373.0
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    usr= cursor.fetchone()
    lat=usr[11]
    lon=usr[12]
    lat2=float(lat)
    lon2=float(lon)

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    cd1=rdate.split("-")
    rdate2=now.strftime("%Y-%m-%d")
    #######
    cursor.execute("SELECT * FROM ev_station")
    sdata= cursor.fetchall()
    for d1 in sdata:
        
        dt=[]
        lat1=float(d1[6])
        lon1=float(d1[7])
        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        print(dlon)
        print(dlat)
        distance = R * c
        print("Distance:"+d1[4])
        print("Result:", distance)

        dis=round(distance,2)
        dis1=str(dis)

        dds=str(distance)
        ddv=dds[0:2]
        cursor.execute("update ev_station set distance=%s where id=%s",(ddv,d1[0]))
        mydb.commit()
    #####

    if request.method=='POST':
        getval=request.form['getval']
        rdate1=request.form['rdate1']
        prd='%'+getval+'%'

        rdd=rdate1.split("-")
        rdx=rdd[2]+"-"+rdd[1]+"-"+rdd[0]

        ##
        d0 = date(int(cd1[2]), int(cd1[1]), int(cd1[0]))
        d1 = date(int(rdd[0]), int(rdd[1]), int(rdd[2]))        
        delta = d1 - d0
        dy=delta.days
        #print(dy)
        ##

        print(rdx)
    
        
        cursor.execute("SELECT count(*) FROM ev_station where area like %s || city like %s || landmark like %s",(prd,prd,prd))
        dn= cursor.fetchone()[0]
        if dn>0 and dy>=0:
            st="1"
            cursor.execute("SELECT * FROM ev_station where area like %s || city like %s || landmark like %s order by  distances",(prd,prd,prd))
            sdata= cursor.fetchall()
            for d1 in sdata:
                dt=[]
                lat1=float(d1[6])
                lon1=float(d1[7])
                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                print(dlon)
                print(dlat)
                distance = R * c
                print("Distance:"+d1[4])
                print("Result:", distance)

                dis=round(distance,2)
                dis1=str(dis)

                dt.append(d1[0])
                dt.append(d1[1])
                dt.append(d1[2])
                dt.append(d1[3])
                dt.append(d1[4])
                dt.append(d1[5])
                dt.append(d1[6])
                dt.append(d1[7])
                dt.append(d1[8])
                dt.append(d1[9])
                dt.append(d1[10])
                dt.append(d1[11])
                dt.append(d1[12])
                dt.append(d1[13])
                

                dt2=[]
                ss=""
                cursor.execute("SELECT count(*) FROM ev_booking where station=%s && rdate=%s && status=1",(d1[0],rdx))
                d4= cursor.fetchone()[0]
                if d4>0:
                    cursor.execute("SELECT * FROM ev_booking where station=%s && rdate=%s && status=1",(d1[0],rdx))
                    d41= cursor.fetchall()
                    dt2.append(d41)
                    ss="yes"
                else:
                    ss="no"

                dt.append(dt2)
                dt.append(ss)
                dt.append(d1[14])
                data.append(dt)
                    
            
        else:
            st="2"

    else:
        st="1"
        ss=""
        cursor.execute("SELECT * FROM ev_station order by distance")
        sdata= cursor.fetchall()
        for d1 in sdata:
            
            dt=[]
            
                
            dt.append(d1[0])
            dt.append(d1[1])
            dt.append(d1[2])
            dt.append(d1[3])
            dt.append(d1[4])
            dt.append(d1[5])
            dt.append(d1[6])
            dt.append(d1[7])
            dt.append(d1[8])
            dt.append(d1[9])
            dt.append(d1[10])
            dt.append(d1[11])
            dt.append(d1[12])
            dt.append(d1[13])
            

            dt2=[]
            ss=""
            cursor.execute("SELECT count(*) FROM ev_booking where station=%s && rdate=%s && status=1",(d1[0],rdx))
            d4= cursor.fetchone()[0]
            if d4>0:
                cursor.execute("SELECT * FROM ev_booking where station=%s && rdate=%s && status=1",(d1[0],rdx))
                d41= cursor.fetchall()
                dt2.append(d41)
                ss="yes"
            else:
                ss="no"

            dt.append(dt2)
            dt.append(ss)
            dt.append(d1[14])
            data.append(dt)

    print(data)
    return render_template('station.html',msg=msg, data=data, uname=uname,st=st,rdate2=rdate2)

@app.route('/slot', methods=['GET', 'POST'])
def slot():
    msg=""
    act=""
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0
    s8=0
    s9=0
    s10=0

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      charset="utf8",
      database="ev_charging"

    )
    uname=""
    if 'username' in session:
        uname = session['username']
    #if request.method=='GET':
    sid=request.args.get('sid')

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]
    num=dd[3]
    sdata=[]
    i=1

    cursor.execute("SELECT * FROM ev_slot where station=%s",(sid, ))
    srow= cursor.fetchall()
    for sr in srow:
        dt=[]
        dd=[]
        dt2=[]
        sv="no"
        ##
        dt.append(sr[2])
        ##
        '''cursor.execute("SELECT count(*) FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
        cn= cursor.fetchone()[0]
        dt1=[]
        if cn>0:
            cursor.execute("SELECT * FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
            dd= cursor.fetchall()
            for ds in dd:
                dt2=[]
                book=ds21=ds[3]+" ["+ds[24]+" - "+ds[25]+"]"
                dt2.append(str(ds[26]))
                dt2.append(book)
                dt2.append(str(ds[0]))
                dt1.append(dt2)
            
        else:
            dt1.append("")'''
            
        dt1=""
        dt.append(dt1)
        ##
        sv=""
        cursor.execute("SELECT count(*) FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
        cn= cursor.fetchone()[0]
        if cn>0:
            cursor.execute("SELECT * FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
            dd= cursor.fetchone()
            if dd[26]==5:
                sv="yes"
            else:
                sv="no"
        else:
            sv="no"
        
        dt.append(sv)
        dt.append(dd)
        ##

        
        '''cursor.execute("SELECT count(*) FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
        cn= cursor.fetchone()[0]
        if cn>0:
            cursor.execute("SELECT * FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
            dd= cursor.fetchone()
            sv="yes"
        else:
            sv="no"
        
        
        dt.append(sv)

        dt.append(str(i))
        dt.append(dd)

        cursor.execute("SELECT * FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(sr[2],sid,rdate))
        dd2= cursor.fetchall()
            
        for ds2 in dd2:            
            ds21=ds2[3]+" ["+ds2[24]+" - "+ds2[25]+"]"
            dt2.append(ds21)'''
            
        #dt.append(dt2)
        sdata.append(dt)
        i+=1
    
     
    act="ok"
    return render_template('slot.html',msg=msg,uname=uname,sid=sid,station=station,act=act,sdata=sdata)

@app.route('/page', methods=['GET', 'POST'])
def page():
    st=""
    mobile=""
    mess=""
    uname=""
    name=""
    msg1=""
    msg2=""
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    rid=request.args.get('rid')

    cursor = mydb.cursor()

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    t = time.localtime()
    rtime = time.strftime("%H", t)
    rmin = time.strftime("%M", t)
    rm=int(rmin)
    
    chour=int(rtime)
    
    cursor.execute("SELECT * FROM ev_booking where status=1 && rdate=%s && alert_st=0",(rdate,))
    dd = cursor.fetchall()
    for ds in dd:
        tt=ds[24]
        print(tt)
        t1=tt.split(":")
        hh=t1[0]
        mm=t1[1]
        mn=int(mm)+3
        rid1=ds[0]
        '''if rtime==hh:
            if rm<=mn:'''
        rid1=ds[0]
        vno=ds[3]
        cursor.execute("SELECT * FROM ev_register where uname=%s",(ds[1],))
        uu = cursor.fetchone()
        name=uu[1]
        mobile=uu[3]
        print(mobile)
        st="1"
        #msg2="2"
        mess=vno+", Slot:"+str(ds[5])+", Charging Time Started"
        #url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name="+name+"&mess="+mess+"&mobile="+str(mobile)
        #webbrowser.open_new(url)
        cursor.execute("update ev_booking set alert_st=1 where status=1 && rdate=%s && alert_st=0 && id=%s",(rdate,rid1))
        mydb.commit()
        break
                
    
    vno=""
    rid1=0
    rid2=""
    cursor.execute("SELECT * FROM ev_booking where status=1 && rdate=%s && alert_st>=1",(rdate,))
    dd2 = cursor.fetchall()
    for ds2 in dd2:
        at=ds2[26]
        rid1=ds2[0]
        rid2=str(ds2[0])
        vno=ds2[3]
        if at==1:
            cursor.execute("SELECT * FROM ev_register where uname=%s",(ds2[1],))
            uu = cursor.fetchone()
            name=uu[1]
            mobile=uu[3]
            print(mobile)
            msg2="2"
            mess=vno+", Slot:"+str(ds2[5])+",Charging Time Started"
            print(mess)
        
        if at<5:
            cursor.execute("update ev_booking set alert_st=alert_st+1 where status=1 && rdate=%s && alert_st>0 && id=%s",(rdate,rid1))
            mydb.commit()
            msg1=str(ds2[26])
            break
        
        


    #cursor.execute("update ev_booking set plan=%s,charge_st=1,charge_min=0,charge_sec=0 where id=%s",(plan, rid))
    #mydb.commit()
        
        
    return render_template('page.html',sid=sid,rid=rid,st=st,mobile=mobile,mess=mess,name=name,msg1=msg1,vno=vno,rid2=rid2,msg2=msg2)

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    msg=""
    act=request.args.get('act')
    rid2=request.args.get('rid2')
    retime=""
    cursor = mydb.cursor()
    cursor.execute("update ev_booking set alert_st=7 where id=%s",(rid2,))
    mydb.commit()

    t = time.localtime()
    rtime = time.strftime("%H", t)
    rmin = time.strftime("%M", t)

    rh=int(rtime)+1
    rh1=str(rh)
    
    btime1=rh1+":"+"00"
    btime2=rh1+":30"
    retime=btime1+" - "+btime2
    
    if act=="ok":
        cursor.execute("update ev_booking set btime1=%s,btime2=%s,alert_st=0,status=1 where id=%s",(btime1,btime2,rid2))
        mydb.commit()
        msg="go"
        #return redirect(url_for('page'))

    if act=="cancel":
        cursor.execute("delete from ev_booking where id=%s",(rid2,))
        mydb.commit()
        msg="go"
        #return redirect(url_for('page'))

        
    return render_template('page2.html',msg=msg,rid2=rid2,act=act,retime=retime)

@app.route('/page3', methods=['GET', 'POST'])
def page3():

    return render_template('page3.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    rid=request.args.get('rid')
    if request.method=='POST':
        plan=request.form['plan']
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set plan=%s,charge_st=1,charge_min=0,charge_sec=0 where id=%s",(plan, rid))
        mydb.commit()
        return redirect(url_for('slot',sid=sid))
        
    return render_template('select.html',sid=sid,rid=rid)


'''@app.route('/book1', methods=['GET', 'POST'])
def book1():
    msg=""
    act=""
    cimage=""
    slot=""
    av=""
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    
    #if request.method=='GET':
        #sid=request.args.get('sid')
        #slot=request.args.get('slot')
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")

    #cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    #data= cursor.fetchall()
    
    if request.method=='POST':
        carno=request.form['carno']
        bdate=request.form['bdate']
        reserve=request.form['reserve']
        sid=request.form['sid']

        t1=request.form['t1']
        t2=request.form['t2']
        t3=request.form['t3']
        t4=request.form['t4']
        btime1=t1+":"+t2
        btime2=t3+":"+t4

        h1=int(t1)
        m1=int(t2)
        h2=int(t3)
        m2=int(t4)

        if h1<=h2:

            cursor.execute("SELECT count(*) FROM ev_booking where station=%s and status=1 and rdate=%s",(sid,rdate ))
            dn= cursor.fetchone()[0]
            if dn>0:
                x=0
                cursor.execute("SELECT * FROM ev_booking where station=%s and status=1 and rdate=%s",(sid,rdate ))
                rw= cursor.fetchall()
                for rf1 in rw:
                    rf2=rf1[24].split(":")
                    rf3=rf1[25].split(":")
                    fh1=int(rf2[0])
                    fm1=int(rf2[1])
                    fh2=int(rf3[0])
                    fm2=int(rf3[1])

                    #if h1>=fh1 and h1<=fh2:
                        
                        

                    if h1>=fh1 and h2<=fh2:
                        if m1>=fm1 or m2<=fm2:
                            x+=1
                if x>0 and x<5:
                    a=x+1
                    slot=str(a)
                    av="1"
                    slot=str(x)
                else:
                    slot=str(x)
                    
            else:
                slot="1"
                av="1"

            if av=="1":

                mycursor = mydb.cursor()
                mycursor.execute("SELECT max(id)+1 FROM ev_booking")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                t = time.localtime()
                rtime = time.strftime("%H:%M:%S", t)
                today= date.today()
                rdate= today.strftime("%d-%m-%Y")

                rn=randint(1, 10)
                #if reserve=="1":
                #    cimage="c"+str(rn)+".jpg"
                #else:
                cimage="evch.jpg"
                cursor = mydb.cursor()
                sql = "INSERT INTO ev_booking(id,uname,station,carno,reserve,slot,cimage,rtime,rdate,status,btime1,btime2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                
                val = (maxid,uname,sid,carno,reserve,slot,cimage,rtime,bdate,'1',btime1,btime2)
                cursor.execute(sql, val)
                mydb.commit()            
                print(cursor.rowcount, "Booked Success")
                msg="ok"
            else:
                msg="no"

        else:
            msg="fail"
        

    
    
    return render_template('book1.html',msg=msg,uname=uname,sid=sid,slot=slot)'''


@app.route('/book', methods=['GET', 'POST'])
def book():
    msg=""
    act=""
    cimage=""
    if 'username' in session:
        uname = session['username']
    sid=request.args.get('sid')
    slot=request.args.get('slot')

    now = datetime.datetime.now()
    rdate=now.strftime("%Y-%m-%d")
    cdate=now.strftime("%d-%m-%Y")
    cd1=cdate.split("-")
  
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]
    ##
    t = time.localtime()
    rtime = time.strftime("%H", t)
    chour=int(rtime)
    i=0
    tarr=[]
    while i<=23:
        tarr.append(str(i))
        i+=1
    ###
    cursor.execute("SELECT * FROM ev_booking where station=%s && status=1 && slot=%s && rdate=%s",(sid,slot,cdate))
    dd1= cursor.fetchall()
    

    arr_time=[]
    for ds1 in dd1:
        tt=ds1[24]
        t1=tt.split(":")

        arr_time.append(t1)

    ##
    '''timefrom=[]
    j=chour
    while j<=23:
        tr1=str(j)
        a=0
        for tr in arr_time:
            if tr1==tr:
                a+=1
            else:
                b=1
        if a==0:
            timefrom.append(tr1)
        j+=1'''
    ##
   

    #cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    #data= cursor.fetchall()
    
    if request.method=='POST':
        carno=request.form['carno']
        reserve=request.form['reserve']
        sid=request.form['sid']
        slot=request.form['slot']
        bdate=request.form['bdate']

        t1=request.form['t1']
        t2=request.form['t2']
        t3=request.form['t3']
        t4=request.form['t4']

        sh=int(t1)

        
        btime1=t1+":"+t2
        btime2=t3+":"+t4

        bd1=bdate.split("-")
        bdate1=bd1[2]+"-"+bd1[1]+"-"+bd1[0]

        ##
        d0 = date(int(cd1[2]), int(cd1[1]), int(cd1[0]))
        d1 = date(int(bd1[0]), int(bd1[1]), int(bd1[2]))        
        delta = d1 - d0
        dy=delta.days
        #print(dy)
        ##

        y=0
        if cdate==bdate1:
            if sh<chour:
                y+=1
        x=0
        cursor.execute("SELECT * FROM ev_booking where station=%s and rdate=%s and status=1",(sid,bdate1 ))
        ts1 = cursor.fetchall()
        for ts2 in ts1:
            th2=ts2[24].split(":")
            if th2[0]==t1:
                x+=1
            
        
        if x<2 and y==0 and dy>=0:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT max(id)+1 FROM ev_booking")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            t = time.localtime()
            rtime = time.strftime("%H:%M:%S", t)
            #today= date.today()
            #rdate= today.strftime("%d-%m-%Y")

            rn=randint(1, 10)
            #if reserve=="1":
            #    cimage="c"+str(rn)+".jpg"
            #else:
            cimage="evch.jpg"
            sql = "INSERT INTO ev_booking(id,uname,station,carno,reserve,slot,cimage,rtime,rdate,status,btime1,btime2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            val = (maxid,uname,sid,carno,reserve,slot,cimage,rtime,bdate1,'1',btime1,btime2)
            cursor.execute(sql, val)
            mydb.commit()            
            print(cursor.rowcount, "Booked Success")
            return redirect(url_for('slot',sid=sid))
        else:
            msg="fail"
        

    
    
    return render_template('book.html',msg=msg,uname=uname,sid=sid,slot=slot,rdate=rdate,tarr=tarr)

##Reinforcement
def DeepQLearning(num_of_slot):
    
    enviroment = "ChargingStation"
    action_space="1"
    action=0
    alpha=1
    reward=0
    
    for customer in range(0, num_of_slot):
        # Reset the enviroment
        state = enviroment

        # Initialize variables
        reward = 0
        terminated = False
        j=1
        n=num_of_cards
        while j<n:
            # Take learned path or explore new actions based on the epsilon
            if random.uniform(0, 1) < num_of_slot:
                i=0
                k=0
                while i<=num_of_slot:
                    i+=3
                    k+=1
                action = i
            else:
                action = np.argmax(q_table[state])

            # Take action
            gamma=1
            #next_state, reward, terminated, info = action
            q_table=num_of_slot/3
            # Recalculate
            q_value = k
            max_value = q_table #np.max(q_table[next_state])
            new_q_value = (1 - alpha) * int(q_value) + alpha * (reward + gamma * max_value)
            
            # Update Q-table
            #q_table[state, action] = new_q_value
            state = new_q_value
            j+=1
            
        #if (queue + 1) % 100 == 0:
        #    clear_output(wait=True)
            #print("Queue: {}".format(queue + 1))
            #enviroment.render()

def QueuePredict(enviroment, optimizer):
        
        # Initialize atributes
        _state_size = enviroment
        _action_size = "1" #enviroment.action_space.n
        _optimizer = optimizer
        
        expirience_replay = int(enviroment/2)
        
        # Initialize discount and exploration rate
        gamma = 0.6
        epsilon = 0.1
        
        # Build networks
        q_network = optimizer
        target_network = expirience_replay
        

def store(state, action, reward, next_state, terminated):
    expirience_replay.append((state, action, reward, next_state, terminated))

def _build_compile_model():
    model = Sequential()
    model.add(Embedding(_state_size, 10, input_length=1))
    model.add(Reshape((10,)))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(_action_size, activation='linear'))
    
    model.compile(loss='mse', optimizer=self._optimizer)
    return model

def alighn_target_model():
    target_network.set_weights(q_network.get_weights())

def act(state):
    if np.random.rand() <= epsilon:
        return enviroment.action_space.sample()
    
    q_values = q_network.predict(state)
    return np.argmax(q_values[0])

def retrain(batch_size):
    minibatch = random.sample(expirience_replay, batch_size)
    
    for state, action, reward, next_state, terminated in minibatch:
        
        target = q_network.predict(state)
        
        if terminated:
            target[0][action] = reward
        else:
            t = target_network.predict(next_state)
            target[0][action] = reward + gamma * np.amax(t)
        
        q_network.fit(state, target, epochs=1, verbose=0)
        
def findTime(T, K):
       
    # convert the given time in minutes
    minutes = (((ord(T[0]) - ord('0'))* 10 +
                 ord(T[1]) - ord('0'))* 60 +
               ((ord(T[3]) - ord('0')) * 10 +
                 ord(T[4]) - ord('0')));
                   
    # Add K to current minutes
    minutes += K
   
    # Obtain the new hour
    # and new minutes from minutes
    hour = (int(minutes / 60)) % 24
   
    min = minutes % 60
    hh=""
    mm=""
    # Print the hour in appropriate format
    if (hour < 10):
        hh="0"+str(hour)
        #print(0,hour,":",end = "")
           
    else:
        hh=""+str(hour)
        #print(hour,":",end = "")
   
    # Print the minute in appropriate format
    if (min < 10):
        mm="0"+str(min)
        #print(0,min,end = "")
   
    else:
        mm=""+str(min)
        #print(min,end = "")
    hm=hh+":"+mm
    return hm

@app.route('/tariff', methods=['GET', 'POST'])
def tariff():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('tariff.html',msg=msg, data=data, uname=uname)

@app.route('/history', methods=['GET', 'POST'])
def history():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking b,ev_station s where b.station=s.id and b.uname=%s",(uname, ))
    data= cursor.fetchall()
    
    
    return render_template('history.html',msg=msg, data=data, uname=uname)

@app.route('/home', methods=['GET', 'POST'])
def home():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    data= cursor.fetchone()
    return render_template('home.html',msg=msg, data=data, uname=uname)

@app.route('/view', methods=['GET', 'POST'])
def view():
    msg=""
    if 'username' in session:
        uname = session['username']

    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    data= cursor.fetchone()
    sid=data[0]
    
    cursor.execute("SELECT * FROM ev_station where id=%s",(sid, ))
    dd= cursor.fetchone()
    station=dd[1]
    num=dd[3]
    sdata=[]
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    i=1
    while i<=num:
        dt=[]
        dd=[]
        cursor.execute("SELECT count(*) FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(i,sid,rdate))
        cn= cursor.fetchone()[0]
        if cn>0:
            cursor.execute("SELECT * FROM ev_booking where slot=%s && station=%s && status=1 && rdate=%s",(i,sid,rdate))
            dd= cursor.fetchone()
            dt.append("yes")
        else:
            dt.append("no")

        dt.append(str(i))
        dt.append(dd)
        sdata.append(dt)
        i+=1

        
    
    
    msg=""
    act=""
    rid=""
    s1=0
    s2=0
    s3=0
    s4=0
    s5=0
    s6=0
    s7=0
    s8=0
    s9=0
    s10=0
    if 'username' in session:
        uname = session['username']
    #if request.method=='GET':
    act=request.args.get('act')
    if act=="pay":
        rid=request.args.get('rid')
        
        cursor.execute("update ev_booking set pay_st=2,status=3 where id=%s",(rid, ))
        mydb.commit()
        return redirect(url_for('view'))
    if act=="start":
        rid=request.args.get('rid')
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=2 where id=%s",(rid, ))
        mydb.commit()
        return redirect(url_for('view'))
        
        
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    station=dd[1]
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where station=%s and status=1",(sid, ))
    data= cursor.fetchall()

    for nn in data:
        if nn[5]==1:
            s1=1
        if nn[5]==2:
            s2=2
        if nn[5]==3:
            s3=3
        if nn[5]==4:
            s4=4
        if nn[5]==5:
            s5=5
        if nn[5]==6:
            s6=6
        if nn[5]==7:
            s7=7
        if nn[5]==8:
            s8=8
        if nn[5]==9:
            s9=9
        if nn[5]==10:
            s10=10
        
        
    
    act="ok"
    return render_template('view.html',msg=msg,uname=uname,sid=sid,station=station,act=act,data=data,sdata=sdata,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9,s10=s10)

@app.route('/charge1', methods=['GET', 'POST'])
def charge1():
    msg=""
    amt=0
    cost=0
    if 'username' in session:
        uname = session['username']

    rid=request.args.get('rid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    cmin=dd[17]
    csec=dd[18]
    plan=dd[8]
    
    if plan==1:
        cost=100
    elif plan==2:
        cost=200
    else:
        cost=300
        
    
    if csec<60:
        csec+=1
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
        

    else:
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=3,charge_time=30,charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
    if dd[19]==3:
        amt=cost
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=4,charge=%s where id=%s",(amt,rid))
        mydb.commit()
    
    return render_template('charge1.html',rid=rid, cmin=cmin, csec=csec)

@app.route('/charge2', methods=['GET', 'POST'])
def charge2():
    msg=""
    if 'username' in session:
        uname = session['username']
    amt=0
    cost=0
    rid=request.args.get('rid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    cmin=dd[17]
    
    csec=dd[18]
    print("sc="+str(csec))
    plan=dd[8]
    
    if plan==1:
        cost=100
    elif plan==2:
        cost=200
    else:
        cost=300
    
    if csec<60:
        csec+=1
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
        

    else:
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=3,charge_time=30,charge_min=%s,charge_sec=%s where id=%s",(cmin,csec,rid))
        mydb.commit()
    if dd[19]==3:
        amt=cost
        #+dd[15]
        cursor = mydb.cursor()
        cursor.execute("update ev_booking set charge_st=4,charge=%s where id=%s",(amt,rid))
        mydb.commit() 
    
    return render_template('charge2.html',rid=rid, cmin=cmin, csec=csec)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' in session:
        uname = session['username']
    amount=0
    rid=request.args.get('rid')
    sid=request.args.get('sid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    uu= cursor.fetchone()
    card=uu[6]
    mobile=uu[3]
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    amt=dd[15]
    ch=dd[15]

    t = time.localtime()
    rtime = time.strftime("%H:%M:%S", t)
    today= date.today()
    rdate= today.strftime("%d-%m-%Y")

    if ch>0:
        amount=ch
    else:
        amount=20

    cursor = mydb.cursor()
    cursor.execute("update ev_booking set edate=%s,etime=%s,amount=%s where id=%s",(rdate,rtime,amount,rid))
    mydb.commit()

    if request.method=='POST':
        pay_mode=request.form['pay_mode']
        if pay_mode=="Bank":
            rn=randint(1000, 9999)
            otp=str(rn)
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_mode=%s,sms_st=1,otp=%s where id=%s",(pay_mode,otp,rid))
            mydb.commit()
            
            return redirect(url_for('verify_otp',rid=rid))
        else:
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_mode=%s,pay_st=1 where id=%s",(pay_mode,rid))
            mydb.commit()
            return redirect(url_for('slot',sid=sid))
            
        
    return render_template('payment.html',sid=sid,rid=rid, uname=uname,amount=amount,card=card)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    msg=""
    if 'username' in session:
        uname = session['username']
    amount=0
    rid=request.args.get('rid')
    sid=request.args.get('sid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_register where uname=%s",(uname, ))
    uu= cursor.fetchone()
    mobile=uu[3]
    cursor.execute("SELECT * FROM ev_booking where id=%s",(rid, ))
    dd= cursor.fetchone()
    key=dd[14]
    amount=dd[15]
    sms_st=dd[22]
    if sms_st==1:
        kk="Key: "+key
        #url="http://iotcloud.co.in/testsms/sms.php?sms=otp&name=User&otp="+key+"&mobile="+str(mobile)
        url="http://iotcloud.co.in/testsms/sms.php?sms=emr&name=User&mess="+kk+"&mobile="+str(mobile)
        webbrowser.open_new(url)
        cursor.execute("update ev_booking set sms_st=0 where id=%s",(rid,))
        mydb.commit()
            
        #params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'RandDC', 'message':message, 'number':mobile})
        #url = "http://pay4sms.in/sendsms/?%s" % params
        #with urllib.request.urlopen(url) as f:
        #    print(f.read().decode('utf-8'))
        #    print("sent"+str(mobile))
                
    if request.method=='POST':
        otp=request.form['otp']
        if key==otp:
            
            cursor = mydb.cursor()
            cursor.execute("update ev_booking set pay_st=2,status=3 where id=%s",(rid,))
            mydb.commit()
            #cursor.execute("update ev_register set amount=amount-%s where uname=%s",(amount,uname))
            #mydb.commit()
            #return redirect(url_for('slot',sid=sid))
            msg="Amount Paid Successfully"
        
    return render_template('verify_otp.html',rid=rid,sid=sid,msg=msg)

@app.route('/report', methods=['GET', 'POST'])
def report():
    msg=""
    if 'username' in session:
        uname = session['username']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM ev_station where uname=%s",(uname, ))
    dd= cursor.fetchone()
    sid=dd[0]
    cursor.execute("SELECT * FROM ev_booking where station=%s",(sid, ))
    data= cursor.fetchall()
    return render_template('report.html',msg=msg, data=data, uname=uname)



@app.route('/map', methods=['GET', 'POST'])
def map():
    msg=""
    if 'username' in session:
        uname = session['username']
    if request.method=='GET':
        lat=request.args.get('lat')
        lon=request.args.get('lon')
    return render_template('map.html',msg=msg, lat=lat, lon=lon)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
