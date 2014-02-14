#! /usr/bin/env python
#coding=utf-8
import http  
import urllib.request  
from bs4 import BeautifulSoup  
import os  
  
def getContent():                     #从建立http连接，在网站中获取所有内容  
    ur ="tu.duowan.com"  
    conn = http.client.HTTPConnection(ur)  
    conn.request("GET", "/m/meinv/index.html")  
    r = conn.getresponse()  
    data = r.read()                #.decode('utf-8') #编码根据实际情况酌情处理  
    return data  
   
def getImageUrl(data,filePath):             #将获取到img链接写到filePath文件  
    sour = open(filePath, 'w')  
    soup = BeautifulSoup(conte)  
    for i in soup.find_all('img'):  
        sour.write(i.get('src'))    #把从标签中提取的url地址写入文件  
        sour.write(os.linesep)      #每次写入一个url地址，然后换行  
    sour.close()  
def downImage(filePath):                    #根据filePath里面的url自动下载图片  
    tt = 0    #name  
    sour = open(filePath)  
    while 1:  
        line = sour.readline()  
        if line:  
            #判断从文件中读取的url是不是图片类型，这里是jpg类型  
            if(line.find('jpg')>0):  
                data = urllib.request.urlopen(line).read()  
                f = open('D:\\download\\tmp\\' + str(tt) + '.jpg', 'wb')   #在tmp文件中存储下载的图片  
                f.write(data)  
                f.close()  
                tt = tt + 1  
            else:  
                pass
        else:
            break
    sour.close()  

if __name__ == '__main__':
    conte = getContent()                          #建立 与网站的链接  
    soup = BeautifulSoup(conte)                   #获取网页的html信息  
    filePath = "D:\\download\\tmp\\1.txt"         #存储url的路径  
    getImageUrl(soup,filePath)                    #提取图片url的信息    
    downImage(filePath)                           #下载图片    
    print("Succeed download pictures")            #下载成功