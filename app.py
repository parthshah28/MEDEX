
#!/usr/bin/env python3
import argparse
#import uuid
import json
#import conversation
# import apiaccess
# import request
import pyglet
import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import threading
import os
#from subprocess import Popen, CREATE_NEW_CONSOLE,PIPE
import sqlite3
import bot



conn = sqlite3.connect('user.db')
c = conn.cursor()

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)
outflag=False
inflag=False
out_buff=""
in_buff=""
global msghistory
msghistory=[]
mplayer=None
stopflag=False
first=True
global terminate_flag
terminate_flag=False


global msg_count
msg_count=0

@app.route('/',methods=['GET', 'POST'])
def sessions():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    global stopflag
    global first
    global msghistory
    global msg_count
    res= request.args.get('res')
    uid= request.args.get('uid')
    if stopflag:
        if first:
            print("not setting history")
            print(bot.result)
            for i in str(bot.result).split('/'):
                i=i.replace("[","")
                i=i.replace("]","")
                i=i.replace("\"","")
                i=i.replace("'","")
                msghistory.append(i)
            temp=json. dumps(msghistory)
            first= False
            return temp
        else:
            print("setting history")
            # dataq=(uid,str(msghistory[-4:]))
            dataq=(uid,str(bot.result))
            print(dataq)
            c.execute("INSERT INTO Histroy VALUES (?,?)",dataq)
            conn.commit()
            conn.close()
            bot.result=[]
            return "stop"
    # print(":-"+res)

    if res == None:
        print(msghistory)
        print(bot.msg,msg_count)
        if len(bot.msg) > msg_count:
            for i in range(msg_count,len(bot.msg)):
                msghistory.append(bot.msg[i])
                msg_count+=1
        # msghistory.append(bot.msg)
        start()
        temp=json. dumps(msghistory)
        return temp
        # return str(msghistory)
    else:# return render_template('session.html')
        global inflag
        global in_buff
        res=str(res)
        # print(res)
        # res.replace('"'," ")
        print(res[1:-1])
        msghistory.append("user:-"+res[1:-1])
        # if res == ".":
        #     in_buff=" "
        # # while inflag:
        # #     continue
        # else:
        # in_buff=res[1:-1]
        # inflag=True

        bot.in_buff=res[1:-1]
        bot.inflag=True
        temp=json. dumps(msghistory)
        return temp
        # return str(msghistory)
@app.route('/start',methods=['GET', 'POST'])
def reset():
    global mplayer
    global msghistory
    global chatbot
    global msg_count
    msg_count=0
    if mplayer!=None:
        chatbot.terminate()
    mplayer=None
    msghistory=[]
    bot.msg=[]
    bot.result=[]
    global terminate_flag
    terminate_flag=False
    start()
    temp=json. dumps(msghistory)
    return temp
    # return str(msghistory)
@app.route('/check',methods=['GET', 'POST'])
def check1():
    return "pass"



@app.route('/stop',methods=['GET', 'POST'])
def stop():
    global mplayer
    global msghistory
    global chatbot
    global stopflag
    global first
    global terminate_flag
    stopflag=False
    first=True
    if mplayer!=None:
        # chatbot.terminate()
        terminate_flag=True
    mplayer=None
    msghistory=[]
    bot.msg=[]
    # result=[]
    msg_count=0
    temp=json. dumps(msghistory)
    return temp
    # return str(msghistory)
@app.route('/get',methods=['GET', 'POST'])
def getData():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    uid= request.args.get('name')
    data={}
    # for row in c.execute('SELECT * FROM Users WHERE uid = '+uid):
    #     print(row,row[0],uid)
    #     if row[0] in uid:
    #         data=row
    #         break
    for row in c.execute('SELECT * FROM Users'):
        print(row)
        if row[0] == uid:
            data=row
            break
    temp=json.dumps(data)

    conn.close()

    return temp
@app.route('/set',methods=['GET', 'POST'])
def setData():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    print("set called")
    # name= request.args.get('name')
    # age= request.args.get('age')
    # sex= request.args.get('sex')
    # weight= request.args.get('weight')
    # height= request.args.get('height')
    # allergies= request.args.get('allergies')

    data= request.args.get('json')
    # data=json.load(data)
    # data = request.__getattribute__
    data=json.loads(data)
    print(data)
    # dataq=( data['uid'],data['name'],data['age'],
    #         data['sex'],data['weight'],data['height'],
    #         data['allergies'])
    # print(dataq)
    row=None
    row=c.execute("UPDATE Users"+
               " SET name = '"+data["name"]+
                "',age = "+data["age"]+
                ",sex = '"+data["sex"]+
                "',weight = "+data["weight"]+
                ",height = "+data["height"]+
                ",allergies = '"+data["allergies"]+
                "' where uid = '"+data['uid']+"'")
    print(row)
    # data={"uname",name,age,sex,weight,height,allergies}
    # c.execute("INSERT INTO Users VALUES (?,?,?,?,?,?,?)",dataq)
    conn.commit()
    for row in c.execute('SELECT * FROM Users'):
        if row[0] in data["name"]:
            data=row[1]
            break
    temp=json.dumps(data)
    conn.close()
    return temp

@app.route('/gethistory',methods=['GET', 'POST'])
def gethistory():
    # name= request.args.get('name')
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    data=[]
    uid= request.args.get('uid')

    for row in c.execute('SELECT * FROM Histroy  where uid = \''+uid+"'"):
        print(row,row[0])
        data.append(row[1])
        # break
    temp=json.dumps(data)
    conn.close()

    return temp

@app.route('/sethistory',methods=['GET', 'POST'])
def sethistory():
    print("set called")
    # name= request.args.get('name')
    # age= request.args.get('age')
    # sex= request.args.get('sex')
    # weight= request.args.get('weight')
    # height= request.args.get('height')
    # allergies= request.args.get('allergies')
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    data= request.args.get('json')
    uid= request.args.get('uid')

    # data=json.load(data)
    # data = request.__getattribute__
    data=json.loads(data)
    print(data)
    c.execute("DELETE FROM Histroy  where uid = '"+uid+"'")
    for row in data:
        print(row)
        dataq=(uid,str(row))
        c.execute("INSERT INTO Histroy VALUES (?,?)",dataq)
    conn.commit()
    conn.close()

    return gethistory()


@app.route('/login',methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    print("login called")
    uid= request.args.get('uname')
    password= request.args.get('pass')
    print(uid,password)
    row=None
    for row in c.execute('SELECT * FROM Users'):
        print(row)
        if row[0] == uid:
            if row[1] == password:
                return "pass"
            else:
                return "fail"

    conn.close()

    # print(row)
        # data.append(row[1])
    # conn.commit()
    # return gethistory()
    return "fail"


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    print("signup called")
    uid= request.args.get('uname')
    password= request.args.get('pass')
    print(uid,password)

    if uid=="":
        print("failed")
        return "fail"
    # check for uid
    row=None
    for row in c.execute('SELECT * FROM Users'):
        # print(row)
        if row[0] == uid:
            print("failed")
            return "fail"
    # ---------------

    # row=None
    dataq=(uid,password,uid,"","","","","")
    c.execute("INSERT INTO Users VALUES (?,?,?,?,?,?,?,?)",dataq)
    conn.commit()
    # for row in c.execute('SELECT * FROM Users WHERE uid = '+uid):
    #     print(row)
        # data.append(row[1])
    # conn.commit()
    # return gethistory()
    conn.close()

    return "pass"


# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)
#     print("\n\nmsg=",json['message'])
#     print("msg received")
def check(arg):
    global out_buff
    global outflag
    # socketio.emit( 'msg')
    # print("checking")
    if outflag:
        print("emited"+out_buff)
        # socketio.emit( 'my response', {
        #     "user_name" :"server",
        #     'message' : out_buff
        #      } )
        msghistory.append(out_buff)
        out_buff=""
        outflag=False
# @socketio.on("start run")
def start():
    global mplayer
    global msg_count

    if mplayer == None:
        msg_count=0
        mplayer=threading.Thread(target=runner,args=())
        mplayer.daemon=True
        mplayer.start()
        # pyglet.clock.schedule_interval(check, 2)
        # pyglet.app.run()



def runner( ):
    global chatbot
    global out_buff
    global in_buff
    global inflag
    global outflag
    global msghistory
    global stopflag
    inpneed=False
    # program = "python bot.py"
    # print("calling subprocess")
    # # inp=input()
    # # print(inp)
    # chatbot=Popen(program,
    #                     stdin=PIPE,
    #                     stderr=PIPE,
    #                     stdout=PIPE,
    #                     creationflags=CREATE_NEW_CONSOLE)
    # # write(chatbot, "30 m")
    # # print("1")
    # # print(read(chatbot))
    # # print("1")
    # # print(read(chatbot))
    # # print("1")
    # # print(read(chatbot))
    # # print("1")
    # # print(read(chatbot))
    # print("waiting")

    # line=""
    # rc=1
    # while rc != 0:
    #     # print(rc)
    #     while True:
    #         # print(".")
    #         if inpneed:
    #             break
    #         line = read(chatbot)
    #         if not line:
    #             break
    #         print (line)
    #         if "inp!:-" not in line:
    #             msghistory.append(line)
    #             # line=None
    #         if "inp!:-" in line:
    #             inpneed=True
    #     if inpneed:
    #         # inp=input(":-")
    #         # write(chatbot, inp)
    #         # print(".",end="")
    #         if inflag:
    #             write(chatbot, in_buff)
    #             inflag=False
    #             print("Done")
    #             inpneed=False
    #             # time.sleep(1)

    #     rc = chatbot.poll()
    # print("done waiting")

    bot.chat()
    stopflag=True
def read(process):
    try:
        return process.stdout.readline().decode("utf-8").strip()
    except:
        return ""

def write(process, message):
    print("msg:-"+message+"/")
    process.stdin.write(f"{message} \n".encode("utf-8"))
    process.stdin.flush()


def terminate(process):
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


# def response(prompt):
    # print("emited:-"+prompt)
    # socketio.emit('my response', { 'message' :prompt})
chatbot=None
if __name__ == '__main__':
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users ( uid text,
                                                    pass text,
                                                    name text,
                                                    age int,
                                                    sex text,
                                                    weight int,
                                                    height int,
                                                    allergies text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS Histroy (uid text,
                                                    history text)''')
    conn.commit()
    app.run(host= '0.0.0.0',port=5000,debug=False)
    conn.close()
    # app.run(host= '0.0.0.0',port=3000,debug=False)
    # socketio.run(app,debug=False)
