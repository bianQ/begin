import socket
import os
import time

sk = socket.socket()
sk.connect(('192.168.1.108',8080))
#path = 'E:/World of Warcraft.zip'
path = 'F:/腾讯游戏/穿越火线.zip'

if os.path.exists(path):
    recved_size = os.stat(path).st_size
    print('准备续传，等待连接。。。')
    time.sleep(3)
else:
    recved_size = 0
sk.send(str(recved_size).encode())
while True:
    print('连接成功，下载即将开始。。。')
    flag = True
    recv_size = recved_size
    #file_size = '38564464935'
    file_size = '5409907685 '
    filename = path
    f = open(filename,'ab')
    while flag:
        if int(file_size) > recv_size:
            data = sk.recv(20480)
            recv_size += len(data)
            print('已下载' + str(recv_size/int(file_size)*100)[0:4]+ '%')
            f.write(data)
        else:
            recv_size = 0
            flag = False

    f.close()
    if os.stat(filename).st_size == int(file_size):
        print('文件下载成功。。。')
        break
    else:
        print('下载失败。。。')
        break
