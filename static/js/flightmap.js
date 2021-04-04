var mapflight;
var ectest = echarts.init(document.getElementById("flightmap"));

var flight = [
    //[{name:'LIMG'},{name:'ZBAA'}],
    //[{name:'ZBAA'},{name:'AYNZ'}]

];

var geoCoordMap = {
    //示例
    //"AYGA": [145.391998291, -6.081689834590001],
    //"AYMD": [145.789001465, -5.20707988739],
    //"AYMH": [144.29600524902344, -5.826789855957031],
};

var airport = [
    {name: "LIMG", value:14},
    {name: "ZBAA", value:16},
    {name: "AYGA", value:13},
    {name: "AYMD", value:14}
];

var color = ['#a6c84c', '#ffa022', '#46bee9'];
var planePath = 'path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z';

var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var dataItem = data[i];
        var fromCoord = geoCoordMap[dataItem[0].name];
        var toCoord = geoCoordMap[dataItem[1].name];
        if (fromCoord && toCoord) {
            res.push({
                fromName: dataItem[0].name,
                toName: dataItem[1].name,
                coords: [fromCoord, toCoord]
            });
        }
    }
    return res;
};
var convertAirport = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var dataItem = data[i];
        var portName = dataItem.name;
        var lng = geoCoordMap[portName][0];
        var lat = geoCoordMap[portName][1];
        res.push({
            name : portName,
            value : [lng,lat],
        });
    }
    return res;
};

option = {
    backgroundColor: '#f8f9fa',
    title : {
        text: 'Flight Map',
        subtext: 'byFlightaware',
        left: 'center',
        textStyle: {
            color: '#6c757d'
        }},
    geo: {
        map: 'world',
        label: {
            show: false
        },
        roam: true,
        itemStyle: {
            areaColor: '#6c757d',
            borderColor: '#404a59'
        },
        emphasis: {
            label: {
                show: true,
                color: '#f8f9fa'
            },
            itemStyle: {
                areaColor: '#272b30'
            }},
    },
    series:""
};
var series = [];
var testAirport = function () {
    series = [];

    //函数包装 参数是对象 包括airport 和 airline
	series.push({
         type: 'effectScatter',
         name: "airport",
         coordinateSystem: 'geo',
         symbolSize: 6,
         color : "#fff",
         data: convertAirport(airport)
    },
    {
        name: 'flight',
        type: 'lines',
        zlevel: 2,
        symbol: ['none', 'arrow'],
        symbolSize: 10,
        effect: {
            show: true,
            period: 6,
            trailLength: 0,
            symbol: planePath,
            symbolSize: 15
        },
        lineStyle: {
            color: color[0],
            width: 1,
            opacity: 0.6,
            curveness: 0.2
        },
        data: convertData(flight)
    }
    );
	option["series"]=series;
    ectest.setOption(option);
};

var initmap = function () {
    ectest.setOption(option);
};

var queryByFlight = function () {
    var flightnumber = mapflight["name"];
    series = [];
    flight = [];
    series = [];
    geoCoordMap[mapflight["origin"]["airport"]] = [mapflight["origin"]["lon"],mapflight["origin"]["lat"]];
    geoCoordMap[mapflight["destnation"]["airport"]] = [mapflight["destnation"]["lon"],mapflight["destnation"]["lat"]];
    flight.push([{"name":mapflight["origin"]["airport"]},{"name":mapflight["destnation"]["airport"]}]);
    series.push({
        name: flightnumber,
        type: 'lines',
        zlevel: 2,
        symbol: ['none', 'arrow'],
        symbolSize: 10,
        effect: {
            show: true,
            period: 6,
            trailLength: 0,
            symbol: planePath,
            symbolSize: 15
        },
        lineStyle: {
            shadowColor: '#ffffff',
            color: '#F4606C',
            width: 2,
            opacity: 0.6,
            curveness: 0.2
        },
        data: convertData(flight)
    });
    option["series"]=series;
    ectest.setOption(option,true);
};

var hotflight = function () {
    var topflight = mapflight["topflight"];
    series = [];
    flight = [];
    geoCoordMap = [];
    airport = [];
    for (var i = 0; i < topflight.length; i++) {
        geoCoordMap[topflight[i]["origin"]["airport"]] = [parseFloat(topflight[i]["origin"]["lon"]),parseFloat(topflight[i]["origin"]["lat"])];
        geoCoordMap[topflight[i]["destnation"]["airport"]] = [parseFloat(topflight[i]["destnation"]["lon"]),parseFloat(topflight[i]["destnation"]["lat"])];
        flight.push([{"name":topflight[i]["origin"]["airport"]},{"name":topflight[i]["destnation"]["airport"]}]);
        airport.push({"name":topflight[i]["origin"]["airport"],"value":1});
        airport.push({"name":topflight[i]["destnation"]["airport"],"value":1});
    }
    series.push({
        name:"test",
        type: 'lines',
        zlevel: 2,
        symbol: ['none', 'arrow'],
        symbolSize: 10,
        effect: {
            show: true,
            period: 6,
            trailLength: 0,
            symbol: planePath,
            symbolSize: 15
        },
        lineStyle: {
            shadowColor: '#ffffff',
            color: '#F4606C',
            width: 2,
            opacity: 0.6,
            curveness: 0.2
        },
        data: convertData(flight),
    },{
        type: 'effectScatter',
        name: "airport",
        coordinateSystem: 'geo',
        symbolSize: 6,
        color : "#ECAD9E",
        data: convertAirport(airport),
    });
    option["series"]=series;
    ectest.setOption(option,true);
};