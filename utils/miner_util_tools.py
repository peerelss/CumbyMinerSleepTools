import re
import json


def parse_time_to_seconds(s):
    # 例如：'20小时 14分 6秒'
    h, m, sec = 0, 0, 0
    match_h = re.search(r"(\d+)\s*小时", s)
    match_m = re.search(r"(\d+)\s*分", s)
    match_s = re.search(r"(\d+)\s*秒", s)
    if match_h:
        h = int(match_h.group(1))
    if match_m:
        m = int(match_m.group(1))
    if match_s:
        sec = int(match_s.group(1))
    return h * 3600 + m * 60 + sec


def sleep_all_miner(df):
    for index, row in df.iterrows():
        ip = row['IP']
        config = {
            "bitmain-fan-ctrl": False,
            "bitmain-fan-pwm": "100",
            "miner-mode": 1,
            "pools": [
                {"url": f"stratum+tcp://{row['矿池1']}", "user": row["矿机名1"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池2']}", "user": row["矿机名2"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池3']}", "user": row["矿机名3"], "pass": "root"},
            ]
        }
        print(json.dumps(config, ensure_ascii=False, indent=2))


def change_miner_work_mode(task_ips, mode):
    for ip in task_ips:
        ip[1]['bitmain-fan-ctrl'] = False
        ip[1]['bitmain-fan-pwm'] = "100"
        ip[1]['miner-mode'] = mode
        print(ip[0], json.dumps(ip[1], ensure_ascii=False, indent=2))


def wake_up_all_miner(df):
    task_ip_list = []
    for index, row in df.iterrows():
        ip = row['IP']
        config = {
            "pools": [
                {"url": f"stratum+tcp://{row['矿池1']}", "user": row["矿机名1"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池2']}", "user": row["矿机名2"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池3']}", "user": row["矿机名3"], "pass": "root"},
            ]
        }
        #     print(json.dumps(config, ensure_ascii=False, indent=2))
        task_ip_list.append([ip, config])
    change_miner_work_mode(task_ip_list, 0)
