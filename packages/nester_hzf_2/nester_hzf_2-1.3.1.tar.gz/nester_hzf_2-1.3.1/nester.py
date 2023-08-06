import sys
"""这是"nester.py"模块，提供了一个名为print_lol()的函数
用来打印列表，其中包含或包含嵌套列表"""
def print_lol(the_list, indent=False, tab=0, store=sys.stdout):
        for each in the_list:
                if isinstance(each, list):
                        print_lol(each, indent, tab+1, store)
                else:
                        if indent:
                                for tab_stop in range(tab):
                                        print("\t", end='', file=store)
                        print(each, file=store)

def new(name):
        print(name)
"""用来测试是不是可以用"""
