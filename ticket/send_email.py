import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import os


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send(content):
    from_addr = '15989490620@163.com'  #发件箱
    password = os.environ.get('PASSWORD')  #授权密码
    to_addr = 'vagaab@foxmail.com'     #收件箱
    smtp_server = 'smtp.163.com'

    url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    style = 'table{ border:1px solid black; text-align:center;}' \
            'td{ border:1px solid black;}' \
            '.width{ width:60px;}'
    message = '''
            <html>
                <head>
                    <style>
                    {}
                    </style>
                    <title>火车票查询</title>
                </head>
                <body>
                    <p>你好！</p>
                    <br/>
                    <p>感谢你的使用。</p>
                    <p>火车票查询结果如下： &nbsp&nbsp&nbsp&nbsp&nbsp <a href="{}">点击跳转到12306官网订票</a></p>
                    <table>
                    <tr><td>车次</td><td class="width">站点</td><td class="width">时间</td><td class="width">历时</td>
                    <td class="width">一等座</td><td class="width">二等座</td><td class="width">软卧</td><td class=
                    "width">硬卧</td><td class="width">硬座</td></tr>
                    {}
                    </table>
                    <br>
                    <a href="{}">点击跳转到12306官网订票</a>
                </body>
            </html>
        '''.format(style, url, content, url)
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = _format_addr('边权的163邮箱 <%s>' % from_addr)
    msg['To'] = _format_addr('Python <%s>' % to_addr)  #to_addr 为str 多个邮箱用，隔开
    msg['Subject'] = Header('来自Python的测试邮件', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()