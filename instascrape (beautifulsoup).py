import time, urllib, os, requests
from bs4 import BeautifulSoup
from selenium import webdriver
## test https://www.instagram.com/eater/?hl=en downloads all pics from here 06022019 12pm

'''
-- Code Explanation --

Basically, we need to use webdriver to activate the page, since we need to get
the urls of the images in instagram, but the image urls are embedded in the
javascript of the instagram page. Thus, we need to activate the page's javascript
to load the image urls so that we can pull the image urls out using beautiful soup
(alt is pull it from json)

Then, because the html for the page doesn't contain all image urls,
ie its probably not loaded yet (for optimisation of resources methinks)
we need to take the img urls we can on the current html, then scroll,
wait for the new images to load, then reinput the updated html code of the
loaded page to take out the new imgs loaded in.

The while loop will stop when bottom of page is reached.

The retry array is because occasionally, imgurls will cause random errors,
and the way to deal with it (since actually it technically CAN work) is to just
use try except to catch the urls that are problematic and put them into another
array to retry later on.

For some reason, when retried in a smaller batch, the urls behave fine.

Goddamn. Idk what causes these errors, but this is the best fix. Code isn't super
fast, but should scrape instagram pages fairly completely and downloads it into
a folder, named by the insta account.




'''

## Constants ##
SCROLL_PAUSE_TIME = 3
i = 1

# Take URL and launch chromedriver from selenium (installed using choco)
url = input("\nPaste the EXACT URL of the OPEN instagram profile you want to scrape from: ")
driver = webdriver.Chrome()
driver.get(url) #accesses url thru webdriver

# init arrays for later use 
imgurl_arr = []
retry_arr = []

# this block is to read in the name of the account
# then name the folder after the account
soup = BeautifulSoup(driver.page_source,'html.parser')
account_name = str(soup.find('h1').get_text())
folder_name = "./"+ account_name

try:
    os.mkdir(folder_name)
except FileExistsError:
    print("folder already exists what the hell dude")
    
os.chdir(folder_name)
# Get current scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # while loop will only break when last recorded height
    # is same as new height after scrolling, i.e no more to scroll

    # First we init the beautiful soup object to 
    soup = BeautifulSoup(driver.page_source,'html.parser')

    for div in soup.find_all(class_="FFVAD"):
        imgurl = str(div['src'])
        try:
            imgurl = str(div['src'])
            if imgurl not in imgurl_arr:
                imgurl_arr.append(imgurl)
                filename = account_name + " " + str(i)+'.jpg'
                urllib.request.urlretrieve(imgurl,filename)
                i += 1
        except:
            retry_arr.append(imgurl)
            
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# retry to get all pics in case some urls spoil (v likely)
for aiyo in retry_arr:
    try:
        filename = str(i)+'.jpg'
        urllib.request.urlretrieve(aiyo,filename)
        i += 1
    except:
        # this just a joke bit usually code wont come here 
        print(aiyo)
        print("fku pis of sheet")

    
