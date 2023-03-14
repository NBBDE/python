import requests
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor
#每日一文网址： https://meiriyiwen.com/

class Mryw():
    def __init__(self):
        self.url="https://meiriyiwen.com/"
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"}
        for i in range(2000):
            with ThreadPoolExecutor(500)as t:
                t.submit(self.run)
    def visit(self,url):
        res=requests.get(url,headers=self.headers)
        return res
    def screen(self,resp):
        html=etree.HTML(resp.text)
        title=html.xpath("//div[@id='article_show']/h1/text()")[0]
        author=html.xpath("//p[@class='article_author']/span/text()")[0]
        main_body=html.xpath("//div[@class='article_text']/p/text()")
        return title,author,main_body
    def save(self,filename,keep):
        with open("E:/result/download/"+filename+".txt",'w',encoding="utf-8")as f:
            for i in keep:
                f.write('   '+i+"\n")
        print("--- 《{}》 -----download successfully-----".format(filename))
        return
        
    def run(self):
        #访问页面
        resp=self.visit(self.url)
        #筛选内容
        title,author,main_body=self.screen(resp)
        #保存内容
        self.save(re.sub("[?!，。、：\'\"]","_",title+"_"+author),main_body)
            
p=Mryw()
