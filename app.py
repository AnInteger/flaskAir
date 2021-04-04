import csv

import pymysql
from flask import Flask, render_template
from flask import request

from spider import spiderFlight
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/flightdata')
def loadflightdata():
    #file = open('./airdata/flightdata.csv', 'r', encoding='utf-8')
    #csvreader = csv.reader(file)
    ##航班号,日期,机型,始发地四字,目的地四字,始发时间,到达时间,飞行时间
    #data = {
    #    "name" :"flightdata",
    #    "data" : [],
    #}
    #head =next(csvreader)
    #temp = {}
    #for i in  csvreader:
    #    temp["flight"] = i[0]
    #    temp["date"] = i[1]
    #    temp["plane"] = i[2]
    #    temp["origin"] = i[3]
    #    temp["destnation"] = i[4]
    #    temp["start"] = i[5]
    #    temp["end"] = i[6]
    #    temp["really"] = i[7]
    #    data["data"].append(temp)
    #    temp = {}

    flightnumber = request.values.get("data")
    #按照航班号查询



    result = queryflightdatabyflight(flightnumber)
    if not result:
        spiderFlight(flightnumber)
        result = queryflightdatabyflight(flightnumber)

    if not result:
        return None

    #按照四字码查询相应的城市名称
    originName = queryairportnamebyicao(result[0][3])
    destnationName = queryairportnamebyicao(result[0][4])

    originicao = result[0][3]
    destnationicao = result[0][4]

    data = {
        "name": flightnumber,
        "data": [],
        "origin": "",
        "destnation": "",
    }


    bundel1 = {}
    airportresult = querylonlatbyairport(originicao)
    if not airportresult:
        print("Can't find the airport, please insert " + originicao +" by hand.")
        return None
    bundel1["airport"] = originicao
    bundel1["lon"] = airportresult[3]
    bundel1["lat"] = airportresult[4]
    data["origin"] = bundel1
    #print(bundel1)
    #print(data)

    bundel2 = {}
    airportresult = querylonlatbyairport(destnationicao)
    bundel2["airport"] = destnationicao
    bundel2["lon"] = airportresult[3]
    bundel2["lat"] = airportresult[4]
    data["destnation"] = bundel2
    #print(bundel2)
    #print(data)

    temp = {}
    for i in result:
        temp["flight"] = i[0]
        temp["date"] = i[1]
        temp["origin"] = originName
        temp["destnation"] = destnationName
        temp["starttime"] = i[5]
        temp["endtime"] = i[6]
        temp["reallytime"] = i[7]
        data["data"].append(temp)
        temp = {}

    return data

@app.route('/hotflight')
def loadhotdata():
    tophotflight = queryhotflight()[0:50]

    data = {
        #"topflight" : [
        #    {
        #        "name": '',
        #        "origin": "",
        #        "destnation": "",
        #    }
        #]
        "topflight": []
    }

    for i in tophotflight:
        flight = queryflightdatabyflight(i["flight"])
        onefilght = {
            "name":i["flight"],
        }
        temp = {}
        airportresult = querylonlatbyairport(flight[0][3])  #第一条数据记录的第三列是始发地，第四列是目的地
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["origin"] = temp
        temp = {}

        temp = {}
        airportresult = querylonlatbyairport(flight[0][4])
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["destnation"] = temp
        temp = {}

        data["topflight"].append(onefilght)
    return data

@app.route('/loadCnoutter')
def Cnoutter():
    result = queryflightdataChinaoutter()
    data = {
        #"topflight" : [
        #    {
        #        "name": '',
        #        "origin": "",
        #        "destnation": "",
        #    }
        #]
        "topflight": []
    }

    for i in result:
        onefilght = {
            "name":i["flight"],
        }
        temp = {}
        airportresult = querylonlatbyairport(i["origin"])  #第一条数据记录的第三列是始发地，第四列是目的地
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["origin"] = temp
        temp = {}

        temp = {}
        airportresult = querylonlatbyairport(i["destnation"])
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["destnation"] = temp
        temp = {}

        data["topflight"].append(onefilght)
    return data

@app.route('/loadCninner')
def loadCninner():
    result = queryflightdataChinainner()
    data = {
        #"topflight" : [
        #    {
        #        "name": '',
        #        "origin": "",
        #        "destnation": "",
        #    }
        #]
        "topflight": []
    }

    for i in result:
        onefilght = {
            "name":i["flight"],
        }
        temp = {}
        airportresult = querylonlatbyairport(i["origin"])  #第一条数据记录的第三列是始发地，第四列是目的地
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["origin"] = temp
        temp = {}

        temp = {}
        airportresult = querylonlatbyairport(i["destnation"])
        temp["airport"] = airportresult[2]
        temp["lon"] = airportresult[3]
        temp["lat"] = airportresult[4]
        onefilght["destnation"] = temp
        temp = {}

        data["topflight"].append(onefilght)
    return data

def queryairportnamebyicao(icao):
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8')
    cursorairport = db.cursor()
    sql = "SELECT name FROM airport WHERE icao = %s"

    try:
        cursorairport.execute(sql,(icao))
        result = cursorairport.fetchone()
        db.close()
        return result
    except:
        print("error")
        return None

def querylonlatbyairport(airport):
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8')
    cursorairport = db.cursor()
    sql = "SELECT * FROM airport WHERE icao = %s"
    try:
        cursorairport.execute(sql,(airport))
        result = cursorairport.fetchone()
        db.close()
        return result
    except:
        print("error")
        return None

def queryflightdatabyflight(flight):
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8')
    cursorflightdata = db.cursor()
    sql = "SELECT * FROM flightdata WHERE flight = %s order by date desc"

    try:
        cursorflightdata.execute(sql, (flight))
        result = cursorflightdata.fetchall()
        db.close()
        return result

    except:
        print("error")
        return None

def queryhotflight():
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8')
    cursorflightdata = db.cursor()

    sql = "select flight,count(flight) from flightdata group by flight order by count(flight) desc"
    try:
        cursorflightdata.execute(sql)
        result = cursorflightdata.fetchall()
        db.close()
        data = []
        temp = {}
        for i in result:
            #print(i[0])
            temp["flight"] = i[0]
            temp["num"] = i[1]
            data.append(temp)
            temp={}
        return data

    except:
        print("error")
        return None

def queryflightdataChinainner():
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    cursorflightdata1 = db.cursor()
    cursorflightdata2 = db.cursor()

    sql1 = "select flightdata.flight from flightdata,airport " \
          "where ((flightdata.origin = airport.icao and airport.country = 'China')) " \
          "group by flightdata.flight "

    sql2 = "select flightdata.flight from flightdata,airport " \
          "where ((flightdata.destnation = airport.icao and airport.country = 'China')) " \
          "group by flightdata.flight "

    cursorflightdata1.execute(sql1)
    result1 = cursorflightdata1.fetchall()
    cursorflightdata2.execute(sql2)
    result2 = cursorflightdata2.fetchall()
    set1 = []
    set2 = []
    for i in result1:
        set1.append(i["flight"])

    for i in result2:
        set2.append(i["flight"])

    temp = list(set(set1) & set(set2))

    cursorflightdata3 = db.cursor()
    sql3 = "select * from flightdata where flight = %s "

    result3 = []

    for i in temp:
        cursorflightdata3.execute(sql3, (i))
        result3.append(cursorflightdata3.fetchone())

    db.close()
    return result3

def queryflightdataChinaoutter():
    db = pymysql.connect("localhost", "root", "sx29264", "airdata", charset='utf8',cursorclass = pymysql.cursors.DictCursor)
    cursorflightdata1 = db.cursor()
    cursorflightdata2 = db.cursor()

    sql1 = "select flightdata.flight from flightdata,airport " \
          "where ((flightdata.origin = airport.icao and airport.country = 'China')) " \
          "group by flightdata.flight "

    sql2 = "select flightdata.flight from flightdata,airport " \
          "where ((flightdata.destnation = airport.icao and airport.country != 'China')) " \
          "group by flightdata.flight "

    cursorflightdata1.execute(sql1)
    result1 = cursorflightdata1.fetchall()
    cursorflightdata2.execute(sql2)
    result2 = cursorflightdata2.fetchall()
    set1 = []
    set2 = []
    for i in result1:
        set1.append(i["flight"])

    for i in result2:
        set2.append(i["flight"])

    temp = list(set(set1) & set(set2))

    cursorflightdata3 = db.cursor()
    sql3 = "select * from flightdata where flight = %s "

    result3 = []

    for i in temp:
        cursorflightdata3.execute(sql3, (i))
        result3.append(cursorflightdata3.fetchone())

    db.close()
    return result3

if __name__ == '__main__':
    app.run()

