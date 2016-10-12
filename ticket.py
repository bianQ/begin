"""Train tickets query via command-line.
Usage:
    ticket [-GDTKZ]  <from> <to> <date>

Options:
    -h, --help  显示帮助菜单
    -G          高铁
    -D          动车
    -T          特快
    -K          快速
    -Z          直达

Example:
    ticket shenzhen wuhan 2016-10-14
"""
from docopt import docopt
from prettytable import PrettyTable
import re, requests


city_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8955'
def get_CityCode(url):
    '''
    获取城市代码
    '''
    code = requests.get(url,verify=False)
    dict_code = dict(re.findall(r'([A-Z]+)\|([a-z]+)',code.text))
    #因为得到的dict结果为  BJP：beijing，所以需要将key与value的位置对调
    Code = dict(zip(dict_code.values(),dict_code.keys()))
    #Code = pprint(Code)
    return Code

def get_StationUrl():
    '''
    获取列车信息url
    '''
    arguments = docopt(__doc__)
    from_station = get_CityCode(city_url).get(arguments['<from>'])
    to_station = get_CityCode(city_url).get(arguments['<to>'])
    date = arguments['<date>']
    station_url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_' \
                  'station={}'.format(date, from_station, to_station)
    return station_url


def get_info(url):
    '''
    获取每趟列车详细信息
    '''
    text = requests.get(url, verify=False)
    data = text.json()['data']['datas']
    arguments = docopt(__doc__)
    trainG = arguments['-G']
    trainD = arguments['-D']
    trainT = arguments['-T']
    trainK = arguments['-K']
    trainZ = arguments['-Z']
    for each_train in data:
        duration = each_train.get('lishi').replace(':', '小时') + '分钟'
        if duration.startswith('00'):
            duration = duration[4:]
        if duration.startswith('0'):
            duration = duration[1:]
        train = [
            #车次
            each_train['station_train_code'],
            #出发、到达站
            '\n'.join([each_train['from_station_name'], each_train['to_station_name']]),
                # 出发、到达时间
                '\n'.join([each_train['start_time'], each_train['arrive_time']]),
                # 历时
                duration,
                # 一等坐
                each_train['zy_num'],
                # 二等坐
                each_train['ze_num'],
                # 软卧
                each_train['rw_num'],
                # 软坐
                each_train['yw_num'],
                # 硬坐
                each_train['yz_num']
            ]
        if trainG and 'G' in each_train['station_train_code']:
            trains.append(train)
        if trainD and 'D' in each_train['station_train_code']:
            trains.append(train)
        if trainT and 'T' in each_train['station_train_code']:
            trains.append(train)
        if trainK and 'K' in each_train['station_train_code']:
            trains.append(train)
        if trainZ and 'Z' in each_train['station_train_code']:
            trains.append(train)
    return trains

def pretty_print(header, trains):
    pt = PrettyTable()
    pt._set_field_names(header)
    for train in trains:
        pt.add_row(train)
    print(pt)


if __name__ == '__main__':
    trains = []
    header = "车次 站点 时间 历时 一等座 二等座 软卧 硬卧 硬座".split()
    TrainInfo = get_info(get_StationUrl())
    pretty_print(header,TrainInfo)