#这是一个nester.py模块，提供一个print_lol()函数，这个函数的作用是打印列表,其中可能是
#多重的嵌套列表

def print_lol(the_list):
    #这个函数取一个位置参数，名为"the_list"，这可以是任何python列表。所指定的列表中的
    #每个数据项都会一一的输出到屏幕上，各数据项各占一行
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)
