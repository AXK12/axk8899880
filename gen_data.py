import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

# Read from the xls file to build JSON
import xlrd
import pandas as pd

output_dir = r'C:\Users\xiank\.openclaw\workspace\toolbox\data'
os.makedirs(output_dir, exist_ok=True)

# SSQ
print('Processing SSQ...')
df = pd.read_excel(r'C:\Users\xiank\Desktop\双色球回测分析\ssq_asc.xls')
data = df.iloc[2:].copy().reset_index(drop=True)
ssq = []
for idx in range(len(data)):
    try:
        ssq.append({
            'period': str(data.iloc[idx, 0]),
            'date': str(data.iloc[idx, 1]),
            'reds': [int(float(data.iloc[idx, c])) for c in range(2, 8)],
            'blue': int(float(data.iloc[idx, 8]))
        })
    except: pass

ssq_out = {
    'version': 2,
    'updated_at': '2026-07-02',
    'total': len(ssq),
    'data': ssq
}
with open(os.path.join(output_dir, 'ssq.json'), 'w', encoding='utf-8') as f:
    json.dump(ssq_out, f, ensure_ascii=False)
print(f'  {len(ssq)} periods')

# DLT
print('Processing DLT...')
df2 = pd.read_excel(r'C:\Users\xiank\Desktop\大乐透回测分析\dlt_asc.xls')
data2 = df2.iloc[2:].copy().reset_index(drop=True)
dlt = []
for idx in range(len(data2)):
    try:
        dlt.append({
            'period': str(data2.iloc[idx, 0]),
            'date': str(data2.iloc[idx, 1]),
            'fronts': [int(float(data2.iloc[idx, c])) for c in range(2, 7)],
            'backs': [int(float(data2.iloc[idx, 7])), int(float(data2.iloc[idx, 8]))]
        })
    except: pass

dlt_out = {
    'version': 2,
    'updated_at': '2026-07-02',
    'total': len(dlt),
    'data': dlt
}
with open(os.path.join(output_dir, 'dlt.json'), 'w', encoding='utf-8') as f:
    json.dump(dlt_out, f, ensure_ascii=False)
print(f'  {len(dlt)} periods')

print('Done!')
