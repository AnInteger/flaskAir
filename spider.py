import pymysql
import requests

from bs4 import BeautifulSoup

allflight = []
#allflight = ['CES219']

data_header = ['航班号', '日期', '机型', '始发地四字', '目的地四字', '始发时间', '到达时间', '飞行时间']

def get_XML(usr_url):
    #浏览器中的cookie信息
    cookie = '''_ga=GA1.2.996770685.1589163575; __gads=ID=a67a65c55c6ef04a:T=1589163577:S=ALNI_MaPhpf1cjX1WWPEBM5ahIYPvsPPVA; __qca=P0-947320160-1589163581766; _fbp=fb.1.1589163797336.692418153; __zlcmid=y9j7oLHRnxg5kA; d7s_uid=ka1vaj4ddnenp2; w_sid=4ff0af0d191071f1b0b842f38b5fcf690af976a14876e18cac200f3baf0db95e; update_time=1589171980; _gid=GA1.2.629797681.1589638124; __rtgt_sid=kaak4phbqd1pzb'''
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'referer': usr_url
    }
    url = usr_url
    #创建session会话
    seesion = requests.session()
    response = seesion.get(url, headers=header)
    # response.coding="gbk"
    wbdata = response.text
    #file = open("flight.html","w")
    #file.write(wbdata)
    #print("正在打开请求")
    #print(response.url)
    soup = BeautifulSoup(wbdata, 'lxml')
    #print(soup)
    return soup

def flight_format(td):
    temp = []
    temp.append(td[0])
    date = td[1]
    plane = td[2]
    source = td[3]
    destnation = td[4]
    starttime = td[5]
    endtime = td[6]
    realstart = td[7]

    #data
    date_s = date[0:4]+"."+date[6:8]+"."+date[10:12]
    temp.append(date_s)

    #plane
    temp.append(plane)

    #source
    #num = source.find('(')
    #temp.append(source[num+1:num+4])
    #temp.append(source[num+7:num+11])
    end = len(source)
    if(source[end-1]!=')'):
        return 0
    else:
        temp.append(source[end-5:end-1])


    #destination
    #num = destnation.find('(')
    #temp.append(destnation[num+1:num+4])
    #temp.append(destnation[num+7:num+11])
    end = len(destnation)
    if(end == 0 or destnation[-1]!=')'):
        return 0
    else:
        temp.append(destnation[end-5:end-1])

    if (starttime=='' or endtime == ''):
        return 0
    else:
        #starttime
        if starttime[5] == "下":
           temp.append(str(int(starttime[0:2])+12)+':'+starttime[3:5])
        else:
           temp.append(starttime[0:2]+':'+starttime[3:5])
        #endtime
        if endtime[5] == "下":
           temp.append(str(int(endtime[0:2])+12)+':'+endtime[3:5])
        else:
           temp.append(endtime[0:2]+':'+endtime[3:5])

    #realtime
    temp.append(realstart)
    return temp

def spiderFlight(flight):
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8' )
    cursor = db.cursor()
    # flight = input("请输入查询的航班号：")
    url = "https://zh.flightaware.com/live/flight/" + flight + "/history/180"
    soup = get_XML(url)
    if not soup.findAll("tr", {"class": ["smallActiverow1 rowClickTarget", "smallActiverow2 rowClickTarget"]}):
        return None
    for tr in soup.findAll("tr", {"class": ["smallActiverow1 rowClickTarget", "smallActiverow2 rowClickTarget"]}):  # 两类class，1和2
        temp_flight = []
        temp_flight.append(flight)
        for td in tr.findAll("td"):
            temp_flight.append(td.text)
        temp_format = flight_format(temp_flight)

        if temp_format:
            sql = """INSERT INTO flightdata(flight,date,plane,origin,destnation,starttime,endtime,reallytime) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )""" % \
                  (temp_format[0],pymysql.escape_string(temp_format[1]),temp_format[2],temp_format[3],temp_format[4],temp_format[5],temp_format[6],temp_format[7])
            try:
                cursor.execute(sql)
                db.commit()
                print("Insert success: ",temp_format)
            except:
                db.rollback()
                print("Insert error: ",temp_format)
    db.close()