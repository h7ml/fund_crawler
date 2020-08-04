import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
from bs4 import BeautifulSoup
import re
import urllib.request
import numpy as np
from time import sleep
import time


class my_mail:
    """
        处理邮件
    """
    def __init__(self):
        self.mail_server = "smtp.88.com"
        self.mail_admin = os.environ["emailUser"]
        self.mail_admin_password = os.environ["emailPassword"]
        self.mail_port = 465
        self.smtpObj = smtplib.SMTP_SSL(self.mail_server,
                                        self.mail_port,
                                        timeout=10)
        self.smtpObj.login(self.mail_admin, self.mail_admin_password)

    def send_message(self, msg):
        # 接受消息发送出去
        message = MIMEText(msg, "html", "utf-8")
        message["Form"] = Header("爬虫", "utf-8")
        message["To"] = Header("h7ml", "utf-8")
        year = str(time.localtime().tm_year)
        month = str(time.localtime().tm_mon)
        day = str(time.localtime().tm_mday)
        hour = str(time.localtime().tm_hour)
        minute = str(time.localtime().tm_min)
        second = str(time.localtime().tm_sec)
        nowTime = year + '年' + month + '月' + day + '日' + hour + '时' + minute + '分' + second + '秒'
        subject = nowTime + "基金爬虫数据"
        message["Subject"] = Header(subject, "utf-8")

        try:
            self.smtpObj.sendmail(self.mail_admin, self.mail_admin,
                                  message.as_string())
            print(nowTime + "邮件发送成功")
        except smtplib.SMTPException:
            print("出错了")

    def quit(self):
        # 退出
        self.smtpObj.quit()


class Gupiao(object):
    """获取股票信息"""
    def __init__(self):
        """初始化 """
        self.url = "http://stocks.sina.cn/fund/?code={}&vt=4"
        self.msg = ""

    def get_code_info(self, fund_code, fund_title):

        url = "http://fund.eastmoney.com/" + str(fund_code) + ".html"
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8')
        last_10_days_percent = re.findall(
            '<td class="alignLeft">[0-9][0-9]-[0-9][0-9]</td>  <td class="alignRight bold">(.+?)</td>',
            content)
        mean_data = []
        for i in last_10_days_percent:
            mean_data.append(float(i))
            last_10_days_mean = np.mean(mean_data)
        real_time_valuation = re.findall('id="gz_gsz">(.+?)</span>', content)
        rt_percent = re.findall('id="gz_gszzl">(.+?)%</span>', content)
        image_url = "http://j4.dfcfw.com/charts/pic6/{}.png".format(fund_code)

        # 发送 的内容
        self.msg = self.msg + """
            <table style="border-collapse:collapse;border:1px solid #ddd;text-align:center">
            <tbody>
                <tr>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">基金代码</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">基金名</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">实时净值估值</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">估计增长百分数</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">近十日净值平均值</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">趋势图</th>
                <th style="border:1px solid #ddd;padding:6px;background-color:#eee">100份收益</th>
                </tr>
                <tr style="border:1px solid #ddd;padding:6px">
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                <td style="border:1px solid #ddd;padding:6px"><a target="_top" title="点击查看详情" href="{}"><img src="{}" style="width:88px;height:88px" /></a></td>
                <td style="border:1px solid #ddd;padding:6px">{}</td>
                </tr>
            </tbody>
            </table>
            \n
        """.format(str(fund_code),str(fund_title), str(real_time_valuation[0]),
                   str(rt_percent[0]),
                   str(last_10_days_mean)[0:5], image_url, image_url,str(rt_percent[0]))

    def send(self, mail):
        mail.send_message(self.msg)


def main():
    # 主函数
    b = my_mail()
    json_str =  [
        {
            "id": "161725",
            "text": "招商中证白酒"
        },
        {
            "id": "003096",
            "text": "中欧医疗健康混合C"
        },
        {
            "id": "008935",
            "text": "大成科技消费股票C"
        },
        {
            "id": "003291",
            "text": "信达澳银健康中国混合"
        },
        {
            "id": "004698",
            "text": "博时军工主题股票"
        },
        {
            "id": "001704",
            "text": "国投瑞银进宝灵活配置混合"
        }
    ]
    a = Gupiao()
    for c in json_str:
        try:
            a.get_code_info(c['id'],c['text'])
            print("基金代码  " + c['id'],c['text'] + "  爬取成功")
        except:
            print("出错代码:{}".format(c['id'],c['text']))
    a.send(b)
    b.quit()


if __name__ == "__main__":
    main()
