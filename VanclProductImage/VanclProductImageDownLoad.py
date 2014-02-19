#! /usr/bin/env python
#coding=utf-8
import os
import time
import socket
import threading
import urllib.request
import logging
import sys
import pyodbc

homedir = os.getcwd()
socket.setdefaulttimeout(10)#设置socket操时时间，默认为60秒
imageUrlFormart = "http://p2.vanclimg.com/product/%s/%s/%s/%s/Big/%s"
connString=''
sql ="""
SELECT w.ProductCode,w.PhotoPath,w.ImageName
FROM dbo.w_ProductPhotos w(NOLOCK)
  WHERE w.PhotoType=0  
  AND w.productcode IN ('0002201','0002200','0002199','0002203','0002202','0004778','0004775','0004777','0004776','0004761','0004764','0004760','0004763','0004762','0004774','0004773','0004769','0004765','0004772','0004768','0004771','0004767','0004766','0004770','0004753','0004759','0004758','0004752','0004757','0004756','0004751','0004755','0004750','0004754','0002212','0004050','0002213','0002208','0002207','0002209','0002206','0002211','0002205','0002204','0002210','0002193','0002196','0002198','0002192','0002197','0002191','0002190','0002195','0002189','0002194','0147257','0147259','0147261','0147256','0147260','0147133','0147135','0147132','0147130','0147131','0030050','0030051','0030049','0030048','0164858','0030047','0030052','0029648','0029649','0029647','0030007','0029645','0029644','0066884','0066883','0066882','0066881','0066885','0066886','0066880','0066879','0030128','0030127','0030126','0030125','0030124','0030129','0030130','0030120','0030123','0030119','0030122','0030121','0030090','0030091','0030089','0030087','0030088','0030086','0030085','0030084','0030083','0030093','0030094','0030082','0030081','0030092','0168263','0168264','0168265','0168266','0168267','0168268','0168269','0168270','0168271','0168272','0168273','0168274','0168275','0173629','0173630','0173631','0173632','0173635','0173634','0173633','0173623','0178334','0173624','0173625','0173626','0173627','0173628','0173637','0178409','0173638','0173640','0173641','0173642','0173643','0173645','0173646','0173647','0179569','0179570','0173649','0178402','0178401','0173650','0173652','0173654','0173655','0173658','0173660','0173636','0173639','0173644','0173648','0173651','0173653','0173656','0173657','0173659','0029646','0188813','0188812','0188814','0188815','0188834','0188835','0188836','0188837','0188816','0188818','0188819','0188817','0188838','0188839','0188840','0188841','0192473','0192474','0192475','0192476','0192445','0192446','0192447','0192448','0192449','0192450','0192451','0192452','0192453','0192454','0192415','0192416','0192417','0192418','0192419','0192420','0192424','0192425','0192426','0192427','0192428','0192429','0192430','0192431','0192432','0192433','0192434','0192435','0192518','0192519','0192520','0192521','0192522','0192523','0192524','0192525','0192526','0192527','0192528','0192529','0192530','0192531','0192532','0192407','0192408','0192409','0192410','0192411','0194694','0194695','0194696','0194697','0194698','0194693','0194699','0194703','0194704','0194705','0194706','0194707','0194708','0194700','0194701','0194702')
ORDER BY w.ProductCode ,w.IsMain desc
"""
def getDataFromDB():
    with pyodbc.connect(connString) as cnxn:
        with cnxn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
    dealData(rows)

def getDataFromtxt():
    if not os.path.isfile(dataJsonPath):
        logger.debug('当前目录%s下未找到datajons.txt文件', homedir)
        return
    with open(dataJsonPath) as f:
        lines = f.readlines()
    dealData(lines)

def dealData(rows):
    logger.debug('共需下载数%d'%(len(rows)))
    for row in rows:
        ThreadDownload.lck.acquire()
        if(isinstance(row,str)):#如果数据行为str类型，则通过eval函数将其转为tuple，以适应下面的代码row[i]
            row=eval(row)
        pcode=row[0]
        ppath=row[1]
        iname=row[2]
        
        if len(ThreadDownload.taskList)>=ThreadDownload.maxThreads:
            ThreadDownload.lck.release()
            #logger.debug('下载线程已经达到最大值%d，等待线程完成中' %(ThreadDownload.maxThreads))
            ThreadDownload.even.wait()
        else:
            ThreadDownload.lck.release()

        savePath = '%s\\Images\\%s' %(homedir,pcode)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        sFileName = '%s\\%s' %(savePath,ppath if len(iname)==0 else iname)
        iUrl = imageUrlFormart %(pcode[0],pcode[1],pcode[2],pcode,ppath)
        #print('%s---开始下载 %s 的 %s' %(time.ctime(),pCode,pPath))
        ThreadDownload.addTask(iUrl,sFileName)

class ThreadDownload(threading.Thread):
    taskList=[]
    maxThreads=10
    even = threading.Event()
    lck = threading.Lock()
    def __init__(self,imgUrl,saveFileName):
        threading.Thread.__init__(self)
        self.url=imgUrl
        self.sname = saveFileName

    def run(self):
        try:
            with urllib.request.urlopen(self.url) as conn:
                imageData = conn.read()
                with open(self.sname,'wb') as s:
                   s.write(imageData)
                   logger.debug('完成下载 %s' ,self.url)
            time.sleep(2)
        except Exception as e:
            logger.error('发生异常：%s' ,e)
        ThreadDownload.lck.acquire()
        ThreadDownload.taskList.remove(self)
        if len(ThreadDownload.taskList) == ThreadDownload.maxThreads-1:
            ThreadDownload.even.set()
            ThreadDownload.even.clear()
        ThreadDownload.lck.release()

    def addTask(imgUrl,saveFileName):
        ThreadDownload.lck.acquire()
        dl = ThreadDownload(imgUrl,saveFileName)
        ThreadDownload.taskList.append(dl)
        ThreadDownload.lck.release()
        dl.start()

class MyLogger():
    def __init__(self, logfilename,loggername):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logfilename)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        #formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

if __name__ == '__main__':
    startTime = time.clock()
    firstArgErrmsg='第一个参数为数据源类型，db表示从sqlserver获取数据，txt表示从文本获取数据'
    secondArgErrmsg='第二个参数为txt文件名称'
    logger = MyLogger(logfilename='log.txt',loggername='VanclProductImageDownLoad').getlog()
    if len(sys.argv)<=1:
            logger.debug(firstArgErrmsg)
            exit()
    dataType = sys.argv[1]
    if(dataType=='db'):
        getDataFromDB()
    elif(dataType=='txt'):
        if(len(sys.argv)<=2):
            logger.debug(secondArgErrmsg)
            exit()
        dataJsonPath = '%s\\%s' %(homedir,sys.argv[2])
        logger.debug('本次处理的文件为%s' %(dataJsonPath))
        getDataFromtxt()
    else:
        logger.debug(firstArgErrmsg)
    logger.debug('全部完毕,耗时{0}s'.format(time.clock()-startTime))