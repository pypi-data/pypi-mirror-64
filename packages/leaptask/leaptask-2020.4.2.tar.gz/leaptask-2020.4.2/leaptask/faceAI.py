# -*- coding: utf-8 -*-
from base64 import b64encode
from pprint import pprint
import requests
from pyleap import *

ty = Text("",860,550,20,"red",font_name="STHupo")
window.set_size(1000,600)
Open = Sprite("https://rss.leaplearner.com/ud/production//19671/158520767187985.png",880,50,200,70)
bg = Sprite("https://rss.leaplearner.com/ud/production//19671/158521057455946.png",350,300,700,550)
a=0
state = 1
m =1
error = Text("",130,250,30,"red",font_name="STHupo")
photo = ["1.jpg"]
pic = Sprite(photo[a],350,300)

def judge():
    global m,photo,Result,face,Emotion,gender,Mask,state
    if m == 1:
        url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"#接口地址
        headers = {"content-type":"application/json"}#固定参数
        p = open(photo[a],"rb")#用二进制的方式打开图片并保存到变量p中,注意后缀名
        image = str(b64encode(p.read()),"utf-8")#加密图片p并转换成字符格式保存到变量image中
        params = '{"image":"'+image+'","image_type":"BASE64","face_field":"faceshape,facetype,age,beauty,emotion,expression,gender,landmark,mask"}'
        ##验证信息，必要参数，获取方式见access_token项目
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=uEaxmSYYxuZNU0pa84TofGUE&client_secret=OWGZ8ffTySgDLhtbW2ZAUKbKUs1bwt0f'
        response = requests.get(host)
        access_token=response.json()['access_token']
        request_url = url +"?access_token="+access_token  #连接地址和验证信息
        #填写所有信息发送给百度，获取识别结果保存到变量response中
        response = requests.post(request_url,data = params,headers = headers)  
        response=response.json()
        R = response['result']
        if R != None:
            Result =  response['result']['face_list'][0]
            pprint(Result)
        #pprint(R)
        m = -1
        if R != None:
            state = 1
            R2 = response['result']['face_list'][0]
            error.src = ""
            score = int(R2['beauty'])
            face = response['result']['face_list'][0]['face_type']['type']
            if face=="cartoon":
                ty.src = "卡通"
            else:
                ty.src = ""
        else:
            state = 0
            error.src = "检测不到人脸,重新上传"
        
    window.clear()
    Rectangle(0, 0, window.w, window.h, "white").draw()
    pic.src = photo[a]
    pic.draw()
    bg.draw()
    if state == 1:
        c = []
        for j in range(72):
            x = Result['landmark72'][j]['x']
            y = Result['landmark72'][j]['y']
            c.append(Circle(int(x)+350-0.5*pic.w,300+0.5*pic.h-int(y),1,"red"))     
        for j in range(72):
            c[j].draw()
    Open.draw()
    if a == len(photo)-1:
        Text("这是最后一张图片",100,60,20,"red",font_name="STHupo").draw()
    error.draw()

    
def Next():
    global state,m,a
    m = 1
    state = 1
    if a < len(photo)-1:
        a += 1
    pic.src = photo[a]
Open.on_press(Next)

