from bs4 import BeautifulSoup, SoupStrainer
import requests

import re
#функция чистки строки
def delEl(a):
    a= a.replace(" ",'')
    flag=-1
    i=0
    a= a.replace("\n",'')
    a=a.replace("'","")
    a= a.replace(" ",'')
    a= a.replace("'",'')
    a= a.replace('"','')
    a= a.replace(" ",'')
    a= a.replace(',','')
    a= a.replace(" ",'')
    
    while (i<len(a)-1):
        if a[i] in "<>=;:~!@#$^&*()[]":
            flag=i
            break
        i+=1
    if flag!=-1:
        a=a[0:flag]
    return (a)
#функция получения адреса в на код установки
def getUrl(a):
    a=a.lower()
    URL = 'https://pypi.org/pypi/'
    #a='flask'
    URL=URL+a+'/'
    if a[-1] in "0123456789":
        a=a[0:-1]
    page = requests.get(URL)    
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    result=''
    for link in soup.find_all('a'):
        if link!="NoneType":
            if (link.get('href')!=None):
                if "https://github.com/" in (link.get('href')):
                    help=link.get('href')
                    helpInd=len(help)-1
                    res=help.rfind(a)
                    if res==helpInd-(len(a)-1) or (res==helpInd-(len(a)) and help[len(help)-1]=='/'):
                        result =(link.get('href'))
    osnova=result.replace("https://github.com/","")
    if result!='':
        URL=result
        page = requests.get(URL)    
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')

        for link in soup.find_all('a'):
            if link!="NoneType":
                if (link.get('href')!=None):
                    if "setup.py" in (link.get('href')):
                        help=link.get('href')
                        helpInd=len(help)-1
                        res=help.rfind(a)
                        result=help

        example="https://raw.githubusercontent.com"
        if (osnova[len(osnova)-1]!='/'):
            osnova+='/'
        result=result.replace("blob/","")
        result=example+result
        return(result)
def func_help(library):
    url=getUrl(library)#получаем ссылку на файл с кодом зависимостей
    if url!=None  and url!='':
        mas = getmas(url)#получаем массив зависящих элементов
        if mas!=[''] and mas!=None and mas!=-1:
            resultar=''
            print(outs(library,mas,resultar))

def getmas(url):
    page = requests.get(url)    
    html = page.text
    f = open('test.txt', 'w', encoding="utf-8")
    f.write(html)
    f.close()

    file1 = open("test.txt", "r")

    beBegin=False   
    beEnd=False
    res=''
    while True:
        line = file1.readline()
        if not line:
            break
        
        elif 'install_requires=["' in line :
            b=line.split("=")
            line=' '.join(b[1])
            line= line.replace(" ",'')
            b=line.split(":")
            line=' '.join(b[0])
            line= line.replace(" ",'')
            line= line.replace('[','')
            line = re.sub(r'\'', '',line)
            line= line.replace(" ",'')
            line= line.replace("\n",'')
            line= line.replace('"','')
            line= line.replace(",",'')
            line= line.replace("'",'')
            help=line.split('>')
            line=' '.join(help[0])
            line= line.replace(" ",'')
            b=line.split(";")
            line=' '.join(b[0])
            line= line.replace(" ",'')
            res+=line+","
            break
        elif "install_requires=[" in line or "install_requires = [" in line or "requires = [" in line:
            beBegin=True
        else:
            if (beBegin==True and "]" in line):
                beBegin=False
                break
            if (beBegin==True):
                line = delEl(line)
                line= line.replace(" ",'')
                line= line.replace("\n",'')
                line= line.replace('"','')
                line= line.replace("'",'')
                res+=line+","
    if res=='': return -1
    while res[-1]==',':
        res=res[0:-1]
    a=res.split(",")
    file1.close
    return a

#выполнение основной логики программы
def outs(consnanta1, json1,res):
    for i in json1:
        constanta=consnanta1
        if "-"  in constanta:  
            constanta='"' +constanta+'"'  #редактирование для ввода на сайт
        always=' -> '
        if "-"  in i:  
            i='"' +i+'"' #редактирование для ввода на сайт
        func_help(i)
        res=res+constanta+always+i+';'
    return res


#главная функция с первоначальным вводом бибилиотеки
def main():
    library=input()#вводим название библиотек
    url=getUrl(library)#получаем ссылку на файл с кодом зависимостей
    if url!=None and url!='':
        mas = getmas(url)#получаем массив зависящих элементов
        if mas!=[''] and mas!=None and mas!=-1:
            resultMain=''
            print(outs(library,mas,resultMain))

main()