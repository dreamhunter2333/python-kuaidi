# -*- coding: utf-8 -*-

__author__ = 'jinmu333'

from tkinter import *
from multiprocessing import Process
import tkinter.messagebox as messagebox
import urllib,hashlib
import random
import requests,sys
import requests


def GetComName(comCode):
	if comCode=='shentong':
		return '申通快递'
	elif comCode=='zhontong':
		return '中通快递'
	elif comCode=='ems':
		return 'EMS'
	elif comCode=='huitongkuaidi':
		return '汇通快运'
	else:
		return comCode

# 函数: 取状态文本
def GetStateText(num):
	if num==0:
		return '运输中'
	elif num==1:
		return '揽件'
	elif num==2:
		return '疑难'
	elif num==3:
		return '已签收'
	elif num==4:
		return '退回签收'
	elif num==5:
		return '派送中'
	elif num==6:
		return '退回中'

root = Tk()
root.title("快递单号查询 by jinmu333")
root.geometry('400x600')                 #是x 不是*
root.resizable(width=True, height=True) #宽不可变, 高可变,默认为True
l = Label(root, text="反馈请邮件至idl253841@gmial.com", font=("Arial", 9), width=20)
l.pack(side=BOTTOM)
t = Text()
t.pack()
t.insert('1.0', "此处显示历史查询记录\n")
var = StringVar()
e = Entry(root, textvariable = var)
var.set('请在下方输入')
e.pack()
class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.nameInput = Entry(self)
		self.nameInput.bind('<Key-Return>',self. hello)
		self.nameInput.pack()
		self.alertButton = Button(self, text='查询物流', command=self.hello,width = 20,height = 2,bd = 2)
		self.alertButton.pack()
	
	
	def hello(self,event):
		s = self.nameInput.get() or '请输入查询内容'

		var.set('请在下方键入快递单号')
		t.insert('1.0', "-------------------------------------------------------\n")

		p = {}
		p['text'] = s
		autoComNum = requests.get("http://www.kuaidi100.com/autonumber/autoComNum", params=p)
		com = autoComNum.json()


		if com['auto'] == []:
			print("这是一个错误的运单编号!")
			t.insert('1.0', "---------这是一个错误的运单编号-----------\n")
		else:
			print("\n---------------- 承运公司 ------------------\n")
			i=0
			for this in com['auto']:
				i = i + 1
			#	print( str(i) + ". " + GetComName(this['comCode']) + "\n")

			num = 1
			print("\n---------------- 正在查询, 请稍等... ------------------\n")

			data = {}
			data['type'] = com['auto'][int(num)-1]['comCode']
			data['postid'] =  p['text']
			data['valicode'] = ''
			data['id'] = 1
			data['temp'] = '0.14881871496191512'
			query = requests.get("http://www.kuaidi100.com/query", params=data)
			res = query.json()

			print("\n运单编号 --> " + res['nu'])
			print("\n承运公司 --> " + GetComName(res['com']))
			print("\n当前状态 --> " + GetStateText(int(res['state'])))
			print("\n---------------- 跟踪信息 ------------------\n")
			for this in res['data']:
				print(this['time'] + "\t" + this['context'] + "\n")
				t.insert('1.0', this['time'] + "\t" + this['context'] + "\n")
			t.insert('1.0', "当前状态 -->  %s\n" %GetStateText(int(res['state'])))
			t.insert('1.0', "承运公司 -->  %s\n" %GetComName(res['com']))
			t.insert('1.0', "运单编号 -->  %s\n" %res['nu'])
			t.insert('1.0', "------------------正在查询, 请稍等--------------------\n")
app = Application()

# 主消息循环:
app.mainloop()