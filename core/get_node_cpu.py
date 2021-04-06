import requests
import time
import sys
import os

CONFIG_PAHT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CONFIG_PAHT)

from settings import config




def get_avg_cpu(up_node_list, node_cpu_dict):
    start_time = str(int(time.time() - 43200))
    end_time = str(int(time.time()))
    node_cpu_dict[up_node_list] = {}

    one_ip, two_ip, three_ip, four_ip = up_node_list.split('.')
    url_ip = one_ip + "%5C%5C." + two_ip + "%5C%5C." + three_ip + "%5C%5C." + four_ip
    url = 'http://172.31.2.37:3000/api/datasources/proxy/1/api/v1/query_range?query=(1%20-%20avg(rate(node_cpu_seconds_total%7Binstance%3D~%22('+ url_ip +'%3A8100%7C'+ url_ip +'%3A9100)%22%2Cmode%3D%22idle%22%7D%5B2m%5D))%20by%20(instance))*100&start='+ start_time +'&end='+ end_time +'&step=300'
    node_cpu_list = []
    response = requests.request('GET', url=url, headers=config.headers)
    if response.status_code == 200:
        try:
            all_time_cpu = response.json()["data"]["result"][0]["values"]
            for time_cpu in all_time_cpu:
                node_cpu_list.append(float('%.2f' % float(time_cpu[1])))

            node_cpu_dict[up_node_list]['max_used_cpu'] = str(max(node_cpu_list)) + "%"
            node_cpu_dict[up_node_list]['min_used_cpu'] = str(min(node_cpu_list)) + "%"
            node_cpu_dict[up_node_list]['avg_used_cpu'] = str(
                float("%.3f" % (sum(node_cpu_list) / len(node_cpu_list)))) + "%"

        except IndexError:
            #print(url)
            node_cpu_dict[up_node_list]['max_used_cpu'] = 'NULL'
            node_cpu_dict[up_node_list]['min_used_cpu'] = 'NULL'
            node_cpu_dict[up_node_list]['avg_used_cpu'] = 'NULL'


        return node_cpu_dict


def get_node_dict(up_node_list):
    node_cpu_avg = {}
    # print('在线服务器%s个 :  %s' % (len(uplist), uplist))
    # print('掉线服务器%s个 :  %s' % (len(downlist), downlist))
    for up_node_ip in up_node_list:
        get_avg_cpu(up_node_ip, node_cpu_avg)
    return node_cpu_avg

