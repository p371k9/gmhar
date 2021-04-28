# %load_ext autoreload
# %autoreload 2
import json
def prep(body):                
    body = body[body.find(b'\\n') + 2 : body.rfind(b'\\n')]
    body = body.replace(b'\/', b'/')
    body = bytes(body.decode('unicode_escape'), 'latin-1')
    return body    
def getEntries(harFileName):
    with open(harFileName, "r") as read_file:
        data = json.load(read_file)
    return data['log']['entries']        
def getBusinessData(e, b): # e: entry, b: business index
    ebin = prep(e.encode('utf-8'))
    edata = json.loads(ebin.decode('utf-8'))
    return {
        'name' :edata[0][1][b][14][11],
        'url': edata[0][1][b][14][7][0]
    }
def sav(body):  # for testing
    with open("maps.json", "wb") as f:
        f.write(body)   
   
harFile = 'www.google.com_Archive [21-04-11 10-44-37].json'
entries = getEntries(harFile)
entry = entries[0]['response']['content']['text']
x = getBusinessData(entries[1], 1)
listOfKeys = list(x.keys())

'''
def prep(body):                
    body = body[body.find(b'\\n') + 2 : body.rfind(b'\\n')]
    body = body.replace(b'\/', b'/')
    body = bytes(body.decode('unicode_escape'), 'latin-1')
    return body    
def getEntries(harFileName):
    with open(harFileName, "r") as read_file:
        data = json.load(read_file)
    return data['log']['entries']        
def getBusinessData(subs):
    subbin = prep(subs.encode('utf-8'))
    ???? innen folyt. json.loads(subbin.decode('utf-8'))
def sav(body):
    with open("maps.json", "wb") as f:
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
