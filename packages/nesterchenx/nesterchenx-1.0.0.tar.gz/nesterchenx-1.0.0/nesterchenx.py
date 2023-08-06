"""这个是nester.py模块，提供了一个名为print_lol()的函数"""
def print_lol(the_list):
    """这个函数取名为"the_list"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
