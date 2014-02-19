#! /usr/bin/env python
#coding=utf-8
import threading
import time

class scanner(threading.Thread):
    tlist=[] #用来存储队列的线程
    maxthreads=1 # int(sys.argv[2])最大的并发数量，此处我设置为100，测试下系统最大支持1000多个
    evnt=threading.Event()#用事件来让超过最大线程设置的并发程序等待
    lck=threading.RLock() #线程锁    
    def __init__(self,counter):
        threading.Thread.__init__(self)
        self.id=counter
    def run(self):
        try:
            print('%s runing %d' %(time.ctime(),self.id))
            time.sleep(3)
        except Exception as e:
            print(e)
        #以下用来将完成的线程移除线程队列
        scanner.lck.acquire()
        scanner.tlist.remove(self)
        #如果移除此完成的队列线程数刚好达到99，则说明有线程在等待执行，那么我们释放event，让等待事件执行
        if len(scanner.tlist)==scanner.maxthreads-1:
            print('scanner.evnt.set()')
            scanner.evnt.set()
            scanner.evnt.clear()
        scanner.lck.release()
    def newthread(counter):
        scanner.lck.acquire()#上锁
        sc=scanner(counter)
        scanner.tlist.append(sc)
        scanner.lck.release()#解锁
        sc.start()
    #将新线程方法定义为静态变量，供调用
    #newthread=staticmethod(newthread)

def runscan():
    for i in range(1,10):
        
        scanner.lck.acquire()
        #如果目前线程队列超过了设定的上线则等待。
        if len(scanner.tlist)>=scanner.maxthreads:
            scanner.lck.release()
            print('scanner.evnt.wait()')
            scanner.evnt.wait()#scanner.evnt.set()遇到set事件则等待结束
        else:
            scanner.lck.release()
            print('scanner.lck.release()')
        print('scanner.newthread(%d)' %(i))
        scanner.newthread(i)
        '''
    for t in scanner.tlist:
        t.join()#join的操作使得后面的程序等待线程的执行完成才继续
'''
if __name__=="__main__":
    runscan()
    
