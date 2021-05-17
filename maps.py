import json, csv
import sys, os, logging, argparse

def felt(lll, str, ret=False):
    try:
        sss = 'lll'+str        
        return eval(sss)
    except: 
        return ret
def getImage(b):
    try:
        s = b[14][72][0][0][6][0]
        return s
        #return s.split('=')[0]
    except: 
        return ''
def getOpening(b):    
    nyitva = ''; dik = 0;
    try:
        a = b[14][34][1]
        for n in a:
            nyitva += n[0] + ': ' + n[1][0] 
            if dik <= 5:
                nyitva += ', '
            dik += 1
        return str(nyitva)
    except:
        return ''
def getCategories(b):    
    cate = ''; dik = 0;
    try:
        a = b[14][13]
        for n in a:
            cate += n
            if dik <= len(a) -2 :
                cate += ', '
            dik += 1
        return str(cate)
    except:
        return ''        
def getBusinessData(bu):
    d = {}    
    d['name'] = bu[14][11]
    d['address'] = bu[14][39]
    d['phone'] = felt(bu, '[14][178][0][0]', '')    
    d['categories'] = getCategories(bu)
    d['rating'] = float(felt(bu, '[14][4][7]', 0))
    d['reviews'] = felt(bu, '[14][4][8]', 0)
    d['latlong'] = str(bu[14][9][2]) + ', ' + str(bu[14][9][3])    
    d['placeid'] = bu[14][78]
    d['website'] = felt(bu, '[14][7][0]', '')
    d['claimed'] = 'no' if type(bu[14][49]) == list else 'yes'     
    d['opening_hours'] = getOpening(bu)
    d['addr1'] = felt(bu, '[14][183][1][0]', '')
    d['addr2'] = felt(bu, '[14][183][1][1]', '')
    d['addr3'] = felt(bu, '[14][183][1][2]', '')
    d['addr4'] = felt(bu, '[14][183][1][3]', '')
    d['addr5'] = felt(bu, '[14][183][1][4]', '')
    d['addr6'] = felt(bu, '[14][183][1][5]', '')
    d['addr7'] = felt(bu, '[14][183][1][6]', '')   
    d['thumbnail'] = getImage(bu)
    global queryString
    d['search_string'] = queryString
    return d
def getEntries(harHandl):    
    data = json.load(harHandl)
    return data['log']['entries']        
def prep(body):                
    body = body[body.find(b'\\n') + 2 : body.rfind(b'\\n')]
    body = body.replace(b'\/', b'/')
    body = bytes(body.decode('unicode_escape'), 'latin-1')
    return body       
def main(harFileHandler, f):    # f=outfile handler
    entries = getEntries(harFileHandler)  # 1 entry == 1 searchpage
    global queryString    
    needHeader = True
    for e in entries:
        entry = e['response']['content']['text']
        ebin = prep(entry.encode('utf-8'))
        edata = json.loads(ebin.decode('utf-8'))
        queryString = edata[0][0]
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
def savEntry(jsonFileName, e): # Csak teszteléshez. Pgm nem hívja. 
    ebin = prep(e.encode('utf-8'))
    with open(jsonFileName, 'wb') as f:
        f.write(ebin)            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Google Maps HAR to .csv .', epilog='.har file filterd to <search> keyword.')
    parser.add_argument('har', type=argparse.FileType('r'), help='Input HAR file name for processing. REQUIRED.')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='If not specified, the output will be sent to STDOUT.')
    parser.add_argument('--same', '-s', action="store_true", help='The name of the output file will be the same as the name of the input file, but with the extension .csv.')
    args = parser.parse_args()
    if args.same and args.outfile.name != '<stdout>':
        logging.error('outfile+same')
        exit()
    if args.same:       
        if os.path.splitext(args.har.name)[1] == '.csv':
            #print("sfs")
            logging.error('Already has a .csv file extension!')
            exit()
        else:
            args.outfile = open(os.path.splitext(args.har.name)[0]+'.csv', 'w')    
    main(args.har, args.outfile)    
    args.har.close() 
    args.outfile.close()

'''      
# %load_ext autoreload
# %autoreload 2

import maps
mapsHandler = open('maps.json')
import json
entry = json.load(mapsHandler)
businesses = entry[0][1]
maps.getBusinessData(businesses[1])


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

def sav(jsonFileName, body):  # for testing
    with open(jsonFileName, "wb") as f:
        f.write(body)   

#def getplaceid(u):
#    parsed =  urlparse.urlparse(u)
#    return parse_qs(parsed.query)['placeid'][0]


with open('www.google.com_Archive [21-04-11 10-44-37].json', "r") as read_file:
    data = json.load(read_file)
subs = data['log']['entries'][0]['response']['content']['text']  
subbin = prep(subs.encode('utf-8'))
#sav(subbin)
subdata = json.loads(subbin.decode('utf-8'))
print(subdata[0][1][1][14][11])
print(subdata[0][1][2][14][11])
'''


