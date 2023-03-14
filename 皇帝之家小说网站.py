from tqdm import tqdm
import time
import requests
from lxml import etree
import re
import os
from concurrent.futures import ThreadPoolExecutor,as_completed

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"}
filepath="E:/result/download/"
title=""
undown=[]

def getbook(url):
    global headers
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    book_link=html.xpath("//div[@class='online-read']/a/@href")[0]
    return "https://www.huangdizhijia.com"+book_link

def getchapterlist(url):
    global headers,filepath,title
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    chapters=html.xpath("//div[@class='tagCol']/ul/li/a")
    book_name=html.xpath("//div[@id='content']/h1/text()")[0]
    title=book_name
    filepath+=re.sub("[\s\/]","",book_name)
    if not os.path.isdir(filepath):
        os.mkdir(filepath)
    chapterlist=[]
    seq=1001
    for i in chapters:
        chapter_name=str(seq)+i.text
        seq+=1
        chapter_url="https://www.huangdizhijia.com"+i.get("href")
        chapterlist.append([chapter_name,chapter_url])
    return chapterlist

def download(url,name):
    global headers,filepath
    res=requests.get(url,headers=headers)
    html=etree.HTML(res.text)
    main_body=html.xpath("//div[@class='tagCol']/p/text()")
    with open(filepath+"/"+name+".txt","w")as f:
        for i in main_body:
            f.write("   "+i+"\n")
    return

def check():
    global chapter_list,undown,filepath
    print("\n---完整性检查---\n")
    for i in chapter_list:
        if not os.path.exists(filepath+"/"+i[0]+".txt"):
            undown.append(i)
    if len(undown)!=0:
        print("\n---有{}章待下载---\n".format(len(undown)))
    else:
        print("\n---已全部加载完毕---\n")
    return
    

def merge():
    global filepath,title
    file_list=os.listdir(filepath)
    with open(filepath+"/00"+title+".txt","w+")as f:
        for i in tqdm(file_list,desc="\n---合并中---"):
            with open(filepath+"/"+i,"r")as r:
                f.write(r.read())
    for i in file_list:
        os.remove(filepath+"/"+i)
    print("---合并完成---")

    
url=input("---输入皇帝之家网站小说简介页的链接：\n")


book_link=getbook(url)
chapter_list=getchapterlist(book_link)
while True:
    check()
    if len(undown)==0:
        break
    with ThreadPoolExecutor(1000)as t:
        com=[]
        for i in tqdm(undown,desc="\n---《"+title+"》加载中---"):
            com.append(t.submit(download,i[1],i[0]))
        with tqdm(total=len(com),desc="\n---《"+title+"》下载中---")as xz:
            for i in as_completed(com):
                xz.update(1)
    undown.clear()

print("---《{}》---下载完成---\n---共计{}章---".format(title,len(chapter_list)))
merge()

