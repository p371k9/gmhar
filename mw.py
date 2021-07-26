import os, csv, readchar, re, time 
from urllib.parse import urlparse
from requests.utils import requote_uri
from w3lib.html import remove_tags
from html import unescape
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.firefox.options import Options as FirefoxOptions
class wo: #this class depended by the input csv file (alias without) struct.
    def __init__(self, row): # row is a dict from the without mail csv 
        self.row = row
        self.searchString = 'mail @ "{}" {}'.format(self.row['name'], self.row['addr4'])    
    def getId(self):
        return self.row['placeid']
    def itHasAWebsite(self):  # have more query
        return len(self.row['website']) > 1
    def getQuery(self):
        return self.searchString
    def info(self):
        print("{}, {}, {}".format(self.row['name'], self.row['address'], self.row['website']))
        
class Engine:
    engines = ['bing', 'duck', 'google'] # ['bing', 'duck'] 
    def __init__(self, driver):
        self.driver = driver
        self.x = 1
        print(            
            "\nThese will be the search engines: {}. Open and set these! Then hit any key...".format(
            ', '.join(self.engines)
            )
        )
        readchar.readchar();    
    def google(self, searchString):
        print('Google search. Search string = {}'.format(searchString))
        self.driver.get("https://www.google.co.in/search?q="+requote_uri(searchString))
        # watching CAPTCHA    
        if self.driver.find_elements_by_id('captcha-form') != []:
            print('****************CAPTCHA***************!!!!!!!!!!!!')    
    def bing(self, searchString):
        print('BING search. Search string = {}'.format(searchString))
        self.driver.get("http://www.bing.com/search?q="+requote_uri(searchString))
    def duck(self, searchString):
        print('DuckDuckGO search. Search string = {}'.format(searchString))
        self.driver.get("https://duckduckgo.com/?q="+requote_uri(searchString))    
    def search(self, ss):
        eval('self.' + self.engines[self.x - 1])(ss)
        #if len(self.engines) == 2:
        #    self.x = 2 if self.x == 1 else 1
        self.x = self.x + 1 if self.x < len(self.engines) else 1
        
def refreshMails(driver):  # Frissíti, megsorszámozza és kiírja őket   
    print('-----------------refresh mails--------------------')
    source1 = remove_tags(unescape(driver.page_source)).strip()
    mails = re.findall(r'[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', source1)        #unique it!
    mails = list(set(mails))
    counter = 0
    for m in mails:
        if counter == 0:
            pass
        else:
            print(', ', end='', flush=True)
        counter += 1
        if counter > 9: str = m 
        else: str = '{}:{}'.format(counter,m)
        print(str, end='', flush=True)
    #captcha(driver)
    return mails  
     
def siteWalk(url, driver):    
    driver.get(url)
    time.sleep(.2)
    mails = refreshMails(driver)
    if len(mails) > 0:
        return mails
    global ben
    elems = driver.find_elements_by_xpath("//a[@href]")    
    for elem in elems:
        h = elem.get_attribute("href")
        for b in ben:
            if b in h:
                driver.get(h)                
                time.sleep(.2)
                return refreshMails(driver)      
    return mails                 

def process(row, driver):  # process a business: search a mail for it.  
    # fejléc ehhez a céghez
    print('\n>>>>>>>>>>>--------------------------------------------------------*')
    w = wo(row)
    w.info()
    sor = {
        'id': row['placeid'],
        'email': '' 
    }
    if w.itHasAWebsite():
        mails = siteWalk(row['website'],driver)
    else:
        engine.search(w.getQuery())
        time.sleep(.2)        
        mails = refreshMails(driver)       
    # fő ciklus        
    while True:             
        inputString = '\nenTer/type mail, refResh mails, reJect, Quit'
        if w.itHasAWebsite():            
            inputString += ', Search'
        inputString += ': '
        print(inputString, end='', flush=True)
        c = readchar.readchar(); 
        print(c)
        ema = False
        i = ' 123456789'.find(c)
        if i  > 0:
            if i <= len(mails):
                ema = mails[i-1]
        elif c.upper()=='S':
            if w.itHasAWebsite():
                engine.search(w.getQuery())
                mails = refreshMails(driver)
        elif c.upper()=='T':
            ema = input('E-mail begépelése: ')
            if ema == '':
                ema = False
                print('Data entry aborted.')
        elif c.upper()=='R':
            mails = refreshMails(driver)       
        elif c.upper()=='J':
            return 1
        elif c.upper()=='Q':
            return 0
        if ema:
            sor['email'] = ema
            return sor

def main(withoutHandler, mailHandler, driver, tekerjIde=False): 
    global delMailsCsv 
    delMailsCsv = True # For aborting cases: del the empty file 
    reader = csv.DictReader(withoutHandler)
    for row in reader:
        if tekerjIde:
            needMailHeader = False
            w = wo(row)
            if w.getId() == tekerjIde:
                tekerjIde = False 
                delMailsCsv = False           
                writer = csv.DictWriter(mailHandler, ['id', 'email'])
        else:
            mrow = process(row, driver)  # mrow for output, row input
            if mrow == 0:    # next search
                break
            elif mrow == 1:  # reJect
                pass
            else:
                if delMailsCsv:                             
                    writer = csv.DictWriter(mailHandler, ['id', 'email'])
                    writer.writeheader()
                    delMailsCsv = False
                writer.writerow(mrow)
                mailHandler.flush()
    print("\nNormally ended.\n")
    return 
        
def getLastId(mailFileName):
    with open(mailFileName) as f:
        csv_reader = csv.DictReader(f)
        for mrow in csv_reader:
            pass
    return mrow['id']
    
def initParser():
    parser = argparse.ArgumentParser(epilog='Searching for e-mails.') 
    parser.add_argument("infile", help="Input file name. File without mails")
    parser.add_argument("outfile", help="Out file name where store mails. If --cont is set, it is an existing file. If not set, the pgm. create the file.")
    parser.add_argument("-c", "--cont", action='store_true', help="Continue data entry to outfile.")
    parser.add_argument("-m", "--more_search_string", nargs='*', help='add more searchs string to "contact" and "about". Will search these strings in href-s.')
    return parser
        
import argparse  
def initDriver():
    driver = Firefox()
    driver.set_window_size(800, 600)
    driver.set_window_position(0, 0)    
    return driver  
    
if __name__ == '__main__':
    parser = initParser()
    args = parser.parse_args()
    global ben
    ben = 'contact', 'about', 'elerhetoseg', 'kapcsolat'  
    if args.more_search_string:
        ben += tuple(args.more_search_string)
        print(ben)    
    if args.infile:
        try:
            withoutHandler = open(args.infile, 'r')
            if args.cont:
                lastId = getLastId(args.outfile)
                mailHandler = open(args.outfile, mode='a')
            else:
                lastId = False
                mailHandler = open(args.outfile, mode='x')
            print('Open Firefox with Selenium...')
            driver=initDriver()
            engine = Engine(driver)
            main(withoutHandler, mailHandler, driver, lastId)
        finally:
            print('Close all things...')
            withoutHandler.close()
            mailHandler.close()
            global delMailsCsv
            if delMailsCsv: 
                os.remove(args.outfile)
            driver.quit()
            del driver    
                
'''        
    try:        
        mailHandler = open('mails.csv', mode='x')
        withoutHandler = open('without.csv', mode='r')              
        driver = initDriver() # init selenium webdriver
        
        main(withoutHandler, mailHandler, driver)
    finally:
        print('Close all things...')
        mailHandler.close()
        global delMailsCsv
        if delMailsCsv: 
            os.remove("mails.csv")  
        withoutHandler.close()
        driver.quit()
        del driver
        
def googleSearch(searchString, drv):
    print('Google search. Search string = {}'.format(searchString))
    drv.get("https://www.google.co.in" + "/search?q="+requote_uri(searchString))
    # watching CAPTCHA    
    if drv.find_elements_by_id('captcha-form') != []:
        print('****************CAPTCHA***************!!!!!!!!!!!!')    
     
              
/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input 
/html/body/div[4]/form/div[1]/div[1]/div[2]/div/div[2]/input
 
'''
