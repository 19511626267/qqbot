import json
from class_Schedule.main import get_schedule,get_score
import requests, emoji.mixer
import time,os
import datetime


def private_chat(uid, content):
    requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}'.format(uid, content))

def group_chat(gid, content):
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, content))

def sent_pic_to_group(gid):
    # url = r"[CQ:image,file=file:///C:\Users\86186\Desktop\pyclass\bot\listener\img.png]"
    url = r"[CQ:image,file=file:///" + os.path.dirname(__file__) + "\img.png]"
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, url))

def sent_pic_to_friend(uid):
    url = r"[CQ:image,file=file:///" + os.path.dirname(__file__) + "\img.png]"
    requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}'.format(uid, url))

def today_schedule():
    # weeknum是从开学到现在的周数 dayoweek是今天是周几
    week = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", "Thursday": "星期四", "Friday": "星期五",
            "Saturday": "星期六", "Sunday": "星期日"}
    dayoweek = week[str(time.strftime("%A", time.localtime()))]
    term_start = datetime.datetime(2022, 2, 28)
    t = time.localtime()
    now = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday)
    days = (now - term_start).days
    days += 1
    weeknum = days // 7
    day_of_week = days % 7
    if (day_of_week != 0):
        # weeknum是从开学到现在的周数 dayoweek是今天是周几
        weeknum += 1
    with open("minschedule.json", "r", encoding="gbk") as f:
        dic = f.read()
    dic = json.loads(dic)
    dic = dic[dayoweek]
    content = "========" + str(weeknum) + "周========\n"
    for i in dic:
        content += i[0] + "\n" + i[1] + " " + i[2] + " " + i[3] + "\n"
        content += "-------\n"

    return content


def get_weather():
    # url的key是在高德申请的API  https://console.amap.com/dev/key/app
    QD = "https://restapi.amap.com/v3/weather/weatherInfo?city=370200&key=2b2f7b64c1da3adc1f0cee2097f03c72"
    CQ_yongchuan = "https://restapi.amap.com/v3/weather/weatherInfo?city=500118&key=2b2f7b64c1da3adc1f0cee2097f03c72"
    weather = ""
    jsoon = json.loads(requests.get(QD).text)
    weather += "QD 天气:" + jsoon["lives"][0]["weather"] + " 气温:" + jsoon["lives"][0]["temperature"] + " 湿度:" + \
               jsoon["lives"][0]["humidity"] + "\n"

    jsoon = json.loads(requests.get(CQ_yongchuan).text)
    weather += "CQ 天气:" + jsoon["lives"][0]["weather"] + " 气温:" + jsoon["lives"][0][
        "temperature"] + " 湿度:" + jsoon["lives"][0]["humidity"] + "\n"

    return weather




def keyword(message, uid, gid=None):
    if (message == "重置课表"):
        s = get_schedule()
        if (gid == None):
            private_chat(uid, s)
        else:
            group_chat(gid, s)
        return s
    if (message == "课表"):
        weather = get_weather()
        s = today_schedule()
        if (gid == None):
            private_chat(uid, str(weather) + str(s))
        else:
            group_chat(gid, str(weather) + str(s))
        return str(weather) + str(s)
    # emojimixer
    if (str(message).find("+")!=-1):
        emoji.mixer.main(message)
        if (gid == None):
            sent_pic_to_friend(uid)
        else:
            sent_pic_to_group(gid)

    # setu功能
    if (message=="成绩"):
        score=get_score()
        if (gid == None):
            private_chat(uid, str(score))
        else:
            group_chat(gid, str(score))
        return str(score)
    if (message == "setu"):
        setu(uid)


def setu(uid):

    url = r"[CQ:image,file=file:///C:\Users\86186\Desktop\pyclass\bot\listener\img.png]"
    requests.get(url='http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}'.format(uid, url))


if __name__ == '__main__':
    print(get_score())
