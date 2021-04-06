import os
import sys

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

headers = {
    'Authorization': 'Bearer eyJrIjoiZUJhMDdaZE4ya1FyR0JDM2owZGJHck5ISHVRa2ZDNksiLCJuIjoiYWRtaW4iLCJpZCI6MX0='
}

node_info_file = os.path.join(PATH, 'config/性能周报.xlsx')
