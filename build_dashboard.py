"""Create an executive-style screenshot and offline interactive dashboard from synthetic scheduling data."""
from pathlib import Path
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
import json, plotly
base=Path(__file__).resolve().parent
x=pd.read_csv(base/'synthetic_appointments.csv',parse_dates=['appointment_date'])
x['no_show']=(x.status=='No Show').astype(int)
x['month']=x.appointment_date.dt.strftime('%b')
x['month_order']=x.appointment_date.dt.month
x['lead_band']=pd.cut(x.days_to_appointment,[-1,7,14,30,1000],labels=['0–7 days','8–14 days','15–30 days','31+ days'])
wait=x.loc[x.status=='Completed','checkin_wait_minutes']
navy='#101d36'; muted='#69788e'; cyan='#1b83a5'; teal='#0f9b87'; red='#ce605c'; bg='#f3f7fa'; grid='#e6ebf2'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#d9e2eb','axes.labelcolor':muted,'xtick.color':muted,'ytick.color':muted,'text.color':navy})
fig=plt.figure(figsize=(19.2,12),facecolor=bg)
fig.text(.055,.947,'CARE ACCESS  /  OPERATIONS INTELLIGENCE',weight='bold',color=teal,fontsize=12)
fig.text(.055,.908,'Patient Access & Scheduling Performance',weight='bold',fontsize=28)
fig.text(.055,.874,'Operational analytics across 3 fictional facilities  •  January – June 2026',fontsize=12,color=muted)
fig.text(.94,.945,'PORTFOLIO DEMO',fontsize=11,color=navy,ha='right',weight='bold')
fig.text(.94,.918,'SYNTHETIC DATA ONLY',fontsize=10,color=red,ha='right',weight='bold')

def card(x0,y0,w,h):
    fig.add_artist(FancyBboxPatch((x0,y0),w,h,boxstyle='round,pad=0.012,rounding_size=0.014',transform=fig.transFigure,facecolor='white',edgecolor='#e7ecf3',lw=.85,zorder=0))
def kpi(left,label,value,note,tone=navy):
    card(left,.733,.205,.103)
    fig.text(left+.016,.803,label,color=muted,fontsize=11)
    fig.text(left+.016,.762,value,color=tone,fontsize=29,weight='bold')
    fig.text(left+.016,.746,note,color=muted,fontsize=9)
rate=100*x.no_show.mean();avg_wait=wait.mean()
kpi(.055,'Scheduled visits',f'{len(x):,}','Jan – Jun 2026')
kpi(.284,'No-show rate',f'{rate:.1f}%','249 missed visits',red)
kpi(.513,'Mean check-in wait',f'{avg_wait:.1f} min','Completed visits',cyan)
kpi(.742,'Visit completion',f'{100-rate:.1f}%','951 completed',teal)

# Cards and chart panels
card(.055,.392,.432,.304);card(.513,.392,.434,.304)
card(.055,.094,.285,.255);card(.365,.094,.285,.255);card(.675,.094,.272,.255)
fig.text(.077,.661,'NO-SHOW TREND',fontsize=12,weight='bold')
fig.text(.077,.639,'Monthly visit volume and missed-appointment rate',color=muted,fontsize=10)
fig.text(.535,.661,'FACILITY PERFORMANCE',fontsize=12,weight='bold')
fig.text(.535,.639,'Compare missed visits and average check-in waits',color=muted,fontsize=10)
fig.text(.077,.314,'BY CLINICAL SPECIALTY',fontsize=12,weight='bold')
fig.text(.077,.292,'Missed visits / all scheduled visits',color=muted,fontsize=9)
fig.text(.387,.314,'SCHEDULING LEAD TIME',fontsize=12,weight='bold')
fig.text(.387,.292,'No-show rate by booking interval',color=muted,fontsize=9)
fig.text(.697,.314,'OPERATIONAL INTERPRETATION',fontsize=12,weight='bold')
fig.text(.697,.292,'What an analyst should investigate',color=muted,fontsize=9)

ax=fig.add_axes([.08,.445,.386,.161]);ax.set_facecolor('white')
m=x.groupby('month_order').agg(n=('no_show','size'),missed=('no_show','sum')).reindex(range(1,7),fill_value=0)
months=['Jan','Feb','Mar','Apr','May','Jun'];rates=100*m.missed/m.n
ax.bar(months,m.n,color='#d8e8f1',width=.58)
ax.set_ylim(0,max(m.n)*1.27);ax.set_ylabel('Appointments',fontsize=9)
ax.yaxis.set_major_locator(plt.MaxNLocator(4));ax.grid(axis='y',color=grid,zorder=-1);ax.set_axisbelow(True)
ax2=ax.twinx();ax2.plot(months,rates,color=red,linewidth=2.8,marker='o',markersize=6);ax2.set_ylim(0,max(35,max(rates)+6));ax2.set_ylabel('No-show rate (%)',fontsize=9,color=red);ax2.spines['top'].set_visible(False);ax2.spines['right'].set_visible(False);ax2.tick_params(axis='y',colors=red)
for i,p in enumerate(rates):ax2.annotate(f'{p:.1f}%',(i,p),xytext=(0,10),textcoords='offset points',ha='center',fontsize=9,color=red,weight='bold')

ax=fig.add_axes([.545,.444,.36,.160]);ax.set_facecolor('white')
f=x.groupby('facility').agg(n=('no_show','size'),missed=('no_show','sum'),wait=('checkin_wait_minutes','mean')).sort_values('missed',ascending=False)
fr=100*f.missed/f.n
bars=ax.barh(np.arange(len(f)),fr,color=[cyan,teal,'#8bbcd0'],height=.48)
ax.set_yticks(np.arange(len(f)),f.index,fontsize=10);ax.invert_yaxis();ax.set_xlim(0,max(fr)+10)
ax.set_xlabel('No-show rate (%)',fontsize=9);ax.grid(axis='x',color=grid);ax.set_axisbelow(True)
for i,(b,r) in enumerate(zip(bars,fr)):
 ax.text(r+.45,i,f'{r:.1f}%',va='center',weight='bold',fontsize=10)
 ax.text(max(fr)+9.5,i,f'{f.wait.iloc[i]:.1f}m wait',ha='right',va='center',fontsize=9,color=muted)

ax=fig.add_axes([.079,.139,.227,.123]);ax.set_facecolor('white')
s=x.groupby('specialty').agg(n=('no_show','size'),missed=('no_show','sum'));s['pct']=100*s.missed/s.n;s=s.sort_values('pct')
ax.barh(s.index,s.pct,color=teal,height=.53);ax.set_xlim(0,max(s.pct)+8);ax.tick_params(labelsize=9);ax.grid(axis='x',color=grid);ax.set_axisbelow(True)
for i,r in enumerate(s.pct):ax.text(r+.55,i,f'{r:.1f}%',va='center',fontsize=9,weight='bold')
ax=fig.add_axes([.387,.139,.223,.123]);ax.set_facecolor('white')
l=x.groupby('lead_band',observed=True).agg(n=('no_show','size'),missed=('no_show','sum'));l['pct']=100*l.missed/l.n
ax.bar(range(4),l.pct,color=[teal,'#62b6a8','#e7b277',red],width=.63);ax.set_xticks(range(4),l.index,fontsize=8);ax.set_ylim(0,max(l.pct)+8);ax.grid(axis='y',color=grid);ax.set_axisbelow(True);ax.tick_params(axis='y',labelsize=9)
for i,r in enumerate(l.pct):ax.text(i,r+.8,f'{r:.1f}%',ha='center',weight='bold',fontsize=9)
# Insight narrative, no causal claims
fig.text(.697,.252,'01   Investigate',weight='bold',fontsize=11,color=teal)
fig.text(.697,.229,'Variation in missed-visit rates',fontsize=10)
fig.text(.697,.208,'across facilities and specialties.',fontsize=10)
fig.text(.697,.179,'02   Validate',weight='bold',fontsize=11,color=teal)
fig.text(.697,.157,'Whether longer lead times correlate',fontsize=10)
fig.text(.697,.137,'with nonattendance in real data.',fontsize=10)
fig.text(.055,.045,'SOURCE  •  1,200 synthetic appointment records   |   METHODS  •  SQLite, Python, descriptive analytics',fontsize=10,color=muted)
fig.text(.945,.045,'Illustrative findings  •  No PHI',fontsize=10,color=muted,ha='right')
fig.savefig(base/'dashboard_preview.png',dpi=155,facecolor=bg)
plt.close(fig)

# Standalone offline interactive HTML, entirely browser-side; no servers or network dependencies
# Serialize aggregate/filterable non-identifying synthetic rows
records=[{'d':r.appointment_date.strftime('%Y-%m-%d'),'f':r.facility,'s':r.specialty,'l':int(r.days_to_appointment),'w':None if pd.isna(r.checkin_wait_minutes) else int(r.checkin_wait_minutes),'n':int(r.no_show)} for r in x.itertuples(index=False)]
plotlyjs=plotly.offline.get_plotlyjs()
html='''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>Patient Access | Healthcare Operations</title><style>
*{box-sizing:border-box}body{margin:0;background:#f3f7fa;color:#101d36;font-family:Inter,Arial,sans-serif}header{background:#11223b;color:#fff;padding:27px 4% 25px}header .eyebrow{color:#72d7cb;letter-spacing:2px;font-size:11px;font-weight:800}header h1{font-size:29px;margin:8px 0}header p{color:#b9cadd;margin:4px 0;font-size:13px}.wrap{padding:25px 4%;max-width:1600px;margin:auto}.filterbox{background:white;border:1px solid #e6edf5;border-radius:14px;padding:15px;display:flex;gap:20px;align-items:end;flex-wrap:wrap;margin-bottom:20px}.filterbox label{font-size:11px;display:grid;gap:7px;color:#60728a;font-weight:700;letter-spacing:.4px}.filterbox select{border:1px solid #dce6ed;border-radius:8px;padding:10px 15px;min-width:180px;background:#fff;color:#142941;font-size:14px}.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.kpi,.panel{background:white;border-radius:14px;border:1px solid #e6edf5;box-shadow:0 2px 6px #163b6010}.kpi{padding:19px 21px}.kpi .name{color:#65748a;font-size:13px}.kpi .num{font-size:32px;font-weight:800;margin:10px 0 3px}.kpi .sub{color:#8190a4;font-size:12px}.charts{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}.panel{padding:18px}.panel h2{font-size:15px;margin:0 0 5px}.panel .note{color:#7e8b9b;font-size:12px;margin:0}.chart{width:100%;height:300px}.insight{background:#e8f5f2;border-left:4px solid #0f9b87;padding:17px 21px;border-radius:10px;margin-top:20px;font-size:14px;line-height:1.55}.footer{margin:20px 0;color:#78889b;font-size:12px}button{background:#143650;color:white;padding:10px 15px;border:0;border-radius:8px;cursor:pointer} @media(max-width:920px){.kpis,.charts{grid-template-columns:1fr 1fr}}@media(max-width:620px){.kpis,.charts{grid-template-columns:1fr}.filterbox select{min-width:140px}} </style></head><body>
<header><div class="eyebrow">CARE ACCESS / OPERATIONS INTELLIGENCE</div><h1>Patient Access & Scheduling Performance</h1><p>Healthcare Informatics Portfolio | January – June 2026 | Synthetic appointment records only</p></header>
<main class="wrap"><div class="filterbox"><label>FACILITY<select id="facility"><option value="">All facilities</option><option>Baltimore Central</option><option>Towson North</option><option>Columbia West</option></select></label><label>SPECIALTY<select id="specialty"><option value="">All specialties</option><option>Primary Care</option><option>Cardiology</option><option>Orthopedics</option><option>Endocrinology</option></select></label><label>MONTH<select id="month"><option value="">All months</option><option value="01">January</option><option value="02">February</option><option value="03">March</option><option value="04">April</option><option value="05">May</option><option value="06">June</option></select></label><button id="reset">Reset filters</button></div>
<div class="kpis"><div class="kpi"><div class="name">Scheduled visits</div><div class="num" id="visits">—</div><div class="sub">Filtered appointment volume</div></div><div class="kpi"><div class="name">No-show rate</div><div class="num" id="rate">—</div><div class="sub" id="missed">Missed appointments</div></div><div class="kpi"><div class="name">Average check-in wait</div><div class="num" id="wait">—</div><div class="sub">Completed appointments only</div></div><div class="kpi"><div class="name">Visit completion rate</div><div class="num" id="completed">—</div><div class="sub">Scheduled visits completed</div></div></div>
<div class="charts"><section class="panel"><h2>Monthly Volume & No-show Rate</h2><p class="note">Compare scheduled visits with missed-appointment trends</p><div id="trend" class="chart"></div></section><section class="panel"><h2>Facility Comparison</h2><p class="note">No-show rate and location-level variation</p><div id="facilities" class="chart"></div></section><section class="panel"><h2>Performance by Specialty</h2><p class="note">Appointment nonattendance across care areas</p><div id="specialties" class="chart"></div></section><section class="panel"><h2>Lead-time Risk Exploration</h2><p class="note">Descriptive association, not a causal relationship</p><div id="lead" class="chart"></div></section></div>
<div class="insight"><b>Analyst takeaway</b><div id="insight"></div></div><p class="footer">All 1,200 records are synthetic. Facility names are fictional labels. No protected health information is included. No-show rate denominator excludes cancellations because this simulated dataset contains only completed and missed appointments. Rates for small filtered groups should be interpreted cautiously.</p></main>
<script>''' + plotlyjs + '</script><script>const DATA='+json.dumps(records,separators=(',',':'))+''';
const color='#0f9b87',red='#ce605c',blue='#1b83a5',txt='#182840';const layoutBase={paper_bgcolor:'#fff',plot_bgcolor:'#fff',font:{family:'Arial',color:txt,size:12},margin:{t:30,b:50,l:115,r:45},showlegend:false};const conf={responsive:true,displaylogo:false};const rate=a=>a.length?100*a.filter(r=>r.n).length/a.length:0;
function draw(){let f=document.querySelector('#facility').value,s=document.querySelector('#specialty').value,m=document.querySelector('#month').value;let d=DATA.filter(r=>(!f||r.f===f)&&(!s||r.s===s)&&(!m||r.d.slice(5,7)===m));const no=d.filter(r=>r.n).length,done=d.length-no,w=d.filter(r=>r.w!==null).map(r=>r.w);document.querySelector('#visits').textContent=d.length.toLocaleString();document.querySelector('#rate').textContent=rate(d).toFixed(1)+'%';document.querySelector('#missed').textContent=no+' missed visits';document.querySelector('#wait').textContent=w.length?(w.reduce((a,b)=>a+b,0)/w.length).toFixed(1)+' min':'N/A';document.querySelector('#completed').textContent=d.length?(100-rate(d)).toFixed(1)+'%':'N/A';
function groups(key,labels){return labels.map(v=>({name:v,arr:d.filter(r=>key(r)===v)}))}
let months=['01','02','03','04','05','06'];let byMonth=groups(r=>r.d.slice(5,7),months);Plotly.react('trend',[{type:'bar',x:['Jan','Feb','Mar','Apr','May','Jun'],y:byMonth.map(z=>z.arr.length),marker:{color:'#c3e0e5'},name:'Appointments'},{type:'scatter',mode:'lines+markers+text',x:['Jan','Feb','Mar','Apr','May','Jun'],y:byMonth.map(z=>rate(z.arr)),yaxis:'y2',name:'No-show rate',text:byMonth.map(z=>z.arr.length?rate(z.arr).toFixed(1)+'%':''),textposition:'top center',line:{color:red,width:3},marker:{size:7}}],{...layoutBase,margin:{t:25,b:40,l:45,r:55},yaxis:{title:'Visits',gridcolor:'#edf1f5'},yaxis2:{title:'Rate %',overlaying:'y',side:'right',rangemode:'tozero'},showlegend:false},conf);
let fac=groups(r=>r.f,['Baltimore Central','Towson North','Columbia West']);Plotly.react('facilities',[{type:'bar',orientation:'h',y:fac.map(z=>z.name),x:fac.map(z=>rate(z.arr)),marker:{color:[blue,color,'#76bdc7']},text:fac.map(z=>z.arr.length?rate(z.arr).toFixed(1)+'%':'—'),textposition:'outside'}],{...layoutBase,xaxis:{title:'No-show rate (%)',gridcolor:'#edf1f5',range:[0,Math.max(10,...fac.map(z=>rate(z.arr)))+10]},yaxis:{autorange:'reversed'}},conf);
let sp=groups(r=>r.s,['Primary Care','Cardiology','Orthopedics','Endocrinology']);Plotly.react('specialties',[{type:'bar',orientation:'h',y:sp.map(z=>z.name),x:sp.map(z=>rate(z.arr)),marker:{color:color},text:sp.map(z=>z.arr.length?rate(z.arr).toFixed(1)+'%':'—'),textposition:'outside'}],{...layoutBase,xaxis:{title:'No-show rate (%)',gridcolor:'#edf1f5',range:[0,Math.max(10,...sp.map(z=>rate(z.arr)))+10]}},conf);
let buckets=[{name:'0–7 days',fn:v=>v<=7},{name:'8–14 days',fn:v=>v>7&&v<=14},{name:'15–30 days',fn:v=>v>14&&v<=30},{name:'31+ days',fn:v=>v>30}];let b=buckets.map(z=>({name:z.name,arr:d.filter(r=>z.fn(r.l))}));Plotly.react('lead',[{type:'bar',x:b.map(z=>z.name),y:b.map(z=>rate(z.arr)),marker:{color:[color,'#65b9a7','#e4b074',red]},text:b.map(z=>z.arr.length?rate(z.arr).toFixed(1)+'%':'—'),textposition:'outside'}],{...layoutBase,margin:{t:35,b:45,l:52,r:20},xaxis:{title:'Days from booking to appointment'},yaxis:{title:'No-show rate (%)',gridcolor:'#edf1f5',range:[0,Math.max(10,...b.map(z=>rate(z.arr)))+10]}},conf);
document.querySelector('#insight').textContent='Across '+d.length.toLocaleString()+' filtered synthetic appointments, the missed-visit rate is '+rate(d).toFixed(1)+'%. Compare facility, specialty, and scheduling lead-time segments to identify which patterns deserve validation against real operational data. This simulation does not establish causality or predict outcomes for real patients.';
}for(const k of ['facility','specialty','month'])document.getElementById(k).addEventListener('change',draw);document.querySelector('#reset').onclick=()=>{for(const k of ['facility','specialty','month'])document.getElementById(k).value='';draw()};draw();</script></body></html>'''
(base/'interactive_dashboard.html').write_text(html,encoding='utf-8')
print('Generated PNG and HTML', (base/'dashboard_preview.png').stat().st_size, (base/'interactive_dashboard.html').stat().st_size)
