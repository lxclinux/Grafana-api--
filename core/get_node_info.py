import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)
from core import get_node_list, get_node_cpu, get_node_mem, write_excel


def get_node_info():
    # get node list
    up_node_list, down_node_list = get_node_list.getTargetsStatus()
    # get node cpu_info
    node_dict_cpu = get_node_cpu.get_node_dict(up_node_list)
    # #获取内存
    node_dict = get_node_mem.get_mem(node_dict_cpu)
    # 写入excel
    write_excel.write_excel(node_dict,down_node_list)
