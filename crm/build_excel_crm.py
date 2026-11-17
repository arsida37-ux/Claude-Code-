import datetime as dt, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.chart import BarChart, Reference
from openpyxl.comments import Comment

OUT=sys.argv[1]
NL=1000; NG=3000   # lead rows, log rows
F='Arial'
TEAL='0F766E'; GRAY='EEF2F1'; YEL='FFF4C2'
hdr_font=Font(name=F,bold=True,color='FFFFFF'); hdr_fill=PatternFill('solid',fgColor=TEAL)
calc_fill=PatternFill('solid',fgColor=GRAY); yel=PatternFill('solid',fgColor=YEL)
base=Font(name=F,size=10); bold=Font(name=F,size=10,bold=True)
thin=Side(style='thin',color='D5DDDA')

wb=Workbook()
def sheet(name,first=False):
    ws=wb.active if first else wb.create_sheet()
    ws.title=name; return ws
def headers(ws,cols,widths,row=1):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(row,i,c); x.font=hdr_font; x.fill=hdr_fill; x.alignment=Alignment(vertical='center',wrap_text=True)
        ws.column_dimensions[x.column_letter].width=w
    ws.row_dimensions[row].height=30

start=sheet('Start Here',True)
today=sheet('Today'); leads=sheet('Leads'); log=sheet('Call Log'); lists=sheet('Lists')

# ---------- Lists ----------
headers(lists,['Callers (edit me)','Outcome','Sets status to','Counts as connect?','Default follow-up (days)','','Status','Closed?'],[22,18,16,18,22,3,14,10])
for i,n in enumerate(['Caller 1','Caller 2','Caller 3'],2):
    c=lists.cell(i,1,n); c.fill=yel
for r in range(5,17): lists.cell(r,1).fill=yel
OUT_ROWS=[('No answer','Attempting','No',1),('Voicemail','Attempting','No',1),('Gatekeeper','Attempting','Yes',1),
 ('Call back','Callback','Yes',2),('Interested','Interested','Yes',3),('Meeting booked','Meeting','Yes',None),
 ('Deal won','Won','Yes',None),('Not interested','Lost','Yes',None),('Wrong number','Lost','No',None),('Do not call','DNC','Yes',None)]
for i,(o,s,cn,d) in enumerate(OUT_ROWS,2):
    lists.cell(i,2,o); lists.cell(i,3,s); lists.cell(i,4,cn); lists.cell(i,5,d)
STAT=[('New','No'),('Attempting','No'),('Callback','No'),('Interested','No'),('Meeting','Yes'),('Won','Yes'),('Lost','Yes'),('DNC','Yes')]
for i,(s,c) in enumerate(STAT,2): lists.cell(i,7,s); lists.cell(i,8,c)
lists.freeze_panes='A2'
OUTC="Lists!$B$2:$B$11"; OSTAT="Lists!$C$2:$C$11"; OCONN="Lists!$D$2:$D$11"; ODAYS="Lists!$E$2:$E$11"
SNAME="Lists!$G$2:$G$9"; SCLOSED="Lists!$H$2:$H$9"

# ---------- Call Log ----------
headers(log,['Date','Time','Caller','Business (pick from list)','Phone (auto)','Outcome','Notes','Follow-up date (optional)'],[12,10,14,32,17,16,45,16])
L=lambda col:f"'Call Log'!${col}$2:${col}${NG+1}"
for r in range(2,NG+2):
    log.cell(r,1).number_format='yyyy-mm-dd'; log.cell(r,2).number_format='h:mm AM/PM'; log.cell(r,8).number_format='yyyy-mm-dd'
    e=log.cell(r,5,f'=IF(D{r}="","",IFERROR(INDEX(Leads!$B$2:$B${NL+1},MATCH(D{r},Leads!$A$2:$A${NL+1},0)),""))'); e.fill=calc_fill
log['A2']=dt.date(2026,11,16); log['B2']=dt.time(9,30); log['C2']='Caller 1'; log['D2']='EXAMPLE - Smith Roofing LLC'
log['F2']='Voicemail'; log['G2']='EXAMPLE row - left message for owner, delete me'
for dv in [DataValidation(type='list',formula1='=Lists!$A$2:$A$16',allow_blank=True),
           DataValidation(type='list',formula1=f'=Leads!$A$2:$A${NL+1}',allow_blank=True),
           DataValidation(type='list',formula1=f'={OUTC}',allow_blank=True)]:
    log.add_data_validation(dv)
log.data_validations.dataValidation[0].add(f'C2:C{NG+1}')
log.data_validations.dataValidation[1].add(f'D2:D{NG+1}')
log.data_validations.dataValidation[2].add(f'F2:F{NG+1}')
log.freeze_panes='A2'; log.auto_filter.ref=f'A1:H{NG+1}'
log['A1'].comment=Comment('Tip: Ctrl+; enters today\'s date, Ctrl+Shift+; enters the time.','Dial Desk')

# ---------- Leads ----------
cols=['Business','Phone','City','State','Decision maker','Role','Email','Address','Google Maps link','Notes',
      'Calls','Last call','Last outcome','Last caller','Status','Next follow-up','Call now?']
headers(leads,cols,[32,17,14,7,18,12,24,30,18,30,7,12,15,13,12,14,11])
for c in range(11,18): leads.cell(1,c).fill=PatternFill('solid',fgColor='134E4A')
last=lambda col,r:f"LOOKUP(2,1/({L('D')}=$A{r}),{L(col)})"
for r in range(2,NL+2):
    f={
    11:f'=IF($A{r}="","",COUNTIF({L("D")},$A{r}))',
    12:f'=IF(OR($A{r}="",K{r}=0),"",_xlfn.MAXIFS({L("A")},{L("D")},$A{r}))',
    13:f'=IF(OR($A{r}="",K{r}=0),"",{last("F",r)})',
    14:f'=IF(OR($A{r}="",K{r}=0),"",{last("C",r)})',
    15:f'=IF($A{r}="","",IF(K{r}=0,"New",IFERROR(INDEX({OSTAT},MATCH(M{r},{OUTC},0)),"Attempting")))',
    16:f'=IF(OR($A{r}="",K{r}=0),"",IF(INDEX({SCLOSED},MATCH(O{r},{SNAME},0))="Yes","",IF(N({last("H",r)})>0,{last("H",r)},L{r}+IFERROR(INDEX({ODAYS},MATCH(M{r},{OUTC},0)),1))))',
    17:f'=IF($A{r}="","",IF(INDEX({SCLOSED},MATCH(O{r},{SNAME},0))="Yes","Done",IF(OR(P{r}="",P{r}<=TODAY()),"Call now","Later")))',
    }
    for c,v in f.items():
        x=leads.cell(r,c,v); x.fill=calc_fill
    leads.cell(r,12).number_format='yyyy-mm-dd'; leads.cell(r,16).number_format='yyyy-mm-dd'
for c,v in enumerate(['EXAMPLE - Smith Roofing LLC','(555) 010-1234','Austin','TX','','','','','','EXAMPLE row - replace with your leads'],1):
    leads.cell(2,c,v or None)
leads.freeze_panes='B2'; leads.auto_filter.ref=f'A1:Q{NL+1}'
rng=f'A2:Q{NL+1}'
for txt,col in [('Call now','DCFCE7'),('Later','FEF3C7'),('Done','E5E7EB')]:
    leads.conditional_formatting.add(f'Q2:Q{NL+1}',CellIsRule(operator='equal',formula=[f'"{txt}"'],fill=PatternFill('solid',fgColor=col)))
for txt,col in [('Interested','DCFCE7'),('Meeting','BBF7D0'),('Won','86EFAC'),('Callback','FEF3C7'),('Lost','FEE2E2'),('DNC','FECACA')]:
    leads.conditional_formatting.add(f'O2:O{NL+1}',CellIsRule(operator='equal',formula=[f'"{txt}"'],fill=PatternFill('solid',fgColor=col)))
leads.conditional_formatting.add(f'A2:A{NL+1}',FormulaRule(formula=[f'AND($A2<>"",COUNTIF($A$2:$A${NL+1},$A2)>1)'],fill=PatternFill('solid',fgColor='FECACA')))

# ---------- Today ----------
ws=today
for col,w in zip('ABCDEFGH',[22,14,14,14,14,16,16,4]): ws.column_dimensions[col].width=w
ws['A1']='Cold Calling - Today'; ws['A1'].font=Font(name=F,size=18,bold=True,color=TEAL)
ws['A2']='Updates by itself from the Call Log. Nothing to type on this sheet.'; ws['A2'].font=Font(name=F,size=10,italic=True,color='5D6B67')
ws['A3']='Date'; ws['B3']='=TODAY()'; ws['B3'].number_format='dddd, mmm d'
ws['C3']='Week starts'; ws['D3']='=B3-WEEKDAY(B3,2)+1'; ws['D3'].number_format='mmm d'
D="$B$3"; W="$D$3"
conn_today=f'SUMPRODUCT(COUNTIFS({L("A")},{D},{L("F")},{OUTC})*({OCONN}="Yes"))'
tiles=[('Dials',f'=COUNTIF({L("A")},{D})','0'),('Connects',f'={conn_today}','0'),
       ('Connect rate',f'=IFERROR(B6/A6,0)','0%'),('Meetings',f'=COUNTIFS({L("A")},{D},{L("F")},"Meeting booked")','0'),
       ('Ready to call',f'=COUNTIF(Leads!$Q$2:$Q${NL+1},"Call now")','0')]
for i,(lab,fm,nf) in enumerate(tiles):
    c=ws.cell(5,1+i,lab); c.font=Font(name=F,size=10,bold=True,color='5D6B67')
    v=ws.cell(6,1+i,fm); v.font=Font(name=F,size=24,bold=True,color=TEAL); v.number_format=nf
    for rr in (5,6): ws.cell(rr,1+i).border=Border(left=thin,right=thin,top=thin if rr==5 else None,bottom=thin if rr==6 else None); ws.cell(rr,1+i).fill=PatternFill('solid',fgColor='F6F8F7')
ws.row_dimensions[6].height=36
ws['A8']='By caller'; ws['A8'].font=Font(name=F,size=13,bold=True)
hh=['Caller','Dials today','Connects','Meetings','Connect rate','Dials this week','Meetings this week']
for i,h in enumerate(hh,1):
    c=ws.cell(9,i,h); c.font=hdr_font; c.fill=hdr_fill; c.alignment=Alignment(wrap_text=True,vertical='center')
ws.row_dimensions[9].height=30
for k in range(15):
    r=10+k; lr=2+k
    ws.cell(r,1,f'=IF(Lists!A{lr}="","",Lists!A{lr})')
    ws.cell(r,2,f'=IF($A{r}="","",COUNTIFS({L("A")},{D},{L("C")},$A{r}))')
    ws.cell(r,3,f'=IF($A{r}="","",SUMPRODUCT(COUNTIFS({L("A")},{D},{L("C")},$A{r},{L("F")},{OUTC})*({OCONN}="Yes")))')
    ws.cell(r,4,f'=IF($A{r}="","",COUNTIFS({L("A")},{D},{L("C")},$A{r},{L("F")},"Meeting booked"))')
    c=ws.cell(r,5,f'=IF($A{r}="","",IFERROR(C{r}/B{r},0))'); c.number_format='0%'
    ws.cell(r,6,f'=IF($A{r}="","",COUNTIFS({L("A")},">="&{W},{L("A")},"<="&{D},{L("C")},$A{r}))')
    ws.cell(r,7,f'=IF($A{r}="","",COUNTIFS({L("A")},">="&{W},{L("A")},"<="&{D},{L("C")},$A{r},{L("F")},"Meeting booked"))')
    for c in range(1,8): ws.cell(r,c).border=Border(bottom=thin)
ws.conditional_formatting.add('B10:B24',FormulaRule(formula=['AND(ISNUMBER(B10),B10=MAX($B$10:$B$24),B10>0)'],fill=PatternFill('solid',fgColor='DCFCE7'),font=Font(name=F,bold=True)))
ws['A27']='Pipeline (all leads)'; ws['A27'].font=Font(name=F,size=13,bold=True)
for i,(s,_) in enumerate(STAT):
    c=ws.cell(28,1+i if i<7 else 1,None)
for i,(s,_) in enumerate(STAT):
    r=29+i
    ws.cell(r,1,s); ws.cell(r,2,f'=COUNTIF(Leads!$O$2:$O${NL+1},A{r})')
    for c in (1,2): ws.cell(r,c).border=Border(bottom=thin)
ws.cell(28,1,'Status').font=hdr_font; ws.cell(28,1).fill=hdr_fill
ws.cell(28,2,'Leads').font=hdr_font; ws.cell(28,2).fill=hdr_fill
ch=BarChart(); ch.type='bar'; ch.style=10; ch.title="Dials today by caller"
ch.add_data(Reference(ws,min_col=2,min_row=9,max_row=24),titles_from_data=True)
ch.set_categories(Reference(ws,min_col=1,min_row=10,max_row=24))
ch.legend=None; ch.roundedCorners=False; ch.title.overlay=False
ch.x_axis.delete=False; ch.y_axis.delete=False; ch.y_axis.majorGridlines=None
ch.height=8; ch.width=13
ch.series[0].graphicalProperties.solidFill=TEAL
ws.add_chart(ch,'D27')
ws.freeze_panes='A4'

# ---------- Start Here ----------
s=start; s.column_dimensions['A'].width=4; s.column_dimensions['B'].width=95
lines=[('Cold Calling CRM','t'),('',''),
('SET UP (once)','h'),
('1. Save this file to OneDrive or SharePoint, then click Share so your team can open it.',''),
('2. Go to the Lists tab and replace Caller 1, 2, 3 with your team\'s names (yellow cells).',''),
('3. Go to the Leads tab and paste your leads into columns A-J (Business, Phone, City, State...).',''),
('4. Delete the two rows that start with EXAMPLE (one in Leads, one in Call Log).',''),
('',''),
('EVERY CALL','h'),
('1. Leads tab: filter "Call now?" to show Call now. Pick a lead.',''),
('2. Call Log tab: add one row - Date, Time, your name, pick the Business, pick the Outcome.',''),
('3. That\'s it. Status, follow-up date and the Today dashboard update by themselves.',''),
('',''),
('WHAT TO TYPE','h'),
('White cells = you type here.   Grey cells = automatic, don\'t type.   Yellow = setup.',''),
('Shortcuts:  Ctrl + ;  = today\'s date      Ctrl + Shift + ;  = current time',''),
('',''),
('WATCH PROGRESS','h'),
('Today tab: dials, connects, meetings for the team and for each caller. Anyone with the link can view it.',''),
('',''),
('HOW FOLLOW-UPS WORK','h'),
('No answer / Voicemail / Gatekeeper: call again in 1 day.  Call back: 2 days.  Interested: 3 days.',''),
('Type your own date in "Follow-up date" in the Call Log to override. Change the default days in Lists.',''),
('Meeting booked, Deal won, Not interested, Wrong number, Do not call: lead is Done and leaves the queue.',''),
('',''),
('Holds up to 1,000 leads and 3,000 calls.','n'),
]
for i,(t,k) in enumerate(lines,1):
    c=s.cell(i,2,t)
    c.font={'t':Font(name=F,size=18,bold=True,color=TEAL),'h':Font(name=F,size=11,bold=True,color=TEAL),'n':Font(name=F,size=9,italic=True,color='5D6B67')}.get(k,base)
for ws_ in wb.worksheets:
    for row in ws_.iter_rows():
        for c in row:
            if c.font.name!=F: c.font=Font(name=F,size=c.font.size or 10,bold=c.font.bold,italic=c.font.italic,color=c.font.color)
for ws_,col in [(start,TEAL),(today,TEAL),(leads,'1D4ED8'),(log,'15803D'),(lists,'6B7280')]:
    ws_.sheet_properties.tabColor=col
wb.active=1
wb.save(OUT)
