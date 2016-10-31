"""lagou query via command-line.
Usage:
    spider <job> <city>

Options:
    -h, --help  显示帮助菜单

Example:
    python spider.py python工程师 深圳
"""

from docopt import docopt
from parsering import parsering

'''header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/54.0.2840.71 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,''application/xml;q=0.9,image/webp,*/*;q=0.8'
                        }'''
'''
添加job 、city命令，根据输入指令获取相关职位信息
'''

if __name__=='__main__':
    args = docopt(__doc__)
    job = args['<job>']
    city = args['<city>']
    Parser = parsering(job=job, city=city)
    Parser.getPageResult()

    print('相关职位信息已爬取完毕。。。')