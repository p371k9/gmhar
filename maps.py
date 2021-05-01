# %load_ext autoreload
# %autoreload 2
import json
def getEntries(harFileName):
    with open(harFileName, "r") as read_file:
        data = json.load(read_file)
    return data['log']['entries']        
def prep(body):                
    body = body[body.find(b'\\n') + 2 : body.rfind(b'\\n')]
    body = body.replace(b'\/', b'/')
    body = bytes(body.decode('unicode_escape'), 'latin-1')
    return body       
def getBusinessData(bu):
    d = {}
    d['name']= bu[14][11]
    try: d['url'] = bu[14][7][0]
    except: d['url'] = ''
    return d
def savEntry(jsonFileName, e): # Csak teszteléshez. Pgm nem hívja. 
    ebin = prep(e.encode('utf-8'))
    with open(jsonFileName, 'wb') as f:
        f.write(ebin)
   
harFile = 'www.google.com_Archive [21-04-11 10-44-37].json'
f = sys.stdout
entries = getEntries(harFile)

needHeader = True
for e in entries:
    entry = e['response']['content']['text']
    ebin = prep(entry.encode('utf-8'))
    edata = json.loads(ebin.decode('utf-8'))
    businesses = edata[0][1]
    first = True
    for business in businesses:
        if not first:
            businessData = getBusinessData(business)
            if needHeader:                
                writer = csv.DictWriter(f, list(businessData.keys()))
                writer.writeheader()
                needHeader = False
            writer.writerow(businessData)
        first = False
    #print(len(businesses))    
    

listOfKeys = list(x.keys())
# optional
savEntry('uj.json', entry)


'''   
def sav(jsonFileName, body):  # for testing
    with open(jsonFileName, "wb") as f:
        f.write(body)   


with open('www.google.com_Archive [21-04-11 10-44-37].json', "r") as read_file:
    data = json.load(read_file)
subs = data['log']['entries'][0]['response']['content']['text']  
subbin = prep(subs.encode('utf-8'))
#sav(subbin)
subdata = json.loads(subbin.decode('utf-8'))
print(subdata[0][1][1][14][11])
print(subdata[0][1][2][14][11])
'''
