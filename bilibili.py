# -*- coding: UTF-8 -*-
import tkinter as tk
import time
import requests
import tkinter.messagebox
from tkinter.filedialog import askdirectory
from bs4 import BeautifulSoup
from urllib import parse
import json
import os
import _thread
import threading
   
def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()

class OhMy(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.window = tk.Tk()
        self.path = tk.StringVar()
        self.paths = ""
        self.urls = tk.StringVar()
        self.canGet = False;
        self.pageNum = 0
        self.mid = ""
        self.downLoadArr = [];
        self.label = tk.StringVar()
        self.tips = tk.StringVar()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        }

    # 开始
    def start(self):
        self.initWindow()

   # 初始化窗口
    def initWindow(self):

        # 窗口设置
        self.window.title("哔哩哔哩（BY：狗敦A季）")
        self.window.geometry('405x200')
            
        frame1 = tk.LabelFrame(self.window, width=395, height=150, text='1、输入UP主主页地址')
        frame1.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        tk.Label(frame1, text="UP主主页地址:").grid(row=0, column=0)
        tk.Entry(frame1, textvariable = self.urls, width = 32).grid(row=0, column=1)
        tk.Button(frame1, text="连接测试", command = self.test).grid(row=0, column=2)
        self.urls.set("https://space.bilibili.com/176037767/")

         # 目录选择
        frame1 = tk.LabelFrame(self.window, width=395, height=100, text='2、选择目录')
        frame1.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        tk.Label(frame1, text="选择存放目录:").grid(row=0, column=0)
        tk.Entry(frame1, textvariable=self.path, width = 32).grid(row=0, column=1)
        tk.Button(frame1, text="路径选择", command = self.selectPath).grid(row=0, column=2)

        label = tk.Label(self.window,textvariable=self.label,width=20,height=0)
        label.place(x=180, y=165)

        tips = tk.Label(self.window,textvariable=self.tips,width=20,height=0)
        tips.place(x=5, y=165)
        
        #抓取数据
        gets = tk.Button(self.window,text='下载',width=6,height=0,command=lambda :thread_it(self.startGet))
        gets.place(x=328, y=160)

        self.window.mainloop()
    
    def startGet(self):
        url = self.urls.get()
        paths = self.paths
        pageNum = self.pageNum

        if self.canGet:
            if paths != "":
                for index in range(1, pageNum+1):
                    urls = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+self.mid+"&pagesize=30&tid=0&page=" +str(index) + "&keyword=&order=pubdate"
                    doc = requests.get(url= urls,headers = self.headers, timeout=6)
                    docs = doc.text
                    jsonData = json.loads(docs)
                    vlist = jsonData["data"]["vlist"]
                    for ind, vli in enumerate(vlist):
                        aid = vli["aid"]
                        self.downLoadArr.append(aid)
                self.downLoad()
                
            else:
                tkinter.messagebox.showwarning('提示','选择路径！')
        else:
            tkinter.messagebox.showwarning('提示','连接测试失败！')

    def downLoad(self):
        paths = self.paths
        _self = self;
        for ind, aid in enumerate(self.downLoadArr): 
            aid =  "https://www.bilibili.com/video/av" + str(aid);
            print("开始下载" + str(aid))
            ind = ind + 1
            _self.tips.set("正在下载第"+str(ind)+"条视频")
            paths = paths.replace("/","\\")
            os.system('you-get -o {paths} {url}'.format( url=aid,paths=paths))

    def getPageNum(self):
        mid = self.urls.get();
        mid = mid.replace("https://space.bilibili.com/","")
        mid = mid.replace("/","")
        url = "https://space.bilibili.com/ajax/member/getSubmitVideos?mid="+mid+"&pagesize=30&tid=0&page=1&keyword=&order=pubdate"
        
        doc = requests.get(url= url,headers = self.headers, timeout=6)
        docs = doc.text
        num = json.loads(docs)
        self.pageNum = int(num["data"]["pages"])
        count = num["data"]["count"]
        self.mid = mid
        self.label.set("UP主共有"+str(count)+"条视频")

    def test(self):
        try:
            url = self.urls.get()
            doc = requests.get(url= url,headers = self.headers, timeout=6)
            docs = doc.text
            soup = BeautifulSoup(docs, 'html.parser')
            title = soup.select("title")[0].string
            if '个人空间' in title:
                tkinter.messagebox.showinfo('提示','成功！')
                self.canGet = True
                self.getPageNum()
            else:
                tkinter.messagebox.showerror('提示','失败！')
                self.canGet = True
        except:
            tkinter.messagebox.showerror('提示','失败！')
            self.canGet = True

    # 选择文件存放位置
    def selectPath(self):
        path_ = askdirectory()
        self.path.set(path_)
        self.paths = path_

ohmy = OhMy();
ohmy.start()
