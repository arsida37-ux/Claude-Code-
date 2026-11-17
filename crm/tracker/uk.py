# UK English: visible name "Defence", and notes corrected to UK spelling on save
# (typos, US -> UK spellings, -ize -> -ise, contractions, capitals). Runs last in build.py.

# visible text (internal save keys stay the same so saved data and old backups keep working)
s = s.replace('<title>Defense Call Tracker</title>', '<title>Defence Call Tracker</title>', 1)
rep('</svg></i>Defense Call Tracker</div>', '</svg></i>Defence Call Tracker</div>')
rep("toast('That file is not a Defense Call Tracker backup')", "toast('That file is not a Defence Call Tracker backup')")
s = s.replace("download('defense-call-tracker-backup-'", "download('defence-call-tracker-backup-'").replace("download('defense-call-tracker-' + today() + '.csv'", "download('defence-call-tracker-' + today() + '.csv'")

FIX_MORE = {
 # typos seen often when typing fast
 'thta':'that','tht':'that','hte':'the','waht':'what','hwta':'what','wnat':'want','wnan':'want','jsut':'just','juts':'just','cna':'can','nto':'not',
 'becasue':'because','becuase':'because','beacuse':'because','bcause':'because','conatct':'contact','contcat':'contact','conatcts':'contacts','contacs':'contacts',
 'compnay':'company','comapny':'company','compnany':'company','comany':'company','compnaies':'companies','evrything':'everything','everyting':'everything',
 'evrythign':'everything','evrytime':'every time','everytime':'every time','evry':'every','folow':'follow','followup':'follow-up','remeber':'remember',
 'remebr':'remember','rememebr':'remember','remidner':'reminder','remidners':'reminders','intrested':'interested','interseted':'interested','intersted':'interested',
 'meeitng':'meeting','meetign':'meeting','metting':'meeting','calender':'calendar','tomorow':'tomorrow','wiht':'with','whihc':'which','wich':'which',
 'alot':'a lot','wierd':'weird','ahve':'have','knwo':'know','konw':'know','adress':'address','buisness':'business','busness':'business','managment':'management',
 'maintainance':'maintenance','occured':'occurred','ocurred':'occurred','sucessful':'successful','succesful':'successful','oppurtunity':'opportunity',
 'oportunity':'opportunity','propsal':'proposal','emial':'email','emal':'email','numebr':'number','nubmer':'number','phoen':'phone','speicifc':'specific',
 'speciffic':'specific','lsat':'last','laslt':'last','mroe':'more','abotu':'about','aobut':'about','coudl':'could','cuold':'could','woudl':'would','shoudl':'should',
 'logisitcs':'logistics','logistcs':'logistics','delivey':'delivery','delivary':'delivery','urgnet':'urgent','colleage':'colleague','collegue':'colleague',
 'colleuge':'colleague','collegues':'colleagues','aerosapce':'aerospace','aerospce':'aerospace','recieve':'receive','recieved':'received','guarentee':'guarantee',
 'beign':'being','wnated':'wanted','sasid':'said','siad':'said','tehy':'they','thye':'they','tehm':'them','thme':'them','htem':'them','thier':'their','theyre':"they're",
 # contractions
 'dont':"don't",'dotn':"don't",'doesnt':"doesn't",'didnt':"didn't",'cant':"can't",'wont':"won't",'isnt':"isn't",'wasnt':"wasn't",'arent':"aren't",
 'couldnt':"couldn't",'wouldnt':"wouldn't",'shouldnt':"shouldn't",'havent':"haven't",'hasnt':"hasn't",'im':"I'm",'ive':"I've",'youre':"you're",'thats':"that's",
 # US -> UK
 'defense':'defence','center':'centre','centers':'centres','color':'colour','colors':'colours','favorite':'favourite','favor':'favour','behavior':'behaviour',
 'honor':'honour','labor':'labour','neighbor':'neighbour','gray':'grey','traveling':'travelling','traveled':'travelled','canceled':'cancelled','canceling':'cancelling',
 'labeled':'labelled','modeling':'modelling','catalog':'catalogue','aluminum':'aluminium','analyze':'analyse','analyzed':'analysed','analyzing':'analysing',
 'fulfill':'fulfil','enroll':'enrol','program':'programme','programs':'programmes',
}

for w in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','january','february','march','april','june','july','august','september','october','november','december',
          'london','manchester','birmingham','bristol','glasgow','edinburgh','leeds','liverpool','sheffield','cardiff','belfast','newcastle','southampton','portsmouth','plymouth',
          'derby','nottingham','leicester','coventry','reading','oxford','cambridge','aberdeen','dundee','swindon','preston','barrow','farnborough','filton','broughton','yeovil',
          'stevenage','luton','gosport','brize','norton','heathrow','gatwick','stansted','uk','mod','raf','nato','aog','dhl','ups','fedex','tnt','dpd']:
    FIX_MORE[w] = w.upper() if w in ('uk','mod','raf','nato','aog','dhl','ups','tnt','dpd') else ('FedEx' if w == 'fedex' else w.capitalize())
FIX_MORE.update({'thru':'through','tho':'though','logistisc':'logistics','logisitc':'logistic','urgnetly':'urgently','asap':'ASAP','ok':'OK','fyi':'FYI'})
import json as _j
rep("function autocorrect(t){", "Object.assign(FIX, " + _j.dumps(FIX_MORE) + ");\nconst IZE_KEEP = new Set(['size','sizes','sized','sizing','prize','prizes','prized','seize','seizes','seized','seizing','capsize','capsized','maize','resize','resized','resizing','downsize','downsized','downsizing','oversize','oversized','outsize','supersize','baize']);\nfunction autocorrect(t){")
rep(r"  o = o.replace(/\bi\b/g,'I')", r"  o = o.replace(/\b([A-Za-z]{2,})iz(e|es|ed|ing|ation|ations)\b/g, (m, b, x) => IZE_KEEP.has(m.toLowerCase()) ? m : b + 'is' + x);" + "\n" + r"  o = o.replace(/\bi\b/g,'I')")
# spoke-to and the account notes also get tidied; placeholder tells you it happens
rep("if(form.spoke.trim()) extra.spoke = form.spoke.trim();", "if(form.spoke.trim()) extra.spoke = autocorrect(form.spoke.trim());")
rep('placeholder="New note for this call"', 'placeholder="New note for this call (spelling is fixed to UK English when you save)"')
