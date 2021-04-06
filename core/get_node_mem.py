import requests
import time
import os
import sys

CONFIG_PAHT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CONFIG_PAHT)

from settings import config


class Get_mem(object):
    def __init__(self, up_node_ip, headers):
        self.core_num = ''
        self.total_mem = ''
        self.headers = headers
        self.up_node_ip = up_node_ip
        self.starttime = str(int(time.time() - 43200))
        self.now_time = str(int(time.time()))

    def res(self, port):
        used_mem = []
        one, two, three, four = self.up_node_ip.split('.')
        ip = one + "%5C%5C." + two + "%5C%5C." + three + "%5C%5C." + four
        urls = "http://172.31.2.37:3000/api/datasources/proxy/1/api/v1/query_range?query=node_memory_MemTotal_bytes%7Binstance%3D~%22" + ip + "%3A" + port +"%22%7D%20-%20node_memory_MemAvailable_bytes%7Binstance%3D~%22" + ip + "%3A" + port + "%22%7D&start=" + self.starttime + "&end=" + self.now_time + "&step=120"
        response = requests.request('GET', url=urls, headers=self.headers)
        if response.status_code == 200:
            try:
                all_time_mem = response.json()["data"]["result"][0]["values"]
                for time_cpu in all_time_mem:
                    used_mem.append(float("%.2f" % ((int(time_cpu[1])) / 1024 / 1024 / 1024)))
            except IndexError:
                pass
        return used_mem

    def get_used_mem(self):
        for port in ['8100', '9100']:
            used_mem = self.res(port)
            if len(used_mem) != 0:
                return used_mem

    def get_total_mem(self):
        one, two, three, four = self.up_node_ip.split('.')
        ip = one + "%5C%5C." + two + "%5C%5C." + three + "%5C%5C." + four
        urls_8100 = "http://172.31.2.37:3000/api/datasources/proxy/1/api/v1/query_range?query=node_memory_MemTotal_bytes%7Binstance%3D~%22" + ip + "%3A8100%22%7D&start=" + self.starttime + "&end=" + self.now_time + "&step=300"
        urls_9100 = "http://172.31.2.37:3000/api/datasources/proxy/1/api/v1/query_range?query=node_memory_MemTotal_bytes%7Binstance%3D~%22" + ip + "%3A9100%22%7D&start=" + self.starttime + "&end=" + self.now_time + "&step=300"
        try:
            response = requests.request('GET', url=urls_8100, headers=self.headers)
            total_mem = response.json()["data"]["result"][0]["values"][1][1]
            self.total_mem = float("%.2f" % (int(total_mem) / 1024 / 1024 / 1024))
        except IndexError:
            response = requests.request('GET', url=urls_9100, headers=self.headers)
            total_mem = response.json()["data"]["result"][0]["values"][1][1]
            self.total_mem = float("%.2f" % (int(total_mem) / 1024 / 1024 / 1024))
        return self.total_mem

    def get_core_self(self, port):
        heard = 'http://172.31.2.37:8090' + '/api/v1/query?query='
        expr = 'count(node_cpu_seconds_total{instance="' + self.up_node_ip + ':' + port + '",mode="system"})'
        urls = heard + expr
        response = requests.request('GET', url=urls, headers=self.headers)
        if response.status_code == 200:
            try:
                self.core_num = response.json()["data"]["result"][0]["value"][1]
            except IndexError:
                self.core_num = 'NULL'
        return self.core_num

    def get_core(self):
        for port in ['8100', '9100']:
            if self.get_core_self(port) != 'NULL':
                return self.get_core_self(port)


def get_mem(node_dict):
    for node_ip in node_dict:
        mem_info = Get_mem(node_ip, config.headers)

        # get core num
        node_dict[node_ip]['core_num'] = str(mem_info.get_core())

        # get total_mem
        node_dict[node_ip]['total_mem'] = str(mem_info.get_total_mem())

        # get max_mem  min_mem
        used_mem = mem_info.get_used_mem()
        try:
            node_dict[node_ip]['max_used_mem'] = str(max(used_mem)) + 'G'
            node_dict[node_ip]['min_used_mem'] = str(min(used_mem)) + 'G'
            node_dict[node_ip]['avg_used_mem'] = str(float("%.2f" % (sum(used_mem) / len(used_mem)))) + 'G'
        except:
            node_dict[node_ip]['max_used_mem'] = '0'
            node_dict[node_ip]['min_used_mem'] = '0'
            node_dict[node_ip]['avg_used_mem'] = '0'
    return node_dict
