import pygal
import json
from flask import Flask


app = Flask(__name__)

def getData(file):
    with open(file, 'r') as f:
        data = json.loads(f.read())
        sort_data = sorted(data.items(), key=lambda x:x[1], reverse=True)[:10]
        return sort_data

@app.route('/')
def index():
    city_path = "../city.json"
    keyword_path = "..keyword.json"
    data_city = getData(city_path)
    data_keyword = getData(keyword_path)
    title = '51job职位分析'
    line_charCity = pygal.HorizontalBar()
    line_charCity.title = 'Python需求最高的十个城市'
    for item in data_city:
        line_charCity.add(item[0], item[1])

    line_charKeyword = pygal.HorizontalBar()
    line_charKeyword.title = 'Python相关职位中提到最多的十项技能'
    for item in data_keyword:
        line_charKeyword.add(item[0], item[1])
    html="""
        <html>
    <head>
        <title>%s</title>
    </head>
    <body>
        %s
        <br>
        %s
    </body>
    </html>
        """ % (title, line_char.render(is_unicode=True), line_char2.render(is_unicode=True))
    return html


if __name__ == '__main__':
    app.run()
