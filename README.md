# 基于go-cphttp的qq机器人 + 青岛科技大学教务系统爬虫

由爬虫提供课表,成绩文本 使用qq机器人进行消息发送 

* 功能
  * 爬取每日课表+天气
  * 爬取成绩
  * 学工系统每日打卡(待完成)





* 配置方式 
  * 爬虫配置
    * class_Schedule\login.js中5375行(var enPassword = hex2b64(rsaKey.encrypt(""));)的冒号中填入教务系统密码
    * class_Schedule\main.py 的13 14 行的url的su=后填入学号 45行("yhm", "")的冒号中填入学号



**第一次写可移植性做的不好,可能之后会优化一下**

