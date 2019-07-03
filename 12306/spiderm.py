# -*- coding: utf-8 -*-

import urllib.request
import http.cookiejar
import re
import ssl
import urllib.parse
import datetime
import time
import json

# 防止ssl出现问题
ssl._create_default_https_context = ssl._create_unverified_context

# 查询余票信息
date = input('请输入出发日期（格式为2018-11-01）：')
from_station = input('请输入出发车站：')
to_station = input('请输入目的地车站：')
purpose = input('是否为学生（1为学生，0 为否）：')

f = open('/media/wangxl/a84d5450-ee22-469c-a813-c774821af033/wangxl/爬虫笔记/12306/city_3.json', 'r')
data = f.read()
f.close()
city_name = json.loads(data)

fs = city_name[from_station]
ts = city_name[to_station]
p = '0X00' if purpose == '1' else 'ADULT'

# 访问接口获取余票信息
url = 'https://kyfw.12306.cn/otn/leftTicketDTO/query?leftTicketDTO.train_date=' + \
    str(date) + '&leftTicketDTO.from_station=' + str(fs) + \
    '&leftTicketDTO.to_station=' + str(ts) + '&purpose_codes=' + str(p)
print('url:', url)
opener = urllib.request.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')]
urllib.request.install_opener(opener)
piao = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
print(piao)
# 格式化输出余票信息
try:
    result = json.loads(piao)
except Exception as e:
    print('无法查询!')
    raise e
allcheci = result['data']['result']
mapp = result['data']['map']

print('车次\t能否预定\t出发站名\t到达站名\t出发时间\t到达时间\t历时\t一等座\t二等座\t硬卧\t硬座\t无座\t')
# 能否预定 0为空则不能预定， 有值则能预定
# 车次 3
# 出发车站 6
# 到达车站 7
# 发车时间 8
# 到达时间 9
# 历时 10
# 无座 26
# 硬座 29
# 硬卧 28
# 软卧 23
# 商务座 32
# 一等座 31
# 二等座 30
for i in allcheci:
    try:
        a = i.split('|')
        cc = a[3]
        yd = '1' if a[0] != '' else '0'
        ss = mapp[a[6]]
        ast = mapp[a[7]]
        fc = a[8]
        dd = a[9]
        ls = a[10]
        yi = a[31]
        er = a[30]
        yw = a[28]
        yz = a[29]
        wz = a[26]
        print(cc + '\t' + yd + '\t' + ss + '\t' + ast + '\t' + fc + '\t' + dd +
              '\t' + ls + '\t' + yi + '\t' + er + '\t' + yw + '\t' + yz + '\t' + wz)
    except Exception as e:
        continue
status = input('查票完成，请按1确定继续')
if (status == 1 or status == '1'):
    pass
else:
    raise Exception('------程序结束------')


# 处理cookie ，注册为全局
print('正在处理cookie……')
cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
urllib.request.install_opener(opener)

# 验证码处理
yzmurl = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
while True:
    urllib.request.urlretrieve(yzmurl, '/home/wangxl/Desktop/yzm.png')
    yzm = input('请输入验证码，输入图片序号即可：')
    if (yzm != 're'):
        break
print('.......正在登录......')
# 格式化要提交的验证码数据
pat1 = '"(.*?)"'
allpic = re.compile(pat1, re.S).findall(yzm)


def getxy(pic):
    if(pic == 1):
        xy = (33, 43)
    if(pic == 2):
        xy = (109, 52)
    if(pic == 3):
        xy = (192, 46)
    if(pic == 4):
        xy = (277, 30)
    if(pic == 5):
        xy = (53, 112)
    if(pic == 6):
        xy = (121, 126)
    if(pic == 7):
        xy = (176, 108)
    if(pic == 8):
        xy = (285, 108)
    return xy


allpicpos = ""
for i in allpic:
    thisxy = getxy(int(i))
    for j in thisxy:
        allpicpos = allpicpos + str(j) + ','
allpicpos2 = re.compile("(.*?).$").findall(allpicpos)[0]

# 验证码验证
answerdata = urllib.request.quote(allpicpos2)
# yzmgeturl = 'https://kyfw.12306.cn/passport/captcha/captcha-check?callback=jQuery191046729284054219655_1542355477328&answer='+ str(answerdata) +'&rand=sjrand&login_site=E&_=1542355477333'
yzmgeturl = 'https://kyfw.12306.cn/passport/captcha/captcha-check?answer=' + \
    str(answerdata) + '&rand=sjrand&login_site=E'
req1 = urllib.request.Request(yzmgeturl)
req1.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req1data = urllib.request.urlopen(req1).read().decode('utf-8', 'ignore')

# 账号密码验证
login_url = 'https://kyfw.12306.cn/passport/web/login'
login_post_data = urllib.parse.urlencode({
    "answer": allpicpos2,
    "username": "18234169002",
    "appid": "otn",
    "password": "Feng970707"
}).encode('utf-8')
req2 = urllib.request.Request(login_url, login_post_data)
req2.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req2data = urllib.request.urlopen(req2).read().decode('utf-8', 'ignore')
print(req2data)

# 其他验证
login_url2 = 'https://kyfw.12306.cn/otn/login/userLogin'
req3 = urllib.request.Request(login_url2)
req3.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req3data = urllib.request.urlopen(req3).read().decode('utf-8', 'ignore')

# 获取tk值
login_url3 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
login_post_data2 = urllib.parse.urlencode({
    "appid": "otn"
}).encode('utf-8')
req4 = urllib.request.Request(login_url3, login_post_data2)
req4.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req4data = urllib.request.urlopen(req4).read().decode('utf-8', 'ignore')
pat2 = '"newapptk":"(.*?)"'
tk = re.compile(pat2, re.S).findall(req4data)[0]

# 提交tk值
login_url4 = 'https://kyfw.12306.cn/otn/uamauthclient'
login_post_data3 = urllib.parse.urlencode({
    "tk": tk
}).encode('utf-8')
req5 = urllib.request.Request(login_url4, login_post_data3)
req5.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req5data = urllib.request.urlopen(req5).read().decode('utf-8', 'ignore')
print(req5data)

login_url5 = 'https://kyfw.12306.cn/otn/login/userLogin'
req6 = urllib.request.Request(login_url5)
req6.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req6data = urllib.request.urlopen(req6).read().decode('utf-8', 'ignore')

login_url6 = 'https://kyfw.12306.cn/otn/login/conf'
login_post_data4 = urllib.parse.urlencode('').encode('utf-8')
req7 = urllib.request.Request(login_url6, login_post_data4)
req7.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req7data = urllib.request.urlopen(req7).read().decode('utf-8', 'ignore')

login_url7 = 'https://kyfw.12306.cn/otn/index/initMy12306Api'
login_post_data5 = urllib.parse.urlencode('').encode('utf-8')
req8 = urllib.request.Request(login_url7, login_post_data5)
req8.add_header(
    'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
req8data = urllib.request.urlopen(req8).read().decode('utf-8', 'ignore')
print(req8data)
print('........登录成功.........')

isdo=input("如果需要订票，请输入1继续，否则请输入其他数据")
# thiscode=input("请输入要预定的车次：")
bookticket = input('请输入要乘坐的车次：如（Z22）')
chooseno="None"
while True:
    try:
        print('----进入循环----')
        # 初始化订票页面
        initurl="https://kyfw.12306.cn/otn/leftTicket/init"
        reqinit=urllib.request.Request(initurl)
        reqinit.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        initdata=urllib.request.urlopen(reqinit).read().decode("utf-8","ignore")
        # 提交预定申请
        # 访问接口获取余票信息
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + \
            str(date) + '&leftTicketDTO.from_station=' + str(fs) + \
            '&leftTicketDTO.to_station=' + str(ts) + '&purpose_codes=' + str(p)
        getpiao = urllib.request.Request(url)
        getpiao.add_header('User', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        piao = urllib.request.urlopen(getpiao).read().decode('utf-8', 'ignore')

        # 格式化输出余票信息
        try:
            result = json.loads(piao)
        except Exception as e:
            print('无法查询!')
            raise e
        allcheci = result['data']['result']
        mapp = result['data']['map']
        # bookticket = input('请输入要乘坐的车次：如（Z22）')
        back_train_date = datetime.datetime.now()
        back_train_date = back_train_date.strftime('%Y-%m-%d')
        back_train_date
        bookpostdata = {}
        for i in allcheci:
            a = i.split('|')
            bookpostdata[a[3]] = {}
            bookpostdata[a[3]]['secretStr'] = a[0]
            bookpostdata[a[3]]['train_date'] = date
            bookpostdata[a[3]]['back_train_date'] = back_train_date
            bookpostdata[a[3]]['tour_flag'] = 'dc'
            bookpostdata[a[3]]['purpose_codes'] = p
            bookpostdata[a[3]]['query_from_station_name'] = mapp[a[6]]
            bookpostdata[a[3]]['query_to_station_name'] = mapp[a[7]]
            bookpostdata[a[3]]['undefined'] = ''

        # 其他验证访问
        # checkurl="https://kyfw.12306.cn/otn/login/checkUser"
        # checkdata =urllib.parse.urlencode({
        # "_json_att":""
        # }).encode('utf-8')
        # req5 = urllib.request.Request(checkurl,checkdata)
        # req5.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
        # req5data=urllib.request.urlopen(req5).read().decode("utf-8","ignore")
        checkurl = 'https://kyfw.12306.cn/otn/login/checkUser'
        checkpost = urllib.parse.urlencode({
            "_json_att": ""
        }).encode('utf-8')
        req9 = urllib.request.Request(checkurl, checkpost)
        req9.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req9data = urllib.request.urlopen(req9).read().decode('utf-8', 'ignore')

        bookurl = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        # submitur"https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        # secretStr   ePn88XJWtSf4SC6Gm8bqqVtfE9mQITTsZQazAilKc34r71sJa4e1fJ3JHfNgGdBEBrAIsudmvuJk
        # MzwtdU4zTOsqMno7HbUU7f12yLjvGq+mHpLrPjGNt4zwz4vc5/g4MPBO39DC0yVO8K7kz4MUP9jg
        # sj8iclPwmmiVlxXchqVogjxUrwQnQEBT1axJlJqgtfhcT+Cy0l1OmBsnUY1Ny4k4DhfqzNHJ3uGa
        # CLHhjewp0HWzU4XsBbf2Jmu8KorwHK+FVg24=
        # train_date  2018-12-06
        # back_train_date 2018-11-17
        # tour_flag   dc
        # purpose_codes   ADULT
        # query_from_station_name 太原
        # query_to_station_name   北京
        # undefined
        submitdata = urllib.parse.urlencode(bookpostdata[bookticket])
        submitdata2 = submitdata.replace('%25', '%')
        submitdata3 = submitdata2.encode('utf-8')

        req10 = urllib.request.Request(bookurl, submitdata3)
        req10.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req10data = urllib.request.urlopen(req10).read().decode('utf-8', 'ignore')

        passengerurl = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        passengerdata = urllib.parse.urlencode({
            "_json_att": ""
        }).encode('utf-8')
        req11 = urllib.request.Request(passengerurl, passengerdata)
        req11.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req11data = urllib.request.urlopen(req11).read().decode('utf-8', 'ignore')

        # 从此处换代码
        # pat3 = "globalRepeatSubmitToken = \\'(.*?)\\'"
        # submittoken = re.compile(pat3, re.S).findall(req11data)[0]
        train_no_pat="'train_no':'(.*?)'"
        leftTicketStr_pat="'leftTicketStr':'(.*?)'"
        fromStationTelecode_pat="from_station_telecode':'(.*?)'"
        toStationTelecode_pat="'to_station_telecode':'(.*?)'"
        train_location_pat="'train_location':'(.*?)'"
        pattoken="var globalRepeatSubmitToken.*?'(.*?)'"
        patkey="'key_check_isChange':'(.*?)'"
        train_no_all=re.compile(train_no_pat).findall(req11data)
        if(len(train_no_all)!=0):
            train_no=train_no_all[0]
        else:
            raise Exception("train_no获取失败")
        leftTicketStr_all=re.compile(leftTicketStr_pat).findall(req11data)
        if(len(leftTicketStr_all)!=0):
            leftTicketStr=leftTicketStr_all[0]
        else:
            raise Exception("leftTicketStr获取失败")
        fromStationTelecode_all=re.compile(fromStationTelecode_pat).findall(req11data)
        if(len(fromStationTelecode_all)!=0):
            fromStationTelecode=fromStationTelecode_all[0]
        else:
            raise Exception("fromStationTelecod获取失败")
        toStationTelecode_all=re.compile(toStationTelecode_pat).findall(req11data)
        if(len(toStationTelecode_all)!=0):
            toStationTelecode=toStationTelecode_all[0]
        else:
            raise Exception("toStationTelecode获取失败")
        train_location_all=re.compile(train_location_pat).findall(req11data)
        if(len(train_location_all)!=0):
            train_location=train_location_all[0]
        else:
            raise Exception("train_location获取失败")
        tokenall=re.compile(pattoken).findall(req11data)
        if(len(tokenall)!=0):
            token=tokenall[0]
        else:
            raise Exception("Token获取失败")
        keyall=re.compile(patkey).findall(req11data)
        if(len(keyall)!=0):
            key=keyall[0]
        else:
            raise Exception("key_check_isChange获取失败")

        getpassurl = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        getpassdata = urllib.parse.urlencode({
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": token
        }).encode('utf-8')
        req12 = urllib.request.Request(getpassurl, getpassdata)
        req12.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req12data = urllib.request.urlopen(req12).read().decode('utf-8', 'ignore')
        namepat='"passenger_name":"(.*?)"'
        #提取身份证
        idpat='"passenger_id_no":"(.*?)"'
        #提取手机号
        mobilepat='"mobile_no":"(.*?)"'
        #提取对应乘客所在的国家
        countrypat='"country_code":"(.*?)"'
        nameall=re.compile(namepat).findall(req12data)
        idall=re.compile(idpat).findall(req12data)
        mobileall=re.compile(mobilepat).findall(req12data)
        countryall=re.compile(countrypat).findall(req12data)
        #选择乘客
        if(chooseno!="None"):
            pass
        else:
            #输出乘客信息，由于可能有多位乘客，所以通过循环输出
            for i in range(0,len(nameall)):
                print("第"+str(i+1)+"位用户,姓名:"+str(nameall[i]))
            chooseno=input("请选择要订票的用户的序号，此处只能选择一位哦，如需选择多位，可以自行修改一下代码")
            #thisno为对应乘客的下标，比序号少1，比如序号为1的乘客在列表中的下标为0
            thisno = int(chooseno) - 1
        if(bookpostdata[bookticket]['secretStr']==""):
            print("当前无票，继续监控…")
            continue

        #总请求1-点击提交后步骤1-确认订单(一等座，座位类型为M，二等座，座位类型为O如需选择多种类型座位，可以自行修改一下代码使用if判断一下即可)
        checkOrderurl="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        checkdata=urllib.parse.urlencode({
        "cancel_flag":2,
        "bed_level_order_num":"000000000000000000000000000000",
        "passengerTicketStr":"O,0,1,"+str(nameall[thisno])+",1,"+str(idall[thisno])+","+str(mobileall[thisno])+",N",
        "oldPassengerStr":str(nameall[thisno])+",1,"+str(idall[thisno])+",1_",
        "tour_flag":"dc",
        "randCode":"",
        "whatsSelect":1,
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token,
        }).encode('utf-8')
        req13 = urllib.request.Request(checkOrderurl,checkdata)
        req13.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req13data=urllib.request.urlopen(req13).read().decode("utf-8","ignore")
        print("确认订单完成，即将进行下一步")

        #总请求2-点击提交后步骤2-获取队列
        getqueurl="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        #checkdata=checkOrderdata.encode('utf-8')
        #将日期转为格林时间
        #先将字符串转为常规时间格式
        thisdatestr=date#需要的买票时间
        thisdate=datetime.datetime.strptime(thisdatestr,"%Y-%m-%d").date()
        #再转为对应的格林时间
        gmt='%a+%b+%d+%Y'
        thisgmtdate=thisdate.strftime(gmt)
        #将leftstr2转成指定格式
        leftstr2=leftTicketStr.replace("%","%25")
        getquedata="train_date="+str(thisgmtdate)+"+00%3A00%3A00+GMT%2B0800&train_no="+train_no+"&stationTrainCode="+bookticket+"&seatType=M&fromStationTelecode="+fromStationTelecode+"&toStationTelecode="+toStationTelecode+"&leftTicket="+leftstr2+"&purpose_codes=00&train_location="+train_location+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
        getdata=getquedata.encode('utf-8')
        req14 = urllib.request.Request(getqueurl,getdata)
        req14.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req14data=urllib.request.urlopen(req14).read().decode("utf-8","ignore")
        print("获取订单队列完成，即将进行下一步")

        #总请求3-确认步骤1-配置确认提交
        confurl="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        confdata2=urllib.parse.urlencode({
        "passengerTicketStr":"O,0,1,"+str(nameall[thisno])+",1,"+str(idall[thisno])+","+str(mobileall[thisno])+",N",
        "oldPassengerStr":str(nameall[thisno])+",1,"+str(idall[thisno])+",1_",
        "randCode":"",
        "purpose_codes":"00",
        "key_check_isChange":key,
        "leftTicketStr":leftTicketStr,
        "train_location":train_location,
        "choose_seats":"",
        "seatDetailType":"000",
        "whatsSelect":"1",
        "roomType":"00",
        "dwAll":"N",
        "_json_att":"",
        "REPEAT_SUBMIT_TOKEN":token,
        }).encode('utf-8')
        req15 = urllib.request.Request(confurl,confdata2)
        req15.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req15data=urllib.request.urlopen(req15).read().decode("utf-8","ignore")
        print("配置确认提交完成，即将进行下一步")

        time1=time.time()
        while True:
            #总请求4-确认步骤2-获取orderid
            time2=time.time()
            if((time2-time1)//60>5):
                print("获取orderid超时，正在进行新一次抢购")
                break
            getorderidurl="https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random="+str(int(time.time()*1000))+"&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
            req16 = urllib.request.Request(getorderidurl)
            req16.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
            req16data=urllib.request.urlopen(req16).read().decode("utf-8","ignore")
            patorderid='"orderId":"(.*?)"'
            orderidall=re.compile(patorderid).findall(req16data)
            if(len(orderidall)==0):
                print("未获取到orderid，正在进行新一次的请求。")
                continue
            else:
                orderid=orderidall[0]
                break
        print("获取orderid完成，即将进行下一步")

        #总请求5-确认步骤3-请求结果
        resulturl="https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue"
        resultdata="orderSequence_no="+orderid+"&_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
        resultdata2=resultdata.encode('utf-8')
        req17 = urllib.request.Request(resulturl,resultdata2)
        req17.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
        req17data=urllib.request.urlopen(req17).read().decode("utf-8","ignore")
        print("请求结果完成，即将进行下一步")
        try:
            #总请求6-确认步骤4-支付接口页面
            payurl="https://kyfw.12306.cn/otn//payOrder/init"
            paydata="_json_att=&REPEAT_SUBMIT_TOKEN="+str(token)
            paydata2=paydata.encode('utf-8')
            req18 = urllib.request.Request(payurl,paydata2)
            req18.add_header(
                'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
            req18data=urllib.request.urlopen(req18).read().decode("utf-8","ignore")
            print("订单已经完成提交，您可以登录后台进行支付了。")
            break
        except Exception as err:
            print(err)
            break
    except Exception as err:
        print(err)
