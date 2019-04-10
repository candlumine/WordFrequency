#word_freq.py
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

def get_top(filename,mod='-en',topk=10):
	"""
	获取出现频率最高的topk个词
	:param filename:需要统计词频的文本文件
	:param topk:需要返回的出现频率最高的前topk个词，默认为10个
	"""
	# 统计filename文本中的词频信息，保存到dict中
	if mod == '-en':
		word_dict = count_word_en(filename)
	elif mod == '-cn':
		word_dict = count_word_cn(filename)
	# 对word_dict根据出现的词频进行降序排序
	topk_words = sorted(word_dict.items(),key=lambda x:x[1],reverse=True)
	return topk_words[:topk]

def get_all(filename,mod='-en',allk=1):
	"""
	获取出现频率高于allk次的词
	:param filename:需要统计词频的文本文件
	:param allk:需要返回的词出现频率不能小于allk，默认为1次
	"""
	# 统计filename文本中的词频信息，保存到dict中
	if mod == '-en':
		word_dict = count_word_en(filename)
	elif mod == '-cn':
		word_dict = count_word_cn(filename)
	# 对word_dict根据出现的词频进行降序排序
	allk_words = sorted(word_dict.items(),key=lambda x:x[1],reverse=True)
	allt = -1
	for k,v in allk_words:
		if v > allk:
			allt = allt+1
	return allk_words[:allt]

def export_csv(datadict):
	"""
	导出csv文件
	:param datadict:数据数组
	"""
	import os,csv
	path = os.getcwd()+"\\export.csv"
	if os.path.exists(path):
		coverif = input("Will you cover the export.csv exist?(Y/N)")
		if coverif != 'Y' and coverif != 'y':
			path = os.getcwd()+"\\"+input("What name is the exported csvfile：")+".csv"
	with open(path,'w',newline='') as csvfile:
		writer = csv.DictWriter(csvfile,fieldnames=['word','time(s)'])
		writer.writeheader()
		for k,v in datadict:
			writer.writerow({'word':k,'time(s)':v})
	print("Successfully exported to {}".format(path))

if '__main__' == __name__:
	import sys
	if len(sys.argv) == 5:
		if sys.argv[1] == '-topk':
			dict_words = get_top(sys.argv[3],sys.argv[2],int(sys.argv[4]))
			export_csv(dict_words)
			sys.exit(0)
		elif sys.argv[1] == '-allk':
			dict_words = get_all(sys.argv[3],sys.argv[2],int(sys.argv[4]))
			export_csv(dict_words)
			sys.exit(0)
	print('Usage: {} -topk -cn/en filename topk'.format(sys.argv[0]),file=sys.stderr)
	print('       {} -allk -cn/en filename allk'.format(sys.argv[0]),file=sys.stderr)
		




