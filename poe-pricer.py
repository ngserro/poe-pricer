from __future__ import print_function
import time
import requests #
import re
import sys
import signal
import json
import argparse #
from termcolor import colored, cprint #
from pprint import pprint
from tabulate import tabulate #

# TODO: Add number of links of item

# Function to handle CTRL+C
def signal_handler(signal, frame):
        print ("")
        print ('Terminated by user')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Function to handle pathofexile.com API requests
def request (URL,cookie):
    while True:    
        r = requests.get(URL, cookies=cookie)
        response = json.loads(r.text)
        if 'error' not in response:
            break
        else:
            print ("")
            print ("Rate limit exceeded. Waiting 60s...")
            time.sleep(60)
    return response

# Function to iterate through pricesPoeNinja and uptade item with price
def get_item_price( item, pricesPoeNinja ):
    for itemPoeNinja in pricesPoeNinja:
        if itemPoeNinja['name'] == item['name']:
            item['chaosValue'] = itemPoeNinja['chaosValue']
            item['exaltedValue'] = itemPoeNinja['exaltedValue']
            return item

# Return item type
def get_frame_type(frameType):
    if frameType == 3: return "Unique"
    if frameType == 4: return "Gem"
    if frameType == 5: return "Currency"
    if frameType == 6: return "D. Card"
    if frameType == 9: return "Relic"
    return frameType


# Main
def main(argv):

    print(time.strftime("%Y-%m-%d"))
    sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("POESESSID", help="Use your POESESSID")
    parser.add_argument("account", help="Your POE account name")
    parser.add_argument("league", help="POE league")
    args = parser.parse_args()
    POESESSID = args.POESESSID
    account = args.account
    league = args.league

    # Get poe.ninja item prices
    print ("Processing poe.ninja item prices... ",end="")
    sys.stdout.flush()
    categoriesPoeNinja=["UniqueArmour","UniqueWeapon","DivinationCards","Map","UniqueFlask","UniqueAccessory","UniqueJewel","UniqueMap"]
    for category in categoriesPoeNinja:
        URLPoeNinja = "http://poe.ninja/api/Data/Get"+category+"Overview?league="+league+"&date=" + time.strftime("%Y-%m-%d")
        r = requests.get(URLPoeNinja)
        if 'pricesPoeNinja' in locals():
            pricesPoeNinja = pricesPoeNinja+ r.json().get('lines')
        else:
            pricesPoeNinja = r.json().get('lines')
    # Currency
    URLPoeNinja = "http://poe.ninja/api/Data/GetCurrencyOverview?league="+league+"&date=" + time.strftime("%Y-%m-%d")
    r = requests.get(URLPoeNinja)
    currencyPricesPoeNinja = r.json().get('lines')
    for item in currencyPricesPoeNinja:
        if item['currencyTypeName'] == "Exalted Orb":
            ratioExalted = item['chaosEquivalent']
    cprint("DONE", 'green')

    # Get private tab index
    cookie = {'POESESSID': POESESSID}
    URLPrivateStashInfo = "https://www.pathofexile.com/character-window/get-stash-items?league="+league+"&tabs=1&tabIndex=0&accountName="+account
    print ("Processing private stash index... ",end="")
    sys.stdout.flush()
    privateStashInfo=request(URLPrivateStashInfo, cookie)
    cprint("DONE", 'green')
    print ("Found ",end=""),cprint(privateStashInfo['numTabs'], 'blue',end=""),print(" tabs")

    # Iterate all tabs
    myItems = []
    for tabIndex in range(0, privateStashInfo['numTabs']-1):
        itemIndex=0
        URLPrivateStash = "https://www.pathofexile.com/character-window/get-stash-items?league="+league+"&tabs=1&tabIndex="+`tabIndex`+"&accountName="+account
        sys.stdout.flush()
        print ("Processing tab "+privateStashInfo['tabs'][tabIndex]['n']+" ("+`tabIndex`+")...                                                      ",end='\r')
        privateStash = request(URLPrivateStash, cookie)
        for itemPrivateStash in privateStash['items']:
            if (itemPrivateStash['frameType'] == 3 or itemPrivateStash['frameType'] == 9) and itemPrivateStash['name']!="":
                item = {
                "name": itemPrivateStash['name'].replace("<<set:MS>><<set:M>><<set:S>>",""),
                "chaosValue": '',
                "exaltedValue": '',
                "typeLine": itemPrivateStash['typeLine'], 
                "tabIndex":  tabIndex,
                "frameType":  get_frame_type(itemPrivateStash['frameType']),
                }
                myItems.append(item)

    print ("Finished processing all tabs                                                      ",end='\r')
    print ("")

    # Update item prices
    print ("Updating item prices... ",end="")
    sys.stdout.flush()
    for item in range(0,len(myItems)):
        myItems[item]=get_item_price(myItems[item], pricesPoeNinja)
    cprint("DONE", 'green')
    
    # Total value of tab
    totalChaos=0
    totalExalted=0
    for tabIndex in range(0, privateStashInfo['numTabs']-1):
        tabSumChaos=0
        tabSumExalted=0
        tabItems=[]
        for item in range(0,len(myItems)):
            if myItems[item]['tabIndex'] == tabIndex:
                tabItems.append(myItems[item])
                tabSumChaos=tabSumChaos+myItems[item]['chaosValue']
                tabSumExalted=tabSumExalted+myItems[item]['exaltedValue']
                tabName=privateStashInfo['tabs'][tabIndex]['n']
        if tabSumChaos != 0:
            totalChaos=round(totalChaos+tabSumChaos,2)
            totalExalted=round(totalExalted+tabSumExalted,2)
            cprint("\nTab "+tabName+" - total value: "+`round(tabSumChaos,2)`+" chaos | "+`round(tabSumExalted,2)`+" exalted", 'blue')
            print (tabulate(tabItems,headers="keys",tablefmt="rst"))

    # Top 10 most valueable
    for item in myItems:
        item['tabName']=privateStashInfo['tabs'][item['tabIndex']]['n']
    print("")
    cprint("Top 10 most valuable items", 'blue')
    myItems = sorted(myItems, key=lambda x: x['chaosValue'], reverse=True)
    print (tabulate(myItems[:10],headers="keys",tablefmt="rst"))

    # Total account sum
    print("")
    cprint("Account Totals", 'blue')
    print ("Total chaos value: "+`totalChaos`)
    print ("Total exalted value: "+`totalExalted`)
    print ("1 exalted = "+`ratioExalted`+" chaos")
    
if __name__ == "__main__":
   main(sys.argv[1:])
