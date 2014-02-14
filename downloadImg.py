import os  
import urllib.request  
def rename(name):  
    if len(name) == 2:  
        name = '0' + name + '.jpg'  
    elif len(name) == 1:  
        name = '00' + name + '.jpg'  
    else:  
        name = name + '.jpg'  
    return name
    
os.chdir("D:\\download")
os.getcwd()
count = 0
baseurl = 'http://bgimg1.meimei22.com/list/2012-5-24/2/sa'
while count < 15:
    count = count + 1
    name=str(count)
    name = rename(name)
    print(name)
    url = baseurl + name
    try:
        a = urllib.request.urlopen(url)
        f = open(name, "wb")
        f.write(a.read())
        f.close()
        print(url + ' Saved!')
    except (Exception) as e:
        print(e)
    else:
        pass
else:
    print(url + ' not found')
    print(a.status)