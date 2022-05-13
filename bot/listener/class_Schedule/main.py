import subprocess
import requests
import json
from lxml import etree
import time,os
import os

class QUST:
    def __init__(self):
        self.post_url = "https://jwglxt1.qust.edu.cn/jwglxt/xtgl/login_slogin.html?time="
        self.login_url = "https://jwglxt1.qust.edu.cn/jwglxt/xtgl/login_slogin.html"
        self.time_url = "https://jwglxt1.qust.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time="
        self.score_url="https://jwglxt1.qust.edu.cn/jwglxt/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su="
        self.class_schedule="https://jwglxt1.qust.edu.cn/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151&su="
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
        }

    def get_token(self):
        res = self.session.get(self.login_url, headers=self.headers)
        html = etree.HTML(res.text)
        self.token = html.xpath('//html/body/div[1]/div[2]/div[2]/form/input[1]/@value')
        self.token = str(self.token)[2:-2]


    def get_time(self):
        self.t = int(time.time()*1000)

    def get_publickey(self):
        res = self.session.get(self.time_url + str(self.t), headers=self.headers)
        self.dic = json.loads(res.text)

    def encrypt(self):
        path=os.path.dirname(__file__)+"\login.js"
        # print(path)
        self.mm = subprocess.check_output(r"node "+str(path)+" " + str(self.dic["modulus"]) + " " + str(self.dic['exponent']),shell=True)
        self.mm = str(self.mm)[2:-3]
        # print(self.mm)

    def login(self):
        data = [("csrftoken", self.token), ("language", "zh_CN"), ("yhm", ""), ("mm", self.mm),("mm", self.mm)]
        res = self.session.post(self.post_url+str(self.t), headers=self.headers, data=data)
        # print(res.text)
    def get_minschedule(self):
        dic = {"星期一": [], "星期二": [], "星期三": [], "星期四": [], "星期五": [], "星期六": [], "星期日": []}
        with open(r"Schedule.json", "r", encoding="utf-8") as f:
            a = f.read()
        s = json.loads(a)
        for i in s['kbList']:
            date = i["xqjmc"]
            list = dic[date]
            week =i["zcd"]
            num = i["jc"]
            room=i["cdmc"]


            list.append([i["kcmc"].strip(), week, num,room])
            dic[date] = list
        file = json.dumps(dic, ensure_ascii=False)  # ensure_ascii=False 没搞懂其实

        with open("minschedule.json", "w") as f:
            f.write(file)
    def get_class_schedule(self,academic_year,semester):
        class_post_data=[("xnm",str(academic_year)),("xqm",str(semester)),("kzlx","ck")]
        res=self.session.post(self.class_schedule,class_post_data)
        # print(res.text)
        with open("Schedule.json","w",encoding="utf-8") as f:
            f.write(res.text)
        self.get_minschedule()
    def get_score(self):
        score_data = [("xnm", "2021"), ("xqm", "3"), ("_search", "false"), ("nd", str(self.t)),("queryModel.showCount", "15"),("queryModel.currentPage", "1"),("queryModel.sortName", ""),("queryModel.sortOrder", "asc"),("time", "1")]
        score_json=self.session.post(self.score_url,score_data).text
        score_json=json.loads(str(score_json))
        score_list=score_json["items"]
        message='-----score-----\n'
        for course in score_list:
            message+=course["kcmc"]+":"+course["bfzcj"]+"\n"
        # print(message)
        return message

def get_schedule():
    try:
        qust = QUST()
        qust.get_token()
        qust.get_time()
        qust.get_publickey()
        qust.encrypt()
        qust.login()
        #                      学年,学期
        qust.get_class_schedule(2021, 12)

        return "success!"
    except Exception :
        return "fail!"

def get_score():
    qust = QUST()
    qust.get_token()
    qust.get_time()
    qust.get_publickey()
    qust.encrypt()
    qust.login()
    message=qust.get_score()
    return message
if __name__ == '__main__':
    get_score()