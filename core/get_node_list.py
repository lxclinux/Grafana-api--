import requests


def getTargetsStatus():
    up_node_list = []
    down_node_List = []
    url = 'http://172.31.2.37:8090/api/v1/targets'

    response = requests.request('GET', url)
    if response.status_code == 200:
        targets = response.json()['data']['activeTargets']
        for target in targets:
            if target['health'] == 'up':
                up_node_list.append(target['discoveredLabels']['__address__'].split(':')[0])
            else:
                down_node_List.append(target['labels']['instance'].split(':')[0])
    print(down_node_List)
    return up_node_list, down_node_List