import http
import urllib.request
url = "desk.zol.com.cn"  
conn = http.client.HTTPConnection(url)
conn.request("GET", "/dongman/") 
r = conn.getresponse()  
print(r.status, r.reason)  
data1 = r.read()#.decode('utf-8') #编码根据实际情况酌情处理 
#print(data1)