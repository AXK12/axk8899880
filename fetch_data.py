#!/usr/bin/env python3
"""彩票开奖数据抓取脚本 - GitHub Actions 自动运行"""
import json, os, urllib.request, sys
from datetime import datetime

def fetch_txt(url, encoding='gb2312'):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=30)
    raw = resp.read()
    try:
        text = raw.decode(encoding)
    except:
        text = raw.decode('utf-8', errors='replace')
    return text

def parse_ssq(text):
    """解析双色球数据：期号 日期 红1红2...红6 蓝 其他..."""
    lines = text.strip().split('\n')
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 9: continue
        try:
            period = parts[0]
            date = parts[1]
            reds = [int(p) for p in parts[2:8]]
            blue = int(parts[8])
            data.append({'period':period, 'date':date, 'reds':reds, 'blue':blue})
        except: continue
    return data

def parse_dlt(text):
    """解析大乐透数据：期号 日期 前1-5 后1-2 其他..."""
    lines = text.strip().split('\n')
    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) < 7: continue
        try:
            period = parts[0]
            date = parts[1]
            fronts = [int(p) for p in parts[2:7]]
            backs = [int(p) for p in parts[7:9]]
            data.append({'period':period, 'date':date, 'fronts':fronts, 'backs':backs})
        except: continue
    return data

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # 双色球
    print('Fetching SSQ...')
    ssq_text = fetch_txt('https://data.17500.cn/ssq_asc.txt')
    ssq_data = parse_ssq(ssq_text)
    out = {
        'version': 2,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total': len(ssq_data),
        'data': ssq_data
    }
    with open(os.path.join(output_dir, 'ssq.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print(f'  {len(ssq_data)} 期')
    
    # 大乐透
    print('Fetching DLT...')
    dlt_text = fetch_txt('https://data.17500.cn/dlt2_asc.txt')
    dlt_data = parse_dlt(dlt_text)
    out = {
        'version': 2,
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total': len(dlt_data),
        'data': dlt_data
    }
    with open(os.path.join(output_dir, 'dlt.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print(f'  {len(dlt_data)} 期')
    print('Done!')

if __name__ == '__main__':
    main()
