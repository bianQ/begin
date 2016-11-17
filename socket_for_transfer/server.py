import socket
import os

sk = socket.socket()
sk.bind(('192.168.1.108',8080))
sk.listen(5)

while True:
    conn = sk.accept()[0]
    #ilename = 'D:/World of Warcraft.zip'
    filename = 'F:/腾讯游戏/穿越火线.zip'
    file_size = os.stat(filename).st_size
    client_recv = int(conn.recv(1024).decode())
    sent_size = client_recv
    file = open(filename,'rb')
    if client_recv != 0:
        print('服务器正在计算上次传输中断位置。。。')
        file.seek(client_recv)
        print('服务器已跳转到中断位置，已下载%s字节，开始续传。。。' % client_recv)
    flag = True
    while flag:
        if sent_size + 20480 > file_size:
            data = file.read(file_size - sent_size)
            Flag = False
        else:
            data = file.read(20480)
            sent_size += 20480
        conn.send(data)
        #print(data)
    print('对方已下载完毕。。。')
    file.close()

sk.close()

