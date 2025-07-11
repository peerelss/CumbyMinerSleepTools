import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'http://10.102.1.143',
    'Authorization': 'Digest username="root", realm="antMiner Configuration", nonce="68695f7e82979e8636957c0788c7cb19", uri="/cgi-bin/set_miner_conf.cgi", response="a954bf4eff410b6eb0ffb26f4a866c66", qop=auth, nc=00000041, cnonce="0664436edfd7834f"',
    'Connection': 'keep-alive',
    'Referer': 'http://10.102.1.143/',
    'Priority': 'u=0',
}


def config_miner_work_mode(task_ip):
    ip = task_ip[0]
    data = json.dumps(task_ip[1])
    print(data)
    # data = '{"bitmain-fan-ctrl":false,"bitmain-fan-pwm":"100","bitmain-hashrate-percent":"100","miner-mode":1,"pools":[{"url":"stratum+tcp://ss.antpool.com:3333","user":"AMTX22","pass":"root"},{"url":"stratum+tcp://ss.antpool.com:443","user":"AMTX22","pass":"root"},{"url":"stratum+tcp://btc.f2pool.com:1314","user":"amtx22f2pool","pass":"root"}]}'

    try:
        response = requests.post(f'http://{ip}/cgi-bin/set_miner_conf.cgi', headers=headers, data=data )
        result = response.json()
        if result['stats'] == 'success':
            # 执行成功
            if task_ip[1]['miner-mode'] == 1:
                return [ip, '休眠成功']
            else:
                return [ip, '唤醒成功']
        return [ip, '请求失败']
    except Exception as e:
        print(ip, str(e))
        return [ip, str(e)]
