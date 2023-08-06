"""这是"nester.py"模块，提供了一个名为print_lol()的函数
用来打印列表，其中包含或包含嵌套列表"""
def print_lol(the_list, tab=0):
        for each in the_list:
                if isinstance(each, list):
                        print_lol(each, tab+1)
                else:
                        for tab_stop in range(tab):
                                print("\t", end='')
                        print(each)

def new(name):
        print(name)
"""用来测试是不是可以用"""
