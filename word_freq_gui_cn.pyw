#word_freq_gui.py
#coding=utf-8
'''
Author: Candlumine
Name(en): Word Frequency For English & Chinese
Name(cn): 中英文词频统计
Problem to-solve: symbol pick up doesn't work
'''

def contains_cn(ustr):
	"""
	判断unicode字符串中是否包含中文文字
	:param ustr:unicode字符串
	"""
	return any('\u4E00' <= char <= '\u9FFF' for char in ustr)
'''
def contains_gbk(ustr):
	"""
	判断unicode字符串中是否包含中日韩文字
	:param ustr:unicode字符串
	"""
	return any('\u2E80' <= char <= '\u9FFF' for char in ustr)
'''
def strip_symbol(ustr):
	"""
	删除unicode字符串中英文的标点符号数字
	:param ustr:unicode字符串
	"""
	import re
	symbol = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'+'！￥…（）【】、；：‘’“”《》，。？—'+'1234567890'
	return re.sub(symbol,' ',ustr)

def count_word_cn(filename):
	"""
	统计filename文本文件中中文词的出现频率
	:param filename:需要统计词频的文本文件
	"""
	import jieba,collections,re
	word_counter = collections.Counter()
	with open(filename,'r',encoding='utf-8') as f:
		seg_list = jieba.cut(f.read(), cut_all=False)
		for line in seg_list:
			line = strip_symbol(line)
			word_counter.update([word for word in re.split('\s+',line) if word !=''])
	return dict(word_counter)
	
def count_word_en(filename):
	"""
	统计filename文本文件中非中文词的出现频率
	:param filename:需要统计词频的文本文件
	"""
	import collections,re
	# 返回值为dict，会自动进行计数
	word_counter = collections.Counter()
	
	with open(filename,'r',encoding='utf-8') as f:
		for line in f:
            #过滤中文
			if contains_cn(line):
				continue
            # 去除英文标点符号
			line = strip_symbol(line)
			# 全部转为小写
			line = line.lower()
			word_counter.update([word for word in re.split('\s+',line) if word !=''])	
	return dict(word_counter)

def get_top():
	"""
	获取出现频率最高的topk个词
	"""
	filename = inpath
	mod = mode1
	topk = mode2_k.get()
	global datadict
	# 统计filename文本中的词频信息，保存到dict中
	if mod == '英文':
		word_dict = count_word_en(filename)
	elif mod == '中文':
		word_dict = count_word_cn(filename)
	# 对word_dict根据出现的词频进行降序排序
	topk_words = sorted(word_dict.items(),key=lambda x:x[1],reverse=True)
	datadict = topk_words[:topk]

def get_all():
	"""
	获取出现频率高于allk次的词
	"""
	filename = inpath
	mod = mode1
	allk = mode2_k.get()
	global datadict
	# 统计filename文本中的词频信息，保存到dict中
	if mod == '英文':
		word_dict = count_word_en(filename)
	elif mod == '中文':
		word_dict = count_word_cn(filename)
	# 对word_dict根据出现的词频进行降序排序
	allk_words = sorted(word_dict.items(),key=lambda x:x[1],reverse=True)
	allt = -1
	for k,v in allk_words:
		if v > allk:
			allt = allt+1
	datadict = allk_words[:allt]

def choosefile_in():
	"""
	选择文件
	"""
	import os
	from tkinter import filedialog,messagebox
	filename = filedialog.askopenfilename()
	global inpath
	if filename != '' and os.path.exists(filename):
		if_format = messagebox.askyesno("", "请确认"+filename+"是否为utf-8格式？")
		if if_format:
			inpath = filename
	in_info.config(text=inpath)
		

def choosefile_out():
	"""
	选择文件
	"""
	import os
	from tkinter import filedialog,messagebox
	filename = filedialog.askopenfilename()
	global outpath
	if filename != '':
		if os.path.exists(filename):
			if_cover = messagebox.askyesno("", "检测到存在"+filename+"，是否需要覆盖？")
			if if_cover:
				outpath = filename
		else:
			outpath = filename
	out_info.config(text=outpath)

def export_csv():
	"""
	导出csv文件
	"""
	import os,csv
	from tkinter import messagebox
	global datadict,outpath
	with open(outpath,'w',newline='') as csvfile:
		writer = csv.DictWriter(csvfile,fieldnames=['词语','频率'])
		writer.writeheader()
		for k,v in datadict:
			writer.writerow({'词语':k,'频率':v})
	messagebox.showinfo("","已经导出到{}".format(outpath))

if '__main__' == __name__:
	import tkinter as tk
	from tkinter import ttk
	# 实例化TK类，主窗口必须为.TK(),而其他子窗口为.Toplevel()
	root = tk.Tk()
	# 设置窗口标题
	root.title("中英文词频统计")
	# 源文件
	inpath = ''
	in_btn = tk.Button(root, text="文本文件：", command=choosefile_in)
	in_btn.grid(row=0,column=0)
	in_info = tk.Label(root,text=inpath)
	in_info.grid(row=0,column=1)
	# 导出文件
	outpath = ''
	out_btn = tk.Button(root, text="导出文件：", command=choosefile_out)
	out_btn.grid(row=1,column=0)
	out_info = tk.Label(root,text=outpath)
	out_info.grid(row=1,column=1)
	# 模式选择
	mode_info = tk.Label(root,text='模式:')
	mode_info.grid(row=3,column=0)
	mode1_chk = tk.StringVar()
	mode1_btn = ttk.Combobox(root, textvariable=mode1_chk, state='readonly')
	mode1_btn.grid(row=3,column=1)
	mode1_btn['values'] = ('英文', '中文')
	mode1_btn.current(0)
	mode1 = mode1_btn.get()
	mode2_chk = tk.StringVar()
	mode2_btn = ttk.Combobox(root, textvariable=mode2_chk, state='readonly')
	mode2_btn.grid(row=4,column=0)
	mode2_btn['values'] = ("排名超过", "次数高于")
	mode2_btn.current(0)
	mode2 = mode2_btn.get()
	mode2_k = tk.StringVar()
	mode2_k.set('')
	mode2_k0 = tk.Entry(root, textvariable=mode2_k)
	mode2_k0.grid(row=4,column=1)
	# 导出按钮
	run_btn = tk.Button(root, text='运行', command=export_csv).grid(row=5,column=1)
	# 启动界面
	root.mainloop()




