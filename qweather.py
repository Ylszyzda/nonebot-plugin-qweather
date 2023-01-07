import requests
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Bot

key = 'XXX'#填写你的和风天气key/没有key?阅读README查看获取教程
url='https://devapi.qweather.com/v7/weather/3d?'
cityidurl = 'https://geoapi.qweather.com/v2/city/lookup?'

msg = on_command('msg',aliases={'天气'})
@msg.handle()
async def searchweather(bot: Bot, event: GroupMessageEvent, state: T_State):
    cityget=str(event.get_message()).strip()#城市名称，支持模糊搜索
    city = cityget.strip('天气 ')
    params2 = {
        'location': city,
        'key':key,
        'lang': 'zh'
    }
    res2 = requests.get(url=cityidurl,params=params2)
    try:
        cityjson = res2.json()['location']
        city = cityjson[0]
        cityname = city['name']
        location = city['id']
        params1 = {
            'location': location,
            'key':key,
            'lang': 'zh'
        }
        res1 = requests.get(url=url,params=params1)
        jsondata=res1.json()['daily']
        todaydata = jsondata[0]
        tomdata = jsondata[1]
        #afterdata = jsondata[2]
        readweather1 ='今日'+cityname+'天气'+todaydata['textDay']+','+todaydata['windDirDay']+todaydata['windScaleDay']+'级。最高温度'+todaydata['tempMax']+'度，最低温度'+todaydata['tempMin']+'度。'
        readweather2 ='明日'+cityname+'天气'+tomdata['textDay']+','+tomdata['windDirDay']+tomdata['windScaleDay']+'级。最高温度'+tomdata['tempMax']+'度，最低温度'+tomdata['tempMin']+'度。'
        await msg.send(readweather1)
        await msg.send(readweather2)
    except KeyError:
        await msg.send('未找到城市或城市id拼写有误！')

