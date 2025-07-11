import re
import json
from utils.miner_http_tools import config_miner_work_mode
from concurrent.futures import ThreadPoolExecutor, as_completed


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


def change_work_mode(df, mode):
    task_ip_list = []
    for index, row in df.iterrows():
        ip = row['IP']
        config = {
            "bitmain-fan-ctrl": False,
            "bitmain-fan-pwm": "100",
            "bitmain-hashrate-percent": "100",
            "miner-mode": mode,

            "pools": [
                {"url": f"stratum+tcp://{row['矿池1']}", "user": row["矿机名1"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池2']}", "user": row["矿机名2"], "pass": "root"},
                {"url": f"stratum+tcp://{row['矿池3']}", "user": row["矿机名3"], "pass": "root"},
            ]
        }
        #     print(json.dumps(config, ensure_ascii=False, indent=2))
        task_ip_list.append([ip, config])
    results = []  # 用于保存所有结果
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(config_miner_work_mode, task) for task in task_ip_list]

        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(["未知IP", f"执行失败: {e}"])

    return results
