"""Analyze the supplied synthetic appointment dataset. No patient data is used."""
import csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).resolve().parent
with (base/'synthetic_appointments.csv').open(newline='') as f:
    data=list(csv.DictReader(f))
facilities=defaultdict(list);lead=defaultdict(list)
for row in data:
    facilities[row['facility']].append(row)
    days=int(row['days_to_appointment'])
    bucket=('0–7 days' if days<=7 else '8–14 days' if days<=14 else '15–30 days' if days<=30 else '31+ days')
    lead[bucket].append(row)
def rate(group): return 100*sum(r['status']=='No Show' for r in group)/len(group)
print('Simulated appointment count:',len(data))
print('Simulated no-show rate: %.1f%%'%rate(data))
print('Facility rates:')
for k,v in sorted(facilities.items(),key=lambda kv:-rate(kv[1])):print(' ',k,round(rate(v),1))
fig, ax=plt.subplots(1,2,figsize=(12,5),layout='constrained')
a=sorted(facilities.items(),key=lambda kv:-rate(kv[1]))
ax[0].barh([k for k,v in a],[rate(v) for k,v in a]);ax[0].invert_yaxis();ax[0].set_title('No-show rates by facility');ax[0].set_xlabel('No-show rate (%)')
b=[(k,lead[k]) for k in ['0–7 days','8–14 days','15–30 days','31+ days']]
ax[1].bar([k for k,v in b],[rate(v) for k,v in b]);ax[1].set_title('Lead time and missed visits');ax[1].set_ylabel('No-show rate (%)');ax[1].tick_params(axis='x',rotation=15)
fig.suptitle('Healthcare Access & Scheduling Analytics | Synthetic Data')
fig.savefig(base/'basic_analysis.png',dpi=180,bbox_inches='tight')
print('Updated basic_analysis.png')
