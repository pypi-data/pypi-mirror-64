
'''模块名：PrintListGS
这个模块提供一个print_list函数，功能是打印列表每个元素，列表可以嵌套
但该模块还是能输出每个原始； '''

def print_list_glws(a):

	''' 该函数判断每个元素是不是列表，
	不是，直接输出，是，递归调用自己'''

	for each_items in a:
		if isinstance(each_items,list):
			print_list_glws(each_items)
		else:
			print(each_items,end ='\t')


