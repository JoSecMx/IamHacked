from mechanize import Browser
import json
import mechanize
import argparse
import colorama
from colorama import Fore
from os import path
import time
from bs4 import BeautifulSoup

colorama.init(autoreset=True)

parse = argparse.ArgumentParser()
parse.add_argument('-e','--email',help="Email")
parse.add_argument('-f','--file',help='Email File')
parse.add_argument('-l','--list',help='List Hacked Domains',action="store_true")
parse = parse.parse_args()

class colors:
    black = Fore.LIGHTBLACK_EX
    blue = Fore.LIGHTBLUE_EX
    cyan = Fore.LIGHTCYAN_EX
    green = Fore.LIGHTGREEN_EX
    magenta = Fore.LIGHTMAGENTA_EX
    red = Fore.LIGHTRED_EX
    white = Fore.LIGHTWHITE_EX
    yellow = Fore.LIGHTYELLOW_EX

c = colors()

banner = c.cyan + """
.___                 ___ ___                __              .___
|   |____    _____  /   |   \_____    ____ |  | __ ____   __| _/
|   \__  \  /     \/    ~    \__  \ _/ ___\|  |/ // __ \ / __ | 
|   |/ __ \|  Y Y  \    Y    // __ \\  \___|    <\  ___// /_/ | 
|___(____  /__|_|  /\___|_  /(____  /\___  >__|_ \\___  >____ | 
         \/      \/       \/      \/     \/     \/    \/     \/ 
"""

headers = {
    'Host':'haveibeenpwned.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language':'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'Accept-Encoding'
    }

def parse_file(email_list):
    file_list = open(email_list, 'r')
    file_list = file_list.read().split()
    file_list = [f for f in file_list if f != ""]
    return file_list



def parse_sites_owned():
    browser = Browser()
    browser.set_handle_robots(False)
    browser.set_handle_equiv(False)
    browser.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'),
    ('Host', 'haveibeenpwned.com'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    ('Accept-Language', 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Accept-Encoding', 'Accept-Encoding')
    ]

    browser.open('https://haveibeenpwned.com/PwnedWebsites')
    response = browser.response().read()

    data = BeautifulSoup(response, 'html5lib')

    domains = data.findAll('div', attrs={"class" : 'col-sm-10'})

    for n in domains:
        d = n.findAll('h3')
        print("\n\n{}[!] {}Domain Hacked: ".format(c.white, c.red) + d[0].text.strip() + '\n')

        info = n.findAll('p')
        
        print(c.white + info[1].text.strip())


def haveibeenpwned(email):
    time.sleep(0.5)
    browser = Browser()
    browser.set_handle_robots(False)
    browser.set_handle_equiv(False)
    browser.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'),
    ('Host', 'haveibeenpwned.com'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
    ('Accept-Language', 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'),
    ('Accept-Encoding', 'Accept-Encoding')
    ]

    print("\n{}[+] {}{}...".format(c.yellow,c.white,email))

    try:
        browser.open('https://haveibeenpwned.com/unifiedsearch/{}'.format(email))
        data = json.loads(browser.response().read())

        for k in data:
            try:
                val = data[k][0]
                for n in val:
                    print("{}[+] {}{}: {}".format(c.red,c.white,n,val[n]))
            except:
                continue
    except mechanize.HTTPError as e:

        if str(e.code) == '404':
            print('{}[+] Email not found!'.format(c.green))


print(banner)
print('\t{}[*] {}By: Jo-Sec || IDX4CKS'.format(c.green,c.white))

if parse.email and parse.file:
    print('{}[!] Invalid arguments!'.format(c.red))

elif parse.email and not parse.file:
    haveibeenpwned(email=parse.email)

elif parse.file and not parse.email:
    if path.exists(parse.file):
        list_emails = parse_file(email_list=parse.file)
        
        for email in list_emails:
            if "@" in email:
                haveibeenpwned(email=email)
            else:
                print("{}[!] Email incorrect: ".format(c.red) + email)

    else:
        print('\n{}[!] Input a valid file!'.format(c.red))

elif parse.list and not parse.email and not parse.file:
    parse_sites_owned()
