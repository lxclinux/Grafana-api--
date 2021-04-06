import requests
headers = {
    'Authorization': 'Bearer eyJrIjoiZUJhMDdaZE4ya1FyR0JDM2owZGJHck5ISHVRa2ZDNksiLCJuIjoiYWRtaW4iLCJpZCI6MX0='
}



def get_core():
    heard = 'http://172.31.2.37:8090' + '/api/v1/query?query='
    expr = 'count(node_cpu_seconds_total{instance="' + '172.20.47.46' + ':8100",mode="system"})'
    urls = heard + expr
    print(urls)
    response = requests.request('GET', url=urls, headers=headers)
    if response.status_code == 200:
        try:
            core_num = response.json()["data"]["result"][0]["value"][1]
        except IndexError:
            core_num = "NULL"
    print(core_num)



get_core()