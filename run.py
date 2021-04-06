import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH)

from core.get_node_info import get_node_info



if __name__ == '__main__':
    get_node_info()
